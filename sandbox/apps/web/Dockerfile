# =============================================================================
# Next.js Frontend — multi-stage, Alpine, non-root UID 1001
# =============================================================================

# ---------- Stage 1: Deps ----------
FROM node:22-alpine AS deps
RUN apk add --no-cache libc6-compat
RUN corepack enable && corepack prepare pnpm@9 --activate
WORKDIR /app
COPY apps/web/package.json apps/web/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# ---------- Stage 2: Builder ----------
FROM node:22-alpine AS builder
RUN corepack enable && corepack prepare pnpm@9 --activate
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY apps/web/ .
ENV NEXT_TELEMETRY_DISABLED=1
RUN pnpm build

# ---------- Stage 3: Runtime ----------
FROM node:22-alpine AS runtime
RUN apk add --no-cache tini curl \
    && addgroup -g 1001 -S appgroup \
    && adduser -u 1001 -S appuser -G appgroup -h /app

WORKDIR /app
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PORT=3000

COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
COPY --chown=1001:1001 infra/entrypoint.sh /entrypoint.sh
RUN chmod 0555 /entrypoint.sh

USER 1001:1001
EXPOSE 3000

ENTRYPOINT ["/sbin/tini", "--", "/entrypoint.sh"]
CMD ["node", "server.js"]
