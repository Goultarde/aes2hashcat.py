#!/usr/bin/env python3

import sys
import hashlib
import hmac as hmac_module
from Crypto.Cipher import AES
import struct

def derive_key(password, iv):
    """Derive an AES-256 key from the password"""
    key = hashlib.sha256(password.encode('utf-8') + iv).digest()
    for _ in range(8191):
        key = hashlib.sha256(key).digest()
    return key

def decrypt_aescrypt(filename, password):
    """Decrypt an AESCrypt v2 file with HMAC verification"""
    
    with open(filename, 'rb') as f:
        # Read the entire file
        file_content = f.read()
    
    offset = 0
    
    # Signature
    signature = file_content[offset:offset+3]
    offset += 3
    if signature != b'AES':
        raise Exception("Not a valid AESCrypt file")
    
    # Version
    version = file_content[offset:offset+1]
    offset += 1
    if version != b'\x02':
        raise Exception("Only AESCrypt version 2 is supported")
    
    # Reserved byte
    offset += 1
    
    # Skip extensions
    while True:
        ext_size = struct.unpack('>H', file_content[offset:offset+2])[0]
        offset += 2
        if ext_size == 0:
            break
        offset += ext_size
    
    # Read cryptographic components
    iv_kdf = file_content[offset:offset+16]
    offset += 16
    
    iv_enc = file_content[offset:offset+16]
    offset += 16
    
    key_enc = file_content[offset:offset+32]
    offset += 32
    
    hmac_header = file_content[offset:offset+32]
    offset += 32
    
    # Derive the key
    derived_key = derive_key(password, iv_kdf)
    
    # HMAC VERIFICATION to validate the password
    hmac_calc = hmac_module.new(derived_key, file_content[:offset], hashlib.sha256).digest()
    
    if hmac_calc != hmac_header:
        raise Exception("WRONG PASSWORD! HMAC verification failed.")
    
    print("[+] Password verified (HMAC valid)")
    
    # Decrypt the AES key and IV
    cipher_key = AES.new(derived_key, AES.MODE_ECB)
    aes_key = cipher_key.decrypt(key_enc)
    iv_real = cipher_key.decrypt(iv_enc)
    
    # Encrypted data (everything that remains)
    encrypted_data = file_content[offset:]
    
    # Remove the last block: HMAC (32 bytes) + size (1 byte)
    if len(encrypted_data) < 33:
        raise Exception("File too short")
    
    file_size_modulo = encrypted_data[-1]
    hmac_data = encrypted_data[-33:-1]
    encrypted_data = encrypted_data[:-33]
    
    # Decrypt
    cipher_data = AES.new(aes_key, AES.MODE_CBC, iv_real)
    decrypted_data = cipher_data.decrypt(encrypted_data)
    
    # Remove padding
    if file_size_modulo > 0:
        padding_length = 16 - file_size_modulo
        decrypted_data = decrypted_data[:-padding_length]
    
    return decrypted_data

def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file.aes> <password>")
        sys.exit(1)
    
    filename = sys.argv[1]
    password = sys.argv[2]
    
    try:
        print(f"[+] Decrypting {filename}...")
        decrypted = decrypt_aescrypt(filename, password)
        
        # Create output filename
        if filename.endswith('.aes'):
            output_filename = filename[:-4]
        else:
            output_filename = filename + '.decrypted'
        
        # Save
        with open(output_filename, 'wb') as f:
            f.write(decrypted)
        
        print(f"[+] Successfully decrypted to: {output_filename}")
        print(f"[+] Size: {len(decrypted)} bytes")
        
        # Display magic bytes
        print(f"[+] Magic bytes: {decrypted[:4].hex()} ({decrypted[:4]})")
        
    except Exception as e:
        print(f"[-] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
