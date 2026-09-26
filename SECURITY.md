# Security Policy

## Supported versions

Security fixes are applied on the latest release on the default branch.

## Reporting a vulnerability

If you discover a security issue, please **do not** open a public GitHub issue with sensitive details. Contact the repository owner privately so the issue can be addressed before disclosure.

## Secrets and credentials

- Never commit storage account keys, connection strings, or other secrets to the repository.
- Configure credentials via environment variables (`AZURE_STORAGE_ACCOUNT_NAME`, `AZURE_STORAGE_ACCOUNT_KEY`, or `AZURE_STORAGE_CONNECTION_STRING`) or CLI flags at runtime.
- If a secret was ever committed to git history, rotate it immediately in Azure Portal and purge it from history if required by your policy.

## Dependencies

Dependency updates are managed via Dependabot. Run `pip install -e ".[dev]"` and keep `azure-storage-blob` current for security patches.
