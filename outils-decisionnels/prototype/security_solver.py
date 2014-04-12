#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2013 Freaxmind
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__author__  = 'Freaxmind'
__email__   = 'freaxmind@freaxmind.pro'
__version__ = '0.1'
__license__ = 'GPLv3'

"""
    Security Solver: help you decide how to protect your Information System.
    If you can modelize it, you can solve it !

    See the file LICENSE for copying permission.
"""

import random
import math
import sys
import os

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout, we will set the default encoding ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')





class SolverException(Exception):
    """Program-specific Exception"""
    pass





def dijkstra(G, assignments=dict()):
    """
    Based on: http://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
            G: Graph object
            assignements: hash table of edge => list of measure (specific to this program)
    """
    # functions
    def smallest_dist(Q, dist):
        """
        Returns the unprocessed vertex with the smallest distance
            Q: set of unprocessed vertices
            dist: hash table of vertex => distance (int)
        """
        min = float('Inf')      # minimum distance thanks Python !
        vmin = None             # vertex with the minimum distance
        for v in Q:
            if dist[v] < min:   # regular minimum condition
                min = dist[v]
                vmin = v
            # when 2 distances are equals, we take the one with smallest degree
            # => attacker prefers to take the smallest path and the most direct !
            elif dist[v] == min and (vmin is not None and v.degree < vmin.degree):
                min = dist[v]
                vmin = v
        return vmin

    # initialization
    dist = dict()       # store the edge => distance
    previous = dict()   # store the edge => its predecessors
    source = G.V[0]     # root vertex
    target = None       # stores which leaf vertex was found first
    Q = set(G.V)        # stores the unprocessed vertices

    for v in G.V:       # initialize the collection
        dist[v] = float('Inf')
        previous[v] = None

    dist[source] = 0

    # main loop (check the pseudo-code)
    while len(Q) != 0:
        u = smallest_dist(Q, dist)
        Q.remove(u)

        if u in G.leaves:               # shortest path found to a leaf => stop the search !
            target = u
            break

        for v, e in u.children.items():
            alt = dist[u] + e.p         # compute alternative distance
            if e in assignments.keys(): # specific to this program: add assignement ponderation
                for m in assignments[e]:
                    #print 'Edge %s extended by measure: %s (+%s)' % (e, m, m.p(e))
                    alt += m.p(e)

            if alt > 100:               # distance from 0 to 100, no more no less !
                alt = 100

            if alt < dist[v]:           # if the alternative distance is shorter, we take it
                dist[v] = alt
                previous[v] = u

        # uncomment to debug
        #print 'MIN: %s => %d' % (u, dist[u])
        #print ''
        #for u, d in dist.items():
            #if u in Q:
                #print u, d
        #print ''

    # compute the shortest path
    u = target
    shortest_path = list()
    while u in previous.keys():         # we have to reverse the previous dict
        shortest_path.insert(0, u)
        u = previous[u]

    return dist[target], shortest_path





class Vertex(object):

    def __init__(self, id, asset, privilege):
        # attributes
        self.id = id                # Vertex ID
        self.degree = -1            # graph degree (computed elsewhere)
        self.asset = asset          # company asset (description)
        self.privilege = privilege  # attacker privilege (description)
        self.parents = dict()       # vertex parents
        self.children = dict()      # vertex children

    def __repr__(self):
        return '(%d)' % self.id





class Edge(object):

    def __init__(self, id, action, p, nfrom, nto):
        # attributes
        self.id = id                # edge ID
        self.action = action        # attacker action (description)
        self.p = p                  # ponderation (0-100) => effort for the attacker to get through
        self.nfrom = nfrom          # source vertex
        self.nto = nto              # destination vertex
        # vertex linking
        nfrom.children[nto] = self
        nto.parents[nfrom] = self

    def __repr__(self):
        return '=%d=' % self.id





class Measure(object):

    def __init__(self, id, name, c, r):
        # attributes
        self.id = id                # measure ID
        self.name = name            # measure name (description)
        self.c = c                  # cost to deploy by the company
        self.r = r                  # relevance by edge (=hash table edge => ponderation)

    def p(self, e):
        """Returns the ponderation for an edge"""
        if not e in self.r.keys():
            raise SolverException("Measure %s doesn't work with edge %s (key error)" % (self, e))
        return self.r[e]

    def __repr__(self):
        return '$%d$' % self.id





class Graph(object):

    def __init__(self):
        # attributes
        self.V = list()             # graph vertices (nodes)
        self.A = list()             # graph edges (arcs)
        self.L = list()             # vertices by level (degree => list of vertices)
        self.leaves = list()        # leaves are vertices without successors and attacker targets
        self.initial_length = None  # store the initial length of the graph
        self.initial_sp = None      # store initial shortest path of the graph

    def print_levels(self):
        """Print vertices by level"""
        print 'LEVEL\t|\tVERTICES'
        for i, vertices in enumerate(self.L):
            values = [str(v) for v in vertices]
            print "%d\t|\t%s" % (i, ''.join(values))





class Problem(object):
    """It's a really useful class, but I'm a POO junky !"""

    def __init__(self, G, M):
        # attributes
        self.G = G                          # initial graph
        self.M = M                          # security measures available





class Individual(object):
    """
    Used by the genetic algorithm.
    A gene is an assignement of a measure to an edge.
    """
    ID_COUNTER = 0                                                  # counter to determine ind ID automaticaly

    def __init__(self, P):
        # attributes
        Individual.ID_COUNTER += 1                                  # it's automatic
        self.id = Individual.ID_COUNTER                             # individual ID
        self.P = P                                                  # we use the problem  to compute the length and create the genotype
        self.score = -1                                             # score of the individual (set by evalutation function)
        self.budget = 0                                             # total budget
        self.length = P.G.initial_length                            # length of the shortest path
        self.shortest_path = P.G.initial_sp                         # shortest path (list of vertices)
        self.genotype = Individual.get_clean_genotype(P.M)          # characteristic of an individual [(edge+measure) => False/True]
        self.assignements = Individual.get_clean_assignements(P.G.A)# assignement of measures to an edge {e1 => [m1, m2], e2 => [m2, m3]}

    @staticmethod
    def gene_id(e, m):
        """Converts an assignement (e+m) to a gene ID"""
        e_part = bin(e.id).replace('0b', '').zfill(8)
        m_part = bin(m.id).replace('0b', '').zfill(8)

        return int(e_part + m_part, 2)

    @staticmethod
    def get_clean_genotype(M):
        """Returns an empty genotype"""
        genotype = dict()

        for m in M:
            for e in m.r.keys():
                gene_id = Individual.gene_id(e, m)
                genotype[gene_id] = None    # no code is set yet

        return genotype

    @staticmethod
    def get_clean_assignements(A):
        """Returns an empty assignements"""
        assignements = dict()

        for e in A:
            assignements[e] = set()

        return assignements

    def get_gene(self, e, m):
        """Gets the code of a gene by assignement => returns True/False"""
        return self.genotype[Individual.gene_id(e, m)]

    def get_gene_by_id(self, gene_id):
        """Gets the code of a gene by ID => returns True/False"""
        return self.genotype[gene_id]

    def set_gene(self, e, m, code):
        """Sets the code of a gene and the corresponding assignement"""
        if code == True:
            self.genotype[Individual.gene_id(e, m)] = True
            self.assignements[e].add(m)
        elif code == False:
            self.genotype[Individual.gene_id(e, m)] = False
            if m in self.assignements[e]:
                self.assignements[e].remove(m)
        else:
            raise SolverException("Unknown gene code: %d" % code)

    def compute(self):
        """Computes the length, the shortest path and the budget of this individual"""
        # length and shortest path
        l, sp = dijkstra(self.P.G, self.assignements)
        self.length = l
        self.shortest_path = sp

        # budget
        self.budget = 0         # reset !
        for e, ms in self.assignements.items():
            for m in ms:
                self.budget += m.c

    def __repr__(self):
        genes = []
        for e, ms in self.assignements.items():
            if len(ms) > 0:
                genes.append('%s%s' % (e, ','.join([str(m) for m in ms])))
        path = ', '.join([str(v) for v in self.shortest_path])
        score = 'Score %.2f => ' % self.score if self.score > 0 else ''

        return "%sInd %s = LEN: %s/100, SHORT_PATH: (%s), COST: %s$, ASSIGN: %s" % (score, self.id, self.length, path, self.budget, ' | '.join(genes))





class SolverResult(object):

    def __init__(self, n):
        self.n = n                          # number of generation
        self.optimum = list()               # best individual sorted descending
        # many stats !
        self.score_means = list()
        self.score_maxs = list()
        self.score_mins = list()
        self.length_means = list()
        self.length_maxs = list()
        self.length_mins = list()
        self.budget_means = list()
        self.budget_maxs = list()
        self.budget_mins = list()
        self.path_means = list()
        self.path_maxs = list()
        self.path_mins = list()
        self.pop_size = list()





class GeneticSolver(object):

    def __init__(self, P, p, crosses_rate, mutation_rate, target_budget):
        # attributes
        self.P = P                                  # a security decision problem
        self.p = p                                  # ratio priority => p*length (efficiency) / (1-p)*budget (cost)
        self.crosses_rate = crosses_rate            # rate of mutation in a population and a genotype
        self.mutation_rate = mutation_rate          # rate of mutation in a population and a genotype
        self.target_budget = float(target_budget)   # budget the CISO wants to invest

    @staticmethod
    def _flat_assignements(M):
        """Converts the measure list to a list of assignement => returns [[e,m], [e,m] ...]"""
        ass = list()

        for m in M:
            for e in m.r.keys():
                ass.append([e,m])

        return ass

    def decomposition(self):
        """Decompose the graph by level"""
        # reset previous result
        self.P.G.L = list()
        self.P.G.leaves = list()

        # initialization
        my_vertices = list(self.P.G.V)
        tagged = list()
        degree = 0

        # main loop
        while len(my_vertices) != 0:
            # get the vertices for this degree
            degree_vertices = list()

            for v in my_vertices:
                # checks if the vertex has untagged predecessors
                has_untagged_predecessors = False
                for u in v.parents.keys():
                    if not u in tagged:
                        has_untagged_predecessors = True
                        break

                # no untagged predecessors means it belongs to this degree
                if not has_untagged_predecessors:
                    degree_vertices.append(v)
                    v.degree = degree

            # tags and removes them
            for v in degree_vertices:
                my_vertices.remove(v)
                tagged.append(v)

                # find leaves
                if len(v.children) == 0:
                    self.P.G.leaves.append(v)

            # insert only when vertices have been found
            if len(degree_vertices) > 0:
                self.P.G.L.insert(degree, degree_vertices)

            degree += 1

    def set_initial_graph_data(self):
        """Computes the initial data of the graph (length and shortest path)"""
        l, path = dijkstra(self.P.G)
        self.P.G.initial_length = l
        self.P.G.initial_sp = path

    def score(self, ind):
        """Scores an individual (evalutation function)"""
        value = self.p * ind.length + (1-self.p) * (100 - ind.budget/self.target_budget*100)
        ind.score = value

        return value

    def procreate(self, n):
        """Returns a population of N individuals (all viable)"""
        pop = list()

        for i in range(n):
            ind = Individual(self.P)

            # set the genotype
            for m in self.P.M:
                for e in m.r.keys():
                    ind.set_gene(e, m, random.choice([False,True]))

            ind.compute()
            pop.append(ind)

        return pop

    def crosses(self, pop):
        """Chooses n family (mother+father), crosses their genotype and procreate 2n children => returns n*2 new individuals"""
        new_pop = []
        flat_ass = GeneticSolver._flat_assignements(self.P.M)
        n = int(math.ceil(len(pop)*self.crosses_rate/2))     # number of family to crosses

        for i in range(n):
            # get parents
            father, mother = random.sample(pop, 2)

            # create children
            son = Individual(self.P)
            daugther = Individual(self.P)

            # crosses their gene
            random.shuffle(flat_ass)
            for i, ass in enumerate(flat_ass):
                if i%2 == 0:
                    son.set_gene(ass[0], ass[1], father.get_gene(ass[0], ass[1]))
                    daugther.set_gene(ass[0], ass[1], mother.get_gene(ass[0], ass[1]))
                else:
                    son.set_gene(ass[0], ass[1], mother.get_gene(ass[0], ass[1]))
                    daugther.set_gene(ass[0], ass[1], father.get_gene(ass[0], ass[1]))

            son.compute()
            daugther.compute()
            new_pop.append(son)
            new_pop.append(daugther)

        return new_pop

    def mutations(self, pop):
        """Mutates some gene of some individual (based on the mutation rate)"""
        mutants = list()
        ass = GeneticSolver._flat_assignements(self.P.M)    # the complete list of assignement
        n = int(math.ceil(len(pop)*self.mutation_rate))     # number of individuals to mutate
        m = int(math.ceil(len(ass)*self.mutation_rate))     # number of gene to mutate per individual

        for i in range(n):
            ind = random.choice(pop)
            mutant = Individual(self.P)
            mutate_ass = random.sample(ass, m)                      # sample of gene to mutate

            # change switch the code of gene in mutate_ass
            for em in ass:
                if em in mutate_ass:
                    code = True if ind.get_gene(em[0], em[1]) == False else False   # switch the code
                else:
                    code = ind.get_gene(em[0], em[1])                               # keep the code
                mutant.set_gene(em[0], em[1], code)

            mutant.compute()
            mutants.append(mutant)

        return mutants

    def selection(self, pop, n):
        """Computes the score, sorts the population and selects the n best individuals"""
        # compute the score
        for ind in pop:
            self.score(ind)

        # sort the population
        pop = sorted(pop, key=lambda ind: ind.score, reverse=True)

        # select the best individuals
        return pop[0:n]

    def _state(self, trace, pop):
        """Saves some stat"""
        score_mean = 0
        score_max = 0
        score_min = float('Inf')
        length_mean = 0
        length_max = 0
        length_min = float('Inf')
        budget_mean = 0
        budget_max = 0
        budget_min = float('Inf')
        path_mean = 0
        path_max = 0
        path_min = float('Inf')

        for ind in pop:
            # means
            score_mean += ind.score
            length_mean += ind.length
            budget_mean += ind.budget
            path_mean += len(ind.shortest_path)
            # min
            score_min = ind.score if ind.score < score_min else score_min
            length_min = ind.length if ind.length < length_min else length_min
            budget_min = ind.budget if ind.budget < budget_min else budget_min
            path_min = len(ind.shortest_path) if len(ind.shortest_path) < path_min else path_min
            # max
            score_max = ind.score if ind.score > score_max else score_max
            length_max = ind.length if ind.length > length_max else length_max
            budget_max = ind.budget if ind.budget > budget_max else budget_max
            path_max = len(ind.shortest_path) if len(ind.shortest_path) > path_max else path_max

        # append
        trace.score_means.append(score_mean/len(pop))
        trace.score_maxs.append(score_max)
        trace.score_mins.append(score_min)
        trace.length_means.append(length_mean/len(pop))
        trace.length_maxs.append(length_max)
        trace.length_mins.append(length_min)
        trace.budget_means.append(budget_mean/len(pop))
        trace.budget_maxs.append(budget_max)
        trace.budget_mins.append(budget_min)
        trace.path_means.append(path_mean/len(pop))
        trace.path_maxs.append(path_max)
        trace.path_mins.append(path_min)
        trace.pop_size.append(len(pop))


    def solve(self, n, max, stat=False):
        """Solves the decision problem using a genetic algorithm"""
        # this is the base algorithm
        trace = SolverResult(n)
        pop = self.procreate(n)
        i = 1

        while i < max:
            pop += self.crosses(pop)
            pop += self.mutations(pop)
            pop = self.selection(pop, n)
            i += 1

            if stat:
                self._state(trace, pop)

        trace.optimum = pop

        return trace
