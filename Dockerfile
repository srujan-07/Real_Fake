FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

WORKDIR /app

# Install Python dependencies first for better layer caching.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user for runtime.
RUN useradd --create-home --shell /usr/sbin/nologin ctf

# Copy application code.
COPY . .

# Ensure app files are readable by the runtime user.
RUN chown -R ctf:ctf /app
USER ctf

EXPOSE 5000

# Single worker is required due to in-memory session storage.
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT} --workers 1 --threads 4 --timeout 120"]
