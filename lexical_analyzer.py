import re

from grammar_generate import GrammarGenerator
from settings import FILE_NAME, IDENTIFIER, KEY_WORD_TYPE, OPERATOR, NUMBER, STRING, GRAMMAR_FILE
from sintax_analyzer import SyntaxAnalyzer
from token_lex import Token


class LexicalAnalyzer(object):
    TOKEN_PRIORITY = {
        'KEY_WORD':  r'^(ni|fi|next|process|final|cap|string|bool|char|global|resource|import|end|op|var|select|if|else|select|body|extend|create|destroy|null|noop|call|send|do|int|and|proc|receive|initial|when|abort|reply|fa|co|getarg|write|mod|stop|procedure|returns)\W',
        'IDENTIFIER': r'^([a-zA-Z]\w*)',
        'COMMENT': '#',
        'NUM': {
            'REAL': r'^(\d+\.{1}\d+)',
            'INT': r'^(\d+)'
        },
        'OPERATOR': {
            'LPAREN': r'^\(',
            'RPAREN': r'^\)',
            'LBRACKET': r'^\[',
            'RBRACKET': r'^]',
            'PERIOD': r'^\.',

            'NOT': r'^~',
            'ADDR': r'^@',
            'QMARK': r'^\?',
            'INCR': r'^\+\+',
            'DEC': r'^--',
            'HAT': r'^\^',

            'LE': r'^<=',
            'LT': r'^<',
            'EQ': r'^=',
            'GT': r'^>',
            'NE': r'^(!=|~=)',

            'PLUS': r'^\+',
            'MINUS': r'^-',
            'ASTER': r'^\*',
            'DIV': r'^/',
            'REMDR': r'^%',
            'EXPON': r'^\*\*',
            'AND': r'^&',
            'OR': r'^\|',
            'LSHIFT': r'^<<',
            'RSHIFT': r'^>>',
            'CONCAT': r'^\|\|',

            'AUG_PLUS': r'^\+:=',
            'AUG_MINUS': r'^-:=',
            'AUG_ASTER': r'^\*:=',
            'AUG_DIV': r'^/:=',
            'AUG_MOD': r'^%:=',
            'AUG_EXPON': r'^\*\*:=',
            'AUG_AND': r'^&:=',
            'AUG_OR': r'^\|:=',
            'AUG_LSHIFT': r'^<<:=',
            'AUG_RSHIFT': r'^>>:=',
            'AUG_CONCAT': r'^\|\|:=',

            'ASSIGN': r'^:=',
            'SWAP': r'^:=:',

            'COMMA': r'^\,',
            'COLON': r'^:',
            'ARROW': r'^->',
            'SQUARE': r'^\[]',
            'PARALLEL': r'^//',

            'LBRACE': r'^\{',
            'RBRACE': r'^\}',
            'SEPARATOR': r'^\;'

        },
        'STRING': r"('.*?')|(\".*?\")"
    }

    def __str__(self):
        return 'SR language Lexical Analyzer'

    def __init__(self):
        self.source_code = ''
        self.current_column = 1
        self.current_row = 1
        self.current_line = ''
        self.token_list = None

    def get_token(self, token_regex, token_type, delete_from_regex=False):
        """
        :param token_regex:
        :param token_type:
        :param delete_from_regex:
        :return:
        """
        token = None
        key_word_matched = re.match(token_regex, self.current_line)
        if key_word_matched:
            key_word = key_word_matched.group()
            if delete_from_regex:
                key_word = re.sub(r'\W', '', key_word)
            token = Token(column=self.current_column, row=self.current_row, type=token_type, lexeme=key_word)
            if token.type == "keyword":
                token.type = "tk_" + key_word
            if token.type == "id":
                token.type = "tk_id"
            self.current_column += len(key_word)
            self.normalize_line(key_word)
        return token

    def analyze_source_code(self):
        self.source_code = (line for line in open(FILE_NAME, 'r', encoding="utf-8"))
        self.token_list = self.analyze_rows()


    def get_next_token(self):
        return next(self.token_list)

    def analyze_rows(self):
        lexical_error = False
        for number_line, line in enumerate(self.source_code, 1):
            self.current_column = 1
            self.current_row = number_line
            self.current_line = line
            self.normalize_line()

            while self.current_line.strip():
                answer = self.identify_token()
                if not answer:
                    lexical_error = True
                    print("Error léxico(linea:", self.current_row, "posicion:", self.current_column, ")")
                    break
                else:
                    if answer.type == 'COMMENT':
                        break
                    yield answer
            if lexical_error:
                break
        yield Token(column=0, row=number_line + 1, type='tk_eof', lexeme='$')

    def identify_token(self):
        token = None
        token = self.get_comment()
        if not token:
            token = self.get_key_word()
        if not token:
            token = self.get_identifiers()
        if not token:
            token = self.get_number()
        if not token:
            token = self.get_operator()
        if not token:
            token = self.get_string()
        if not token:
            self.current_line = ''
        return token

    def get_key_word(self):  # INFO: return class Token
        print
        token = self.get_token(self.TOKEN_PRIORITY['KEY_WORD'], KEY_WORD_TYPE, delete_from_regex=True)
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

    def get_comment(self):  # INFO: return class Token
        token = self.get_token(self.TOKEN_PRIORITY['COMMENT'], 'COMMENT')
        return token

    def get_operator(self):
        for op_type in self.TOKEN_PRIORITY['OPERATOR']:
            token = self.get_token(self.TOKEN_PRIORITY['OPERATOR'][op_type], OPERATOR[op_type])
            if token:
                break
        return token

    def get_string(self):
        token = self.get_token(self.TOKEN_PRIORITY['STRING'], STRING)
        return token

    def normalize_line(self, key_word=None):
        if key_word:
            self.current_line = self.current_line.lstrip(key_word)
        blank_space_num = len(self.current_line) - len(self.current_line.lstrip(' '))
        self.current_line = self.current_line.lstrip('\t')
        blank_space_num += (len(self.current_line) - len(self.current_line.lstrip('\t')))
        self.current_column += blank_space_num
        self.current_line = self.current_line.lstrip(' ')


if __name__ == '__main__':
    lexical = LexicalAnalyzer()
    grammar_gen = GrammarGenerator()
    grammar_gen.run(file_name=GRAMMAR_FILE)
    #grammar_gen.get_all_first_sets()
    grammar_gen.get_all_next_sets()
    print("prediction")
    print(grammar_gen.get_prediction_sets())
    lexical.analyze_source_code()
    syntactic = SyntaxAnalyzer(lexical, grammar_gen)
    syntactic.main_analysis()
