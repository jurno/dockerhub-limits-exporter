# dockerhub-limits-exporter

**dockerhub-limits-exporter** ziska aktualny stav hodnot [pull limitu](https://docs.docker.com/docker-hub/usage/pulls/)
z Docker Hub API a publikuje ich ako Prometheus metriky:

- `dockerhub_rate_limit` - pull rate limit (6 hodin)
- `dockerhub_rate_remaining` - aktualny zostatok pull requestov

## Autentifikacia

Kontajner (skript) po spusteni zobrazuje metriky pre neautentifikovaneho pouzivatela.
V pripade, ze potrebujes ziskat metriky pre autentifikovaneho pouzivatela pouzi
environment variables:

- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub password (alebo token)

```sh
docker run --rm -e DOCKER_USERNAME=username -e DOCKER_PASSWORD=token -p 8000:8000 dockerhub-limits-exporter
```

## Deploy

[Kustomize](./kustomize/)

## Build & Trivy scan

[Makefile](./Makefile)
