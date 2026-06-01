from __future__ import annotations

import base64
import hashlib
import json
import subprocess
import sys

try:
    from cryptography.fernet import Fernet, InvalidToken
    HAS_FERNET = True
except ImportError:
    HAS_FERNET = False


def _derive_key(machine_id: str) -> bytes:
    raw = hashlib.sha256(machine_id.encode()).digest()
    return base64.urlsafe_b64encode(raw)


def get_machine_id() -> str:
    if sys.platform == "win32":
        try:
            result = subprocess.run(
                ["wmic", "csproduct", "get", "uuid"],
                capture_output=True, text=True, timeout=5,
            )
            lines = [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
            for line in lines:
                if line.lower() != "uuid" and line:
                    return line
        except Exception:
            pass
        try:
            result = subprocess.run(
                ["cmd", "/c", "echo", "%COMPUTERNAME%"],
                capture_output=True, text=True, timeout=5,
            )
            return result.stdout.strip() or "default-win-id"
        except Exception:
            return "default-win-id"
    else:
        try:
            with open("/etc/machine-id") as f:
                return f.read().strip()
        except FileNotFoundError:
            try:
                with open("/var/lib/dbus/machine-id") as f:
                    return f.read().strip()
            except FileNotFoundError:
                return "default-unix-id"


def encrypt_data(data: dict) -> str:
    if not HAS_FERNET:
        return _obfuscate(data)
    machine_id = get_machine_id()
    key = _derive_key(machine_id)
    f = Fernet(key)
    return f.encrypt(json.dumps(data).encode()).decode()


def decrypt_data(encrypted: str) -> dict | None:
    if not HAS_FERNET:
        return _deobfuscate(encrypted)
    machine_id = get_machine_id()
    key = _derive_key(machine_id)
    try:
        f = Fernet(key)
        return json.loads(f.decrypt(encrypted.encode()))
    except (InvalidToken, Exception):
        return None


def _obfuscate(data: dict) -> str:
    raw = json.dumps(data, ensure_ascii=False)
    return base64.urlsafe_b64encode(raw.encode()).decode()


def _deobfuscate(encoded: str) -> dict | None:
    try:
        raw = base64.urlsafe_b64decode(encoded.encode())
        return json.loads(raw)
    except Exception:
        return None
