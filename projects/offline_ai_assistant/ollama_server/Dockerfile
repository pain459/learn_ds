FROM python:3.10-slim

WORKDIR /app

# Step 1: Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Step 2: Install dependencies (cached unless requirements.txt changes)
RUN pip install --no-cache-dir -r requirements.txt

# Step 3: Now copy app code, templates, and static assets
COPY app/ ./app/
COPY templates/ ./templates/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
