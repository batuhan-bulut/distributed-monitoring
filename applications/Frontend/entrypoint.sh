#!/bin/sh

export OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED="${OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED:-true}"

opentelemetry-instrument \
    --traces_exporter="${OTEL_TRACES_EXPORTER:-otlp}" \
    --logs_exporter="${OTEL_LOGS_EXPORTER:-otlp}" \
    --metrics_exporter="${OTEL_METRICS_EXPORTER:-otlp}" \
    --service_name="${OTEL_SERVICE_NAME:-frontend}" \
    --exporter_otlp_endpoint="${OTEL_EXPORTER_OTLP_ENDPOINT:-http://otel-collector:4317}" \
    uvicorn "${APP_MODULE:-main:app}" --host 0.0.0.0 --port "${PORT:-8000}" &

pid=$!

term_handler() {
  echo "Caught SIGTERM or SIGINT, forwarding to uvicorn (pid $pid)..."
  kill -TERM "$pid" 2>/dev/null
}

trap 'term_handler' SIGTERM SIGINT

# Wait for the uvicorn process to exit
wait $pid
