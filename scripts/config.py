"""Settings for the Freelancer OS scripts.

Reads config.yml at the repo root (flat `key: value` lines, plus the one nested
`lanes:` block), then .env for keys. Standard library only; no YAML library needed
because the file is deliberately flat.

    from config import get, get_key, path_for
    get("sender_name")            -> "Sam Carter"
    get("lanes.maps_scout")       -> True
    get_key("PAGESPEED_API_KEY")  -> the key, or a clear error
    path_for("leads_dir")         -> Path to the leads folder (created if missing)
"""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = Path(os.environ.get("FOS_CONFIG", ROOT / "config.yml"))
ENV_FILE = ROOT / ".env"

_cfg: dict[str, object] | None = None

DEFAULTS: dict[str, object] = {
    "sender_name": "",
    "sender_email": "",
    "portfolio_url": "",
    "business_one_line": "",
    "resume_path": "",
    "lanes.job_post": True,
    "lanes.job_scout": False,
    "lanes.maps_scout": False,
    "lanes.seo_scout": False,
    "daily_send_cap": 20,
    "per_15_min_cap": 5,
    "stale_days_job_post": 3,
    "stale_days_maps": 7,
    "stale_days_seo": 7,
    "leads_dir": "leads",
    "clients_dir": "clients",
    "runs_dir": "runs",
    "pagespeed_api_key": "",
    "apify_api_token": "",
}


def _coerce(v: str) -> object:
    s = v.strip().strip('"').strip("'")
    low = s.lower()
    if low in ("on", "true", "yes"):
        return True
    if low in ("off", "false", "no"):
        return False
    if s.lstrip("-").isdigit():
        return int(s)
    return s


def _parse(text: str) -> dict[str, object]:
    out: dict[str, object] = {}
    section = ""
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip() or ":" not in line:
            continue
        key, _, val = line.partition(":")
        indented = line.startswith((" ", "\t"))
        key = key.strip()
        if not indented:
            section = ""
            if val.strip() == "":
                section = key
                continue
            out[key] = _coerce(val)
        else:
            out[f"{section}.{key}" if section else key] = _coerce(val)
    return out


def _load_env() -> None:
    if not ENV_FILE.exists():
        return
    for raw in ENV_FILE.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def load() -> dict[str, object]:
    global _cfg
    if _cfg is None:
        _cfg = dict(DEFAULTS)
        if CONFIG_FILE.exists():
            _cfg.update(_parse(CONFIG_FILE.read_text()))
        _load_env()
    return _cfg


def get(key: str, default: object = None) -> object:
    return load().get(key, default)


def get_key(name: str, required: bool = True) -> str:
    """An API key: .env first, then the matching config.yml line, then a clear error."""
    load()
    value = os.environ.get(name, "").strip() or str(get(name.lower(), "") or "").strip()
    if not value and required:
        raise RuntimeError(
            f"{name} is not set. Put it in .env at the repo root as {name}=..., "
            f"or run /activate (see config.example.yml)."
        )
    return value


def path_for(key: str) -> Path:
    """A folder from config (leads_dir, clients_dir, runs_dir), made absolute and created."""
    p = Path(str(get(key) or DEFAULTS[key]))
    if not p.is_absolute():
        p = ROOT / p
    p.mkdir(parents=True, exist_ok=True)
    return p
