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
        #print inp_tuple

        for tf2 in self.transition_function:  #d[tf2,(tf1)] = sx
            if self.current_state == tf2[0]:   
                if input_value in tf2[1]:
                    self.current_state = self.transition_function[tf2]
                    break

        if self.current_state != self.transition_function[tf2]:
            self.current_state = None
        return
    
    # Verifies whether current_state is final_state
    def in_accept_state(self):
        return self.current_state in self.accept_states
    
    def go_to_initial_state(self):
        self.current_state = self.start_state
        return

    def getCurrent_state(self):
        return self.current_state

    def getTransition_function(self):
        return selt.transition_function
    
    # processes each character individualy
    def run_with_input_list(self, input_list):
        self.go_to_initial_state()
        for inp in input_list:
            self.transition_to_state_with_input(inp)
            continue
        return self.in_accept_state()
    pass