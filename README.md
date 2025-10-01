# AES2Hashcat

A Python script to extract encryption information from aescrypt version 2 files and convert them to Hashcat format.

## Description

This script analyzes an aescrypt encrypted file and extracts the components needed for decryption:
- IV (Initialization Vector) for KDF
- Encrypted IV for AES decryption
- Encrypted key
- HMAC

The script generates a Hashcat format hash to facilitate password cracking.

## Usage

```bash
python3 aes2hashcat.py file.txt.aes
```

### Example

```bash
python3 aes2hashcat.py document.txt.aes
```

Expected output:
```
$aescrypt$1*[iv_hex]*[iv_enc_hex]*[key_enc_hex]*[hmac_hex]
```

## Hashcat Usage

After extracting the hash, you can use Hashcat to crack the password:

```bash
# Save the hash to a file
echo '$aescrypt$1*[iv_hex]*[iv_enc_hex]*[key_enc_hex]*[hmac_hex]' > aes_hash.txt

# Run Hashcat with wordlist
hashcat --hash-type 22400 --attack-mode 0 aes_hash.txt `fzf-wordlists`
```

## Decryption

If you have the password, you can decrypt the file directly:

```bash
python3 aes_decrypt.py file.txt.aes -p password
```

This will create a decrypted file with the original name (without .aes extension).

## Requirements

- Python 3.x
- pyAesCrypt (for decryption script): `pip install pyAesCrypt`
- No external dependencies required for hash extraction

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