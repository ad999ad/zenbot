# Don't touch these lines!!!
import random
runid=random.randint(1000,9999)
# -----------------------------------------------------------------------------------------

# User configurable parameters:

# zenbot dir, ex. "/app" for docker or "/full/path/of/zenbot/dir" for linux envinronment
path = '/app'

# name of python executable
pyexc = 'python'

# Autobackfill interval in seconds, min 600 secs -> 10 mins
bkfint = 1800

# Draw graph, on or off, for this is needed pygraphviz module, actual this is in non working state, keep off
dgraph = 'off'

# You can edit this, please respect the python dict syntax
selectors = {
    'BTC-CUR': ['gdax.BTC-USD', 'gdax.BTC-EUR', 'gdax.BTC-GBP'],
    'ETH-BTC': ['gdax.ETH-BTC'],
    'ETH-EUR': ['gdax.ETH-EUR'],
    'ETH-USD': ['gdax.ETH-USD'],
    'ETH-CUR': ['gdax.ETH-USD','gdax.ETH-EUR'],
}

# Concurrent threads
partitions=2

# Swozny please explain these parameters
selectivity = 0.3

# Ditto
sigma = 20

# Ditto
indpb  = 0.3

# Ditto
mutpb = 0.3

# Ditto
cxpb = 0.3
