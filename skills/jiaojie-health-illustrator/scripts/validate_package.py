#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import struct
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


class _ImageSourceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.sources: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "img":
            return
        for name, value in attrs:
            if name.lower() == "src" and value:
                self.sources.append(value)
                break


def png_size(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if len(header) < 24 or header[:8] != PNG_SIGNATURE or header[12:16] != b"IHDR":
        raise ValueError(f"invalid PNG header: {path}")
    return struct.unpack(">II", header[16:24])


def markdown_image_sources(markdown: str) -> list[str]:
    pattern = re.compile(r"!\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))")
    return [angle or plain for angle, plain in pattern.findall(markdown)]


def html_image_sources(html: str) -> list[str]:
    parser = _ImageSourceParser()
    parser.feed(html)
    return parser.sources


def _local_target(document: Path, source: str) -> Path | None:
    if source.startswith("//"):
        return None
    parsed = urlsplit(source)
    if parsed.scheme.lower() in {"http", "https", "data"}:
        return None
    return document.parent / unquote(parsed.path)


def _single_file(package_dir: Path, pattern: str, label: str, errors: list[str]) -> Path | None:
    matches = sorted(package_dir.glob(pattern))
    if len(matches) != 1:
        errors.append(f"{label} count {len(matches)}; expected exactly 1")
        return None
    return matches[0]


def validate_package(
    package_dir: Path,
    min_images: int = 3,
    max_images: int = 5,
    expected_ratio: tuple[int, int] = (3, 2),
) -> list[str]:
    errors: list[str] = []
    package_dir = Path(package_dir)
    if not package_dir.is_dir():
        return [f"package directory does not exist: {package_dir}"]
    if min_images < 1 or max_images < min_images:
        return [f"invalid image range: {min_images}-{max_images}"]
    ratio_width, ratio_height = expected_ratio
    if ratio_width < 1 or ratio_height < 1:
        return [f"invalid ratio: {ratio_width}:{ratio_height}"]

    imgs_dir = package_dir / "imgs"
    prompts_dir = imgs_dir / "prompts"
    if not (imgs_dir / "outline.md").is_file():
        errors.append("missing imgs/outline.md")

    pngs = sorted(imgs_dir.glob("*.png")) if imgs_dir.is_dir() else []
    prompts = sorted(prompts_dir.glob("*.md")) if prompts_dir.is_dir() else []
    if not min_images <= len(pngs) <= max_images:
        errors.append(f"PNG count {len(pngs)} outside allowed range {min_images}-{max_images}")
    if len(prompts) != len(pngs):
        errors.append(f"prompt count {len(prompts)} does not match PNG count {len(pngs)}")

    for png in pngs:
        try:
            width, height = png_size(png)
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
            continue
        if width * ratio_height != height * ratio_width:
            errors.append(
                f"ratio mismatch for {png.name}: {width}:{height}; expected {ratio_width}:{ratio_height}"
            )

    markdown_path = _single_file(package_dir, "*_文章源稿.md", "source Markdown", errors)
    html_path = _single_file(package_dir, "*_公众号可复制版.html", "WeChat HTML", errors)

    if markdown_path is not None:
        markdown_sources = markdown_image_sources(markdown_path.read_text(encoding="utf-8"))
        if len(markdown_sources) != len(pngs):
            errors.append(
                f"Markdown image count {len(markdown_sources)} does not match PNG count {len(pngs)}"
            )
        for source in markdown_sources:
            target = _local_target(markdown_path, source)
            if target is not None and not target.is_file():
                errors.append(f"missing Markdown image: {source}")

    if html_path is not None:
        html = html_path.read_text(encoding="utf-8")
        if "WECHATIMGPH_" in html:
            errors.append("HTML contains WECHATIMGPH placeholder")
        for source in html_image_sources(html):
            target = _local_target(html_path, source)
            if target is not None and not target.is_file():
                errors.append(f"missing HTML image: {source}")

    return errors


def _ratio(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"([1-9]\d*):([1-9]\d*)", value)
    if match is None:
        raise argparse.ArgumentTypeError("ratio must use positive W:H integers")
    return int(match.group(1)), int(match.group(2))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a Jiaojie WeChat publishing package.")
    parser.add_argument("package_dir", type=Path)
    parser.add_argument("--min-images", type=int, default=3)
    parser.add_argument("--max-images", type=int, default=5)
    parser.add_argument("--ratio", type=_ratio, default=(3, 2), metavar="W:H")
    args = parser.parse_args(argv)

    if args.min_images < 1 or args.max_images < args.min_images:
        parser.error("require 1 <= --min-images <= --max-images")

    errors = validate_package(args.package_dir, args.min_images, args.max_images, args.ratio)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("PACKAGE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
