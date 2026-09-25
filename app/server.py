"""Alvo didático local. Nunca publicar como serviço de produção."""
import hashlib
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from jinja2.sandbox import SandboxedEnvironment

MODE = os.environ.get("LAB_MODE", "corrigido")
TEMPLATES = SandboxedEnvironment(autoescape=True)


def demonstration_digest(text):
    """Checksum didático com SHA-256; não é autenticação ou assinatura."""
    return hashlib.sha256(text.encode()).hexdigest()


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, value):
        body = json.dumps(value, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/health"):
            return self.reply(200, {"project": "CP01-DevSecOps", "status": "ok", "mode": MODE})
        if path == "/debug" and MODE == "vulneravel":
            return self.reply(200, {
                "lab_marker": "cp01-debug-exposure",
                "internal_config": {"database_host": "example.internal", "environment": "training-only"},
                "notice": "Dados fictícios: exemplo de exposição de configuração interna.",
            })
        return self.reply(404, {"error": "not found"})

    def do_POST(self):
        if urlparse(self.path).path != "/preview":
            return self.reply(404, {"error": "not found"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 4096:
                return self.reply(400, {"error": "body must contain 1..4096 bytes"})
            data = json.loads(self.rfile.read(length))
            template = data.get("template", "Olá, {{ name }}!")
            if not isinstance(template, str):
                return self.reply(400, {"error": "template must be a string"})
            result = TEMPLATES.from_string(template).render(name="Grupo 2")
            return self.reply(200, {"preview": result, "checksum": demonstration_digest(result)})
        except Exception:
            return self.reply(400, {"error": "invalid template or request"})


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()

