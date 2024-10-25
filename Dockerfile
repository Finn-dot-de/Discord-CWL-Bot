# Verwende ein offizielles Python-Image als Basis
FROM python:3.11-slim

# Setze Umgebungsvariablen
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Installiere Abhängigkeiten
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Kopiere den Rest des Codes
COPY . .

# Exponiere den Port (optional, da Discord keine lokalen Ports nutzt)
# EXPOSE 8000

# Führe den Bot aus
CMD ["python", "main.py"]
