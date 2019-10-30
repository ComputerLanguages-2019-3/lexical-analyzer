import re

epsilon = '€'
starting_char = '^'
file_final = '$'


class GrammarGenerator(object):
    grammar_map = {}
    max_depth = 100

    def __init__(self):
        self.beta_next_by_no_terminal = {}
        self.first_sets_by_no_terminal = {}
        self.next_sets_by_no_terminal = {i: set() for i in self.grammar_map.keys()}
        self.prediction_sets = {}

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

    def get_prediction_sets(self):
        for no_terminal in self.grammar_map.keys():
            self.prediction_sets[no_terminal] = []
            for rule_number, rule in enumerate(self.grammar_map[no_terminal]):
                rule_first_set = self.first_set(rule, set({}))
                if epsilon in rule_first_set:
                    rule_first_set.remove(epsilon)
                    rule_first_set.update(self.next_sets_by_no_terminal[no_terminal])
                    self.prediction_sets[no_terminal].append(rule_first_set)
                else:
                    self.prediction_sets[no_terminal].append(rule_first_set)
            print(no_terminal)
            print(self.prediction_sets[no_terminal])

    def get_all_first_sets(self):
        terminal_rgx = re.compile('[a-z]')
        for no_terminal in self.grammar_map.keys():
            no_terminal_first = set({})
            for alpha in self.grammar_map[no_terminal]:
                no_terminal_first.update(self.first_set(alpha, set({})))
                for symbol in alpha:
                    if terminal_rgx.match(symbol) or symbol == '$' or symbol == '^' or symbol == '€':
                        self.first_sets_by_no_terminal[symbol] = {symbol}
            self.first_sets_by_no_terminal[no_terminal] = no_terminal_first
        print("First set ", self.first_sets_by_no_terminal)

    def get_all_next_sets(self):
        self.next_set(set({}))
        print(self.next_sets_by_no_terminal)

    def load_beta_next(self):
        for no_terminal in self.grammar_map.keys():
            self.beta_next_by_no_terminal[no_terminal] = []
            self.content_grammar = (line for line in open(self.file_name))
            for line in self.content_grammar:
                left_no_terminal, rules = line.split(':')
                rules = rules.split(',')
                for rule in rules:
                    no_terminal_match = re.search("\\b" + no_terminal + "\\b", rule)
                    if no_terminal_match:
                        match_idx = no_terminal_match.start(0)
                        beta_next = rule[match_idx+len(no_terminal)+1:].strip('\n').strip(' ')
                        self.beta_next_by_no_terminal[no_terminal].append([left_no_terminal, beta_next])
        print(self.beta_next_by_no_terminal)

    def next_set(self, no_terminal_next_set):
        terminal_rgx = re.compile('[a-z]')

        print("Grammar Heyyyyy " ,self.grammar_map)
        first = {i: set() for i in self.grammar_map.keys()}
        for nt in self.grammar_map.keys():
            for rule in self.grammar_map[nt]:
                for symbol in rule:
                    if terminal_rgx.match(symbol):
                        first[symbol]= {symbol}

        first['€'] = {'€'}
        first['$'] = {'$'}
        follows = {i: set() for i in self.grammar_map.keys()}
        epsilon = set()
        #print(first)
        #print(follows)
        while True:
            changes = False
            for nt in self.grammar_map.keys():
                for rule in self.grammar_map[nt]:
                    for symbol in rule:
                        sizeBefore = len(first[nt])
                        first[nt].update(first[symbol])
                        sizeAfter = len(first[nt])
                        changes |= (sizeBefore != sizeAfter)
                        if symbol not in epsilon:
                            break
                    else:
                        sizeBefore = len(epsilon[nt])
                        epsilon.update({nt})
                        sizeAfter = len(epsilon[nt])
                        changes |= (sizeBefore != sizeAfter)

                    auxiliary_set = follows[nt]
                    for symbol in reversed(rule):
                        if symbol in follows:
                            sizeBefore = len(follows[symbol])
                            follows[symbol].update(auxiliary_set)
                            sizeAfter = len(follows[symbol])
                            changes |= (sizeBefore != sizeAfter)
                        if symbol in epsilon:
                            auxiliary_set.update(first[symbol])
                        else:
                            auxiliary_set = first[symbol]
            if not changes:
                break
        self.first_sets_by_no_terminal = first
        self.next_sets_by_no_terminal = follows


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
                return alpha_first
            elif epsilon in self.first_set(alpha_i, set({})):
                if len(self.first_set(alpha_i, set({}))) == 1:
                    alpha_first.add(epsilon)
                    return alpha_first
                elif len(self.first_set(alpha_i, set({}))) > 1:
                    alpha_first.update(self.first_set(alpha[1:]), alpha_first=set({}))
                    return alpha_first
        return alpha_first

