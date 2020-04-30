import networkx as nx

total_score = 0
vertex_list = set()

def WVCDP(Graph, node=0):

    score_include = 0
    score_exclude = 0
    print(list(nx.bfs_successors(Graph, node, 1))[0][1])
    for child in list(nx.bfs_successors(Graph, node, 1))[0][1]:
        WVCDP(Graph, node=child)
        # print(child)

        children_wt = [G.nodes[c]['value'] for c in list(nx.bfs_successors(Graph, node, 1))[0][1]]
        score_exclude += sum(children_wt)
        score_include += G.nodes[node]['value']

        if score_include < score_exclude:
            vertex_list.add(node)
            print("Include = Current Node:", node, "; Adding: ", node)
        else:
            for child in list(nx.bfs_successors(Graph, node, 1))[0][1]:
                vertex_list.add(child)
                print("Exclude = Current Node:", node, "; Adding: ", child)


if __name__ == '__main__':
    G = nx.Graph()
    G.add_nodes_from([0,1,2,3,4])
    nx.set_node_attributes(G, None, 'VC')
    G.nodes[0]['value'] = 10
    G.nodes[1]['value'] = 5
    G.nodes[2]['value'] = 6
    G.nodes[3]['value'] = 1
    G.nodes[4]['value'] = 1
    G.add_edges_from([(0,1),(0,2),(1,3),(2,4)])
    g = nx.bfs_tree(G, 0)

    WVCDP(g)

    print(vertex_list)
    score = 0
    for v in vertex_list:
        score += G.nodes[v]['value']
    print(score)
