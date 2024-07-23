FROM python:3.10

WORKDIR /app

# RUN apt-get update && apt-get install -y \
#     build-essential
#     libmysqlclient-dev \
#     pkg-config
#     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

#ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /
COPY wait-for-it.sh /app/wait-for-it.sh
COPY . /app/

RUN chmod +x /app/wait-for-it.sh
RUN chmod +x /app/manage.py

# ENV PYTHONUNBUFFERED 1

# CMD ["/app/wait-for-it.sh", "db:3306", "--", "sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
