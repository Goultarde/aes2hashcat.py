#!/usr/bin/env python3

import pyAesCrypt
import os
import sys
import argparse

buffer_size = 64 * 1024  # 64KB

def detect_file_type(magic_bytes):
    """Detect file type based on magic bytes"""
    magic_signatures = {
        b'PK\x03\x04': 'ZIP archive',
        b'PK\x05\x06': 'ZIP archive (empty)',
        b'PK\x07\x08': 'ZIP archive (spanned)',
        b'\x1f\x8b\x08': 'GZIP archive',
        b'BZh': 'BZIP2 archive',
        b'\x7fELF': 'ELF executable',
        b'MZ': 'Windows executable (PE)',
        b'\x89PNG': 'PNG image',
        b'\xff\xd8\xff': 'JPEG image',
        b'GIF8': 'GIF image',
        b'RIFF': 'RIFF container (WAV/AVI)',
        b'%PDF': 'PDF document',
        b'\x00\x00\x01\x00': 'Windows icon',
        b'\x00\x00\x02\x00': 'Windows cursor',
        b'ftyp': 'MP4 video',
        b'\x00\x00\x00\x18': 'MP4 video',
        b'ID3': 'MP3 audio',
        b'\xff\xfb': 'MP3 audio',
        b'\xff\xf3': 'MP3 audio',
        b'\xff\xf2': 'MP3 audio',
        b'OggS': 'OGG audio/video',
        b'Rar!': 'RAR archive',
        b'\x37\x7a\xbc\xaf': '7-Zip archive',
        b'\x50\x4b\x03\x04': 'ZIP archive',
        b'\x50\x4b\x05\x06': 'ZIP archive (empty)',
        b'\x50\x4b\x07\x08': 'ZIP archive (spanned)',
    }
    
    for signature, file_type in magic_signatures.items():
        if magic_bytes.startswith(signature):
            return file_type
    
    # Check for text files
    try:
        if all(32 <= b <= 126 or b in [9, 10, 13] for b in magic_bytes):
            return 'Text file'
    except:
        pass
    
    return 'Unknown file type'

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
            
            # Detect file type and show appropriate message
            try:
                with open(output_file, 'rb') as f:
                    magic_bytes = f.read(4)
                    file_type = detect_file_type(magic_bytes)
                    print(f"File type: {file_type}")
            except:
                pass
            
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
        # Check if it's a ZIP file and show appropriate message
        try:
            with open(args.file if args.output is None else args.output, 'rb') as f:
                magic_bytes = f.read(4)
                if magic_bytes.startswith(b'PK'):
                    print("You can now extract the ZIP file.")
                elif magic_bytes.startswith(b'%PDF'):
                    print("You can now open the PDF document.")
                elif magic_bytes.startswith(b'\x89PNG') or magic_bytes.startswith(b'\xff\xd8\xff'):
                    print("You can now view the image file.")
                elif magic_bytes.startswith(b'RIFF'):
                    print("You can now play the media file.")
                else:
                    print("The decrypted file is ready to use.")
        except:
            print("The decrypted file is ready to use.")
    else:
        print("The operation failed.")
    print("=" * 60)
