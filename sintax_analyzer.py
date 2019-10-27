class SyntaxAnalyzer(object):
    def __init__(self, lexical):
        self.lexical = lexical

    def analyze_source_code(self):
        pass

    def get_next_token(self):
        self.lexical.get_next_token()

    def pull_symbol_table(self):
        pass

    def push_symbol_table(self):
        pass