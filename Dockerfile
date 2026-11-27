FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN mkdir -p /app/Content

ENV PORT=3003
ENV VIDEO_DIR=/app/Content

EXPOSE 3003

CMD ["python", "server.py"]
