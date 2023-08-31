#Book

Cloud-Native Observability with OpenTelemetry

#Package

> python3 -m venv env
> source env/bin/activate

## ch4

> pip install flask requests

> pip install opentelemetry-api opentelemetry-sdk

> pip freeze | grep opentelemetry

> curl -o hey https://hey-release.s3.us-east-2.amazonaws.com/hey_darwin_amd64
> chmod +x ./hey

## ch5

```
pip install opentelemetry-api==1.10.0 \
opentelemetry-sdk==1.10.0 \
opentelemetry-propagator-b3==1.10.0
```

> pip install opentelemetry-exporter-prometheus==0.29b0

> ./hey http://localhost:5000/products

## ch6

pip install opentelemetry-api \
opentelemetry-sdk \
opentelemetry-propagator-b3

> pip install opentelemetry-instrumentation-wsgi

> pip install flask requests
