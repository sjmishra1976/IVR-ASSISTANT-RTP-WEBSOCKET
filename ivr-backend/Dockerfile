FROM python:3.11-slim

WORKDIR /app

# Install all required build dependencies for llama-cpp-python
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    curl \
    git \
    ffmpeg \
    libopenblas-dev \
    libssl-dev \
    libffi-dev \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Avoid pip trying to install prebuilt binary for llama-cpp-python
ENV FORCE_CMAKE=1

# Install Python deps
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY . .

ENV LLAMA_MODEL_PATH=/models/llama-2-7b-chat.Q2_K.gguf

EXPOSE 5010

CMD ["python", "app/ivr_backend.py"]