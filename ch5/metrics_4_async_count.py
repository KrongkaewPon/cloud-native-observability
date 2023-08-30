from opentelemetry._metrics import set_meter_provider
from opentelemetry.sdk._metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry._metrics import get_meter_provider, set_meter_provider
import time
from opentelemetry._metrics.measurement import Measurement


def configure_meter_provider():
    exporter = ConsoleMetricExporter()
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=1000)
    provider = MeterProvider(metric_readers=[reader], resource=Resource.create())
    set_meter_provider(provider)


def async_counter_callback():
    yield Measurement(5)


if __name__ == "__main__":
    configure_meter_provider()
    meter = get_meter_provider().get_meter(
        name="metric-example",
        version="0.1.2",
        schema_url=" https://opentelemetry.io/schemas/1.9.0",
    )

    meter.create_observable_counter(
        name="major_page_faults",
        callback=async_counter_callback,
        description="page faults requiring I/O",
        unit="fault",
    )
    time.sleep(2)
