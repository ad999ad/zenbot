# Don't touch these lines!!!
import random
runid=random.randint(1000,9999)
# -----------------------------------------------------------------------------------------

# User configurable parameters:

# zenbot dir, ex. "app/zenbot" for docker "/full/path/of/zenbot/dir" for linux envinronment
#path = '/home/gecko/zenbot'
path = '/app'

# name of python executable
pyexc = 'python3.6'

# Autobackfill interval in seconds, min 600 secs -> 10 mins
bkfint = 600

# Draw graph, on or off, for this is needed pygraphviz module, actual this is in non working state, keep off
dgraph = 'off'

# You can edit this, please respect the python dict syntax
selectors = {
    'BTC-CUR': ['gdax.BTC-USD', 'gdax.BTC-EUR', 'gdax.BTC-GBP'],
    'BTC-USD': ['gdax.BTC-USD'],
    'BTC-EUR': ['gdax.BTC-EUR'],
    'BTC-GBP': ['gdax.BTC-GBP'],
    'LTC-USD': ['gdax.LTC-USD'],
    'LTC-BTC': ['gdax.LTC-BTC'],
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
cxpb = 0.5
