FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY nrsak.py /app/nrsak.py
RUN chmod +x /app/nrsak.py

RUN useradd --create-home --shell /bin/bash nrsak
USER nrsak

ENTRYPOINT ["python3", "/app/nrsak.py"]
CMD ["function_list"]
