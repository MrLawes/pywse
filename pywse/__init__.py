from model import *

# Show the choices to user
HELPS = """lv1: countries
"""

def learn():
    lv = raw_input(HELPS)
    exec('%s.start()' % lv)
learn()