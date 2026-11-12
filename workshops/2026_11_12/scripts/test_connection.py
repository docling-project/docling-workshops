"""
test_connection.py — Verify configuration and connectivity to the Docling Service.

Checks that:
  1. The .env file exists and is populated with valid credentials (not placeholders).
  2. The docling-client package is installed and can be imported.
  3. The Docling service is reachable and the API key is accepted.
  4. Document conversion works end-to-end on a sample file.

Usage (from the workshop directory):
    python scripts/test_connection.py
"""

import os
import sys
import time
from pathlib import Path

# ── 1. Locate workshop root and .env file ──────────────────────────────────────
script_dir = Path(__file__).resolve().parent
workshop_dir = script_dir.parent
env_file = workshop_dir / ".env"
docs_dir = workshop_dir / "docs"

print("=" * 60)
print("Docling Workshop — Configuration & Connection Test")
print("=" * 60)
print(f"Workshop directory: {workshop_dir}")

if not env_file.exists():
    print("\n✗ .env file not found!")
    print(f"  Expected location: {env_file}")
    print("  Please create it by copying the template and editing your credentials:")
    print("    cp .env.example .env")
    sys.exit(1)

# ── 2. Load .env variables ────────────────────────────────────────────────────
# Use dotenv if available; otherwise fall back to simple key=value parser
try:
    from dotenv import load_dotenv
    load_dotenv(env_file)
except ImportError:
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

# ── 3. Validate credentials ───────────────────────────────────────────────────
service_url = os.environ.get("DOCLING_SERVICE_URL", "").strip().rstrip("/")
api_key = os.environ.get("DOCLING_SERVICE_API_KEY", "").strip()

PLACEHOLDER_URLS = {"https://your-docling-service.example.com", "http://localhost:5001/v1"}
PLACEHOLDER_KEYS = {"your-api-key", "your-docling-api-key", "your-api-key-here"}

errors = []
if not service_url:
    errors.append("DOCLING_SERVICE_URL is missing in .env")
elif service_url in PLACEHOLDER_URLS or "example.com" in service_url:
    errors.append("DOCLING_SERVICE_URL still contains the placeholder URL")

if not api_key:
    errors.append("DOCLING_SERVICE_API_KEY is missing in .env")
elif api_key in PLACEHOLDER_KEYS or api_key.startswith("your-"):
    errors.append("DOCLING_SERVICE_API_KEY still contains the placeholder value")

if errors:
    print("\n✗ Configuration errors in .env:")
    for err in errors:
        print(f"  • {err}")
    print("\nPlease edit .env with your actual Docling service credentials and re-run.")
    sys.exit(1)

print("\n✓ Configuration loaded from .env:")
# Mask the API key for safe display (show only last 4 chars)
masked_key = f"{'*' * (len(api_key) - 4)}{api_key[-4:]}" if len(api_key) > 4 else "****"
print(f"  • Service URL : {service_url}")
print(f"  • API Key     : {masked_key}")

# ── 4. Verify dependencies ────────────────────────────────────────────────────
try:
    from docling.service_client import DoclingServiceClient
except ImportError:
    print("\n✗ docling-client is not installed in the active Python environment.")
    print("  Make sure the virtual environment is activated:")
    print("    source .venv/bin/activate")
    print("  Or install docling-client directly:")
    print("    uv pip install docling-client")
    sys.exit(1)
except Exception as e:
    print(f"\n✗ Failed to import docling-client ({e}).")
    if sys.version_info >= (3, 14):
        print("💡 Python 3.14+ is not yet supported by some dependencies (e.g. Pydantic).")
        print("   Please use Python 3.10 – 3.13:")
        print("     uv venv --python 3.12 .venv")
        print("     uv pip install docling-client dclq")
    sys.exit(1)

# ── 5. Verify test document ───────────────────────────────────────────────────
doc_path = docs_dir / "regulatory_guidelines_2026.epub"
if not doc_path.exists():
    # Fallback to any file in docs/
    candidates = list(docs_dir.glob("*.pdf")) + list(docs_dir.glob("*.epub")) + list(docs_dir.glob("*.docx"))
    if candidates:
        doc_path = candidates[0]
    else:
        print(f"\n✗ No test document found in {docs_dir}")
        sys.exit(1)

# ── 6. Test service connection and document conversion ────────────────────────
print(f"\nConnecting to Docling service and converting '{doc_path.name}'...")
t0 = time.time()

try:
    with DoclingServiceClient(url=service_url, api_key=api_key) as client:
        result = client.convert(source=doc_path)

    elapsed = time.time() - t0
    markdown = result.document.export_to_markdown()

    print(f"\n✓ Successfully connected and converted in {elapsed:.2f}s!")
    print("\n" + "─" * 60)
    print("Preview of converted Markdown (first 400 characters):")
    print("─" * 60)
    print(markdown[:400].strip())
    print("─" * 60)
    print("\n✓ Environment is ready for the workshop!")

except Exception as e:
    elapsed = time.time() - t0
    err_str = str(e)
    print(f"\n✗ Connection or conversion failed after {elapsed:.2f}s:")
    print(f"  {err_str}\n")

    # Diagnostic troubleshooting hints
    if "401" in err_str or "Unauthorized" in err_str or "forbidden" in err_str.lower():
        print("💡 Troubleshooting Hint:")
        print("   The Docling service rejected your API key (401/403).")
        print("   Please check that DOCLING_SERVICE_API_KEY in .env is correct.")
    elif "404" in err_str or "Not Found" in err_str:
        print("💡 Troubleshooting Hint:")
        print("   The endpoint was not found (404).")
        print("   Please verify the DOCLING_SERVICE_URL in .env.")
    elif "ConnectionRefused" in err_str or "MaxRetryError" in err_str or "getaddrinfo failed" in err_str or "ConnectError" in err_str:
        print("💡 Troubleshooting Hint:")
        print("   Could not establish a network connection to the service.")
        print("   Check that the host URL is reachable and that you have active internet/VPN access.")
    else:
        print("💡 Troubleshooting Hint:")
        print("   Check that DOCLING_SERVICE_URL and DOCLING_SERVICE_API_KEY are correct.")

    sys.exit(1)
