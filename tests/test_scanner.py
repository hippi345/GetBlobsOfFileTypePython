"""Unit tests for blob scanning logic (offline, no Azure credentials)."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from get_blobs_of_file_type.scanner import (
    blob_name_matches,
    scan_containers,
)


@dataclass
class FakeBlob:
    name: str
    size: int | None = 0


class FakeContainerClient:
    def __init__(self, blobs: list[FakeBlob]) -> None:
        self._blobs = blobs

    def list_blobs(self) -> Iterator[FakeBlob]:
        return iter(self._blobs)


class FakeBlobService:
    def __init__(self, containers: dict[str, list[FakeBlob]]) -> None:
        self._containers = containers

    def get_container_client(self, container: str) -> FakeContainerClient:
        if container not in self._containers:
            raise KeyError(container)
        return FakeContainerClient(self._containers[container])


def test_blob_name_matches_suffix():
    assert blob_name_matches("folder/report.pdf", ".pdf")
    assert not blob_name_matches("folder/report.pdf", ".doc")


def test_scan_containers_filters_by_file_type():
    service = FakeBlobService(
        {
            "c1": [
                FakeBlob("a.pdf", 100),
                FakeBlob("b.txt", 50),
            ],
            "c2": [
                FakeBlob("nested/c.pdf", 200),
            ],
        }
    )
    result = scan_containers(service, ["c1", "c2"], ".pdf")
    assert len(result.matches) == 2
    assert result.total_size_bytes == 300
    names = {m.name for m in result.matches}
    assert names == {"a.pdf", "nested/c.pdf"}


def test_scan_containers_empty_when_no_matches():
    service = FakeBlobService({"c1": [FakeBlob("readme.md", 10)]})
    result = scan_containers(service, ["c1"], ".pdf")
    assert result.matches == ()
    assert result.total_size_bytes == 0


def test_scan_containers_handles_none_size():
    service = FakeBlobService({"c1": [FakeBlob("x.pdf", None)]})
    result = scan_containers(service, ["c1"], ".pdf")
    assert result.matches[0].size_bytes == 0
