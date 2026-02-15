FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the model (optional, to speed up first run)
# RUN python -c "from transformers import pipeline; pipeline('text-classification', model='unitary/toxic-bert')"

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
