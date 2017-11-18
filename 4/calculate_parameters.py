#!/usr/bin/env python3

import sympy as sym
import re

P000 = sym.Symbol('P000')
P001 = sym.Symbol('P001')
P010 = sym.Symbol('P010')
P011 = sym.Symbol('P011')
P100 = sym.Symbol('P100')
P101 = sym.Symbol('P101')
P110 = sym.Symbol('P110')
P111 = sym.Symbol('P111')

with open('state_diagram.dot', 'r') as f:
    lines = f.read().splitlines()

states = [line.strip() for line in lines if '->' in line]

nodes = set([state.split('->')[0].strip() for state in states])
equations = {}

for node in sorted(nodes):

    left = [s for s in states if s.split('->')[0].strip() == node]
    right = [
        s for s in states if s.split('->')[1].split('[')[0].strip() == node
    ]

    left_equation = []
    right_equation = []

    for l in left:
        l_eq = re.findall(r'"([^"]*)"', l)[0]

        left_equation.append('{}'.format(l_eq))

    for r in right:
        r_eq = re.findall(r'"([^"]*)"', r)[0]

        input_node = r.split('->')[0].split()[0].strip()

        right_equation.append('P{} * {}'.format(input_node, r_eq))

    left_equation = ' + '.join(left_equation)
    left_equation = 'P{} * ({})'.format(node, left_equation)
    right_equation = ' + '.join(right_equation)

    equations['P{}'.format(node)] = '{} - {}'.format(right_equation,
                                                     left_equation)

equations['P000'] = ' + '.join(equations.keys()) + '-1'

system = [
    sym.sympify(expr).subs({
        'l': 25.0,
        'mu': 4.0
    }) for expr in equations.values()
]

result = sym.solve(system, list(equations.keys()))


l = 25
mu = 4

Px = sum([v for k, v in result.items() if str(k)[1] == '1'])
Py = sum([v for k, v in result.items() if str(k)[2] == '1'])
Pz = sum([v for k, v in result.items() if str(k)[3] == '1'])

Pdeny = result[P111]
A = l * (1 - Pdeny)

for pair in sorted(result.items(), key=str):
    print('{}: {}'.format(*pair))

print('Px: {}'.format(Px))
print('Py: {}'.format(Py))
print('Pz: {}'.format(Pz))
print('A: {}'.format(A))
