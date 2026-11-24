import os

# Local dev only: the suite authenticates with the placeholder secrets.
os.environ.setdefault("SHOP_DEV_MODE", "1")
