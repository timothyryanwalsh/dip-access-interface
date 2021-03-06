FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /src

COPY requirements /src/requirements

RUN set -ex \
    && apk add --update --no-cache --virtual .buildDeps \
        gcc \
        libxslt-dev \
        musl-dev \
    && pip install --no-cache-dir -r requirements/development.txt \
    && runDeps="$( \
        scanelf --needed --nobanner --format '%n#p' --recursive /usr/local \
            | tr ',' '\n' \
            | sort -u \
            | awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 \
                { next } { print "so:" $1 }' \
    )" \
    && apk add --no-cache --virtual .runDeps $runDeps \
    && apk del .buildDeps \
    && find /usr/local -depth \
        \( \
            \( -type d -a \( -name test -o -name tests \) \) \
            -o \
            \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
        \) -exec rm -rf '{}' + \
    && rm -rf /usr/src/python

COPY ./accesspoc /src

EXPOSE 8000

CMD ["gunicorn", "accesspoc.wsgi:application", "-b=0:8000", "-k=gevent"]
