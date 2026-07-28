FROM python:3.11-slim

WORKDIR /app

# BACKEND folder se copy karein (kyunki build context root hai)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Poora backend folder copy karein
COPY backend/. .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
