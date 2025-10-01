#!/usr/bin/env python3

import pyAesCrypt
import os
import sys
import argparse

buffer_size = 64 * 1024  # 64KB

def decrypt_file(encrypted_file, password, output_file=None):
    """
    Decrypt an .aes file
    
    Args:
        encrypted_file: Path to the .aes file to decrypt
        password: Decryption password
        output_file: Output file path (optional)
    """
    # If no output file specified, remove .aes extension
    if output_file is None:
        if encrypted_file.endswith('.aes'):
            output_file = encrypted_file[:-4]
        else:
            output_file = encrypted_file + '.decrypted'
    try:
        # Check that the encrypted file exists
        if not os.path.exists(encrypted_file):
            print(f"Error: File '{encrypted_file}' does not exist")
            print(f"Files in current directory:")
            for f in os.listdir('.'):
                if f.endswith('.aes'):
                    print(f"   - {f}")
            return False
        
        # Display file size
        size = os.path.getsize(encrypted_file)
        print(f"File to decrypt: {encrypted_file}")
        print(f"Size: {size:,} bytes ({size/1024/1024:.2f} MB)")
        print(f"Decryption in progress...")
        
        # Decryption
        pyAesCrypt.decryptFile(
            encrypted_file, 
            output_file, 
            password, 
            buffer_size
        )
        
        # Check that the decrypted file exists
        if os.path.exists(output_file):
            decrypted_size = os.path.getsize(output_file)
            print(f"\nDecryption successful!")
            print(f"File created: {output_file}")
            print(f"Size: {decrypted_size:,} bytes ({decrypted_size/1024/1024:.2f} MB)")
            return True
        else:
            print("Error: The decrypted file was not created")
            return False
        
    except ValueError as e:
        print(f"\nError: Incorrect password or corrupted file")
        print(f"   Details: {e}")
        return False
    except Exception as e:
        print(f"\nError during decryption: {type(e).__name__}")
        print(f"   Details: {e}")
        return False

# Execution
if __name__ == "__main__":
    # Argument parser configuration
    parser = argparse.ArgumentParser(
        description='Decrypt an AES file with pyAesCrypt',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Usage examples:
  python %(prog)s file.aes -p password
  python %(prog)s document.pdf.aes -p secret123 -o document.pdf
  python %(prog)s data.zip.aes --password mypass --output data.zip
        '''
    )
    
    parser.add_argument('file', 
                        help='.aes file to decrypt')
    parser.add_argument('-p', '--password', 
                        required=True,
                        help='Decryption password')
    parser.add_argument('-o', '--output', 
                        help='Output file (optional, by default removes .aes)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("AES FILE DECRYPTION")
    print("=" * 60)
    print()
    
    success = decrypt_file(args.file, args.password, args.output)
    
    print()
    print("=" * 60)
    if success:
        print("Operation completed successfully!")
        print("You can now extract the ZIP file.")
    else:
        print("The operation failed.")
    print("=" * 60)
