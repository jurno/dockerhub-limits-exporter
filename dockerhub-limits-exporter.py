import os
import time
import logging
import requests
from prometheus_client import start_http_server, Gauge

# Logger
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Prometheus metriky
dockerhub_rate_limit = Gauge(
    'dockerhub_rate_limit_limit', 'Docker Hub pull rate limit')
dockerhub_rate_remaining = Gauge(
    'dockerhub_rate_limit_remaining', 'Docker Hub pull rate remaining')

# Repo a scope
REPO = os.getenv("DOCKER_REPO", "library/alpine")
SCOPE = f"repository:{REPO}:pull"
MANIFEST_URL = f"https://registry-1.docker.io/v2/{REPO}/manifests/latest"
TOKEN_URL = f"https://auth.docker.io/token?service=registry.docker.io&scope={SCOPE}"

# Prihlasovacie udaje ak chces ziskat token ako autentifikovany pouzivatel
DOCKER_USERNAME = os.getenv("DOCKER_USERNAME")
DOCKER_PASSWORD = os.getenv("DOCKER_PASSWORD")  # alebo PAT

# Ziskanie tokenu pre Docker Hub API
def get_token():
    try:
        if DOCKER_USERNAME and DOCKER_PASSWORD:
            # Token request pre autentifikovaneho pouzivatela
            logging.info("Fetching authenticated token...")
            resp = requests.get(TOKEN_URL, auth=(DOCKER_USERNAME, DOCKER_PASSWORD))
        else:
            # Token request pre anonymneho pouzivatela
            logging.info("Fetching anonymous token...")
            resp = requests.get(TOKEN_URL)

        resp.raise_for_status()
        token = resp.json().get("token")
        return token
    except Exception as e:
        logging.error(f"Error obtaining token: {e}")
        return None

# Ziskanie rate limitu z Docker Hub API
def fetch_dockerhub_rate_limit():
    token = get_token()
    if not token:
        return 0, 0, 0

    headers = {
        "Accept": "application/vnd.docker.distribution.manifest.v2+json",
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.head(MANIFEST_URL, headers=headers)
        response.raise_for_status()

        limit = response.headers.get("RateLimit-Limit", "0").split(";")[0]
        remaining = response.headers.get("RateLimit-Remaining", "0").split(";")[0]

        logging.info(f"Limit: {limit}, Remaining: {remaining}")
        return int(limit), int(remaining)
    except Exception as e:
        logging.error(f"Error fetching rate limit: {e}")
        return 0, 0, 0

# Aktualizacia metrik
def update_metrics():
    limit, remaining = fetch_dockerhub_rate_limit()
    dockerhub_rate_limit.set(limit)
    dockerhub_rate_remaining.set(remaining)

if __name__ == "__main__":
    # Prometheus klient standardne vystavuje metriky na /metrics
    # start_http_server(8000) spusta HTTP server na porte 8000 s endpointom /metrics
    start_http_server(8000)
    logging.info("Prometheus exporter is running on port 8000 at /metrics...")
    while True:
        update_metrics()
        time.sleep(60)
