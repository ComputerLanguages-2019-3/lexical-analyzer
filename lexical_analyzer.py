from token import Token


class LexicalAnalyzer(object):
    TOKEN_PRIORITY = ()

    def __str__(self):
        return 'SR language Lexical Analyzer'

    def __init__(self, source_code):
        self.source_code = source_code
        self.current_column = 0
        self.current_row = 0

    def get_token(self):
        # TODO: Apply priority rules to identify the Token and its creation.
        pass

