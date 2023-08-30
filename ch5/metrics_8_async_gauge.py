from opentelemetry._metrics import set_meter_provider
from opentelemetry.sdk._metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
import resource, time
from opentelemetry._metrics import get_meter_provider, set_meter_provider
from opentelemetry._metrics.measurement import Measurement


def configure_meter_provider():
    exporter = ConsoleMetricExporter()
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
    provider = MeterProvider(metric_readers=[reader], resource=Resource.create())
    set_meter_provider(provider)


def async_gauge_callback():
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    yield Measurement(rss, {})


if __name__ == "__main__":
    configure_meter_provider()
    meter = get_meter_provider().get_meter(
        name="metric-example",
        version="0.1.2",
        schema_url=" https://opentelemetry.io/schemas/1.9.0",
    )

    meter.create_observable_gauge(
        name="maxrss",
        unit="bytes",
        callback=async_gauge_callback,
        description="Max resident set size",
    )
    time.sleep(3)
