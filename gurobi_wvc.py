import igraph
import gurobipy as gp
from gurobipy import GRB
import random
import time

def WVCLP(G, category='Binary'):
    """
    This solves the Weighted Vertex Cover Problem
    of a networkx Graph (Undirected Tree) using
    Linear Programming.

    The size of the decision variable is the same as
    the order of the Graph (# of nodes)

    The decision variables can take a value of 1/0. 1
    if the node is a part of Independent Subset and 0
    if it isn't. The objective then is to maximise this
    sum.
    """
    # Fetch the number of nodes of the graph
    n = G.vcount()

    # Initializing the problem as an LP
    lp_prob = gp.Model('min_vertex_cover')
    lp_prob.setParam('OutputFlag', 0)
    if category == 'Binary':
        x = lp_prob.addVars(n, vtype=GRB.BINARY, name='x', lb=0, ub=1)
    else:
        x = lp_prob.addVars(n, vtype=GRB.CONTINUOUS, name='x', lb=1, ub=1)

    # Objective Function
    lp_prob.setObjective(x.prod([random.randint(1, n) for _ in range(n)]), GRB.MINIMIZE)

    # Constraints
    for e in G.es:
        lp_prob.addConstr(
            x[e.tuple[0]] + x[e.tuple[1]] >= 1,
            name=" Edge ({} {})".format(e.tuple[0], e.tuple[1])
        )

    lp_prob.optimize()
    return(lp_prob.ObjVal)

if __name__ == '__main__':
    integrality_gap = {}
    lp_time = {}
    ilp_time = {}
    for p in range(3, 10, 1):
        p /= 10
        print("************************")
        print("Probability {}".format(p))
        print("************************")
        for tree_size in range(20, 101, 10):
            repeats = 40
            integrality_gap[tree_size] = 0
            lp_time[tree_size] = 0
            ilp_time[tree_size] = 0
            for iterate in range(repeats):
                G = igraph.Graph.Erdos_Renyi(tree_size, p)

                start = time.perf_counter()
                ilp_liss = WVCLP(G)
                end = time.perf_counter()
                ilp_time[tree_size] += end - start

                start = time.perf_counter()
                lp_liss = WVCLP(G, category='Continuous')
                end = time.perf_counter()
                lp_time[tree_size] += end - start

                gap = lp_liss/ilp_liss
                integrality_gap[tree_size] += gap

            integrality_gap[tree_size] /= repeats
            lp_time[tree_size] /= repeats
            ilp_time[tree_size] /= repeats
            print("{}\t{}\t{}\t{}\t{}".format(p, tree_size, lp_time[tree_size], ilp_time[tree_size], integrality_gap[tree_size]))
