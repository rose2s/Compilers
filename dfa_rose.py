class DFA:

    current_state = None;
    tokenType = {"IDENTIFIER": 's1',"INTLITERAL": 's2',"FLOATLITERAL": 's3', "OPERATOR": 's4'}

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

        for tf2 in self.transition_function:
            if self.current_state == tf2[0]:
                if input_value in tf2[1]:
                    self.current_state = self.transition_function[tf2]
                    print self.current_state
                print "in"
        
        if self.current_state != self.transition_function[tf2]:
            self.current_state = None
            print "out"
        return;
    
    # Verifies whether current_state is final_state
    def in_accept_state(self):
        return self.current_state in accept_states;
    
    def go_to_initial_state(self):
        self.current_state = self.start_state;
        return;
    
    # processes each character individualy
    def run_with_input_list(self, input_list):
        self.go_to_initial_state();
        for inp in input_list:
            self.transition_to_state_with_input(inp);
            continue;
        return self.in_accept_state();
    pass;

# --- Main ---
states = {'s0', 's1', 's2'}

alphabet = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','z','w','y',
            '0','1','2','3','4','5','6','7','8','9',
            ":", ";", ",", "+", "-", "*", "/", "(", ")", "<", "<=", ">", ">=", "!=", "=", ":=", "{", "}"}

tf = {}
# identifier transition
tf[('s0', ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','z','w','y'))] = 's1'
tf[('s1', ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','z','w','y'))] = 's1'
tf[('s1', ('0','1','2','3','4','5','6','7','8','9'))] = 's1'
# int transition
tf[('s0', ('0','1','2','3','4','5','6','7','8','9'))] = 's2'
tf[('s2', ('0','1','2','3','4','5','6','7','8','9'))] = 's2'

start_state = 's0'
accept_states = {'s1','s2'}
# id = s1, int = s2

d = DFA(states, alphabet, tf, start_state, accept_states)

inp_program = "111"
print inp_program

print d.run_with_input_list(inp_program);
