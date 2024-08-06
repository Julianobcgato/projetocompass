FROM python:3.8


WORKDIR /app


COPY requeriments.txt .


RUN pip install -r requeriments.txt


COPY project.py .


EXPOSE 8000


CMD ["uvicorn", "project:app", "--host", "0.0.0.0", "--port", "8000"]
