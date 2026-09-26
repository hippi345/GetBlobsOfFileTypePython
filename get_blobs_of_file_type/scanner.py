"""Core logic for scanning Azure Blob containers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from azure.storage.blob import BlobServiceClient


@dataclass(frozen=True)
class BlobMatch:
    """A blob whose name matches the requested file type."""

    container: str
    name: str
    size_bytes: int


@dataclass(frozen=True)
class ScanResult:
    """Aggregated scan output for one or more containers."""

    matches: tuple[BlobMatch, ...]

    @property
    def total_size_bytes(self) -> int:
        return sum(m.size_bytes for m in self.matches)


class BlobServiceLike(Protocol):
    """Subset of BlobServiceClient used by the scanner (for testing)."""

    def get_container_client(self, container: str): ...


def create_blob_service_client(account_name: str, account_key: str) -> BlobServiceClient:
    account_url = f"https://{account_name}.blob.core.windows.net"
    return BlobServiceClient(account_url=account_url, credential=account_key)


def create_blob_service_client_from_connection_string(connection_string: str) -> BlobServiceClient:
    return BlobServiceClient.from_connection_string(connection_string)


def blob_name_matches(blob_name: str, file_type: str) -> bool:
    """Return True if blob_name ends with the given file type suffix."""
    return blob_name.endswith(file_type)


def scan_containers(
    service: BlobServiceLike,
    container_names: list[str],
    file_type: str,
) -> ScanResult:
    """
    List blobs in each container whose names end with file_type.

    Raises azure.core.exceptions.ResourceNotFoundError if a container does not exist.
    """
    matches: list[BlobMatch] = []
    for container_name in container_names:
        container_client = service.get_container_client(container_name)
        for blob in container_client.list_blobs():
            if blob_name_matches(blob.name, file_type):
                size = blob.size if blob.size is not None else 0
                matches.append(BlobMatch(container=container_name, name=blob.name, size_bytes=size))
    return ScanResult(matches=tuple(matches))
