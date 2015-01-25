#!/usr/bin/env python
#-*- coding:utf-8 -*-
# automato.py
# AFD == Automato Finito Deterministico
#
# Componentes da 4-upla que descreve um AFD.
# NOTA: convencionalmente usa-se uma 5-upla, sendo o primeiro
#       o conjunto dos estados possiveis. Nesta implementacao
#       extrairemos os estados possiveis dos estados de entrada
#       na funcao de transicao.

( ALPHABET,
  TRANSITION_FUNCTION,
  START_STATE,
 FINAL_STATES
) = range(4)

def validate_machine(machine):
    if not machine:
        print 'validate_machine: maquina invalida.'
        return False

    possible_states = set(machine[TRANSITION_FUNCTION].keys())

    if not machine[FINAL_STATES].issubset(possible_states):
        print 'validate_machine: o conjunto dos estados finais (%s) '\
              'nao esta contido no conjunto dos estados possiveis. (%s)' %\
              (str(machine[FINAL_STATES]), str(possible_states))
        return False

    if machine[START_STATE] not in possible_states:
        print 'validate_machine: estado inicial (%s) '\
              'nao pertence ao conjunto dos estados possiveis (%s).' %\
              (str(machine[START_STATE]), str(possible_states))
        return False

    for state in possible_states:
        chars = set(machine[TRANSITION_FUNCTION][state].keys())
        resulting_states = set(machine[TRANSITION_FUNCTION][state].values())

        if not chars.issubset(machine[ALPHABET]):
            print 'validate_machine: pelo menos um dos caracteres de entrada '\
                  'da funcao de transicao nao faz parte do alfabeto {%s}.' %\
                  ','.join(machine[ALPHABET])
            return False

        if not resulting_states.issubset(possible_states):
            print 'validate_machine: algum(ns) dos estados resultantes da '\
                  'funcao de transicao nao faz(em) parte dos estados '\
                  'possiveis (%s).' % possible_states
            return False

    return True


def validate_string(alphabet, string):
    for char in string:
        if char not in alphabet:
            print 'validate_string: '\
                  '"%s" eh uma palavra invalida no alfabeto {%s}' %\
                  (string, ','.join(alphabet))
            return False

    return True


def process_string(machine, string):
    '''
    Avalia se 'string' pertence a linguagem descrita pelo
    AFD descrito por 'machine', retornando True ou False.
    Retorna 'None' em caso de parametros invalidos.
    '''

    if not validate_machine(machine) or \
       not validate_string(machine[ALPHABET], string):
        return None

    state = machine[START_STATE]
    for char in string:
        state = machine[TRANSITION_FUNCTION][state][char]

    return (state in machine[FINAL_STATES])


if __name__ == '__main__':
    # O AFD a seguir descreve uma linguagem sobre o alfabeto {[0-9]}
    # que aceita digitos

    alphabet = set(['0', '1', '2', '3','4','5','6','7','8','9'])
    trans_func = {'q1' : {alphabet : 'q1', alphabet : 'q2'},
                  'q2' : {'.' : q3},
                  'q3' : {alphabet : 'q3'}}
    start_state = 'q1'
    final_states = set(['q1','q3'])

    machine = (alphabet, trans_func, start_state, final_states)

    strings = ['0.1', '3456', 'se31', '10wa2', 'a0d', '']

    for string in strings:
        result = process_string(machine, string)
        if result != None:
		    print '%s = %s' % (string, result)

