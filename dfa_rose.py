class DFA:

    current_state = None;

    def __init__(self, states, alphabet, transition_function, start_state, accept_states):
        self.states = states;
        self.alphabet = alphabet;
        self.transition_function = transition_function;
        self.start_state = start_state;
        self.accept_states = accept_states;
        self.current_state = start_state;
        return;
    
    def transition_to_state_with_input(self, input_value):
        inp_tuple = (self.current_state, input_value)
        print inp_tuple
        if inp_tuple in self.transition_function.keys():
            self.current_state = self.transition_function[(self.current_state, input_value)]
            print "in"
        else:
            self.current_state = None
            print "out"
        return;
    
    def in_accept_state(self):
        return self.current_state in accept_states;
    
    def go_to_initial_state(self):
        self.current_state = self.start_state;
        return;
    
    def run_with_input_list(self, input_list):
        self.go_to_initial_state();
        for inp in input_list:
            self.transition_to_state_with_input(inp);
            continue;
        return self.in_accept_state();
    pass;

# --- Main ---
states = {'s0', 's1'}
"""
alphabet = {0,1,2,3,4,5,6,7,8,9}

tf = {}
tf[('s0', 0)] = 's1'
tf[('s0', 1)] = 's1'
tf[('s0', 2)] = 's1'
tf[('s0', 3)] = 's1'
tf[('s0', 4)] = 's1'
tf[('s0', 5)] = 's1'
tf[('s0', 6)] = 's1'
tf[('s0', 7)] = 's1'
tf[('s0', 8)] = 's1'
tf[('s0', 9)] = 's1'

tf[('s1', '.')] = 's2'

tf[('s2', 0)] = 's2'
tf[('s2', 1)] = 's2'
tf[('s2', 2)] = 's2'
tf[('s2', 3)] = 's2'
tf[('s2', 4)] = 's2'
tf[('s2', 5)] = 's2'
tf[('s2', 6)] = 's2'
tf[('s2', 7)] = 's2'
tf[('s2', 8)] = 's2'
tf[('s2', 9)] = 's2'

start_state = 's0'
accept_states = {'s0','s2'}
"""
alphabet = {'a','b','c','d','e'}

tf = {}

tf[('s0', 'a')] = 's1'
tf[('s0', 'b')] = 's1'
tf[('s0', 'c')] = 's1'
tf[('s0', 'd')] = 's1'
tf[('s0', 'e')] = 's1'
tf[('s0', 'f')] = 's1'
tf[('s0', 'g')] = 's1'
tf[('s0', 'h')] = 's1'
tf[('s0', 'i')] = 's1'
tf[('s0', 'j')] = 's1'
tf[('s0', 'k')] = 's1'
tf[('s0', 'l')] = 's1'
tf[('s0', 'm')] = 's1'
tf[('s0', 'n')] = 's1'
tf[('s0', 'o')] = 's1'
tf[('s0', 'p')] = 's1'
tf[('s0', 'q')] = 's1'
tf[('s0', 'r')] = 's1'
tf[('s0', 's')] = 's1'
tf[('s0', 't')] = 's1'
tf[('s0', 'u')] = 's1'
tf[('s0', 'v')] = 's1'
tf[('s0', 'x')] = 's1'
tf[('s0', 'z')] = 's1'
tf[('s0', 'w')] = 's1'
tf[('s0', 'y')] = 's1'

tf[('s1', 'a')] = 's1'
tf[('s1', 'b')] = 's1'
tf[('s1', 'c')] = 's1'
tf[('s1', 'd')] = 's1'
tf[('s1', 'e')] = 's1'
tf[('s1', 'f')] = 's1'
tf[('s1', 'g')] = 's1'
tf[('s1', 'h')] = 's1'
tf[('s1', 'i')] = 's1'
tf[('s1', 'j')] = 's1'
tf[('s1', 'k')] = 's1'
tf[('s1', 'l')] = 's1'
tf[('s1', 'm')] = 's1'
tf[('s1', 'n')] = 's1'
tf[('s1', 'o')] = 's1'
tf[('s1', 'p')] = 's1'
tf[('s1', 'q')] = 's1'
tf[('s1', 'r')] = 's1'
tf[('s1', 's')] = 's1'
tf[('s1', 't')] = 's1'
tf[('s1', 'u')] = 's1'
tf[('s1', 'v')] = 's1'
tf[('s1', 'x')] = 's1'
tf[('s1', 'z')] = 's1'
tf[('s1', 'w')] = 's1'
tf[('s1', 'y')] = 's1'

tf[('s1', 0)] = 's1'
tf[('s1', 1)] = 's1'
tf[('s1', 2)] = 's1'
tf[('s1', 3)] = 's1'
tf[('s1', 4)] = 's1'
tf[('s1', 5)] = 's1'
tf[('s1', 6)] = 's1'
tf[('s1', 7)] = 's1'
tf[('s1', 8)] = 's1'
tf[('s1', 9)] = 's1'

start_state = 's0'
accept_states = {'s1'}

d = DFA(states, alphabet, tf, start_state, accept_states)

inp_program = "xda2"
print inp_program
#print tf.keys()

print d.run_with_input_list(inp_program);
