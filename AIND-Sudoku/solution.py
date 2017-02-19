assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values



def cross(a, b):
    """Cross product of elements in A and elements in B."""
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
#memory allocation for lists
diag1 = []
diag2 = []
diagonal_units = []
#generating two main diagonals
for i in range(0,9):
	diag1.append(rows[i]+cols[i])
	diag2.append(rows[i]+cols[8-i])

#generating unit with both main diagonals	
diagonal_units.append(diag1)
diagonal_units.append(diag2)
#adding main diagonals unit to unitlist
unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    #iterating through all units
    for unit in unitlist:
    	#getting all boxes that could be twin pairs to reduce amount of boxes being iterated
    	potential_twin_values = [box for box in unit if len(values[box]) == 2]
    	#iteration of potential twins to find twins
    	for box1 in potential_twin_values:
    		#counter is used to keep track of how many boxes there are with the same value
    		counter = 0
    		for box2 in potential_twin_values:
    			if values[box1] == values[box2]:
    				counter += 1
    		#if there are 2 with the same value, go through unit and replace digits in every unit that is not part of the twin pair
    		if counter == 2:
    			for box3 in unit:
    				if values[box3] != values[box1]:
    					values[box3] = values[box3].replace(values[box1][0], '')
    					values[box3] = values[box3].replace(values[box1][1], '')
    return values

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
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
	#code of lesson used
	solved_values = [box for box in values.keys() if len(values[box]) == 1]
	for box in solved_values:
		digit = values[box]
		for peer in peers[box]:
			values[peer] = values[peer].replace(digit,'')
	return values


def only_choice(values):
	#code of lesson used
	for unit in unitlist:
		for digit in '123456789':
			dplaces = [box for box in unit if digit in values[box]]
			if len(dplaces) == 1:
				values[dplaces[0]] = digit
	return values

def reduce_puzzle(values):
	#code of lesson used
	solved_values = [box for box in values.keys() if len(values[box]) == 1]
	stalled = False
	while not stalled:
		solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
		values = eliminate(values)
		values = only_choice(values)
		values = naked_twins(values)
		solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
		stalled = solved_values_before == solved_values_after
		if len([box for box in values.keys() if len(values[box]) == 0]):
			return False
	return values

def search(values):
	#code of lesson used
	values = reduce_puzzle(values)
	if values is False:
		return False ## Failed earlier
	if all(len(values[s]) == 1 for s in boxes):
		return values
	n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
	for value in values[s]:
		new_sudoku = values.copy()
		new_sudoku[s] = value
		attempt = search(new_sudoku)
		if attempt:
			return attempt

def solve(grid):

    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
