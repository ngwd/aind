# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: 
   1.   for each unit u, generate dict like below 
        {'23': ['A1', 'C3'],
         '27': ['B2'],
         ...
        }
   2.   for those item in above dict, if its value is a list of size 2, it is 
        a twin contains in unit u, if its value is a list of size more than 2,
        say,  {'23': ['A1', 'A2', 'A3'],...}, this is not allowed. so  return 
        False earlier,
        Theoretically, we need to examine situation like 
        {'123', ['A1', 'A4', 'A5', 'A9']}. but not do it now.
   3.   get a list from u exclude the items of twin.
   4.   for each of the item in the list of #3, replace the possible occurence
        of each digit in k to nothing.
   5.   Add one more function to check the validity of the solved sodoku.
   
# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: add 2 more unit of diagonal , slash and backslash, into the unitlist. 
   need no more extra code for checking.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

