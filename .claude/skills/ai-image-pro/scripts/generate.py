#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""AI-Image Pro generator.

Commands:
  doctor [--init-env]   Check setup (keys, .env location, .gitignore).
  image  --prompt ...   Generate one image (Kie AI primary, Gemini fallback).

Stdlib only. Keys come from the environment or <project root>/.env.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import mimetypes
import os
import re
import shutil
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
MODELS_FILE = SKILL_DIR / "models.json"
KEY_NAMES = ("KIE_API_KEY", "GEMINI_API_KEY")
ENV_TEMPLATE = """# AI-Image Pro keys. This file must never be committed.
# Primary route: GPT Image 2 via Kie AI (https://kie.ai)
KIE_API_KEY=
# Fallback route: Gemini image models (https://aistudio.google.com/apikey)
GEMINI_API_KEY=
"""


# ---------------------------------------------------------------- utilities
def log(msg: str) -> None:
    print(msg, file=sys.stderr)


def find_project_root(start: Path | None = None) -> Path:
    """Walk up from cwd to the first dir holding .claude/ or .git/."""
    cur = (start or Path.cwd()).resolve()
    for d in (cur, *cur.parents):
        if d == Path.home() and d != cur:
            break
        if (d / ".git").exists() or (d / ".claude").is_dir():
            # A .claude dir that *is* the skills tree's parent is not a root marker
            if d.name == ".claude":
                continue
            return d
    return cur


def parse_env_file(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k = k.strip().removeprefix("export ").strip()
        v = v.strip().strip('"').strip("'")
        if v:
            out[k] = v
    return out


def load_keys(root: Path) -> dict[str, str]:
    keys: dict[str, str] = {}
    leaked = SKILL_DIR / ".env"
    if leaked.is_file():
        log(f"WARNING: {leaked} holds keys inside the skill folder. Move it to {root / '.env'} and delete it.")
        keys.update(parse_env_file(leaked))
    keys.update(parse_env_file(root / ".env"))
    for k in KEY_NAMES:  # shell wins
        if os.environ.get(k):
            keys[k] = os.environ[k]
    return {k: v for k, v in keys.items() if k in KEY_NAMES and v}


def env_gitignored(root: Path) -> bool:
    gi = root / ".gitignore"
    if not gi.is_file():
        return False
    for line in gi.read_text(encoding="utf-8").splitlines():
        if line.strip() in (".env", "/.env", "*.env", ".env*"):
            return True
    return False


def load_models() -> dict:
    return json.loads(MODELS_FILE.read_text(encoding="utf-8"))


def ssl_context() -> ssl.SSLContext:
    for var in ("SSL_CERT_FILE", "REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE", "NODE_EXTRA_CA_CERTS"):
        p = os.environ.get(var)
        if p and Path(p).is_file():
            return ssl.create_default_context(cafile=p)
    return ssl.create_default_context()


class ProviderError(Exception):
    pass


def http_json(method: str, url: str, headers: dict[str, str], body: dict | None = None, timeout: int = 180) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("User-Agent", "ai-image-pro/1.0")
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context()) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        raise ProviderError(f"HTTP {e.code} from {urllib.parse.urlsplit(url).netloc}: {detail}") from None
    except urllib.error.URLError as e:
        raise ProviderError(f"blocked by network or unreachable ({urllib.parse.urlsplit(url).netloc}): {e.reason}") from None


def download(url: str) -> tuple[bytes, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "ai-image-pro/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=180, context=ssl_context()) as r:
            return r.read(), r.headers.get_content_type()
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        raise ProviderError(f"could not download result {url}: {e}") from None


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s[:60] or "image"


def ext_for(mime: str) -> str:
    return {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp"}.get(mime, mimetypes.guess_extension(mime) or ".png")


def read_image(path: str) -> tuple[bytes, str]:
    p = Path(path).expanduser()
    if not p.is_file():
        raise SystemExit(f"input image not found: {path}")
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    return p.read_bytes(), mime


# ---------------------------------------------------------------- providers
def run_gemini(cfg: dict, key: str, model: str, prompt: str, aspect: str | None,
               resolution: str | None, inputs: list[str]) -> dict:
    m = cfg["gemini"]["models"][model]
    parts: list[dict] = []
    for path in inputs:
        raw, mime = read_image(path)
        parts.append({"inline_data": {"mime_type": mime, "data": base64.b64encode(raw).decode()}})
    parts.append({"text": prompt})
    image_cfg: dict = {}
    if aspect:
        image_cfg["aspectRatio"] = aspect
    if resolution and m.get("supports_image_size"):
        image_cfg["imageSize"] = resolution.upper()
    gen_cfg: dict = {"responseModalities": ["TEXT", "IMAGE"]}
    if image_cfg:
        gen_cfg["imageConfig"] = image_cfg
    url = f"{cfg['gemini']['api_base']}/models/{m['id']}:generateContent"
    resp = http_json("POST", url, {"x-goog-api-key": key},
                     {"contents": [{"role": "user", "parts": parts}], "generationConfig": gen_cfg}, timeout=300)
    texts = []
    for cand in resp.get("candidates", []):
        for part in (cand.get("content") or {}).get("parts", []):
            blob = part.get("inlineData") or part.get("inline_data")
            if blob and blob.get("data"):
                mime = blob.get("mimeType") or blob.get("mime_type") or "image/png"
                return {"bytes": base64.b64decode(blob["data"]), "mime": mime, "model_id": m["id"]}
            if part.get("text"):
                texts.append(part["text"])
    reason = resp.get("promptFeedback", {}).get("blockReason") or (resp.get("candidates") or [{}])[0].get("finishReason")
    raise ProviderError(f"Gemini returned no image (reason: {reason}; text: {' '.join(texts)[:300]})")


def kie_upload(cfg: dict, key: str, path: str) -> str:
    raw, mime = read_image(path)
    body = {
        "base64Data": f"data:{mime};base64,{base64.b64encode(raw).decode()}",
        "uploadPath": "images/ai-image-pro",
        "fileName": Path(path).name,
    }
    resp = http_json("POST", cfg["kie"]["upload_base64"], {"Authorization": f"Bearer {key}"}, body)
    data = resp.get("data") or {}
    url = data.get("downloadUrl") or data.get("fileUrl") or data.get("url")
    if not url:
        raise ProviderError(f"Kie upload returned no URL: {json.dumps(resp)[:300]}")
    return url


def run_kie(cfg: dict, key: str, model: str, prompt: str, aspect: str | None,
            resolution: str | None, inputs: list[str]) -> dict:
    k = cfg["kie"]
    m = k["models"][model]
    auth = {"Authorization": f"Bearer {key}"}
    inp: dict = {"prompt": prompt, **m.get("extra", {})}
    slug = m["slug"]
    if inputs:
        inp[m["image_field"]] = [kie_upload(cfg, key, p) for p in inputs]
        slug = m.get("edit_slug") or slug
    if aspect and m.get("aspect_field"):
        inp[m["aspect_field"]] = aspect
    if resolution and m.get("resolution_field"):
        inp[m["resolution_field"]] = resolution.upper()
    resp = http_json("POST", k["api_base"] + k["create_task"], auth, {"model": slug, "input": inp})
    if resp.get("code") not in (None, 200):
        raise ProviderError(f"Kie createTask failed: {resp.get('code')} {resp.get('msg')}")
    task_id = (resp.get("data") or {}).get("taskId")
    if not task_id:
        raise ProviderError(f"Kie createTask returned no taskId: {json.dumps(resp)[:300]}")
    log(f"kie task {task_id} created; polling...")
    deadline = time.time() + k.get("timeout_seconds", 600)
    while time.time() < deadline:
        time.sleep(k.get("poll_seconds", 5))
        q = http_json("GET", f"{k['api_base']}{k['record_info']}?taskId={urllib.parse.quote(task_id)}", auth)
        d = q.get("data") or {}
        state = (d.get("state") or "").lower()
        if state == "success":
            rj = d.get("resultJson") or "{}"
            rj = json.loads(rj) if isinstance(rj, str) else rj
            urls = rj.get("resultUrls") or rj.get("result_urls") or []
            if not urls:
                raise ProviderError(f"Kie task succeeded without resultUrls: {str(rj)[:300]}")
            raw, mime = download(urls[0])  # URLs expire: download now
            return {"bytes": raw, "mime": mime, "model_id": slug, "task_id": task_id}
        if state in ("fail", "failed", "error"):
            raise ProviderError(f"Kie task failed: {d.get('failCode')} {d.get('failMsg')}")
    raise ProviderError(f"Kie task {task_id} timed out")


PROVIDERS = {"kie": (run_kie, "KIE_API_KEY"), "gemini": (run_gemini, "GEMINI_API_KEY")}


def resolve_model(cfg: dict, provider: str, model: str) -> str | None:
    if model in cfg[provider]["models"]:
        return model
    return cfg.get("fallback_model", {}).get(provider, {}).get(model)


# ---------------------------------------------------------------- commands
def cmd_doctor(args: argparse.Namespace) -> int:
    root = find_project_root()
    rows: list[tuple[str, str]] = []
    rows.append(("project_root", str(root)))
    env_path = root / ".env"
    if args.init_env:
        if not env_path.exists():
            env_path.write_text(ENV_TEMPLATE, encoding="utf-8")
            rows.append(("init_env", f"created {env_path}"))
        if (root / ".git").exists() and not env_gitignored(root):
            gi = root / ".gitignore"
            prefix = "" if not gi.exists() or gi.read_text(encoding="utf-8").endswith("\n") or gi.stat().st_size == 0 else "\n"
            with gi.open("a", encoding="utf-8") as f:
                f.write(f"{prefix}.env\n")
            rows.append(("init_env", f"added .env to {gi}"))
    rows.append(("env_file", "OK" if env_path.is_file() else "missing"))
    if (root / ".git").exists():
        rows.append(("env_gitignored", "OK" if env_gitignored(root) else "missing from .gitignore"))
    else:
        rows.append(("env_gitignored", "OK (not a git repo)"))
    rows.append(("skill_folder_clean", "LEAK (.env inside skill folder)" if (SKILL_DIR / ".env").exists() else "OK"))
    keys = load_keys(root)
    for k in KEY_NAMES:
        rows.append((k, "OK" if k in keys else "missing"))
    avail = [p for p, (_, k) in PROVIDERS.items() if k in keys]
    rows.append(("image", f"available ({', '.join(avail)})" if avail else "BLOCKED (no API key)"))
    if len(avail) == 1:
        rows.append(("fallback", "none (only one key)"))
    try:
        cfg = load_models()
        age = (dt.date.today() - dt.date.fromisoformat(cfg.get("updated", "2000-01-01"))).days
        rows.append(("models_registry", f"OK ({age} days old)" + (" - consider refresh" if age > 30 else "")))
        if not cfg["kie"].get("verified"):
            rows.append(("kie_registry", "unverified slugs - see models.json note"))
    except Exception as e:  # noqa: BLE001
        rows.append(("models_registry", f"ERROR {e}"))
    w = max(len(a) for a, _ in rows)
    for a, b in rows:
        print(f"{a.ljust(w)}  {b}")
    return 0 if avail else 1


def cmd_image(args: argparse.Namespace) -> int:
    cfg = load_models()
    root = find_project_root()
    keys = load_keys(root)
    model = args.model or cfg["default_model"]
    first = args.provider or cfg["default_provider"]
    order = [first] + [p for p in PROVIDERS if p != first]
    if args.no_fallback:
        order = [first]

    attempts: list[dict] = []
    result = None
    used_provider = used_model = None
    for prov in order:
        fn, key_name = PROVIDERS[prov]
        pm = resolve_model(cfg, prov, model)
        if not pm:
            attempts.append({"provider": prov, "error": f"model {model} not available on {prov}"})
            continue
        if key_name not in keys:
            attempts.append({"provider": prov, "error": f"{key_name} missing"})
            continue
        if args.dry_run:
            print(json.dumps({"dry_run": True, "provider": prov, "model": pm, "prompt": args.prompt,
                              "aspect_ratio": args.aspect_ratio, "resolution": args.resolution,
                              "input_images": args.input_image}, ensure_ascii=False))
            return 0
        log(f"trying {prov} / {pm} ...")
        try:
            result = fn(cfg, keys[key_name], pm, args.prompt, args.aspect_ratio, args.resolution, args.input_image)
            used_provider, used_model = prov, pm
            break
        except ProviderError as e:
            log(f"{prov} failed: {e}")
            attempts.append({"provider": prov, "model": pm, "error": str(e)})

    if result is None:
        print(json.dumps({"ok": False, "attempts": attempts}, ensure_ascii=False))
        return 1

    title = slugify(args.title or args.prompt[:40])
    base = Path(args.out_dir).expanduser() if args.out_dir else root / "generations"
    folder = base / f"{dt.date.today().isoformat()}-{title}"
    n = 2
    while folder.exists():
        folder = base / f"{dt.date.today().isoformat()}-{title}-{n}"
        n += 1
    folder.mkdir(parents=True)

    refs_saved = []
    if args.input_image:
        refs = base / "refs"
        refs.mkdir(parents=True, exist_ok=True)
        for p in args.input_image:
            src = Path(p).expanduser().resolve()
            dst = refs / src.name
            if src != dst.resolve():
                shutil.copy2(src, dst)
            refs_saved.append(str(dst))

    img_path = folder / f"{title}{ext_for(result['mime'])}"
    img_path.write_bytes(result["bytes"])

    meta = {
        "ok": True,
        "image_path": str(img_path),
        "folder": str(folder),
        "provider": used_provider,
        "model": used_model,
        "model_id": result.get("model_id"),
        "requested_provider": first,
        "requested_model": model,
        "fallback_from": attempts[0]["provider"] if attempts and used_provider != first else None,
        "attempts": attempts,
        "prompt": args.prompt,
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "input_images": refs_saved,
        "task_id": result.get("task_id"),
        "created": dt.datetime.now().isoformat(timespec="seconds"),
    }
    (folder / f"{title}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    (folder / "prompt.md").write_text(
        f"# {title}\n\n- Provider: {used_provider}\n- Model: {used_model} ({result.get('model_id')})\n"
        f"- Aspect ratio: {args.aspect_ratio or 'default'}\n- Resolution: {args.resolution or 'default'}\n"
        f"- Reference images: {', '.join(refs_saved) or 'none'}\n- Created: {meta['created']}\n\n"
        f"## Prompt\n\n{args.prompt}\n", encoding="utf-8")

    if not args.no_downloads:
        dl = Path.home() / "Downloads"
        try:
            dl.mkdir(exist_ok=True)
            shutil.copy2(img_path, dl / img_path.name)
            meta["downloads_copy"] = str(dl / img_path.name)
        except OSError as e:
            log(f"could not copy to Downloads: {e}")

    print(json.dumps(meta, ensure_ascii=False))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="AI-Image Pro")
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("doctor", help="check setup")
    d.add_argument("--init-env", action="store_true", help="create <root>/.env and gitignore it")
    i = sub.add_parser("image", help="generate one image")
    i.add_argument("--prompt", required=True)
    i.add_argument("--title")
    i.add_argument("--provider", choices=list(PROVIDERS))
    i.add_argument("--model", choices=["gpt-image-2", "nano-banana-pro", "nano-banana-2-lite"])
    i.add_argument("--aspect-ratio")
    i.add_argument("--resolution", choices=["1K", "2K", "4K", "1k", "2k", "4k"], default="2K")
    i.add_argument("--input-image", action="append", default=[])
    i.add_argument("--out-dir")
    i.add_argument("--no-fallback", action="store_true")
    i.add_argument("--no-downloads", action="store_true", help="skip the ~/Downloads copy")
    i.add_argument("--dry-run", action="store_true", help="show the chosen route without calling any API")
    args = ap.parse_args()
    return cmd_doctor(args) if args.cmd == "doctor" else cmd_image(args)


if __name__ == "__main__":
    sys.exit(main())
