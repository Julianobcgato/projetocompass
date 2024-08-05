FROM python:3.12

WORKDIR /app

COPY fastapiv2.py .

RUN pip install fastapi uvicorn

EXPOSE 8000

CMD ["uvicorn", "fastapiv2:app", "--host", "0.0.0.0", "--port", "8000"]
