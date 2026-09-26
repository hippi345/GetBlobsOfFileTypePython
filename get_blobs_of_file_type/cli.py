"""Command-line interface for the blob scanner."""

from __future__ import annotations

import argparse
import os
import sys

from azure.storage.blob import BlobServiceClient

from get_blobs_of_file_type.scanner import (
    ScanResult,
    create_blob_service_client,
    create_blob_service_client_from_connection_string,
    scan_containers,
)

EXIT_USAGE = 69


class CredentialError(Exception):
    """Raised when required Azure credentials are missing."""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="main.py",
        description=(
            "Shows blobs of a certain file type in each Azure storage container you provide."
        ),
    )
    parser.add_argument(
        "-s",
        "--storage-account",
        dest="storage_account",
        help="Azure storage account name (or set AZURE_STORAGE_ACCOUNT_NAME)",
    )
    parser.add_argument(
        "-k",
        "--key",
        dest="account_key",
        help="Azure storage account key (or set AZURE_STORAGE_ACCOUNT_KEY)",
    )
    parser.add_argument(
        "-c",
        "--containers",
        nargs="+",
        required=True,
        metavar="CONTAINER",
        help="One or more container names to scan",
    )
    parser.add_argument(
        "-f",
        "--file-type",
        dest="file_type",
        required=True,
        help="File suffix to match (e.g. .pdf or pdf)",
    )
    return parser


def resolve_credentials(args: argparse.Namespace) -> BlobServiceClient:
    connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    if connection_string:
        return create_blob_service_client_from_connection_string(connection_string)

    account_name = args.storage_account or os.environ.get("AZURE_STORAGE_ACCOUNT_NAME")
    account_key = args.account_key or os.environ.get("AZURE_STORAGE_ACCOUNT_KEY")
    if not account_name or not account_key:
        raise CredentialError(
            "Error: provide -s/-k or set AZURE_STORAGE_ACCOUNT_NAME and "
            "AZURE_STORAGE_ACCOUNT_KEY (or AZURE_STORAGE_CONNECTION_STRING)."
        )
    return create_blob_service_client(account_name, account_key)


def format_scan_output(result: ScanResult, file_type: str) -> str:
    lines: list[str] = []
    by_container: dict[str, list] = {}
    for match in result.matches:
        by_container.setdefault(match.container, []).append(match)

    for container in sorted(by_container):
        lines.append(f"     {container}:")
        for match in by_container[container]:
            lines.append(f"{match.name}: {match.size_bytes} bytes")

    lines.append(f"Total size of {file_type} files: {result.total_size_bytes} bytes")
    return "\n".join(lines)


def run(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if not argv or argv[0] in {"help", "h", "-help", "-h", "--help"}:
        build_parser().print_help()
        return EXIT_USAGE

    parser = build_parser()
    args = parser.parse_args(argv)

    print(
        "Welcome to the storage utility. Shows you blobs of a certain file type "
        "in each container you provide!"
    )
    print(f"     The containers are: {args.containers}")
    account_label = args.storage_account or os.environ.get(
        "AZURE_STORAGE_ACCOUNT_NAME", "(from env)"
    )
    print(f"     The Storage account is: {account_label}")
    print("     The key is: [redacted]")
    print(f"     The file type for search is: {args.file_type}")

    try:
        service = resolve_credentials(args)
    except CredentialError as exc:
        print(str(exc), file=sys.stderr)
        return EXIT_USAGE

    result = scan_containers(service, args.containers, args.file_type)
    print(format_scan_output(result, args.file_type))
    return 0


def main() -> None:
    sys.exit(run())
