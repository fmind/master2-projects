# -*- coding: utf-8 -*-

from security_solver import *
from tests import TestSolver

# import the graph lib
import matplotlib
matplotlib.use("Qt4Agg")
import matplotlib.pyplot as plt

# get the test result
TestSolver.setUpClass()
result = TestSolver.S.solve(50, 50, True)

print ""

# compute and save the figure
print 'Generating score plot ...'
score_plot = plt.figure()
l = plt.plot(result.score_maxs)
plt.setp(l, label='Max', color='r')
l = plt.plot(result.score_mins)
plt.setp(l, label='Min', color='b')
l = plt.plot(result.score_means)
plt.setp(l, label='Mean', color='g')
plt.legend(loc=4)
plt.axis([0, 50, 40, 110])
plt.ylabel('Score')
plt.xlabel('Generation')
plt.title('Score per generation')
plt.savefig('img/score.png')

print 'Generating length plot ...'
length_plot = plt.figure()
l = plt.plot(result.length_maxs)
plt.setp(l, label='Max', color='r')
l = plt.plot(result.length_mins)
plt.setp(l, label='Min', color='b')
l = plt.plot(result.length_means)
plt.setp(l, label='Mean', color='g')
plt.legend(loc=4)
plt.axis([0, 50, 40, 110])
plt.ylabel('Length')
plt.xlabel('Generation')
plt.title('Length per generation')
plt.savefig('img/length.png')

print 'Generating budget plot ...'
budget_plot = plt.figure()
l = plt.plot(result.budget_maxs)
plt.setp(l, label='Max', color='r')
l = plt.plot(result.budget_mins)
plt.setp(l, label='Min', color='b')
l = plt.plot(result.budget_means)
plt.setp(l, label='Mean', color='g')
plt.legend(loc=1)
plt.axis([0, 50, 0, 600])
plt.ylabel('Budget')
plt.xlabel('Generation')
plt.title('Budget per generation')
plt.savefig('img/budget.png')

print 'Generating path len plot ...'
path_plot = plt.figure()
l = plt.plot(result.path_maxs)
plt.setp(l, label='Max', color='r')
l = plt.plot(result.path_mins)
plt.setp(l, label='Min', color='b')
l = plt.plot(result.path_means)
plt.setp(l, label='Mean', color='g')
plt.legend(loc=4)
plt.axis([0, 50, 0, 11])
plt.ylabel('Path length')
plt.xlabel('Generation')
plt.title('Path length per generation')
plt.savefig('img/path.png')

print 'Generating population size plot ...'
pop_plot = plt.figure()
plt.plot(result.pop_size)
plt.axis([0, 50, 0, 100])
plt.ylabel('Population size')
plt.xlabel('Generation')
plt.title('Population size per generation')
plt.savefig('img/pop.png')

plt.show()
