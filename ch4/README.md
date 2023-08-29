 <!-- RUN -->

##client
python ./shopper_7_span_exception.py

##server
python ./grocery_store.py
python ./legacy_inventory.py

###pipeline
shopper(W3C Trace Context) > grocery_store(B3) > legacy_inventory
