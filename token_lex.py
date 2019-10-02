from settings import FILE_NAME, IDENTIFIER, KEY_WORD_TYPE, OPERATOR, NUMBER,STRING


class Token(object):
    def __str__(self):
        token_class = None
        if self.type == KEY_WORD_TYPE:
            token_class = '<{},{},{}>'.format(
                self.lexeme,
                self.row,
                self.column
            )
        elif self.type[-2:] == 'op':
            token_class = '<{},{},{}>'.format(
                self.type,
                self.row,
                self.column
            )
        elif self.type == STRING or self.type == IDENTIFIER or self.type[-3:] == 'num':
            token_class = '<{},{},{},{}>'.format(
                self.type,
                self.lexeme,
                self.row,
                self.column
            )
        return token_class

    def __init__(self, column, row, type, lexeme):
        self.column = column
        self.row = row
        self.type = type
        self.lexeme = lexeme
