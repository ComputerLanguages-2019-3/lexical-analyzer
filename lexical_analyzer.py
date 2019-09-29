import re
from settings import FILE_NAME, IDENTIFIER, KEY_WORD_TYPE, OPERATOR, NUMBER
from token import Token


class LexicalAnalyzer(object):
    TOKEN_PRIORITY = {
        'KEY_WORD': r'^(global|resource|import|end|op|var|select|if|else|select|body|extend|create|destroy|null|noop|call|send|do|int|and|proc|receive|initial|when|abort|reply|fa|co)',
        'IDENTIFIER': r'^([a-zA-Z]\w*)',
        'NUM': {
          'REAL': r'^(\d+\.{1}\d+)',
          'INT': r'^(\d+)'
        },
        'OPERATOR': {
            'INCREASE' : r'^\+\+',
            'ADD' : r'^\+',
            'DECREASE' : r'^--',
            'SUB' : r'^-',
            'MUL' : r'^\*',
            'DIV' : r'^/',
            'ASSIGN' : r'^:=',
            'DEFINE' : r'^:',
            'GREATER' : r'^>',
            'LOWER' : r'^<',
            'MOD' : r'^%',
            'PAR_LEFT': r'^\(',
            'PAR_RIGHT': r'^\)',
            'BRACKET_LEFT' : r'^\[',
            'BRACKET_RIGTH' : r'^\]',
            'COMMA' : r'^,',
            'DOT' : r'^\.'
        }
    }

    def __str__(self):
        return 'SR language Lexical Analyzer'

    def __init__(self):
        self.source_code = ''
        self.current_column = 1
        self.current_row = 1
        self.current_line = ''

    def get_token(self, token_regex, token_type):
        token = None
        key_word_matched = re.match(token_regex, self.current_line)
        if key_word_matched:
            key_word = key_word_matched.group()
            token = Token(column=self.current_column, row=self.current_row, type=token_type, lexeme=key_word)
            self.current_column += len(key_word)
            self.normalize_line(key_word)
        return token

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
        if not token:
            token = self.get_number()
        if not token:
            token = self.get_operator()
        if not token:
            self.current_line = ''
        return token

    def get_key_word(self):  # INFO: return class Token
        token =self.get_token(self.TOKEN_PRIORITY['KEY_WORD'], KEY_WORD_TYPE)
        return token

    def get_identifiers(self):
        token = self.get_token(self.TOKEN_PRIORITY['IDENTIFIER'], IDENTIFIER)
        return token

    def get_number(self):
        for num_type in self.TOKEN_PRIORITY['NUM']:
            token = self.get_token(self.TOKEN_PRIORITY['NUM'][num_type], NUMBER[num_type])
            if token:
                break
        return token

    def get_operator(self):
        # pass
        for op_type in self.TOKEN_PRIORITY['OPERATOR']:
            token = self.get_token(self.TOKEN_PRIORITY['OPERATOR'][op_type], OPERATOR[op_type])
            if token:
                break
        return token

    def normalize_line(self, key_word):
        self.current_line = self.current_line.lstrip(key_word)
        blank_space_num = len(self.current_line) - len(self.current_line.lstrip(' '))
        self.current_column += blank_space_num
        self.current_line = self.current_line.lstrip(' ')


if __name__ == '__main__':
    LexicalAnalyzer().analyze_source_code()
