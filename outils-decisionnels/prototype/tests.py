# -*- coding: utf-8 -*-

from security_solver import *
import unittest


class TestSolver(unittest.TestCase):

    def runTest(self):
        """Avoids bug when initialize manually"""
        pass

    @classmethod
    def setUpClass(cls):
        """Test data: Big junk of code"""
        print 'Setting up initial data:'
        print 'Initializing vertices ...'
        cls.v0 = Vertex(0, 'IS', 'nothing')
        cls.v1 = Vertex(1, 'CISCO FW', 'soft access')
        cls.v2 = Vertex(2, 'JUNIPER FW', 'informations gathered')
        cls.v3 = Vertex(3, 'CHAIN OF TRUST', 'physical access')
        cls.v4 = Vertex(4, 'APACHE', 'exception information')
        cls.v5 = Vertex(5, 'OPENSSH', 'remote access')
        cls.v6 = Vertex(6, 'PRO-FTP', 'filesystem access')
        cls.v7 = Vertex(7, 'MYSQL', 'database access')
        cls.v8 = Vertex(8, 'SOURCE CODE', 'source code access')
        cls.v9 = Vertex(9, 'FILESYSTEM', 'file access')
        cls.v10 = Vertex(10, 'SECRET DATA', 'game over !')
        cls.v11 = Vertex(11, 'ROOTKIT', 'game over !')

        print 'Initializing edges ...'
        cls.e0 = Edge(0, 'O-DAY', 0, cls.v0, cls.v1)
        cls.e1 = Edge(1, 'PORT SCAN', 5, cls.v0, cls.v2)
        cls.e2 = Edge(2, 'DDOS', 10, cls.v1, cls.v4)
        cls.e3 = Edge(3, 'BRUTE FORCE', 40, cls.v1, cls.v5)
        cls.e4 = Edge(4, 'HEAP OVERFLOW', 5, cls.v2, cls.v6)
        cls.e5 = Edge(5, 'LACK OF PRIVILEGE', 20, cls.v5, cls.v6)
        cls.e6 = Edge(6, 'SQLI', 50, cls.v4, cls.v7)
        cls.e7 = Edge(7, 'WGET', 50, cls.v4, cls.v8)
        cls.e8 = Edge(8, 'SCP', 0, cls.v5, cls.v9)
        cls.e9 = Edge(9, 'DNS DUMP', 40, cls.v6, cls.v9)
        cls.e10 = Edge(10, 'DNS DUMP', 10, cls.v9, cls.v8)
        cls.e11 = Edge(11, 'PHYSICAL BREACH', 55, cls.v0, cls.v3)
        cls.e12 = Edge(12, 'HARD DRIVE ROBERY', 0, cls.v3, cls.v7)
        cls.e13 = Edge(13, 'WIN', 0, cls.v7, cls.v10)
        cls.e14 = Edge(14, 'WIN', 10, cls.v8, cls.v10)
        cls.e15 = Edge(15, 'WIN', 50, cls.v6, cls.v11)

        print 'Initializing measures ...'
        cls.m1 = Measure(1, 'Patch Cisco FW', 30, {cls.e0: 50})
        cls.m2 = Measure(2, 'PSAD installation', 10, {cls.e0: 20, cls.e1: 25})
        cls.m3 = Measure(3, 'Fail2Ban installation', 20, {cls.e2: 15, cls.e3: 40})
        cls.m4 = Measure(4, 'Patch Pro-FTP', 5, {cls.e4: 60, cls.e5: 25})
        cls.m5 = Measure(5, 'SQL Firewall installation', 40, {cls.e6: 50})
        cls.m6 = Measure(6, 'Apache-modsec installation', 25, {cls.e2: 30, cls.e7: 30, cls.e6: 30})
        cls.m7 = Measure(7, 'IPS deploiement', 15, {cls.e8: 20, cls.e9: 20, cls.e10: 20})
        cls.m8 = Measure(8, 'Data encryption', 35, {cls.e12: 70})
        cls.m9 = Measure(9, 'Super defense', 200, {cls.e11: 100, cls.e1: 100})
        cls.m10 = Measure(10, 'Chmod/chown', 40, {cls.e15: 40})
        M = list()
        M.append(cls.m1)
        M.append(cls.m2)
        M.append(cls.m3)
        M.append(cls.m4)
        M.append(cls.m5)
        M.append(cls.m6)
        M.append(cls.m7)
        M.append(cls.m8)
        M.append(cls.m9)
        M.append(cls.m10)

        print 'Initializing initial graph ...'
        G = Graph()
        G.V.append(cls.v0)
        G.V.append(cls.v1)
        G.V.append(cls.v2)
        G.V.append(cls.v3)
        G.V.append(cls.v4)
        G.V.append(cls.v5)
        G.V.append(cls.v6)
        G.V.append(cls.v7)
        G.V.append(cls.v8)
        G.V.append(cls.v9)
        G.V.append(cls.v10)
        G.V.append(cls.v11)
        G.A.append(cls.e0)
        G.A.append(cls.e1)
        G.A.append(cls.e2)
        G.A.append(cls.e3)
        G.A.append(cls.e4)
        G.A.append(cls.e5)
        G.A.append(cls.e6)
        G.A.append(cls.e7)
        G.A.append(cls.e8)
        G.A.append(cls.e9)
        G.A.append(cls.e10)
        G.A.append(cls.e11)
        G.A.append(cls.e12)
        G.A.append(cls.e13)
        G.A.append(cls.e14)
        G.A.append(cls.e15)

        print 'Initializing problem ...'
        P = Problem(G, M)

        print 'Initializing solver ...'
        cls.S = GeneticSolver(P, 0.75, 0.25, 0.25, 300)

        print 'Decompozing by level ... (mandatory before solving)'
        cls.S.decomposition()

        print 'Setting initial graph data ... (mandatory before solving)'
        cls.S.set_initial_graph_data()

        print 'Set up completed !'

    def test_decomposition(self):
        print '\n\nTesting decomposition ...'
        self.S.P.G.print_levels()
        self.assertItemsEqual(self.S.P.G.L[0], [self.v0])
        self.assertItemsEqual(self.S.P.G.L[1], [self.v1, self.v2, self.v3])
        self.assertItemsEqual(self.S.P.G.L[2], [self.v4, self.v5])
        self.assertItemsEqual(self.S.P.G.L[3], [self.v6, self.v7])
        self.assertItemsEqual(self.S.P.G.L[4], [self.v9, self.v11])
        self.assertItemsEqual(self.S.P.G.L[5], [self.v8])
        self.assertItemsEqual(self.S.P.G.L[6], [self.v10])
        self.assertEqual(len(self.S.P.G.L), 7)

    def test_leaves(self):
        print '\n\nTesting leaves ...'
        print 'Leaves: %s' % self.S.P.G.leaves
        self.assertItemsEqual(self.S.P.G.leaves, [self.v10, self.v11])

    def test_initial_graph_length(self):
        print '\n\nTesting initial graph length ...'
        print 'Initial length: %s' % str(self.S.P.G.initial_length)
        self.assertEqual(self.S.P.G.initial_length, 55)

    def test_initial_graph_shortest_path(self):
        print '\n\nTesting initial graph shortest path ...'
        print 'Shortest path: %s' % str(self.S.P.G.initial_sp)
        self.assertItemsEqual(self.S.P.G.initial_sp, [self.v0, self.v3, self.v7, self.v10])

    def test_dijkstra(self):
        print '\n\nTesting Dijkstra ...'
        length, path = dijkstra(self.S.P.G)
        print "Distance: %d => Path %s" % (length, [str(u) for u in path])
        self.assertEqual(length, 55)
        self.assertSequenceEqual(path, [self.v0, self.v3, self.v7, self.v10])

    def test_dijkstra_with_efficient_assignments(self):
        print '\n\nTesting Dijkstra with efficient assignments ...'
        assignments = {self.e11: [self.m9], self.e1: [self.m9]}
        length, path = dijkstra(self.S.P.G, assignments)
        print "Distance: %d => Path %s" % (length, [str(u) for u in path])
        self.assertEqual(length, 60)
        self.assertSequenceEqual(path, [self.v0, self.v1, self.v5, self.v9, self.v8, self.v10])

    def test_dijkstra_with_inefficient_assignments(self):
        print '\n\nTesting Dijkstra with inefficient assignments ...'
        assignments = {self.e11: [self.m9], self.e0: [self.m1]}
        length, path = dijkstra(self.S.P.G, assignments)
        print "Distance: %d => Path %s" % (length, [str(u) for u in path])
        self.assertEqual(length, 60)
        self.assertSequenceEqual(path, [self.v0, self.v2, self.v6, self.v11])

    def test_gene_coding(self):
        print '\n\nTesting gene coding ...'
        id1 = Individual.gene_id(self.e1, self.m1)
        id2 = Individual.gene_id(self.e5, self.m7)
        id3 = Individual.gene_id(self.e15, self.m10)
        print "Gene ID %s for edge %s and measure %s" % (id1, self.e1, self.m1)
        print "Gene ID %s for edge %s and measure %s" % (id1, self.e5, self.m7)
        print "Gene ID %s for edge %s and measure %s" % (id1, self.e15, self.m10)

        self.assertEqual(Individual.gene_id(self.e1, self.m1), 257)
        self.assertEqual(Individual.gene_id(self.e5, self.m7), 1287)
        self.assertEqual(Individual.gene_id(self.e15, self.m10), 3850)

    def test_set_gene_and_compute(self):
        print '\n\nTesting set gene ...'
        ind = Individual(self.S.P)
        ind.set_gene(self.e5, self.m4, True)
        ind.compute()
        self.assertEqual(ind.get_gene(self.e5, self.m4), True)
        self.assertEqual(ind.budget, 5)
        ind.set_gene(self.e6, self.m5, 1)
        ind.compute()
        self.assertEqual(ind.get_gene(self.e6, self.m5), True)
        self.assertEqual(ind.budget, 45)
        ind.set_gene(self.e5, self.m4, 0)
        ind.compute()
        self.assertEqual(ind.get_gene(self.e5, self.m4), False)
        self.assertEqual(ind.budget, 40)

    def test_procreate(self):
        print '\n\nTesting procreate(n=3)...'
        pop = self.S.procreate(3)
        self.assertEqual(len(pop), 3)

        for ind in pop:
            print ind
            self.assertTrue(ind.length >= 55)
            self.assertTrue(ind.budget > 0)

            # the likelihood that an individual has no code=0 and code=1 is very low
            has_0_code = False
            has_1_code = False
            for gene_id, code in ind.genotype.items():
                if code == False:
                    has_0_code = True
                elif code == True:
                    has_1_code = True
                else:
                    raise Exception("Incorrect code for gene_id %d: %d" % (gene_id, code))

            self.assertTrue(has_0_code)
            self.assertTrue(has_1_code)

    def test_score(self):
        print '\n\nTesting score function ...'
        initial_ind = Individual(self.S.P)
        initial_ind_score = self.S.score(initial_ind)
        print initial_ind
        print "Score: %.2f" % initial_ind_score
        self.assertEqual(int(initial_ind_score*100), 6625)

        infinite_budget_ind = Individual(self.S.P)
        infinite_budget_ind.set_gene(self.e11, self.m9, True)
        infinite_budget_ind.set_gene(self.e1, self.m9, True)
        infinite_budget_ind.set_gene(self.e8, self.m7, True)
        infinite_budget_ind.set_gene(self.e6, self.m5, True)
        infinite_budget_ind.set_gene(self.e7, self.m6, True)
        infinite_budget_ind.compute()
        infinite_budget_ind_score = self.S.score(infinite_budget_ind)
        print infinite_budget_ind
        print "Score: %.2f" % infinite_budget_ind_score
        self.assertEqual(int(infinite_budget_ind_score*100), 4500)

        few_good_measures_ind = Individual(self.S.P)
        few_good_measures_ind.set_gene(self.e0, self.m2, True)
        few_good_measures_ind.set_gene(self.e1, self.m2, True)
        few_good_measures_ind.set_gene(self.e12, self.m8, True)
        few_good_measures_ind.compute()
        few_good_measures_ind_score = self.S.score(few_good_measures_ind)
        print few_good_measures_ind
        print "Score: %.2f" % few_good_measures_ind_score
        self.assertEqual(int(few_good_measures_ind_score*100), 8041)

    def test_crosses(self):
        print '\n\nTesting crosses ... (only for display !!)'
        pop = self.S.procreate(2)
        new_pop_1 = self.S.crosses(pop)
        new_pop_2 = self.S.crosses(self.S.procreate(100))
        self.assertEqual(len(new_pop_1), 2)
        self.assertEqual(len(new_pop_2), 26)

        father = pop[0]
        mother = pop[1]
        son = new_pop_1[0]
        daugther = new_pop_1[1]

        print "Father: %s" % father
        print "Mother: %s" % mother
        print "Son: %s" % son
        print "Daugther: %s" % daugther

        # test son
        for gene_id, code in son.genotype.items():
            if father.get_gene_by_id(gene_id) != code and mother.get_gene_by_id(gene_id) != code:
                raise Exception("Son gene %d=>%d not in mother or father" % (gene_id, code))

        # test daughter
        for gene_id, code in daugther.genotype.items():
            if father.get_gene_by_id(gene_id) != code and mother.get_gene_by_id(gene_id) != code:
                raise Exception("Daugther gene %d=>%d not in mother or father" % (gene_id, code))

    def test_mutations(self):
        print '\n\nTesting mutation ...'
        pop = self.S.procreate(1)
        mutants = self.S.mutations(pop)
        self.assertEqual(len(pop), 1)
        self.assertEqual(len(mutants), 1)
        ind = pop[0]
        mutant = mutants[0]

        mutations = 0
        for gene_id, code in ind.genotype.items():
            if mutant.get_gene_by_id(gene_id) != code:
                mutations += 1

        if not mutations:
            raise Exception("No mutation detected")
        else:
            print "%d mutations for %d genes" % (mutations, len(mutant.genotype))
            print "Original: %s" % ind
            print "Mutant: %s" % mutant

    def test_selection(self):
        print '\n\nTesting selection ...'
        pop = self.S.procreate(12)
        best = self.S.selection(pop, 3)
        self.assertEqual(len(best), 3)

        # best are sorted
        old = float('Inf')
        for ind in best:
            self.assertTrue(ind.score > 0)
            self.assertTrue(ind.score <= old)
            old = ind.score

        for ind in best:
            pop.remove(ind)

        # best are the best
        for ind in pop:
            self.assertTrue(ind.score <= old)

    def test_simple_solve(self):
        print '\n\nTesting solve (n=50, max=50) ...'
        result = self.S.solve(50, 50)

        print 'Best individuals:'
        for ind in result.optimum[0:3]:
            print ind


if __name__ == '__main__':
    unittest.main()
