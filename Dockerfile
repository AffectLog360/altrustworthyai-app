# Use a universal conda-forge/miniforge3 base
FROM condaforge/miniforge3:latest

# Environment variables
ENV ENV_NAME=altenv
ENV PYTHON_VER=3.9

# 1. Install system packages for building wheels (e.g. gevent, aplr)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Create a new conda environment
RUN conda create -y -n $ENV_NAME python=$PYTHON_VER

# 3. For each subsequent RUN, use the conda environment
SHELL ["conda", "run", "-n", "altenv", "/bin/bash", "-c"]

WORKDIR /app

# 4. Copy your requirements and install them in the environment
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Copy the rest of your app code
COPY . .

# 6. Expose the Flask port
EXPOSE 5002

# 7. Ensure the final command also runs in the environment
CMD ["conda", "run", "-n", "altenv", "python", "app.py"]
