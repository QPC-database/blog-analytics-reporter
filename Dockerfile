FROM python:3.7.7-stretch

LABEL maintainer="xuewenG" \
        site="https://github.com/xuewenG/blog-analytics-reporter"

WORKDIR /root

COPY requirements.txt .

RUN set -x \
    && pip install --no-cache-dir -r requirements.txt

COPY src .

ENTRYPOINT ["python", "server.py"]
