class DFA:

    current_state = None;

    def __init__(self):

        self.states = {'s0', 's1', 's2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12','s13','s14','s15'}
        self.alphabet = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','z','w','y',
                    '0','1','2','3','4','5','6','7','8','9',
                    ":", ";", ",", "+", "-", "*", "/", "(", ")", "<", ">", "!", "=", "{", "}"}

        self.start_state = 's0'

        # id = s1, int = s2, float=s4, comp=s6,s7, aritm_op=s8, s9 = equal, s10 = left_par, s11= right_par, 
        #s12= left_bra, s13= right_bra, s14= comma, s15= semi-colon
        self.accept_states = {'s1','s2','s3','s6', 's7','s8','s9','s10','s11','s12','s13','s14','s15'}

        tf = {}
        # identifier transition
        tf[('s0', ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','z','w','y'))] = 's1'
        tf[('s1', ('a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','x','z','w','y'))] = 's1'
        tf[('s1', ('0','1','2','3','4','5','6','7','8','9'))] = 's1'
        # int transition
        tf[('s0', ('0','1','2','3','4','5','6','7','8','9'))] = 's2'
        tf[('s2', ('0','1','2','3','4','5','6','7','8','9'))] = 's2'
        # float transition 
        tf[('s0',('.'))] = 's4'
        tf[('s4', ('0','1','2','3','4','5','6','7','8','9'))] = 's3'
        tf[('s2',('.'))] = 's3'
        tf[('s3', ('0','1','2','3','4','5','6','7','8','9'))] = 's3'
        # operator token
        tf[('s0',("!",':'))] = 's5'
        tf[('s0',("<", ">"))] = 's6'
        tf[('s5',("="))] = 's7'
        tf[('s6',("="))] = 's7'
        tf[('s0',("+", "-", "*", "/"))] = 's8'
        tf[('s0',("="))] = 's9' 
        # separator token
        tf[('s0',("("))] = 's10'
        tf[('s0',(")"))] = 's11' 
        tf[('s0',("{"))] = 's12'
        tf[('s0',("}"))] = 's13' 
        tf[('s0',(","))] = 's14' 
        tf[('s0',(";"))] = 's15' 

        self.transition_function = tf

        return;
    
    def transition_to_state_with_input(self, input_value):

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
        #print "palavra: ", input_list
        for inp in input_list:
            self.transition_to_state_with_input(inp)
            continue
        return self.in_accept_state()
    pass