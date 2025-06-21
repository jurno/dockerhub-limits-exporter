IMAGE := dockerhub-limits-exporter
TAG := 0.1.0

# Variables pre Opencontainers labels
CREATED := $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
REVISION := $(shell git rev-parse --short HEAD)

.PHONY: build-local scan-local build push-latest scan

build-local:
	docker buildx create --use --name=crossplat --node=crossplat
	docker buildx build \
		--pull --no-cache . \
		--build-arg TAG=${TAG} \
		--build-arg CREATED=${CREATED} \
		--build-arg REVISION=${REVISION} \
		-t ${IMAGE}:${TAG} \
		--load

scan-local:
	trivy image -s HIGH,CRITICAL --ignore-unfixed --scanners vuln ${IMAGE}:${TAG}

build:
	docker buildx create --use --name=crossplat --node=crossplat
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		--pull --no-cache . \
		--build-arg TAG=${TAG} \
		--build-arg CREATED=${CREATED} \
		--build-arg REVISION=${REVISION} \
		-t ${ACR}/${IMAGE}:${TAG} \
		--provenance=false --push
	crane validate --fast --remote ${ACR}/${IMAGE}:${TAG}

push-latest:
	crane tag ${ACR}/${IMAGE}:${TAG} latest

scan:
	trivy image -s HIGH,CRITICAL --ignore-unfixed --scanners vuln ${ACR}/${IMAGE}:${TAG}
