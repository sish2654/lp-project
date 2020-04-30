import time

dp = {}
lp = {}
for p in range(5, 10, 1):
    p = p/10.0
    print("*********************")
    print("Probability p: {}".format(p))
    print("*********************")
    for tree_size in range(20, 91, 10):
        print(tree_size)
        dp[tree_size] = 0
        lp[tree_size] = 0
        repeats = 20
        for iterate in range(repeats):
            G = graphs.RandomGNP(tree_size, p)
            # assert(True == nx.is_connected(G))
            # g = nx.bfs_tree(G, 0) # BFS Tree is easy to parse
            # nx.set_node_attributes(g, None, 'LISS')

            start = time.perf_counter()
            dp_liss = G.vertex_cover(algorithm='Cliquer', value_only=True)
            end = time.perf_counter()

            dp[tree_size] += end - start

            start = time.perf_counter()
            lp_liss = G.vertex_cover(algorithm='MILP', value_only=True)
            end = time.perf_counter()

            lp[tree_size] += end - start
            assert(dp_liss == lp_liss)

        dp[tree_size] /= repeats
        lp[tree_size] /= repeats
        print(dp[tree_size], lp[tree_size])

    print(dp, lp)
