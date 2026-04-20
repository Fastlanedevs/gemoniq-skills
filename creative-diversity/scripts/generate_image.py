"""Minimal Gemoniq Studio image generator.

Reads GEMONIQ_API_KEY from the environment or ~/.gemoniq-studio/config.json.
Makes a single POST to the Gemoniq generate-image endpoint and writes the result to disk.
No retries, no interactive prompts, no edit mode -- keep this script small on purpose.

Usage:
    python scripts/generate_image.py --prompt "..." --output out.png --aspect 1:1 --ref source.png
"""
import os, sys, json, argparse, base64
import urllib.request
from pathlib import Path

BASE_URL = os.environ.get("GEMONIQ_BASE_URL", "https://app.gemoniq.com").rstrip("/")
CONFIG_PATH = Path.home() / ".gemoniq-studio" / "config.json"


def get_api_key():
    key = os.environ.get("GEMONIQ_API_KEY")
    if key:
        return key
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text()).get("GEMONIQ_API_KEY")
        except Exception:
            pass
    print(f"ERROR: GEMONIQ_API_KEY not found. Put it in {CONFIG_PATH} or export it.", file=sys.stderr)
    sys.exit(1)


def data_url(path):
    ext = os.path.splitext(path)[1].lower()
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(ext, "image/png")
    with open(path, "rb") as f:
        return f"data:{mime};base64,{base64.b64encode(f.read()).decode()}"


def main():
    p = argparse.ArgumentParser(description="Minimal Gemoniq image generator")
    p.add_argument("--prompt", required=True, help="Image prompt")
    p.add_argument("--output", required=True, help="Output file path (.png)")
    p.add_argument("--ref", action="append", default=[], help="Reference image path (repeatable, up to 4)")
    p.add_argument("--aspect", default="1:1", help="Aspect ratio (e.g. 1:1, 4:5, 9:16, 16:9)")
    p.add_argument("--size", default=None, help="Resolution: 512, 1K, 2K, 4K")
    args = p.parse_args()

    body = {"prompt": args.prompt, "aspectRatio": args.aspect, "referenceMode": "incorporate"}
    if args.size:
        body["resolution"] = args.size
    if args.ref:
        body["imageUrls"] = [data_url(r) for r in args.ref]

    api_key = get_api_key()
    req = urllib.request.Request(
        f"{BASE_URL}/api/studio/generate-image",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=180) as resp:
        result = json.loads(resp.read().decode())

    if not result.get("success"):
        print(f"ERROR: {result.get('error', 'unknown')}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with urllib.request.urlopen(result["imageUrl"], timeout=60) as r:
        Path(args.output).write_bytes(r.read())
    print(f"SAVED {args.output}")


if __name__ == "__main__":
    main()
