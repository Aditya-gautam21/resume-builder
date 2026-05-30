# ═══════════════════════════════════════════════
# Stage 1 — Build frontend
# ═══════════════════════════════════════════════
FROM node:22-alpine AS frontend-builder

WORKDIR /src
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

COPY frontend/ ./
RUN npm run build


# ═══════════════════════════════════════════════
# Stage 2 — Fetch tectonic binary
# ═══════════════════════════════════════════════
FROM debian:bookworm-slim AS tectonic-fetcher

ARG TECTONIC_VERSION=0.16.9
RUN apt-get update && apt-get install -y --no-install-recommends wget ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# tectonic uses different suffixes per arch:
#   x86_64 → x86_64-unknown-linux-gnu
#   aarch64 → aarch64-unknown-linux-musl
RUN ARCH=$(uname -m) && \
    case "$ARCH" in \
      x86_64)  SUFFIX="${ARCH}-unknown-linux-gnu" ;; \
      aarch64) SUFFIX="${ARCH}-unknown-linux-musl" ;; \
      *)       echo "Unsupported arch: $ARCH"; exit 1 ;; \
    esac && \
    URL="https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%40${TECTONIC_VERSION}/tectonic-${TECTONIC_VERSION}-${SUFFIX}.tar.gz" && \
    wget -q "$URL" -O /tmp/tectonic.tar.gz && \
    tar xzf /tmp/tectonic.tar.gz -C /tmp tectonic && \
    chmod +x /tmp/tectonic


# ═══════════════════════════════════════════════
# Stage 3 — Production runtime
# ═══════════════════════════════════════════════
FROM python:3.12-slim

# Install tectonic
COPY --from=tectonic-fetcher /tmp/tectonic /usr/local/bin/tectonic

# Install Python deps (slim set — only what the app needs at runtime)
COPY backend/requirements-prod.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy backend code
COPY backend/ /app/backend/

# Copy built frontend (from Stage 1)
COPY --from=frontend-builder /src/dist/ /app/frontend-dist/

WORKDIR /app

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
