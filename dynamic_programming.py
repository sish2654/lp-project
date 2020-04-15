import time
import sys

# Class to solve the problems using Dynamic Programming
class DP:

    # Function to solve the Knapsack Problem
    def knapsackDP(self, score_list, wt_list, wt_threshold):

        # Getting the Number of Items 
        num_items = len(score_list)

        # Creating the Lookup Matrix
        lookup_matrix = [[0 for x in range(wt_threshold + 1)] \
                        for x in range(num_items + 1)]
        
        for i in range(num_items+1): 
            for w in range(wt_threshold+1): 
                if i==0 or w==0: 
                    lookup_matrix[i][w] = 0
                elif wt_list[i-1] <= w: 
                    lookup_matrix[i][w] = max(score_list[i-1] \
                                        + lookup_matrix[i-1][w-wt_list[i-1]], \
                                        lookup_matrix[i-1][w]) 
                else: 
                    lookup_matrix[i][w] = lookup_matrix[i-1][w] 

        # Returning the Solution
        return lookup_matrix[num_items][wt_threshold]

    # Function to solve the Rod Cutting Problem
    def rodCuttingDP(self, price_list, rod_length):
        
        # Getting the Number of Items 
        minimum = -1 * sys.maxsize

        # Creating the Lookup Matrix
        lookup_matrix = [0 for x in range(rod_length+1)] 
        lookup_matrix[0] = 0
    
        for i in range(1, rod_length+1): 
            max_val = minimum 
            for j in range(i): 
                max_val = max(max_val, price_list[j] + lookup_matrix[i-j-1]) 
            lookup_matrix[i] = max_val 
    
        # Returning the Solution
        return lookup_matrix[rod_length] 

# x = DP()
# print(x.knapsackDP([60,100,120,150], [10,20,30,40], 50))
# print(x.rodCuttingDP([1,5,8,9,10,17,17,20], 8))