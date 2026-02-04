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

# Expose default port (Railway will override this via the PORT env var)
EXPOSE 8080

# The default command will start the Streamlit app.
# For Railway, you can create two services and override the start command for each.
CMD ["sh", "-c", "streamlit run UI/streamlit_app.py --server.port ${PORT:-8080} --server.address 0.0.0.0"]