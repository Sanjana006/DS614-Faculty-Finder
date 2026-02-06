FROM python:3.10-slim

WORKDIR /app

# System deps for sklearn / numpy
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose both ports for FastAPI and Streamlit
EXPOSE 8001 8501

# Start both FastAPI (port 8001) and Streamlit (port 8501)
CMD ["sh", "-c", "uvicorn app.api.main:app --host 0.0.0.0 --port 8001 & streamlit run UI/streamlit_app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true"]