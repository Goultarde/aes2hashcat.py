#!/usr/bin/env python3

import sys
import struct

def read_bytes(file_handle, size):
    """
    Read exactly 'size' bytes from the file.
    Raises an exception if all bytes cannot be read.
    """
    data = file_handle.read(size)
    
    if len(data) != size:
        raise Exception(f"ERROR: Couldn't read {size} bytes from the file. Maybe incorrect file format?")
    
    return data

def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} file.txt.aes")
        sys.exit(1)
    
    file_name = sys.argv[1]
    
    try:
        with open(file_name, 'rb') as file_handle:
            
            # Signature
            signature = read_bytes(file_handle, 3)
            
            if signature != b'AES':
                raise Exception("ERROR: The file doesn't seem to be a correct aescrypt file (signature mismatch)")
            
            # Version
            version = read_bytes(file_handle, 1)
            
            if version != b'\x02':
                raise Exception("ERROR: Currently only aescrypt file version 2 is supported by this script")
            
            # Reserved byte (skip)
            read_bytes(file_handle, 1)
            
            # Loop over extensions until we get extension size 0
            extension_size_bytes = read_bytes(file_handle, 2)
            
            while extension_size_bytes != b'\x00\x00':
                # Unpack as big-endian 16-bit unsigned integer
                skip_size = struct.unpack('>H', extension_size_bytes)[0]
                
                # Skip the extension
                read_bytes(file_handle, skip_size)
                
                extension_size_bytes = read_bytes(file_handle, 2)
            
            # IV (for KDF)
            iv = read_bytes(file_handle, 16)
            
            # IV (encrypted IV for AES decryption)
            iv_enc = read_bytes(file_handle, 16)
            
            # key_enc
            key_enc = read_bytes(file_handle, 32)
            
            # HMAC
            hmac = read_bytes(file_handle, 32)
            
            # Hex conversion
            iv_hex = iv.hex()
            iv_enc_hex = iv_enc.hex()
            key_enc_hex = key_enc.hex()
            hmac_hex = hmac.hex()
            
            # Final output
            print(f"$aescrypt$1*{iv_hex}*{iv_enc_hex}*{key_enc_hex}*{hmac_hex}")
    
    except FileNotFoundError:
        print(f"ERROR: Couldn't open file '{file_name}'")
        sys.exit(1)
    except Exception as e:
        print(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()