import os
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


def configure_otel(service_name: str) -> None:
    """
    Exports traces via OTLP/HTTP to an OpenTelemetry Collector.
    FastAPI instrumentation library docs: see opentelemetry-instrumentation-fastapi. :contentReference[oaicite:10]{index=10}
    """
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT", "http://localhost:4318/v1/traces")
    resource = Resource.create({
        "service.name": service_name,
        "service.version": os.getenv("APP_VERSION", "0.1.0"),
    })
    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # auto-instrument FastAPI once app is created
    # (we call FastAPIInstrumentor in main.py after app init)
    try:
        FastAPIInstrumentor.instrument_app  # type: ignore[attr-defined]
    except Exception:
        pass


def instrument_fastapi(app):
    FastAPIInstrumentor.instrument_app(app)
