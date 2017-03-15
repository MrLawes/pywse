
class Countries(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.adj = kwargs.get('adj', '')
        self.state = kwargs.get('state', '')
        self.language = kwargs.get('language', '')
        self.currency = kwargs.get('currency', '')

    def ask(self):
        print self.name
        print self.adj
        print self.state
        print self.language
        print self.currency

class Questions(object):

    QUESTIONS = [
        {
            'name': 'China',
            'adj': 'Chinese',
            'state': 'Asia',
            'language': 'Chinese',
            'currency': 'RMB',
        },
    ]

    def __init__(self):
        self.ask_questions = []
        for question in self.QUESTIONS:
            self.ask_questions.insert(0, Countries(**question))

    def start(self):
        while self.ask_questions:
            country = self.ask_questions.pop()
            country.ask()

def start():
    questions = Questions()
    questions.start()