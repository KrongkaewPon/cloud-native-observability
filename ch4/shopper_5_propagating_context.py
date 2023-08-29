#!/usr/bin/env python3
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import context, trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from local_machine_resource_detector import LocalMachineResourceDetector
from opentelemetry.semconv.trace import HttpFlavorValues, SpanAttributes
import requests
from common import configure_tracer
from opentelemetry.propagate import inject


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


tracer = configure_tracer("shopper", "0.1.2")

# propagating_context


@tracer.start_as_current_span("browse")
def browse():
    print("visiting the grocery store")
    with tracer.start_as_current_span(
        "web request", kind=trace.SpanKind.CLIENT
    ) as span:
        headers = {}
        inject(headers)
        url = "http://localhost:5000/products"
        span = trace.get_current_span()
        # span.set_attribute("http.method", "GET")
        # span.set_attribute("http.flavor", "1.1")
        span.set_attributes(
            {
                SpanAttributes.HTTP_METHOD: "GET",
                SpanAttributes.HTTP_FLAVOR: HttpFlavorValues.HTTP_1_1.value,
                SpanAttributes.HTTP_URL: url,
                SpanAttributes.NET_PEER_IP: "127.0.0.1",
            }
        )
        resp = requests.get(url, headers=headers)
        span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, resp.status_code)
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
    browse()


if __name__ == "__main__":
    visit_store()
