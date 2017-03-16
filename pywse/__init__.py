import model

# Show the choices to user
HELPS = """1: countries
Waiting for your input (such as 1): """

def learn():
    lv = raw_input(HELPS)
    if not lv:
        lv = '1'
    lv = 'lv' + lv
    exec('from model import %s' % lv)
    exec('%s.start()' % lv)