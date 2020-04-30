import igraph
import pulp

def WVCLP(G, category='Binary'):
    """
    This solves the Largest Independent Subset Problem
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
    decision_variables = ['x_{}'.format(i) for i in range(n)]
    lp_dvs = [pulp.LpVariable(var, cat=category) for var in decision_variables]

    lp_prob = pulp.LpProblem('min_vertex_cover', pulp.LpMinimize)

    # Objective Function
    lp_prob += pulp.lpSum(lp_dvs)

    # Constraints
    for e in G.es:
        lp_prob += pulp.lpSum([lp_dvs[e.tuple[0]] + lp_dvs[e.tuple[1]]]) >= 1, "Edge ({}, {})".format(e.tuple[0], e.tuple[1])

    status = lp_prob.solve()
    assert(1 == status)

    obj_value = pulp.value(lp_prob.objective)
    return(obj_value)

if __name__ == '__main__':
    integrality_gap = {}
    for p in range(3, 10, 1):
        p /= 10
        print("************************")
        print("Probability {}".format(p))
        print("************************")
        for tree_size in range(60, 91, 10):
            print(tree_size)
            repeats = 20
            integrality_gap[tree_size] = 0
            for iterate in range(repeats):
                G = igraph.Graph.Erdos_Renyi(tree_size, p)

                ilp_liss = WVCLP(G)

                lp_liss = WVCLP(G, category='Continuous')

                gap = ilp_liss/lp_liss
                integrality_gap[tree_size] += gap

            integrality_gap[tree_size] /= repeats
            print(integrality_gap[tree_size])
