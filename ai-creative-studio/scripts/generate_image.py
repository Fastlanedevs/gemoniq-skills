"""Generate a single image via the Gemoniq Studio API (metered, token-authenticated).

Credentials resolution order:
  1. Environment variables GEMONIQ_BASE_URL / GEMONIQ_API_KEY
  2. ~/.gemoniq-studio/config.json (auto-created on first interactive run)
  3. Interactive prompt for GEMONIQ_API_KEY (saved to config.json)

GEMONIQ_BASE_URL defaults to https://app.gemoniq.com when neither env nor config
sets it. Override via env for local dev (e.g. GEMONIQ_BASE_URL=http://localhost:3000).

Usage:
    # Text-to-image
    python scripts/generate_image.py --prompt "A cat on a hill at sunset" --output cat.png

    # With character reference image
    python scripts/generate_image.py --prompt "Same person walking in rain" --ref refs/char.png --output scene.png

    # With aspect ratio and resolution
    python scripts/generate_image.py --prompt "..." --output scene.png --aspect 16:9 --size 2K

    # Edit existing image
    python scripts/generate_image.py --prompt "Remove the person" --edit source.png --output edited.png

    # Multiple reference images
    python scripts/generate_image.py --prompt "..." --ref ref1.png --ref ref2.png --output scene.png
"""
import os, sys, argparse, time, json, base64
import urllib.request
from pathlib import Path

DEFAULT_BASE_URL = "https://app.gemoniq.com"
CONFIG_PATH = Path.home() / ".gemoniq-studio" / "config.json"

def _load_config():
    if not CONFIG_PATH.exists():
        return {}
    try:
        return json.loads(CONFIG_PATH.read_text())
    except Exception:
        return {}

def _save_config(config):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n")
    try:
        CONFIG_PATH.chmod(0o600)
    except Exception:
        pass

def resolve_credentials():
    config = _load_config()
    base_url = (os.environ.get("GEMONIQ_BASE_URL") or config.get("GEMONIQ_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
    api_key = os.environ.get("GEMONIQ_API_KEY") or config.get("GEMONIQ_API_KEY")
    if not api_key:
        if not sys.stdin.isatty():
            print(f"ERROR: GEMONIQ_API_KEY not set. Add it to {CONFIG_PATH}, export it, or run interactively.", file=sys.stderr)
            sys.exit(1)
        print(f"No GEMONIQ_API_KEY found. Get one at {base_url}/settings/api", file=sys.stderr)
        api_key = input("Enter GEMONIQ_API_KEY: ").strip()
        if not api_key:
            print("ERROR: no key provided", file=sys.stderr)
            sys.exit(1)
        config["GEMONIQ_API_KEY"] = api_key
        _save_config(config)
        print(f"Saved to {CONFIG_PATH}", file=sys.stderr)
    return base_url, api_key

def image_to_data_url(path):
    """Read an image file and return a data URL."""
    with open(path, "rb") as f:
        data = f.read()
    ext = os.path.splitext(path)[1].lower()
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(ext, "image/png")
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"

def main():
    parser = argparse.ArgumentParser(description="Generate image with Nano Banana 2")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--output", required=True, help="Output file path (.png)")
    parser.add_argument("--ref", action="append", default=[], help="Reference image path (repeatable, up to 4)")
    parser.add_argument("--edit", default=None, help="Source image to edit (inpainting/modification)")
    parser.add_argument("--aspect", default="16:9", help="Aspect ratio (default: 16:9)")
    parser.add_argument("--size", default=None, help="Image size: 512, 1K, 2K, 4K")
    parser.add_argument("--retries", type=int, default=3, help="Max retry attempts")
    parser.add_argument("--skip-existing", action="store_true", help="Skip if output already exists")
    args = parser.parse_args()

    if args.skip_existing and os.path.exists(args.output):
        print(f"SKIP {args.output} (exists)")
        return

    base_url, api_key = resolve_credentials()
    api_url = f"{base_url}/api/studio/generate-image"

    # Build request body
    body = {
        "prompt": args.prompt,
        "aspectRatio": args.aspect,
        "referenceMode": "incorporate",
    }
    if args.size:
        body["resolution"] = args.size

    # Encode reference images as data URLs
    image_urls = []
    if args.edit:
        image_urls.append(image_to_data_url(args.edit))
        body["referenceMode"] = "edit"
    elif args.ref:
        for ref_path in args.ref:
            image_urls.append(image_to_data_url(ref_path))

    if image_urls:
        body["imageUrls"] = image_urls

    payload = json.dumps(body).encode("utf-8")

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    for attempt in range(args.retries):
        try:
            print(f"Generating (attempt {attempt+1}/{args.retries})...")
            req = urllib.request.Request(
                api_url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode())

            if not result.get("success"):
                print(f"Server error: {result.get('error', 'Unknown')}")
                if attempt < args.retries - 1:
                    time.sleep(3 * (attempt + 1))
                continue

            # Download the image from the returned URL
            image_url = result["imageUrl"]
            print(f"Downloading from {image_url[:80]}...")
            with urllib.request.urlopen(image_url, timeout=60) as img_resp:
                img_data = img_resp.read()

            with open(args.output, "wb") as f:
                f.write(img_data)

            credits = result.get("credits", {})
            print(f"SAVED {args.output} (credits used: {credits.get('used', '?')}, remaining: {credits.get('remaining', '?')})")
            return

        except Exception as e:
            print(f"ERROR: {e}")
            if attempt < args.retries - 1:
                time.sleep(3 * (attempt + 1))

    print(f"FAILED after {args.retries} attempts")
    sys.exit(1)

if __name__ == "__main__":
    main()
