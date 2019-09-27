class Token(object):
    def __str__(self):
        return 'Token {}, type {}, row {} and column {}'.format(
            self.lexeme,
            self.type,
            self.row,
            self.column
        )

    def __init__(self, column, row, type, lexeme):
        self.column = column
        self.row = row
        self.type = type
        self.lexeme = lexeme
