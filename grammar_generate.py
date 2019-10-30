import re

epsilon = '€'
starting_char = 'COMPONENT'
file_final = '$'


class GrammarGenerator(object):
    grammar_map = {}

    def __init__(self):
        self.beta_next_by_no_terminal = {}
        self.first_sets_by_no_terminal = {}
        self.next_sets_by_no_terminal = {}
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

    def get_all_first_sets(self):
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
                    no_terminal_match = re.search("\\b" + no_terminal + "\\b", rule)
                    if no_terminal_match:
                        match_idx = no_terminal_match.start(0)
                        beta_next = rule[match_idx + len(no_terminal) + 1:].strip('\n').strip(' ')
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
            print(beta)
            if not beta[0]:
                no_terminal_next_set.update(self.next_set(beta_from, set({})))  # recursion problem
            elif terminal_rgx.match(beta[0]):
                no_terminal_next_set.add(beta[0])
            else:
                if epsilon in self.first_sets_by_no_terminal[beta[0]]:
                    no_terminal_next_set.update(self.next_set(beta_from, set({})))
                else:
                    no_terminal_next_set.update(self.first_sets_by_no_terminal[beta[0]])
        return no_terminal_next_set

    def next_set_iterative(self):
        terminal_rgx = re.compile('[a-z]')
        no_terminal_rgx = re.compile('[A-Z]')
        beta_from_set = set({'$'})
        no_terminal_next_set = set({})
        stack_no_terminals = list(self.grammar_map.keys())
        for no_terminal in stack_no_terminals:
            self.next_sets_by_no_terminal[no_terminal] = set({})

        num_no_terminals = len(stack_no_terminals)
        no_terminal = stack_no_terminals.pop(0)
        stack_no_terminal_rules = [[no_terminal, no_terminal_r] for no_terminal_r in self.beta_next_by_no_terminal[no_terminal]]
        stack_beta_next = []
        init_no_ter = True
        while stack_no_terminal_rules or init_no_ter:
            init_no_ter = False
            get_beta_next = False
            no_terminal_next_set = set({})
            if no_terminal == starting_char:
                no_terminal_next_set.add(file_final)
            if stack_no_terminal_rules:
                no_terminal, no_terminal_rule = stack_no_terminal_rules.pop()
                beta_from = no_terminal_rule[0]
                beta = no_terminal_rule[1].split(' ')
                beta_first_set = self.first_set(beta, set({}))

                if epsilon in beta_first_set:
                    get_beta_next = True
                    beta_first_set.remove(epsilon)

                if '' in beta_first_set:
                    get_beta_next = True
                    beta_first_set.remove('')

                if not beta_first_set:
                    get_beta_next = True

                no_terminal_next_set.update(beta_first_set)
                self.next_sets_by_no_terminal[no_terminal].update(no_terminal_next_set)

                if get_beta_next:
                    if self.next_sets_by_no_terminal[beta_from]:
                        self.next_sets_by_no_terminal[no_terminal].update(self.next_sets_by_no_terminal[beta_from])
                    stack_no_terminal_rules = stack_no_terminal_rules + [[no_terminal, no_terminal_r] for no_terminal_r in self.beta_next_by_no_terminal[beta_from]]
                    continue

            if not stack_no_terminal_rules and stack_no_terminals:
                no_terminal = stack_no_terminals.pop()
                stack_no_terminal_rules = [[no_terminal, no_terminal_r] for no_terminal_r in self.beta_next_by_no_terminal[no_terminal]]
            num_no_terminals = len(stack_no_terminals)
        print('next', self.next_sets_by_no_terminal)

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

