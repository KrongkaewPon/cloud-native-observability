from opentelemetry._metrics import set_meter_provider
from opentelemetry.sdk._metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry._metrics import get_meter_provider, set_meter_provider
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from prometheus_client import start_http_server


def configure_meter_provider():
    exporter = ConsoleMetricExporter()
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
    provider = MeterProvider(metric_readers=[reader], resource=Resource.create())
    set_meter_provider(provider)


if __name__ == "__main__":
    configure_meter_provider()
    meter = get_meter_provider().get_meter(
        name="metric-example",
        version="0.1.2",
        schema_url=" https://opentelemetry.io/schemas/1.9.0",
    )

    counter = meter.create_counter(
        "items_sold", unit="items", description="Total items sold"
    )
    counter.add(6, {"locale": "fr-FR", "country": "CA"})
    counter.add(1, {"locale": "es-ES"})
    counter.add(1, {"locale": "es-ES"})
    counter.add(
        -1, {"unicorn": 1}
    )  # warning  Add amount must be non-negative on Counter items_sold.
