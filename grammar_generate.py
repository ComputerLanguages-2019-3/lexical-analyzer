import re

epsilon = '***'


class GrammarGenerator(object):
    grammar_map = {}

    def run(self, file_name):
        self.content_grammar = (line for line in open(file_name))
        for line in self.content_grammar:
            no_terminal, rules = line.split(':')
            self.load_grammar(no_terminal, rules)

    def load_grammar(self, no_terminal, line):
        self.grammar_map[no_terminal] = list()
        rules = line.split(',')

        for rule in rules:
            alpha = rule.strip(' ').strip('\n').split(' ')
            self.grammar_map[no_terminal].append(alpha)

    def get_prediction_set(self):
        for key in self.grammar_map.keys():
            first_key = set({})
            for alpha in self.grammar_map[key]:
                first_key.update(self.first_set(alpha, set({})))
            print(key)
            print(first_key)

    # return alpha_first       #set
    def first_set(self, alpha, alpha_first):
        terminal_rgx = re.compile('[a-z]')
        no_terminal_rgx = re.compile('[A-Z]')
        if alpha == epsilon:
            return set({alpha})
        for alpha_i in alpha:
            if terminal_rgx.match(alpha_i):
                return set({alpha_i})
            elif no_terminal_rgx.match(alpha_i):
                alpha_i_first = set({})
                for alpha_aux in self.grammar_map[alpha_i]:
                    alpha_aux_first = self.first_set(alpha_aux, set({}))
                    alpha_i_first.update(
                        alpha_aux_first.remove(epsilon) if epsilon in alpha_aux_first else alpha_aux_first
                    )
                alpha_first.update(alpha_i_first.remove(epsilon) if epsilon in alpha_i_first else alpha_i_first)
                return alpha_first
            elif epsilon in self.first_set(alpha_i, set({})):
                if len(alpha_i) == 1:
                    return alpha_first.add(epsilon)
                elif len(alpha_i) > 1:
                    return alpha_first.update(self.first_set(alpha[1:]), set({}))
        return alpha_first

