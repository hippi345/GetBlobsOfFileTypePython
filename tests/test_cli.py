"""CLI tests with mocked Azure client."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from get_blobs_of_file_type.cli import run
from get_blobs_of_file_type.scanner import BlobMatch, ScanResult


def test_help_exits_with_usage_code():
    assert run(["--help"]) == 69


def test_missing_credentials_exits_usage(capsys):
    code = run(["-c", "mycontainer", "-f", ".pdf", "-s", "acct"])
    assert code == 69
    err = capsys.readouterr().err
    assert "AZURE_STORAGE_ACCOUNT_KEY" in err


@patch("get_blobs_of_file_type.cli.scan_containers")
@patch("get_blobs_of_file_type.cli.create_blob_service_client")
def test_run_success_redacts_key(mock_create, mock_scan, capsys):
    mock_create.return_value = MagicMock()
    mock_scan.return_value = ScanResult(
        matches=(BlobMatch(container="c1", name="file.pdf", size_bytes=42),)
    )
    code = run(
        [
            "-s",
            "myaccount",
            "-k",
            "supersecret",
            "-c",
            "c1",
            "-f",
            ".pdf",
        ]
    )
    assert code == 0
    out = capsys.readouterr().out
    assert "supersecret" not in out
    assert "[redacted]" in out
    assert "file.pdf: 42 bytes" in out
    mock_create.assert_called_once_with("myaccount", "supersecret")
