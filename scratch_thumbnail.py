#!/usr/bin/env python3
# coding: utf-8
"""
scratch_image_fetcher.py
使い方（CLI）:
  python scratch_image_fetcher.py "<入力（project id / project URL / direct image URL）>" [--size 1000x1000] [--show]
例:
  python scratch_image_fetcher.py "12345678"
  python scratch_image_fetcher.py "https://scratch.mit.edu/projects/12345678/" --size 480x360 --show
"""

import re
import sys
import argparse
from typing import Optional
from urllib.parse import urlparse
import requests

# 正規表現（大文字小文字無視）
DIRECT_IMAGE_RE = re.compile(
    r"https?://(?:www\.)?scratch\.mit\.edu/get_image/project/(\d+)_.*\.png", re.I
)
PROJECT_PAGE_RE = re.compile(
    r"(?:https?://)?(?:www\.)?scratch\.mit\.edu/projects/(\d+)(?:/.*)?", re.I
)
DIGITS_RE = re.compile(r"^\d{1,10}$")  # reasonable length limit

def extract_project_id(user_input: str) -> Optional[str]:
    if not user_input:
        return None
    s = user_input.strip()
    # direct image url
    m = DIRECT_IMAGE_RE.search(s)
    if m:
        return m.group(1)
    # project page url (with or without scheme)
    m = PROJECT_PAGE_RE.search(s)
    if m:
        return m.group(1)
    # pure digits
    if DIGITS_RE.match(s):
        return s
    return None

def build_image_url(project_id: str, size: str = "1000x1000") -> str:
    # size should be like "1000x1000" or "480x360"
    safe_size = size if re.match(r"^\d+x\d+$", size) else "1000x1000"
    return f"https://scratch.mit.edu/get_image/project/{project_id}_{safe_size}.png"

def check_url_exists(url: str, timeout: float = 5.0) -> bool:
    try:
        # HEAD first; fallback to GET if server doesn't support HEAD
        resp = requests.head(url, allow_redirects=True, timeout=timeout)
        if resp.status_code == 405:  # method not allowed
            resp = requests.get(url, stream=True, timeout=timeout)
        return 200 <= resp.status_code < 400
    except requests.RequestException:
        return False

def is_probably_url(s: str) -> bool:
    try:
        p = urlparse(s)
        return bool(p.scheme and p.netloc)
    except Exception:
        return False

def main(argv=None):
    parser = argparse.ArgumentParser(description="Scratch project image URL builder/fetcher")
    parser.add_argument("input", help="project id | scratch project URL | direct image URL")
    parser.add_argument("--size", default="1000x1000", help="image size, e.g. 1000x1000 or 480x360")
    parser.add_argument("--show", action="store_true", help="If running in Jupyter, attempt to display the image")
    parser.add_argument("--no-check", action="store_true", help="skip checking if the image URL exists (faster)")
    args = parser.parse_args(argv)

    user_input = args.input
    project_id = extract_project_id(user_input)

    if not project_id:
        print("エラー: 有効なプロジェクトIDまたは Scratch プロジェクト URL を指定してください。")
        # If the input looked like a URL, print a little hint
        if is_probably_url(user_input):
            print("ヒント: scratch.mit.edu のプロジェクト URL かプロジェクト ID を渡してください。")
        sys.exit(1)

    image_url = build_image_url(project_id, size=args.size)
    print(f"project_id: {project_id}")
    print(f"generated image url: {image_url}")

    if not args.no_check:
        exists = check_url_exists(image_url)
        print(f"image exists: {exists}")
    else:
        print("image existence check: skipped")

    # If running inside Jupyter and user asked --show, attempt to display
    if args.show:
        try:
            from IPython.display import Image, display  # type: ignore
            display(Image(url=image_url))
        except Exception:
            print("画像を表示できませんでした（Jupyter 環境でないか、IPython が利用できません）。")

if __name__ == "__main__":
    main()

