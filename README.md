# AES2Hashcat

A complete toolkit for working with aescrypt version 2 files. Extract hashes for password cracking with Hashcat or decrypt files directly when you have the password.

## Description

This toolkit provides two main functionalities:

### 1. Hash Extraction (`aes2hashcat.py`)
Extracts encryption components from aescrypt files and converts them to Hashcat format:
- IV (Initialization Vector) for KDF
- Encrypted IV for AES decryption
- Encrypted key
- HMAC

### 2. Direct Decryption (`aes_decrypt.py`)
Decrypts aescrypt files directly when you have the password using pyAesCrypt library.

## Usage

### Option 1: Password Cracking with Hashcat

1. **Extract the hash:**
```bash
python3 aes2hashcat.py file.txt.aes
```

2. **Save the hash and crack with Hashcat:**
```bash
# Save the hash to a file
echo '$aescrypt$1*[iv_hex]*[iv_enc_hex]*[key_enc_hex]*[hmac_hex]' > aes_hash.txt

# Run Hashcat with wordlist
hashcat --hash-type 22400 --attack-mode 0 aes_hash.txt `fzf-wordlists`
```

### Option 2: Direct Decryption (when you have the password)

```bash
python3 aes_decrypt.py file.txt.aes -p password
```

This will create a decrypted file with the original name (without .aes extension).

### Examples

**Hash extraction:**
```bash
python3 aes2hashcat.py document.txt.aes
# Output: $aescrypt$1*[iv_hex]*[iv_enc_hex]*[key_enc_hex]*[hmac_hex]
```

**Direct decryption:**
```bash
python3 aes_decrypt.py document.txt.aes -p secret123
# Creates: document.txt (decrypted)
```

## Requirements

- Python 3.x
- pyAesCrypt (for decryption script)

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or install manually
pip install pyAesCrypt
```

**Note:** No external dependencies required for hash extraction (`aes2hashcat.py`)

## Supported File Format

- AESCrypt version 2 only
- File signature: "AES"

## Error Handling

The script handles the following errors:
- File not found
- Incorrect file format
- Invalid signature
- Unsupported version
- Incomplete data reading

## Exit Codes

- `0`: Success
- `1`: Error (file not found, incorrect format, etc.)

## License

This script is provided as-is for educational and security research purposes.