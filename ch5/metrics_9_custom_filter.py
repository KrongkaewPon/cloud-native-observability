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
from opentelemetry.sdk._metrics.view import View
from opentelemetry._metrics.instrument import Counter


def configure_meter_provider():
    exporter = ConsoleMetricExporter()
    reader = PeriodicExportingMetricReader(exporter, export_interval_millis=1000)
    view = View(instrument_name="inventory", instrument_type=Counter)
    provider = MeterProvider(
        metric_readers=[reader],
        resource=Resource.create(),
        views=[view],
        enable_default_view=False,
    )
    set_meter_provider(provider)


def async_counter_callback():
    yield Measurement(3)


def async_updowncounter_callback():
    yield Measurement(20, {"locale": "en-US"})
    yield Measurement(10, {"locale": "fr-CA"})


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

    # counter
    counter = meter.create_counter(
        "items_sold", unit="items", description="Total items sold"
    )
    counter.add(6, {"locale": "fr-FR", "country": "CA"})
    counter.add(1, {"locale": "es-ES"})

    # async counter
    meter.create_observable_counter(
        name="major_page_faults",
        callback=async_counter_callback,
        description="page faults requiring I/O",
        unit="fault",
    )
    time.sleep(2)

    # up down counter
    inventory_counter = meter.create_up_down_counter(
        name="inventory",
        unit="items",
        description="Number of items in inventory",
    )
    inventory_counter.add(20)
    inventory_counter.add(-5)

    # async up down counter
    upcounter_counter = meter.create_observable_up_down_counter(
        name="customer_in_store",
        callback=async_updowncounter_callback,
        unit="persons",
        description="Keeps a count of customers in the store",
    )

    # histogram
    histogram = meter.create_histogram(
        "response_times",
        unit="ms",
        description="Response times for all requests",
    )
    histogram.record(96)
    histogram.record(9)

    # async_gauge
    meter.create_observable_gauge(
        name="maxrss",
        unit="bytes",
        callback=async_gauge_callback,
        description="Max resident set size",
    )
    time.sleep(2)