import re
from settings import FILE_NAME, IDENTIFIER, KEY_WORD_TYPE, OPERATOR
from token import Token


class LexicalAnalyzer(object):
    TOKEN_PRIORITY = {
        'KEY_WORD': r'^(global|resource|import|end|op|var|select|if|else|select|body|extend|create|destroy|null|noop|call|send|do|int|and|proc|receive|initial|when|abort|reply|fa|co)',
        'IDENTIFIER': (),
        'NUM': {
          'REAL': r'^(\d+\s|\s*\d+\.{1}\d+)',
          'INT': r'^(\d+)'
        },
        'OPERATOR': [
            r'++',
            r'--',
            r':=',
            r'++',
        ]
    }

    def __str__(self):
        return 'SR language Lexical Analyzer'

    def __init__(self):
        self.source_code = ''
        self.current_column = 1
        self.current_row = 1
        self.current_line = ''

    def get_token(self):
        # TODO: Apply priority rules to identify the Token and its creation.
        pass

    def analyze_source_code(self):
        self.source_code = open(FILE_NAME, 'r')
        self.analyze_rows()

    def analyze_rows(self):
        for number_line, line in enumerate(self.source_code, 1):
            self.current_column = 1
            self.current_row = number_line
            self.current_line = line
            while self.current_line.strip():
                print(self.identify_token())

    def identify_token(self):
        token = None
        token = self.get_key_word()
        if not token:
            token = self.get_identifiers()
            self.current_line = ''
        if not token:
            token = self.get_operator()
            self.current_line = ''
        return token

    def get_key_word(self):  # INFO: return class Token
        token = None
        key_word_matched = re.match(self.TOKEN_PRIORITY['KEY_WORD'], self.current_line)
        if key_word_matched:
            key_word = key_word_matched.group()
            token = Token(column=self.current_column, row=self.current_row, type=KEY_WORD_TYPE, lexeme=key_word)
            self.current_column += len(key_word)
            self.normalize_line(key_word)
        return token

    def get_identifiers(self):
        pass

    def get_operator(self):
        pass

    def normalize_line(self, key_word):
        self.current_line = self.current_line.lstrip(key_word)
        blank_space_num = len(self.current_line) - len(self.current_line.lstrip(' '))
        self.current_column += blank_space_num
        self.current_line = self.current_line.lstrip(' ')


if __name__ == '__main__':
    LexicalAnalyzer().analyze_source_code()

