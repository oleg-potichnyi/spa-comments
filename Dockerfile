FROM python:3.10.6-slim-buster
LABEL maintainer="potichnyi.oleg@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /spa_comments

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /vol/web/media && \
    chmod -R 755 /vol/web && \
    chown -R root:root /vol/web

EXPOSE 8000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "spa_comments.wsgi:application", "--bind", "0.0.0.0:8000"]
