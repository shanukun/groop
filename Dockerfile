FROM python:alpine3.17
WORKDIR /app
COPY requirements.txt .
RUN apk add --update py-pip
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

RUN python manage.py makemigrations
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
