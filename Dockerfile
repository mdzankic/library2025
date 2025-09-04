#govori Dockeru kako da izgradi sliku (image) aplikacije iz kojeg pokreće container (gdje aplikacija radi)
# Python slim image
FROM python:3.11-slim

# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
#radni direktorij na /app
WORKDIR /app 

# System deps; Instalira sistemske pakete; Nakon instalacije, briše se cache
RUN apt-get update && apt-get install -y --no-install-recommends     build-essential     && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt /app/
# povećaj timeout i broj pokušaja, bez upgrade-a pipa
ENV PIP_DEFAULT_TIMEOUT=300
RUN pip install --no-cache-dir --timeout 300 --retries 10 -r requirements.txt

# Copy app
COPY app /app/app
COPY .env /app/.env

EXPOSE 8000

# Run
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
