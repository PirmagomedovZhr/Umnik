FROM python:3.10-alpine


WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --upgrade pip && apk add build-base && pip3 install -r requirements.txt

COPY . .

RUN echo 'root:awdkj%W@!#' | chpasswd && find . -type f -exec chmod 644 {} \; && \
    adduser --disabled-password --no-create-home john-doe && chmod 755 manage.py && \
    find . -type d -exec chmod 755 {} \;

USER john-doe
