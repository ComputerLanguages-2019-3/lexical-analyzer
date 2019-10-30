import re


class SyntaxAnalyzer(object):

    def __init__(self, lexical, grammar):
        self.lexical = lexical
        self.init_char_grammar = 'COMPONENT'
        self.grammar = grammar
        self.terminal_rgx = re.compile('[a-z]')
        self.no_terminal_rgx = re.compile('[A-Z]')
        self.current_token = None

    def recursive_desc_syntax_analysis(self, no_ter):
        for rule_idx, pred_rule in enumerate(self.grammar.prediction_sets[no_ter]):
            if self.current_token.lexeme in pred_rule:
                rule = self.grammar.grammar_map[no_ter][rule_idx]
                for rule_char in rule:
                    if self.terminal_rgx.match(rule_char):
                        self.call_match(rule_char)
                    elif self.no_terminal_rgx.match(rule_char):
                        self.recursive_desc_syntax_analysis(rule_char)
            else:
                print('Error sintáctico!!!')

    def call_match(self, expected_token):
        if self.current_token.lexeme == expected_token:
            self.current_token = self.lexical.get_next_token()
        else:
            print('Error sintaácticooo ', expected_token)

    def main_analysis(self):
        self.current_token = self.lexical.get_next_token()
        self.recursive_desc_syntax_analysis(self.init_char_grammar)
        print(self.current_token)