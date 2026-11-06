FROM python:3.13-alpine
RUN addgroup -g 1001 -S app && adduser -u 1001 -S app -G app
WORKDIR /app
COPY --chown=1001:1001 mte ./mte
COPY --chown=1001:1001 pyproject.toml ./
RUN pip install --no-cache-dir .
USER 1001:1001
EXPOSE 8100
CMD ["uvicorn", "mte.server:app", "--host", "0.0.0.0", "--port", "8100"]
