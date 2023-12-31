#!/usr/bin/env python3
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import trace
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor


def browse():
    print("visiting the grocery store")


def add_item_to_cart(item):
    print("add {} to cart".format(item))


def configure_tracer():
    exporter = ConsoleSpanExporter()
    span_processor = SimpleSpanProcessor(exporter)
    provider = TracerProvider()
    provider.add_span_processor(span_processor)
    trace.set_tracer_provider(provider)
    return trace.get_tracer("shopper.py", "0.0.1")


if __name__ == "__main__":
    # v1
    # tracer = configure_tracer()
    # span = tracer.start_span("visit store")
    # ctx = trace.set_span_in_context(span)
    # token = context.attach(ctx)
    # span2 = tracer.start_span("browse")
    # browse()
    # span2.end()
    # context.detach(token)
    # span.end()

    # v2
    tracer = configure_tracer()
    with tracer.start_as_current_span("visit store"):
        with tracer.start_as_current_span("browse"):
            browse()
            with tracer.start_as_current_span("add item to cart"):
                add_item_to_cart("orange")
