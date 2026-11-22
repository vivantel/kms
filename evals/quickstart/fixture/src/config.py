# Sync defaults. Chosen after a warehouse outage in March showed 60s was too slow to
# catch stale inventory before it reached checkout.
SYNC_INTERVAL_SECONDS = 30
MAX_RETRIES = 5
BATCH_SIZE = 200
