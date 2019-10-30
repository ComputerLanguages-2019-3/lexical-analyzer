FILE_NAME = 'files/0.txt'

GRAMMAR_FILE = 'files/grammar_def.txt'

KEY_WORD_TYPE = 'keyword'
IDENTIFIER = 'id'
NUMBER = {
    'REAL': 'real_num',
    'INT': 'int_num'
}
OPERATOR = {
    'LPAREN': 'tk_lparen',
    'RPAREN': 'tk_rparen',
    'LBRACKET': 'tk_lbracket',
    'RBRACKET': 'tk_rbracket',
    'PERIOD': 'tk_period',

    'NOT': 'tk_not',
    'ADDR': 'tk_addr',
    'QMARK': 'tk_qmark',
    'INCR': 'tk_incr',
    'DEC': 'tk_dec',
    'HAT': 'tk_hat',

    'LE': 'tk_le',
    'LT': 'tk_lt',
    'EQ': 'tk_eq',
    'GT': 'tk_gt',
    'NE': 'tk_ne',

    'PLUS': 'tk_plus',
    'MINUS': 'tk_minus',
    'ASTER': 'tk_aster',
    'DIV': 'tk_div',
    'REMDR': 'tk_remdr',
    'EXPON': 'tk_expon',
    'AND': 'tk_and',
    'OR': 'tk_or',
    'LSHIFT': 'tk_lshift',
    'RSHIFT': 'tk_rshift',
    'CONCAT': 'tk_concat',

    'AUG_PLUS': 'tk_aug_plus',
    'AUG_MINUS': 'tk_aug_minus',
    'AUG_ASTER': 'tk_aug_aster',
    'AUG_DIV': 'tk_aug_div',
    'AUG_MOD': 'tk_aug_mod',
    'AUG_EXPON': 'tk_aug_expon',
    'AUG_AND': 'tk_aug_and',
    'AUG_OR': 'tk_aug_or',
    'AUG_LSHIFT': 'tk_aug_lshift',
    'AUG_RSHIFT': 'tk_aug_rshift',
    'AUG_CONCAT': 'tk_aug_concat',

    'ASSIGN': 'tk_assign',
    'SWAP': 'tk_swap',

    'COMMA': 'tk_comma',
    'COLON': 'tk_colon',
    'ARROW': 'tk_arrow',
    'SQUARE': 'tk_square',
    'PARALLEL': 'tk_parallel',

    'LBRACE': 'tk_lbrace',
    'RBRACE': 'tk_rbrace',
    'SEPARATOR': 'tk_separator'
}
STRING = 'string'
