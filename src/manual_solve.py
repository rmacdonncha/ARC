#!/usr/bin/python
#STUDENT NAME:  Ray MacDonncha
#STUDENT ID:    08025479
#CLASS:         1MAO2
import os, sys
import json
import numpy as np
import re


# this function works by identifing the coordinate intersections between the values in the first sublist within the array
# and the last element of each sublist within each array
def solve_2281f1f4(x):
    #creating a new list from the first sublist of input array
    list_x = x[0]
   
    #creating a new list from the last element of every sublist
    list_y = [sublist[-1] for sublist in x]
   
    #create a new list of the postions of every non-zero element of list_x
    x1 = []
    for i in enumerate(list_x):
        x1.append(i)
    x1 = [x for (x,y) in x1 if y == 5]
   
    #create a new list of the postions of every non-zero element of list_y
    y1 = []
    for i in enumerate(list_y):
        y1.append(i)
    y1 = [x for (x, y) in y1 if y == 5]
   
    # getting a list of coordinates by getting the intersection of x and y
    coordinates = [] 
    for i in x1:
        for j in y1:
            coordinates.append((i, j))  
   
    # updating our array by replacing the values of the coordinates of our intersections
    for i,j in coordinates:
            x[j][i] = 2
    
    return x


# the way this function works is to create a new list of the nth elements from each sublist in the input array
# for example  input [[abc], [aab], [cba]]; output [[aac], [bab], [cba]]
# then append a reversed version of each sublist from the new to the existing existing elements of the input array.
# for example  input [[abc], [aab], [cba]]; output [[abccaa], [aabbab], [cbaabc]]
# then finally append a mirror image of you new list to the end 
# final output = [[abccaa], [aabbab], [cbaabc], [cbaabc],[babbaa],[aaccba]]
def solve_46442a0e(x):
    #creating an empty counter so that we can update the nth element for each loop
    counter = 0
    
    #creating two empty lists which we will use to store uor reversed and final lists
    y = []
    z = []
    x = x.tolist()
    
    for sublist in x:
        #this adds every nth element for every sublist to a new list y
        y.append([sublist[counter] for sublist in x])
        #updating the counter so it moves to the next nth element after finishing the loop
        counter += 1
   
    #once y is created, we append each sublist (reversed) to each counterpart sublist in x using zip
    #this is sent to populate list z
    for (x, y) in zip(x, y):
        z.append(x+y[::-1])
   
    #we create a mirrored version of z
    z_rev = [sublist[::-1] for sublist in z]
   
    #finally, we update z by appending the mirrored version we created at the previous step
    z  = z + z_rev[::-1]
    z = np.array(z)

    return z


# this funtion takes the non-zero elements of the input array and arranges them into a 3x3 array 
# their order in the 3x3 output matrix is determined by the postion of the element within their respective list
# if all non-zero elements are accounted for, then remainder of the 3x3 output array is filled with zeros
def solve_cdecee7f(x): 
    # creating an empty list
    newlist = []  
    
    # for every element in every sublist, we want to return tuple of that element and its position in the sublist
    # and append this to our new list
    for sublist in x:
        sublist_en = enumerate(sublist)
        for i in sublist_en:
            newlist.append(i)           
    
    # now we want to remove every tuple from our list where the element is zero
    tuples_filtered = [(x,y) for (x,y) in newlist if y > 0] 
    
    # then sort the tuples in order of the first element in the tuple (which is the position low->high)
    tuples_filtered_sorted = sorted(tuples_filtered, key=lambda tup: tup[0])   
    
    # now we just create a new list with the elements in order of the postion they appeared in, within their respecitive sublists
    final_list = [y for (x,y) in tuples_filtered_sorted]   
    
    # as we know the final grid will have 9 elements, we identify how many zeros we add to the end
    # we add them to a list and append them to our list of ordered elements
    empty_spaces = np.zeros(9 - len(final_list), dtype=int)
    empty_spaces = [num for num in empty_spaces]
    final_list = final_list + empty_spaces 
    
    #now we have a list of our 9 elements, which we need to convert to a 3x3 matrix, using numpy
    final_list = np.array(final_list)
    final_grid = final_list.reshape(3, 3)
    
    # then we convert this matrix back to a list of lists
    final_grid = final_grid.tolist()
    
    # we need to reverse the order of the element in the middle sublist
    final_grid[1].reverse()
    
    #then finally back to an np array for the output
    final_grid = np.array(final_grid)
    
    return final_grid


def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    # if yhat has the right shape, then (y == yhat) is a bool array
    # and we test whether it is True everywhere. if yhat has the wrong
    # shape, then y == yhat is just a single bool.
    print(np.all(y == yhat))

if __name__ == "__main__": main()

#SUMMARY
# The foundation of any solution seems to revolve around enumerating the position of every element in a given array,
# storing that element and its relative position in tuples, and in separate lists, 
# and from there, the commonalities seem to revolve around array/list manipulation, 
# swapping positions, reversing order, skipping, appending etc.. 
# until you have a pattern that gives you your desired output.

#Link to GitHub: https://github.com/rmacdonncha/ARC/blob/master/src/manual_solve.py
