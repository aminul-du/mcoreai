# =============================================================================
# Docker Buildx Bake — orchestration matrix for parallel multi-arch builds
# Usage: docker buildx bake -f docker-bake.hcl --print
#        docker buildx bake -f docker-bake.hcl --push
# =============================================================================

variable "REGISTRY" {
  default = "ghcr.io/your-org/fabric"
}

variable "TAG" {
  default = "latest"
}

group "default" {
  targets = ["ingestion", "policy-core", "web", "neteng", "cyberrange", "shorborno"]
}

target "common" {
  platforms = ["linux/amd64", "linux/arm64"]
  labels = {
    "org.opencontainers.image.source" = "https://github.com/your-org/fabric"
  }
  cache-from = [{ type = "gha" }]
  cache-to = [{ type = "gha", mode = "max" }]
}

target "ingestion" {
  inherits = ["common"]
  context = "."
  dockerfile = "services/Dockerfile.python"
  args = { SERVICE = "ingestion", PORT = "8000" }
  tags = ["${REGISTRY}-ingestion:${TAG}", "${REGISTRY}-ingestion:latest"]
  platforms = ["linux/amd64", "linux/arm64"]
}

target "policy-core" {
  inherits = ["common"]
  context = "."
  dockerfile = "services/policy-core/Dockerfile"
  tags = ["${REGISTRY}-policy-core:${TAG}", "${REGISTRY}-policy-core:latest"]
  platforms = ["linux/amd64"]  # musl static build
}

target "web" {
  inherits = ["common"]
  context = "."
  dockerfile = "apps/web/Dockerfile"
  tags = ["${REGISTRY}-web:${TAG}", "${REGISTRY}-web:latest"]
  platforms = ["linux/amd64", "linux/arm64"]
}

target "neteng" {
  inherits = ["common"]
  context = "."
  dockerfile = "services/Dockerfile.python"
  args = { SERVICE = "neteng", PORT = "9000" }
  tags = ["${REGISTRY}-neteng:${TAG}", "${REGISTRY}-neteng:latest"]
  platforms = ["linux/amd64", "linux/arm64"]
}

target "cyberrange" {
  inherits = ["common"]
  context = "."
  dockerfile = "services/Dockerfile.python"
  args = { SERVICE = "cyberrange", PORT = "9100" }
  tags = ["${REGISTRY}-cyberrange:${TAG}", "${REGISTRY}-cyberrange:latest"]
  platforms = ["linux/amd64", "linux/arm64"]
}

target "shorborno" {
  inherits = ["common"]
  context = "."
  dockerfile = "services/Dockerfile.python"
  args = { SERVICE = "shorborno", PORT = "9200" }
  tags = ["${REGISTRY}-shorborno:${TAG}", "${REGISTRY}-shorborno:latest"]
  platforms = ["linux/amd64", "linux/arm64"]
}
