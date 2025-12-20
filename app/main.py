import os
import random
import time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from .otel import configure_otel

SERVICE_NAME = os.getenv("SERVICE_NAME", "trustchain-api")
configure_otel(service_name=SERVICE_NAME)

app = FastAPI(
    title="TrustChain Playground",
    version=os.getenv("APP_VERSION", "0.1.0"),
    description="A tiny app demonstrating modern supply-chain security + GitOps + policy + observability."
)

QUOTES = [
    "Ship fast, verify faster.",
    "If it’s not attested, it’s not trusted.",
    "Policy is how you scale security.",
    "Observability beats guessing.",
    "Signed artifacts reduce supply-chain risk."
]

@app.get("/healthz")
def healthz():
    return {"ok": True}

@app.get("/api/quote")
def quote():
    return {"quote": random.choice(QUOTES)}

@app.post("/api/echo")
async def echo(payload: dict):
    # simulate variable work so traces/metrics look real
    delay_ms = int(payload.get("delay_ms", random.randint(10, 120)))
    time.sleep(delay_ms / 1000.0)
    return {"echo": payload, "delay_ms": delay_ms}

@app.get("/api/buildinfo")
def buildinfo():
    return {
        "service": SERVICE_NAME,
        "version": os.getenv("APP_VERSION", "0.1.0"),
        "git_sha": os.getenv("GIT_SHA", "dev"),
        "image": os.getenv("IMAGE_REF", "local"),
        "slsa_provenance": os.getenv("SLSA_PROVENANCE", "see GitHub Actions artifacts"),
        "sigstore": os.getenv("SIGSTORE", "cosign keyless (see README)"),
    }

@app.get("/", response_class=HTMLResponse)
async def home(_: Request):
    # Simple, recruiter-friendly UI (no build step)
    html = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <script src="https://cdn.tailwindcss.com"></script>
  <title>TrustChain Playground</title>
</head>
<body class="bg-slate-950 text-slate-100">
  <div class="max-w-4xl mx-auto p-6">
    <div class="flex items-start justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold">TrustChain Playground</h1>
        <p class="text-slate-300 mt-2">
          A tiny app that demonstrates: <span class="font-semibold">signed images</span>,
          <span class="font-semibold">attestations</span>, <span class="font-semibold">policy-as-code</span>,
          <span class="font-semibold">GitOps</span>, and <span class="font-semibold">OpenTelemetry</span>.
        </p>
      </div>
      <div class="rounded-2xl bg-slate-900 px-4 py-3 shadow">
        <div class="text-sm text-slate-400">Status</div>
        <div id="status" class="text-lg font-semibold">Checking...</div>
      </div>
    </div>

    <div class="grid md:grid-cols-2 gap-4 mt-6">
      <div class="rounded-2xl bg-slate-900 p-5 shadow">
        <h2 class="text-xl font-semibold">Try the API</h2>
        <div class="mt-4 flex gap-2">
          <button onclick="getQuote()"
            class="rounded-xl bg-indigo-600 hover:bg-indigo-500 px-4 py-2 font-semibold">Random Quote</button>
          <button onclick="sendEcho()"
            class="rounded-xl bg-emerald-600 hover:bg-emerald-500 px-4 py-2 font-semibold">Echo (latency)</button>
        </div>
        <pre id="out" class="mt-4 text-sm bg-slate-950 rounded-xl p-3 overflow-auto"></pre>
      </div>

      <div class="rounded-2xl bg-slate-900 p-5 shadow">
        <h2 class="text-xl font-semibold">Build Info</h2>
        <p class="text-slate-300 mt-2 text-sm">
          This endpoint is what you point recruiters to. It proves this build came from CI.
        </p>
        <button onclick="getBuildInfo()"
          class="mt-4 rounded-xl bg-slate-800 hover:bg-slate-700 px-4 py-2 font-semibold">Load buildinfo</button>
        <pre id="build" class="mt-4 text-sm bg-slate-950 rounded-xl p-3 overflow-auto"></pre>
      </div>
    </div>

    <div class="rounded-2xl bg-slate-900 p-5 shadow mt-4">
      <h2 class="text-xl font-semibold">What makes this impressive?</h2>
      <ul class="list-disc ml-5 mt-2 text-slate-300">
        <li>CI scans code + IaC + secrets, then builds and signs the image.</li>
        <li>Kubernetes admission blocks unsigned images and bad configs.</li>
        <li>GitOps deploys via Argo CD; drift gets reconciled automatically.</li>
        <li>OpenTelemetry shows traces, metrics, and logs in Grafana.</li>
      </ul>
    </div>

    <div class="text-slate-500 text-xs mt-8">
      Tip: Put the repo link + live demo link on your GitHub + LinkedIn.
    </div>
  </div>

<script>
async function ping() {{
  try {{
    const r = await fetch('/healthz');
    document.getElementById('status').textContent = r.ok ? '✅ Healthy' : '⚠️ Unhealthy';
  }} catch(e) {{
    document.getElementById('status').textContent = '❌ Offline';
  }}
}}
async function getQuote() {{
  const r = await fetch('/api/quote');
  document.getElementById('out').textContent = JSON.stringify(await r.json(), null, 2);
}}
async function sendEcho() {{
  const r = await fetch('/api/echo', {{
    method:'POST',
    headers:{{'Content-Type':'application/json'}},
    body: JSON.stringify({{ hello:'recruiter', delay_ms: Math.floor(Math.random()*180)+20 }})
  }});
  document.getElementById('out').textContent = JSON.stringify(await r.json(), null, 2);
}}
async function getBuildInfo() {{
  const r = await fetch('/api/buildinfo');
  document.getElementById('build').textContent = JSON.stringify(await r.json(), null, 2);
}}
ping();
</script>
</body>
</html>
"""
    return HTMLResponse(html)
