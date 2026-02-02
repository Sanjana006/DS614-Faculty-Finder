FROM python:3.10-slim

WORKDIR /app

# System deps for scikit-learn
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt 

# Copy application
COPY app /app/app

# Expose backend + UI
EXPOSE 8000 8501

# Start both services
CMD bash -c "\
uvicorn app.main:app --host 0.0.0.0 --port 8000 & \
streamlit run app/ui/app.py --server.address 0.0.0.0 --server.port 8501 \
"
