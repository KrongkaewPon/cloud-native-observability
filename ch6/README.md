python3 -m venv env
source env/bin/activate

# install OpenTelemetry packages

pip install opentelemetry-api\
 opentelemetry-sdk\
 opentelemetry-propagator-b3

# install additional libraries

pip install flask requests
pip install opentelemetry-instrumentation-wsgi

#RUN
python ./logs.py
python legacy_inventory.py
python grocery_store.py
python shopper.py
