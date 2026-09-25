#!/usr/bin/env python3
"""Inicializa apenas o SonarQube local deste Compose; guarda segredos em .env."""
import base64
import json
from pathlib import Path
import secrets
import sys
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
URL = "http://127.0.0.1:19000"


def request(path, password, data=None):
    req = urllib.request.Request(URL + path, data=urllib.parse.urlencode(data).encode() if data is not None else None)
    req.add_header("Authorization", "Basic " + base64.b64encode(f"admin:{password}".encode()).decode())
    with urllib.request.urlopen(req, timeout=30) as response:
        body = response.read()
    return json.loads(body) if body else {}


def main():
    try:
        with urllib.request.urlopen(URL + "/api/system/status", timeout=5) as response:
            status = json.load(response).get("status")
        if status != "UP":
            print(f"SonarQube ainda está iniciando ({status}). Aguarde e execute novamente.")
            return 1
    except OSError:
        print("SonarQube ainda não responde em localhost:19000. Confira docker compose logs sonarqube.")
        return 1
    env_file = ROOT / ".env"
    env = {}
    if env_file.exists():
        env = dict(line.split("=", 1) for line in env_file.read_text().splitlines() if "=" in line and not line.startswith("#"))
    password = env.get("SONAR_ADMIN_PASSWORD", "admin")
    if password == "admin":
        password = "Lab9!" + secrets.token_urlsafe(24)
        request("/api/users/change_password", "admin", {"login": "admin", "previousPassword": "admin", "password": password})
        env["SONAR_ADMIN_PASSWORD"] = password
        env_file.write_text("\n".join(f"{k}={v}" for k, v in env.items()) + "\n")
        env_file.chmod(0o600)
    projects = request("/api/projects/search?projects=cp01-devsecops-grupo2", password)
    if not projects.get("components"):
        request("/api/projects/create", password, {"project": "cp01-devsecops-grupo2", "name": "CP01 DevSecOps - Grupo 2", "visibility": "private"})
    if "SONAR_TOKEN" not in env:
        token = request("/api/user_tokens/generate", password, {"name": "cp01-local-" + secrets.token_hex(4), "type": "PROJECT_ANALYSIS_TOKEN", "projectKey": "cp01-devsecops-grupo2"})
        env["SONAR_TOKEN"] = token["token"]
    env_file.write_text("\n".join(f"{k}={v}" for k, v in env.items()) + "\n")
    env_file.chmod(0o600)
    print("SonarQube local configurado. Credenciais somente no .env ignorado pelo Git.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
