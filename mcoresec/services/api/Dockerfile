FROM python:3.13-alpine
RUN addgroup -g 1001 -S app && adduser -u 1001 -S app -G app
WORKDIR /app
COPY --chown=1001:1001 services/api/app ./app
RUN pip install --no-cache-dir fastapi uvicorn[standard] httpx pydantic-settings
USER 1001:1001
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
