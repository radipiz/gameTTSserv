FROM python:3.9-slim-buster AS app
LABEL maintainer="Radipiz <radipizmail@gmail.com>"

WORKDIR /app

ARG UID=1000
ARG GID=1000

RUN apt update \
    && apt install --yes libopenblas-base libopenblas-dev ffmpeg espeak-ng g++ curl \
    && rm -rf /usr/share/doc /usr/share/man /var/lib/apt/lists/* \
    && apt-get clean \
    && groupadd -g "${GID}" python \
    && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python \
    && chown python:python -R /app

USER python

COPY --chown=python:python . .
RUN pip3 install --no-warn-script-location --no-cache-dir --user -r requirements.txt

ENV PYTHONUNBUFFERED="true" \
    PYTHONPATH=".:gametts" \
    PATH="${PATH}:/home/python/.local/bin" \
    USER="python"

EXPOSE 8000

CMD ["gunicorn", "-c", "python:gunicornconfig", "main:get_app()" ]
