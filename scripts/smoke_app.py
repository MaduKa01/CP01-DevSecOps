"""Rodar dentro de cada container; valida apenas requisições didáticas benignas."""
import json
import os
import urllib.error
import urllib.request

base = "http://127.0.0.1:8080"
with urllib.request.urlopen(base + "/health", timeout=5) as response:
    assert json.load(response)["status"] == "ok"
body = json.dumps({"template": "Olá, {{ name }}!"}).encode()
request = urllib.request.Request(base + "/preview", data=body, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(request, timeout=5) as response:
    assert json.load(response)["preview"] == "Olá, Grupo 2!"
try:
    with urllib.request.urlopen(base + "/debug", timeout=5) as response:
        assert os.environ["LAB_MODE"] == "vulneravel"
        assert json.load(response)["lab_marker"] == "cp01-debug-exposure"
except urllib.error.HTTPError as error:
    assert os.environ["LAB_MODE"] == "corrigido" and error.code == 404
print("OK: health, renderização de template e comportamento do /debug")
