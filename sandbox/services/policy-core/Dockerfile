# =============================================================================
# Rust / Axum Policy Core — multi-stage, Alpine, non-root UID 1001
# =============================================================================

# ---------- Stage 1: Builder ----------
FROM rust:1.83-alpine AS builder

RUN apk add --no-cache musl-dev openssl-dev

WORKDIR /build
COPY services/policy-core/Cargo.toml services/policy-core/Cargo.lock ./
COPY services/policy-core/src ./src

# Release build with musl target for static linking
RUN cargo build --release --target x86_64-unknown-linux-musl

# ---------- Stage 2: Runtime ----------
FROM alpine:3.21 AS runtime

RUN apk add --no-cache ca-certificates tini curl \
    && addgroup -g 1001 -S appgroup \
    && adduser -u 1001 -S appuser -G appgroup -h /app

WORKDIR /app

COPY --from=builder /build/target/x86_64-unknown-linux-musl/release/policy-core /app/policy-core
COPY --chown=1001:1001 infra/entrypoint.sh /entrypoint.sh

RUN chmod 0555 /entrypoint.sh /app/policy-core

USER 1001:1001

EXPOSE 8080

ENTRYPOINT ["/sbin/tini", "--", "/entrypoint.sh"]
CMD ["/app/policy-core"]
