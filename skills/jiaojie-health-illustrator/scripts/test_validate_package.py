from __future__ import annotations

import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from validate_package import validate_package


def write_png(path: Path, width: int, height: int) -> None:
    def chunk(kind: bytes, data: bytes) -> bytes:
        payload = kind + data
        return struct.pack(">I", len(data)) + payload + struct.pack(">I", zlib.crc32(payload) & 0xFFFFFFFF)

    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    row = b"\x00" + (b"\xff\xff\xff" * width)
    pixels = zlib.compress(row * height)
    path.write_bytes(signature + chunk(b"IHDR", ihdr) + chunk(b"IDAT", pixels) + chunk(b"IEND", b""))


class ValidatePackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.package = Path(self.temp_dir.name) / "睡眠节律"
        self.imgs = self.package / "imgs"
        self.prompts = self.imgs / "prompts"
        self.prompts.mkdir(parents=True)
        (self.imgs / "outline.md").write_text("# 配图提纲\n", encoding="utf-8")
        for index in range(1, 4):
            stem = f"{index:02d}-sleep"
            (self.prompts / f"{stem}.md").write_text(f"# 提示词 {index}\n", encoding="utf-8")
            write_png(self.imgs / f"{stem}.png", 300, 200)
        self.write_documents(3)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_documents(self, count: int) -> None:
        markdown_images = "\n".join(
            f"![配图{index}](imgs/{index:02d}-sleep.png)" for index in range(1, count + 1)
        )
        html_images = "\n".join(
            f'<img src="imgs/{index:02d}-sleep.png" alt="配图{index}">' for index in range(1, count + 1)
        )
        (self.package / "睡眠节律_文章源稿.md").write_text(markdown_images + "\n", encoding="utf-8")
        (self.package / "睡眠节律_公众号可复制版.html").write_text(html_images + "\n", encoding="utf-8")

    def assert_has_error(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_valid_package_passes(self) -> None:
        self.assertEqual(validate_package(self.package), [])

    def test_missing_png_fails(self) -> None:
        (self.imgs / "03-sleep.png").unlink()
        self.assert_has_error(validate_package(self.package), "PNG count")

    def test_prompt_count_mismatch_fails(self) -> None:
        (self.prompts / "03-sleep.md").unlink()
        self.assert_has_error(validate_package(self.package), "prompt count")

    def test_non_three_to_two_png_fails(self) -> None:
        write_png(self.imgs / "02-sleep.png", 300, 199)
        self.assert_has_error(validate_package(self.package), "ratio")

    def test_html_wechat_image_token_fails(self) -> None:
        html_path = self.package / "睡眠节律_公众号可复制版.html"
        html_path.write_text(html_path.read_text(encoding="utf-8") + "WECHATIMGPH_1\n", encoding="utf-8")
        self.assert_has_error(validate_package(self.package), "WECHATIMGPH")

    def test_missing_html_image_reference_fails(self) -> None:
        html_path = self.package / "睡眠节律_公众号可复制版.html"
        html_path.write_text(
            html_path.read_text(encoding="utf-8") + '<img src="imgs/99-missing.png">\n',
            encoding="utf-8",
        )
        self.assert_has_error(validate_package(self.package), "missing HTML image")

    def test_explicit_image_count_override_passes(self) -> None:
        (self.imgs / "03-sleep.png").unlink()
        (self.prompts / "03-sleep.md").unlink()
        self.write_documents(2)
        self.assertEqual(validate_package(self.package, min_images=2, max_images=2), [])


if __name__ == "__main__":
    unittest.main()
