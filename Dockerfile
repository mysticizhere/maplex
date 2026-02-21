FROM python:3.12-slim

WORKDIR /app

RUN groupadd --gid 1000 app && useradd --uid 1000 --gid app --shell /bin/false app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

COPY config_template.json ./config.json

ENV CONFIG_PATH=/app/config.json
ENV MCP_HOST=0.0.0.0
ENV MCP_PORT=3001

USER app
EXPOSE 3001

CMD ["python", "-m", "app.server"]
