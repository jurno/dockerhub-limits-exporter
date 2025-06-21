FROM python:3.14-rc-alpine3.21

ARG CREATED TAG REVISION

LABEL org.opencontainers.image.created=${CREATED}
LABEL org.opencontainers.image.source=https://github.com/jurno/dockerhub-limits-exporter
LABEL org.opencontainers.image.title=dockerhub-limits-exporter
LABEL org.opencontainers.image.version=${TAG}
LABEL org.opencontainers.image.revision=${REVISION}
LABEL org.opencontainers.image.url=https://github.com/jurno/dockerhub-limits-exporter

WORKDIR /app
COPY dockerhub-limits-exporter.py .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
USER daemon

CMD ["python", "dockerhub-limits-exporter.py"]
