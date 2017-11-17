#!/usr/bin/env python3

import sympy as sym
import re

l, mu = sym.var('l mu')

P0 = sym.Symbol('P0')
P1 = sym.Symbol('P1')
P2 = sym.Symbol('P2')
P3 = sym.Symbol('P3')

with open('state_diagram.dot', 'r') as f:
    lines = f.read().splitlines()

states = [line.strip() for line in lines if '->' in line]

nodes = set([state.split('->')[0].strip() for state in states])
equations = {}

for node in sorted(nodes):

    print('node: {}'.format(node))

    left = [s for s in states if s.split('->')[0][0] == node]
    right = [s for s in states if s.split('->')[1].split('[')[0][1] == node]

    left_equation = []
    right_equation = []

    for l in left:
        l_eq = re.findall(r'"([^"]*)"', l)[0]

        left_equation.append('{}'.format(l_eq))

    for r in right:
        r_eq = re.findall(r'"([^"]*)"', r)[0]

        input_node = r.split('->')[0].split()[0]

        right_equation.append('P{} * {}'.format(input_node, r_eq))

    print(left_equation)
    print(right_equation)

    left_equation = ' + '.join(left_equation)
    left_equation = 'P{} * ({})'.format(node, left_equation)
    right_equation = ' + '.join(right_equation)

    equations['P{}'.format(node)] = '{} - {}'.format(right_equation,
                                                       left_equation)


for pair in sorted(equations.items(), key=str):
    print('{}: {}'.format(*pair))

# equations['P0'] = ' + '.join(equations.keys()) + '-1'

system = [
    sym.sympify(expr).subs({
        l: 25,
        mu: 4,
    }) for expr in equations.values()
]

result = sym.solve(system, list(equations.keys()))

for pair in sorted(result.items(), key=str):
    print('{}: {}'.format(*pair))


# for pair in sorted(equations.items(), key=str):
#     print('{}: {}'.format(*pair))

# nodes = {}
# for line in lines:

#     if '->' not in line:
#         continue

# right = 'P{}'.format(line.split('->')[1][1:5])
# left = line.split('->')[0]
# equation = re.findall(r'"([^"]*)"', line)[0]

# if not nodes.get(right):
#     nodes[right] = 'P{} * ({})'.format(left, equation)
# else:
#     nodes[right] += ' + P{} * ({})'.format(left, equation)

# nodes.update((k, '{} - {}'.format(v, k)) for k, v in nodes.items())

# nodes['P0'] = ' + '.join(nodes.keys()) + '-1'

# equations = [
#     sym.sympify(expr).subs({
#         l: 25,
#         mu: 4,
#     }) for expr in nodes.values()
# ]

# result = sym.solve(equations, list(nodes.keys()))

# p = 0.75
# pi1 = 0.7
# pi2 = 0.65

# Pblock = sum([v for k, v in result.items() if str(k)[1] == '1'])
# Pblockpi1 = sum([v for k, v in result.items() if str(k)[2] == '2'])

# Lqueue = 1 * sum([v for k, v in result.items() if str(k)[3] == '1']) + 2 * sum(
#     [v for k, v in result.items() if str(k)[3] == '2'])

# Lc = Lqueue + sum([v for k, v in result.items() if str(k)[2] != '0']) + sum(
#     [v for k, v in result.items() if str(k)[4] == '1'])

# Wc = Lc / ((1 - p) * (1 - Pblock))

# for pair in sorted(result.items(), key=str):
#     print('{}: {}'.format(*pair))
# print('Pblocked: {}'.format(Pblock))
# print('Lqueue: {}'.format(Lqueue))
# print(Lc)
# print('Wc: {}'.format(Wc))
