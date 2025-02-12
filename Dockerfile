FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN rm entrypoint.sh

RUN pip install -r requirements.txt

COPY entrypoint.sh .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
