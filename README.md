# AESCrypt Extractor

Un script Python pour extraire les informations de chiffrement des fichiers aescrypt version 2.

## Description

Ce script analyse un fichier chiffré avec aescrypt et extrait les composants nécessaires pour le déchiffrement :
- IV (Initialization Vector) pour KDF
- IV chiffré pour le déchiffrement AES
- Clé chiffrée
- HMAC

Le script génère un hash au format John the Ripper pour faciliter le craquage de mot de passe.

## Utilisation

```bash
python3 aescrypt_extractor.py fichier.txt.aes
```

### Exemple

```bash
python3 aescrypt_extractor.py document.txt.aes
```

Sortie attendue :
```
$aescrypt$1*[iv_hex]*[iv_enc_hex]*[key_enc_hex]*[hmac_hex]
```

## Prérequis

- Python 3.x
- Aucune dépendance externe requise

## Format de fichier supporté

- AESCrypt version 2 uniquement
- Signature de fichier : "AES"

## Gestion d'erreurs

Le script gère les erreurs suivantes :
- Fichier introuvable
- Format de fichier incorrect
- Signature invalide
- Version non supportée
- Lecture incomplète des données

## Code de sortie

- `0` : Succès
- `1` : Erreur (fichier introuvable, format incorrect, etc.)

## Licence

Ce script est fourni tel quel pour des fins éducatives et de recherche en sécurité.
