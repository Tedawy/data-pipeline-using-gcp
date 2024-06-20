FROM --platform=linux/amd64 python:3.11-slim as build

# Expose port 8080
EXPOSE 8080 

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/my-creds.json
CMD ["scrapy", "crawl", "bayut"]
