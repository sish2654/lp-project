import networkx as nx
import igraph
import pulp
import time

def DPGeneralLiss(G):
    """
    This code takes a networkx generated random graph
    and converts it into an igraph. And then calculates
    the maximum independent set of the graph
    """
    ig = igraph.Graph()
    ig.add_vertices(G.order())
    for e in G.edges():
        ig.add_edge(e[0], e[1])

    return ig.independence_number()

def DPLiss(G, node=0):
    """
    This is a DP implementation of Largest Independent Subset
    Problem. The optimal substructure for this problem is of
    the form

    DPLiss(node) = max{
                    (1 + sum of all grandchildren of node),
                    (sum of all children of node)
                }

    We choose to include the node or exclude the node
    """

    # LISS is already calculated.
    # No need to calculate it again
    if G.nodes[node]['LISS']:
        return(G.nodes[node]['LISS'])

    # If the nodes are just leaves, then
    # LISS is just 1
    if len(list(nx.bfs_successors(G, node))[0][1]) == 0:
        G.nodes[node]['LISS'] = 1
        return(G.nodes[node]['LISS'])

    # Whats the value of LISS if we to exclude the node?
    node_exclude = 0
    for parent in nx.bfs_successors(G, node, 1):
        children = parent[1]
        for child in children:
            node_exclude += DPLiss(G, child)

    # Whats the value of LISS if we include the node?
    node_include = 1 # As we're including the current node
    for child in list(nx.bfs_successors(G, node, 2))[1:]:
        grand_children = child[1]
        for grand_child in grand_children:
            node_include += DPLiss(G, grand_child)

    # The optimal sub-structure
    G.nodes[node]['LISS'] = max(node_exclude, node_include)
    return(G.nodes[node]['LISS'])

def LPLiss(G):
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
    n = G.order()

    # Initializing the problem as an LP
    decision_variables = ['x_{}'.format(i) for i in range(n)]
    lp_dvs = [pulp.LpVariable(var, cat='Binary') for var in decision_variables]

    lp_prob = pulp.LpProblem('independent_set', pulp.LpMaximize)

    # Objective Function
    lp_prob += pulp.lpSum(lp_dvs)

    # Constraints
    for e in G.edges():
        lp_prob += pulp.lpSum([lp_dvs[e[0]] + lp_dvs[e[1]]]) <= 1, "Edge ({}, {})".format(e[0], e[1])

    status = lp_prob.solve()
    assert(1 == status)

    obj_value = pulp.value(lp_prob.objective)
    return(obj_value)

if __name__ == '__main__':
    dp = {}
    lp = {}
    for tree_size in range(50, 101, 10):
        print(tree_size)
        dp[tree_size] = 0
        lp[tree_size] = 0
        repeats = 20
        for iterate in range(repeats):
            G = nx.erdos_renyi_graph(tree_size, 0.3)
            # assert(True == nx.is_connected(G))
            # g = nx.bfs_tree(G, 0) # BFS Tree is easy to parse
            # nx.set_node_attributes(g, None, 'LISS')

            start = time.perf_counter()
            dp_liss = DPGeneralLiss(G)
            end = time.perf_counter()

            dp[tree_size] += end - start

            start = time.perf_counter()
            lp_liss = LPLiss(G)
            end = time.perf_counter()

            lp[tree_size] += end - start
            assert(dp_liss == lp_liss)

        dp[tree_size] /= repeats
        lp[tree_size] /= repeats
        print(dp[tree_size], lp[tree_size])

    print(dp, lp)
