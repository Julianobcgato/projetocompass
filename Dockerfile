FROM python:3.12


WORKDIR /app


RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .


RUN pip install -r requirements.txt


COPY project.py .


EXPOSE 8000


CMD ["uvicorn", "project:app", "--host", "0.0.0.0", "--port", "8005"]
