import time
import pulp

# Class to solve the problems using Integer Linear Programming
class ILP:
    
    # Function to solve the Knapsack Problem
    def knapsackILP(self, score_list, wt_list, wt_threshold):

        # Creating LP Decision Variables
        lp_dvs = [pulp.LpVariable('x_{}'.format(i), lowBound=0, upBound=1, \
                    cat='Integer') for i in range(1, len(score_list)+1)]
        
        # Initializing the Linear Program
        lp_prob = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

        # Adding Objective Function
        lp_prob += pulp.lpSum([coeff * var 
                    for coeff, var in zip(score_list, lp_dvs)])

        # Adding Constraints
        lp_prob += pulp.lpSum([wt*var \
                    for wt, var in zip(wt_list, lp_dvs)]) <= wt_threshold, \
                    "Item(s) Weight Sum must be >={}".format(wt_threshold)

        print(lp_prob)

        # Solving the Linear Program
        lp_prob.solve()

        # Printing the Solution
        print("Solution Status: "+str(pulp.LpStatus[lp_prob.status]))
        for v in lp_prob.variables():
            print(v.name, "=", round(v.varValue, 2))
        print("Objective Value = ", pulp.value(lp_prob.objective))

        # Returning the Solution
        return pulp.value(lp_prob.objective)

    # Function to solve the Rod Cutting Problem
    def rodCuttingILP(self, price_list, rod_length):

        # Creating LP Decision Variables
        lp_dvs = [pulp.LpVariable('x_{}'.format(i), lowBound=0, \
                    cat='Integer') for i in range(1, rod_length+1)]
        
        # Initializing the Linear Program
        lp_prob = pulp.LpProblem("RodCuttingProblem", pulp.LpMaximize)

        # Adding Objective Function
        lp_prob += pulp.lpSum([coeff * var for coeff, var \
                    in zip(price_list, lp_dvs)])

        # Adding Constraints
        lp_prob += pulp.lpSum([i*var \
                    for i, var in zip(range(1, rod_length+1), \
                    lp_dvs)]) >= rod_length, \
                    "Cut Length Sum must be >={}".format(rod_length)
        lp_prob += pulp.lpSum([i*var \
                    for i, var in zip(range(1, rod_length+1), \
                    lp_dvs)]) <= rod_length, \
                    "Cut Length Sum must be <={}".format(rod_length)

        print(lp_prob)

        # Solving the Linear Program
        lp_prob.solve()

        # Printing the Solution
        print("Solution Status: "+str(pulp.LpStatus[lp_prob.status]))
        for v in lp_prob.variables():
            print(v.name, "=", round(v.varValue, 2))
        print("Objective Value = ", pulp.value(lp_prob.objective))
        
        # Returning the Solution
        return pulp.value(lp_prob.objective)

# x = ILP()
# x.knapsackILP([80,100,120,150], [10,20,30,40], 50)
# x.rodCuttingILP([1,5,8,9,10,17,17,20], 8)