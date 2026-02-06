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

# Expose Streamlit port
EXPOSE 8501

# Run only Streamlit with dynamic PORT support for Railway
CMD streamlit run UI/streamlit_app.py --server.port ${PORT:-8501} --server.address 0.0.0.0 --server.headless true