# GetBlobsOfFileTypePython

[![CI](https://github.com/hippi345/GetBlobsOfFileTypePython/actions/workflows/ci.yml/badge.svg)](https://github.com/hippi345/GetBlobsOfFileTypePython/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Command-line utility that lists blobs in Azure Blob Storage containers whose names end with a given file type (extension), and reports the total size of matching files.

## Features

- Scan one or more containers in a storage account
- Filter blobs by filename suffix (e.g. `.pdf`)
- Print per-blob sizes and a total size summary
- Credentials via CLI flags or environment variables (keys are never printed)

## Requirements

- Python 3.12 or newer
- An Azure Storage account with access to the target containers

## Setup

```bash
git clone https://github.com/hippi345/GetBlobsOfFileTypePython.git
cd GetBlobsOfFileTypePython
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Copy `.env.example` to `.env` for local reference (do not commit `.env`).

## Configuration

| Variable | Description |
|----------|-------------|
| `AZURE_STORAGE_ACCOUNT_NAME` | Storage account name (used with account key) |
| `AZURE_STORAGE_ACCOUNT_KEY` | Storage account key |
| `AZURE_STORAGE_CONNECTION_STRING` | Full connection string (optional; takes precedence when set) |

CLI flags `-s` / `-k` override environment variables for account name and key when not using a connection string.

## Usage

```bash
python main.py -s myaccount -k "$AZURE_STORAGE_ACCOUNT_KEY" -c container1 container2 -f .pdf
```

Or with environment variables:

```bash
export AZURE_STORAGE_ACCOUNT_NAME=myaccount
export AZURE_STORAGE_ACCOUNT_KEY='...'
python main.py -c logs backups -f .json
```

Example output:

```
Welcome to the storage utility...
     The containers are: ['logs', 'backups']
     The Storage account is: myaccount
     The key is: [redacted]
     The file type for search is: .pdf
     logs:
2024/report.pdf: 1024 bytes
Total size of .pdf files: 1024 bytes
```

Installed package entry point (optional):

```bash
get-blobs-of-file-type -c mycontainer -f .txt -s myaccount -k "$AZURE_STORAGE_ACCOUNT_KEY"
```

## Running tests

Tests run offline with mocked storage clients (no Azure credentials required):

```bash
pytest
ruff check .
ruff format --check .
```

## Project structure

```
├── get_blobs_of_file_type/   # Package: scanner + CLI
│   ├── cli.py
│   └── scanner.py
├── main.py                   # Backward-compatible entry point
├── tests/
├── pyproject.toml
├── .github/workflows/ci.yml
└── SECURITY.md
```

## License

MIT License — Copyright (c) 2026 Joel Shearon. See [LICENSE](LICENSE).
