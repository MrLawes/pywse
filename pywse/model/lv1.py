
class Countries(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.adj = kwargs.get('adj', '')


def start():
    print 'start'