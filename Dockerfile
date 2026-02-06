FROM python:3.10-slim

WORKDIR /app

# System deps for sklearn / numpy
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY DS614-Faculty-Recommender/requirements.txt .
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY DS614-Faculty-Recommender/ .

# Expose ports
EXPOSE 8001
EXPOSE 8501

# Run both services locally, or only Streamlit on Railway with dynamic PORT
CMD if [ -n "$PORT" ]; then \
    streamlit run UI/streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true; \
    else \
    uvicorn app.api.main:app --host 0.0.0.0 --port 8001 & \
    streamlit run UI/streamlit_app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true; \
    fi
