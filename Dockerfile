FROM python:3.8.2-slim-buster

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        make \
        automake \
        gcc \
        g++ \
        curl \
        libpq-dev \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

ENV APP_DIR=/var/www/app \
    PYTHONBUFFERED=1

WORKDIR ${APP_DIR}

COPY requirements.txt ${APP_DIR}

RUN pip install -r requirements.txt \
    && python -c "import nltk; nltk.download('stopwords')"

COPY rootfs /
COPY . ${APP_DIR}

RUN ./manage.py collectstatic --noinput \
    && python -m whitenoise.compress ./staticfiles/

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

HEALTHCHECK \
    --start-period=15s \
    --timeout=2s \
    --retries=3 \
    --interval=5s \
    CMD /healthcheck.sh
