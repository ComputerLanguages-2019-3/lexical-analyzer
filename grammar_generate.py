import re

epsilon = '***'
starting_char = 'A'
file_final = '$'


class GrammarGenerator(object):
    grammar_map = {}

    def __init__(self):
        self.beta_next_by_no_terminal = {}
        self.first_sets_by_no_terminal = {}
        self.next_sets_by_no_terminal = {}

    def run(self, file_name):
        self.file_name = file_name
        self.content_grammar = (line for line in open(file_name))
        for line in self.content_grammar:
            no_terminal, rules = line.split(':')
            self.load_grammar(no_terminal, rules)
        self.load_beta_next()

    def load_grammar(self, no_terminal, line):
        self.grammar_map[no_terminal] = list()
        rules = line.split(',')

        for rule in rules:
            alpha = rule.strip(' ').strip('\n').split(' ')
            self.grammar_map[no_terminal].append(alpha)

    def get_prediction_set(self):
        for no_terminal in self.grammar_map.keys():
            no_terminal_first = set({})
            for alpha in self.grammar_map[no_terminal]:
                no_terminal_first.update(self.first_set(alpha, set({})))
            self.first_sets_by_no_terminal[no_terminal] = no_terminal_first
        print(self.first_sets_by_no_terminal)

    def get_all_next_sets(self):
        for no_terminal in self.grammar_map.keys():
            self.next_sets_by_no_terminal[no_terminal] = self.next_set(no_terminal, set({}))

    def load_beta_next(self):
        for no_terminal in self.grammar_map.keys():
            self.beta_next_by_no_terminal[no_terminal] = []
            self.content_grammar = (line for line in open(self.file_name))
            for line in self.content_grammar:
                left_no_terminal, rules = line.split(':')
                rules = rules.split(',')
                for rule in rules:
                    no_terminal_match = re.search(no_terminal, rule)
                    if no_terminal_match:
                        match_idx = no_terminal_match.start(0)
                        beta_next = rule[match_idx+1:].strip('\n').strip(' ')
                        self.beta_next_by_no_terminal[no_terminal].append([left_no_terminal, beta_next])
        print(self.beta_next_by_no_terminal)

    def next_set(self, no_terminal, no_terminal_next_set):
        terminal_rgx = re.compile('[a-z]')
        no_terminal_rgx = re.compile('[A-Z]')
        if no_terminal == starting_char:
            no_terminal_next_set.add(file_final)
        for no_terminal_next in self.beta_next_by_no_terminal[no_terminal]:
            beta_from = no_terminal_next[0]
            beta = no_terminal_next[1].split(' ')
            if not beta[0]:
                no_terminal_next_set.update(self.next_set(beta_from, set({})))
            elif terminal_rgx.match(beta[0]):
                no_terminal_next_set.add(beta[0])
            else:
                if epsilon in self.first_sets_by_no_terminal[beta[0]]:
                    no_terminal_next_set.update(self.next_set(beta_from, set({})))
                else:
                    no_terminal_next_set.update(self.first_sets_by_no_terminal[beta[0]])
        return no_terminal_next_set

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
                    if epsilon in alpha_aux_first:
                        alpha_aux_first.remove(epsilon)
                    alpha_i_first.update(
                         alpha_aux_first
                    )
                alpha_first.update(alpha_i_first.remove(epsilon) if epsilon in alpha_i_first else alpha_i_first)
            elif epsilon in self.first_set(alpha_i, set({})):
                if len(self.first_set(alpha_i, set({}))) == 1:
                    alpha_first.add(epsilon)
                    return alpha_first
                elif len(self.first_set(alpha_i, set({}))) > 1:
                    alpha_first.update(self.first_set(alpha[1:]), alpha_first=set({}))
                    return alpha_first
        return alpha_first

