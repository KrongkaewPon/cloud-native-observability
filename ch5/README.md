 <!-- RUN -->

##client
python ./shopper.py

##server
python ./grocery_store.py
python ./legacy_inventory.py

###pipeline
shopper(W3C Trace Context) > grocery_store(B3) > legacy_inventory
