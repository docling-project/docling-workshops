#!/usr/bin/env bash
# OpenTech Connect 2026 — get your environment ready.
#
# Run this script from within the cloned repository:
#
#     cd workshops/2026_11_12
#     ./bootstrap.sh
#
# It verifies prerequisites, installs uv (if needed), creates the Python
# virtual environment, and leaves you ready to fill in your .env file.
# It is safe to run again: a second run updates dependencies and leaves an existing .env alone.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

step() { printf '\n\033[1m▸ %s\033[0m\n' "$*"; }
info() { printf '  %s\n' "$*"; }
warn() { printf '  \033[33m! %s\033[0m\n' "$*" >&2; }
die()  { printf '\n\033[31m✗ %s\033[0m\n' "$*" >&2; exit 1; }

# --- 1. git ------------------------------------------------------------------
have_git() { command -v git >/dev/null 2>&1; }

check_git() {
  if have_git; then
    info "git is already installed"
  else
    warn "git is not installed on this system"
  fi
}

# --- 2. uv -------------------------------------------------------------------
install_uv() {
  if command -v uv >/dev/null 2>&1; then
    info "uv $(uv --version | awk '{print $2}') is already installed"
    return 0
  fi
  info "installing uv ..."
  curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1 \
    || die "could not install uv — check network access to astral.sh"
  export PATH="$HOME/.local/bin:$PATH"
  command -v uv >/dev/null 2>&1 || die "uv installed but is not on PATH"
}

ensure_path() {
  export PATH="$HOME/.local/bin:$PATH"
  local rc=""
  if [[ -f "$HOME/.bashrc" ]]; then
    rc="$HOME/.bashrc"
  elif [[ -f "$HOME/.zshrc" ]]; then
    rc="$HOME/.zshrc"
  else
    rc="$HOME/.profile"
  fi
  local line='export PATH="$HOME/.local/bin:$PATH"'
  grep -qF "$line" "$rc" 2>/dev/null && return 0
  printf '\n# added by Docling workshop bootstrap\n%s\n' "$line" >> "$rc"
  info "added ~/.local/bin to your PATH in $rc"
}

# --- 3. Python virtual environment -------------------------------------------
create_venv() {
  local dir="$1"
  if [[ -d "$dir/.venv" ]]; then
    info "virtual environment already exists — reusing it"
  else
    info "creating virtual environment with Python 3.12 ..."
    uv venv --python 3.12 --quiet "$dir/.venv" \
      || die "uv venv failed — check that uv can download Python (network access required)"
  fi
  info "installing or upgrading docling-client and dclq ..."
  uv pip install --quiet --upgrade --python "$dir/.venv/bin/python" "docling-client" "dclq" \
    || die "uv pip install failed"
}

# --- go ----------------------------------------------------------------------
printf '\n\033[1mOpenTech Connect 2026 — Hands-On with Docling\033[0m\n'

step "System packages"
check_git

step "uv"
install_uv
ensure_path

step "Python virtual environment"
create_venv "$SCRIPT_DIR"
# Activate for the current subshell (or parent shell if script was sourced)
# shellcheck source=/dev/null
source "$SCRIPT_DIR/.venv/bin/activate"

step "Your configuration"
if [[ -f .env ]]; then
  info ".env is already here — left untouched"
elif [[ -f .env.example ]]; then
  cp .env.example .env
  info ".env created from .env.example — add your Service URL and API key"
fi

printf '\n\033[1m✓ Ready.\033[0m\n\n'
cat <<NEXT
  Your workshop directory is: $SCRIPT_DIR

  Next steps:
  1  cd $SCRIPT_DIR
  2  open .env and fill in DOCLING_SERVICE_URL and DOCLING_SERVICE_API_KEY
  3  source .venv/bin/activate
  4  python scripts/test_connection.py

  The workshop guide has the rest (README.md). If uv is not found in a new
  terminal, run:  export PATH="\$HOME/.local/bin:\$PATH"

NEXT
