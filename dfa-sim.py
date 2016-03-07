usage = """
Input file format:
  Set of states (q)
  Set of input symbols (i)
  Start state (q0)
  Set of accept states (f)
  Transition function (t)

If number of input symbols is 'n' and number of states is 'm', then
transition function is represented as an 'm x n' matrix with rows
corresponding to each state and columns corresponding to input symbol.
All rows in the input file except first four rows are part of transition
function.

Example - DFA for strings having at least one zero:
s1,s2
0,1
s1
s2,s1
s2,s2

"""
DEBUG = False

import os
import sys

while True:
    print('Path of file having input DFA (default input.txt):'),
    path = raw_input()
    if not path:
        path = 'input.txt'
        break
    if os.path.exists(path) and os.access(path, os.R_OK):
        break
    else:
        print('Error: File not found')

with open(path) as f:
    dfa = f.readlines()

if len(dfa) < 5:
    sys.exit('Error: Invalid DFA\n' + usage)

# parse first four lines
q = dfa[0].rstrip('\n').split(',')
i = dfa[1].rstrip('\n').split(',')
q0 = dfa[2].rstrip('\n')
f = list(set(dfa[3].rstrip('\n').split(',')))

if DEBUG:
    print(q, i, q0, f)

# validate first four lines
if not q:
    sys.exit('Error: Set of states should not be empty.')
if not i:
    sys.exit('Error: Set of input symbols should not be empty.')
for symbol in i:
    if len(symbol) != 1:
        sys.exit('Error: Input symbol "' + symbol + '" should be single character.')
if not q0:
    sys.exit('Error: Start state is required.')
if q0 not in q:
    sys.exit('Error: Start state "' + q0 + '" is not in set of states.')
for s in f:
    if s not in q:
        sys.exit('Error: Final state "' + s + '" is not in set of states.')

# parse and validate transition table
transition = [] 
t = dfa[4:]
if len(t) != len(q):
    sys.exit('Error: Transition function does not have sufficient rows')
for row_number, row in enumerate(t):
    states = row.rstrip('\n').split(',')
    if len(states) != len(i):
        m = 'Row ' + str(row_number) + ' "' + row.rstrip('\n')
        m += '" of transition function should have '
        m += str(len(i)) + ' columns.'
        sys.exit(m)
    for state in states:
        if state not in q:
            m = 'Error: State "' + state + '" of transition table '
            m += 'does not belong to set of states.'
            sys.exit(m)
    transition.append(states)

# input string and validate alphabet
while True:
    print('Input string:'),
    input_string = raw_input()
    for char in input_string:
        if char not in i:
            print('Symbol "' + char + '" is not in input alphabet.')
            continue
    break


# simulate DFA
current = q.index(q0)
if DEBUG:
    print('\nTransition steps:')
    print("- " + q[current])

for char in input_string:
    symbol = i.index(char)
    current = q.index(transition[current][symbol])
    if DEBUG:
        print(i[symbol] + ' ' + q[current])
if q[current] in f:
    print('\nOutput: Yes')
else:
    print('\nOutput: No')

