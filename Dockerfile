FROM python:3.8

WORKDIR /app

COPY project.py .

RUN pip install fastapi uvicorn

EXPOSE 8000

CMD ["uvicorn", "project:app", "--host", "0.0.0.0", "--port", "8000"]