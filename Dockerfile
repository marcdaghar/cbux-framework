FROM python:3.11-slim

LABEL maintainer="marc.gilbert.daghar@gmail.com"
LABEL version="1.0"
LABEL description="CBU-X Framework"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=src/api/api_taux.py
ENV FLASK_ENV=production

WORKDIR /app

RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY tests/ /app/tests/
COPY data/ /app/data/

EXPOSE 5000
EXPOSE 8501

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
