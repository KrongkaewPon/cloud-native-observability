 <!-- RUN -->
<!--  -->

python3 -m venv env
source env/bin/activate

# install OpenTelemetry packages

pip install opentelemetry-api==1.10.0 \
opentelemetry-sdk==1.10.0 \
opentelemetry-propagator-b3==1.10.0

# install additional libraries

pip install flask requests

pip install opentelemetry-exporter-prometheus==0.29b0

curl -o hey https://hey-release.s3.us-east-2.amazonaws.com/hey_darwin_amd64
chmod +x ./hey

# RUN

### pipeline

shopper(W3C Trace Context) > grocery_store(B3) > legacy_inventory

## client

python ./shopper.py

## server

python ./grocery_store.py
python ./legacy_inventory.py

./hey http://localhost:5000/products
