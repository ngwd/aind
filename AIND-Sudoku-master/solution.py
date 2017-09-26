assignments = []

cols = '123456789'
rows = 'ABCDEFGHI'
def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B];

def dot_concate(A, B):
    return [v[0] + v[1] for v in zip(A,B)];
slash = dot_concate(rows, cols[::-1])
backslash = dot_concate(rows, cols)

boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units + [slash] + [backslash]  # add slash and backslash unit for diagonal sodoku
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for u in unitlist:
        temp = {k:v for k, v in values.items() if k in u and len(v)==2}
        twins = {};
        """ generate dict twins like below 
        {'23': ['A1', 'C3'],
         '27': ['B2'],
        }
        """
        for k, v in temp.items():
            twins.setdefault(v, []).append(k);
        
        # {'24':['A2', 'B3', 'C1']} is not allowed. return False earlier
        if (len([k for k,v in twins.items() if len(v)>2 ])):
            return False;
                           
        for k, v in twins.items():
            other_boxes = [ b for b in u if len(v)==2 and b not in v];
            for o in other_boxes:
                for digit in k:
                    values[o] = values[o].replace(digit, '');

    return values;


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid)==81
    lgrid = list( map(lambda x: '123456789' if x=='.' else x, list(grid)));
    return dict(zip(boxes, lgrid));

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def validity(values):
    # check the sodoku solution validity
    for u in unitlist:
        t = sum(ord(values[v])-ord('0') for v in u)
        if t!= 45:
            return False;
    return True;

def eliminate(values):
    settled_values = {k:v for k, v in values.items() if len(v)==1};
    unsettled_values = {k:v for k, v in values.items() if len(v)!=1};
    for k, v in unsettled_values.items():
        set_v = set(list(v));
        for i in peers[k]:
            if i in settled_values:
                set_v -= set(settled_values[i]);
        values[k] = ''.join(set_v);
    return values;

def only_choice(values):
    for u in unitlist:
        for d in '123456789':
            dplaces = [b for b in u if d in values[b]];
            if len(dplaces) == 1:
                values[dplaces[0]] = d;
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values =  eliminate(values);
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values);
        values = naked_twins(values);
        # naked_twins might return false
        if values is False:
            return False;

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values);
    if values is False:
        return False;        
    
    if len( [v for k, v in values.items() if len(v)>1] ) == 0:
        return values if validity(values) else False;

    min_box, min_val = min((len(values[s]), s) for s in values.keys() if len(values[s])>1);
    
    for s in values[min_val]:
        new_values = values.copy();
        
        new_values[min_val] = s;
        print ("\n choose  " + min_val + ":   " + s)
        r = search(new_values);
        if r :
            return r;

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid);
    values = search(values);
    if values is False:
        return False
    return values;

if __name__ == '__main__':
    
    #diag_sudoku_grid = '4.......3..9.........1...7.....1.8.....5.9.....1.2.....3...5.........7..7.......8' # D1.00
    #diag_sudoku_grid = '......3.......12..71..9......36...................56......4..67..95.......8......' # D1.01
    
    #diag_sudoku_grid = '....3...1..6..........9...5.......6..1.7.8.2..8.......3...1..........7..9...2....' # D1.02
    #diag_sudoku_grid = '...47..........8.........5.9..2.1...4.......6...3.6..1.7.........4..........89...' # D1.03
    #diag_sudoku_grid = '...4.....37.5............89....9......2...7......3....43............2.45.....6...' # D1.04
    #diag_sudoku_grid = '..7........5.4...........18...3.6....1.....7....8.2...62...........9.6........4..' # D1.05
    #diag_sudoku_grid = '....29.......7......3...8..........735.....161..........6...4......6.......83....' # D1.06
    #diag_sudoku_grid = '7.......8.....14...4........7..1.......4.3.......6..2........3...35.....5.......4' # D1.07
    #diag_sudoku_grid = '5.......7......2.....3...1...8.4.......7.8.......2.9...8...5.....1......6.......9' # D1.08
    #diag_sudoku_grid = '..682...........69..7.......2..........9.4..........8.......5..58...........521..' # D1.09
    
    #diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #diag_sudoku_grid = '........4......1.....6......7....2.8...372.4.......3.7......4......5.6....4....2.'
    diag_sudoku_grid = '9.1....8.8.5.7..4.2.4....6...7......5..............83.3..6......9................'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
