import pytest
from pathlib import Path
from downloader import WeatherPDFDownloader


class DummyDL(WeatherPDFDownloader):
    """Extending a class and override methods for testing."""

    def __init__(self, data_dir, content):
        super().__init__(data_dir, weather_pdf_url="dummy")
        self.fake_content = content
        self.calls = 0

    def _download(self):
        """Simulate downloading by writing predefined content."""
        self.calls += 1
        with self.current_pdf_path.open("wb") as f:
            f.write(self.fake_content[self.calls - 1])


def test_case_A(tmp_path):
    """Case A: neither exists"""
    dl = DummyDL(tmp_path, [b"PDF-A"])

    changed = dl.update()

    assert changed is True
    assert dl._exists(dl.current_pdf_path)
    assert not dl._exists(dl.last_pdf_path)


def test_case_B(tmp_path):
    """Case B: only current exists"""
    current_pdf_path = tmp_path / "current.pdf"
    current_pdf_path.write_bytes(b"OLD")

    dl = DummyDL(tmp_path, [b"NEW"])
    changed = dl.update()

    # After rename: last.pdf=OLD, current.pdf=NEW
    assert (tmp_path / "last.pdf").read_bytes() == b"OLD"
    assert (tmp_path / "current.pdf").read_bytes() == b"NEW"
    assert changed is True


def test_case_C_no_change(tmp_path):
    """Case C: only last exists"""
    last = tmp_path / "last.pdf"
    last.write_bytes(b"SAME")

    dl = DummyDL(tmp_path, [b"SAME"])
    changed = dl.update()

    assert changed is False
    assert (tmp_path / "last.pdf").read_bytes() == b"SAME"
    assert not (tmp_path / "current.pdf").exists()
