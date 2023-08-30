#!/usr/bin/env python3
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import context, trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from local_machine_resource_detector import LocalMachineResourceDetector
from opentelemetry.semconv.trace import HttpFlavorValues, SpanAttributes
import requests
from common import configure_tracer, configure_meter
from opentelemetry.propagate import inject
from opentelemetry.trace import Status, StatusCode
import time

tracer = configure_tracer("shopper", "0.1.2")
meter = configure_meter("shopper", "0.1.2")

total_duration_histo = meter.create_histogram(
    name="duration",
    description="request duration",
    unit="ms",
)
upstream_duration_histo = meter.create_histogram(
    name="upstream_request_duration",
    description="duration of upstream requests",
    unit="ms",
)


def configure_tracer(name, version):
    exporter = ConsoleSpanExporter()
    span_processor = BatchSpanProcessor(exporter)
    local_resource = LocalMachineResourceDetector().detect()
    resource = local_resource.merge(
        Resource.create(
            {
                "service.name": name,
                "service.version": version,
            }
        )
    )

    provider = TracerProvider(resource=resource)
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)
    return trace.get_tracer(name, version)


@tracer.start_as_current_span("browse")
def browse():
    print("visiting the grocery store")
    with tracer.start_as_current_span(
        "web request",
        kind=trace.SpanKind.CLIENT,
        record_exception=False,
        set_status_on_exception=True,
    ) as span:
        headers = {}
        inject(headers)
        url = "http://localhost:5000/products"
        span = trace.get_current_span()
        span.set_attributes(
            {
                SpanAttributes.HTTP_METHOD: "GET",
                SpanAttributes.HTTP_FLAVOR: HttpFlavorValues.HTTP_1_1.value,
                SpanAttributes.HTTP_URL: url,
                SpanAttributes.NET_PEER_IP: "127.0.0.1",
            }
        )
        span.add_event("about to send a request")
        start = time.time_ns()
        resp = requests.get(url, headers=headers)
        duration = (time.time_ns() - start) / 1e6
        upstream_duration_histo.record(duration)
        if resp:
            span.set_status(Status(StatusCode.OK))
        else:
            span.set_status(
                Status(StatusCode.ERROR, "status code: {}".format(resp.status_code))
            )
        span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, resp.status_code)
        span.add_event("request sent", attributes={"url": url}, timestamp=0)
        add_item_to_cart("orange", 5)


@tracer.start_as_current_span("add item to cart")
def add_item_to_cart(item, quantity):
    span = trace.get_current_span()
    span.set_attributes(
        {
            "item": item,
            "quantity": quantity,
        }
    )
    print("add {} to cart".format(item))


@tracer.start_as_current_span("visit store")
def visit_store():
    start = time.time_ns()
    browse()
    duration = (time.time_ns() - start) / 1e6
    total_duration_histo.record(duration)


if __name__ == "__main__":
    visit_store()
