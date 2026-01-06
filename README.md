# TrustChain Playground 🔐⛓️
End-to-end software supply-chain pipeline: **build → scan → sign (cosign) → attest (SLSA / in-toto) → verify at deploy with policy guardrails**.

This repo is a practical playground to learn (and demonstrate) **modern DevSecOps / SLSA-style integrity** with a workflow you can actually run locally and in CI.

---

## What this project shows

✅ Build a container image  
✅ Generate SBOM (optional but recommended)  
✅ Scan for vulnerabilities (example: Trivy)  
✅ Sign the image with **cosign** (keyless or key-based)  
✅ Create an **attestation** (SLSA provenance / in-toto)  
✅ Enforce **policy at deploy time** (example: Kyverno)  
✅ GitOps-style delivery (optional example: Argo CD + Helm)  
✅ Observability hooks (optional example: OpenTelemetry)

---

## Architecture (high level)

- **CI (GitHub Actions)**
  - Build image → scan → sign → attest → push
- **CD / Deployment**
  - Deploy via Helm (optionally through Argo CD)
  - Policy engine verifies:
    - image signature is valid
    - required attestation exists
    - no `:latest`, probes/limits required, etc.

---

## Tech stack

- **Docker** (image build)
- **GitHub Actions** (CI)
- **cosign** (sign/verify, attestations)
- **Kyverno** (policy enforcement on Kubernetes)
- **Helm** (deployment packaging)
- **Argo CD** (GitOps, optional)
- **OpenTelemetry** (optional instrumentation)

---

## Repo structure (example)

> Your folders may differ — adjust to match your repo.

```txt
.
├─ app/                       # demo app (optional)
├─ helm/                      # Helm chart
├─ policies/                  # Kyverno policies
├─ .github/workflows/         # CI pipeline (build/scan/sign/attest)
├─ docker/                    # Dockerfiles, build context
└─ README.md
