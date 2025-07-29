FROM python:3.10-slim

WORKDIR /chatbot

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8005

CMD ["python", "main.py"]
