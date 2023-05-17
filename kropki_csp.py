#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Kropki Grid CSP models.
'''

from cspbase import *
import itertools

class KropkiBoard:
    '''Abstract class for defining KropkiBoards for search routines'''
    def __init__(self, dim, cell_values, consec_row, consec_col, double_row, double_col):
        '''Problem specific state space objects must always include the data items
           a) self.dim === the dimension of the board (rows, cols)
           b) self.cell_values === a list of lists. Each list holds values in a row on the grid. Values range from 1 to dim);
           -1 represents a value that is yet to be assigned.
           c) self.consec_row === a list of lists. Each list holds values that indicate where adjacent values in a row must be
           consecutive.  For example, if a list has a value of 1 in position 0, this means the values in the row between 
           index 0 and index 1 must be consecutive. In general, if a list has a value of 1 in position i,
           this means the values in the row between index i and index i+1 must be consecutive.
           d) self.consec_col === a list of lists. Each list holds values to indicate where adjacent values in a column must be 
           consecutive. Same idea as self.consec_row, but for columns instead of rows.
           e) self.double_row === a list of lists. Each list holds values to indicate where adjacent values in a row must be
           hold two values, one of which is the twice the value of the other.  For example, if a list has a value of 1 in 
           position 0, this means the value in the row at index 0 myst be either twice or one half the value at index 1 in the row.
           f) self.double_col === a list of lists. Each list holds values to indicate where adjacent values in a column must be
           hold two values, one of which is the twice the value of the other.  For example, if a list has a value of 1 in 
           position 0, this means the value in the column at index 0 myst be either twice or one half the value at index 1 in that
           column.
        '''
        self.dim = dim
        self.cell_values = cell_values
        self.consec_row = consec_row
        self.consec_col = consec_col        
        self.double_row = double_row
        self.double_col = double_col        


def kropki_csp_model_1(initial_kropki_board):
    '''Return a tuple containing a CSP object representing a Kropki Grid CSP problem along 
       with an array of variables for the problem. That is, return

       kropki_csp, variable_array

       where kropki_csp is a csp representing Kropki grid of dimension N using model_1
       and variable_array is a list such that variable_array[i*N+j] is the Variable 
       (object) that you built to represent the value to be placed in cell i,j of
       the Kropki Grid.
              
       The input board is specified as a KropkiBoard (see the class definition above)
              
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {1-N} if the board
       has a -1 at that position, and domain equal {i} if the board has
       a non-negative number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all variables in the
       same row, etc.).

       model_1 also contains binary consecutive and double constraints for each 
       column and row, as well as sub-square constraints.

       Note that we will only test on boards of size 6x6, 9x9 and 12x12
       Subsquares on boards of dimension 6x6 are each 2x3.
       Subsquares on boards of dimension 9x9 are each 3x3.
       Subsquares on boards of dimension 12x12 are each 4x3.
    '''
    #IMPLEMENT
    domain_dft = []
    
    cons = []
   
    vars = []
    dim = initial_kropki_board.dim
    
    #The default domain
    for i in range(dim):
       domain_dft.append(i+1)
       
    # Initiating the Variables
    # Naming convention: Q {ROW}{COLUMN}
    for i in range(dim):
       for j in range(dim):
          dom_sel = domain_dft
          if initial_kropki_board.cell_values[i][j] != -1:
             dom_sel = [initial_kropki_board.cell_values[i][j]]
          temp = Variable("Q{}{}".format(i, j), dom_sel)
          if temp.domain_size() == 1:
             temp.assign(temp.domain()[0])   
          vars.append(temp)
   
    # Initiating the horizontial constrains
    for i in range(dim):
       # Row NON-EQUAL
       for qi in range (dim):
          for qj in range (qi+1, dim):
             c = Constraint("C(Q{}{}, Q{}{})".format(i+1, qi+1, i+1, qj+1), [vars[i*dim+qi], vars[i*dim+qj]])
             tups = []
             for a in itertools.product(domain_dft, domain_dft):
                if a[0] != a[1]:
                   tups.append(a)
             c.add_satisfying_tuples(tups)
             cons.append(c)
             
       # Row consecutive
       cur = initial_kropki_board.consec_row[i]
       for rc_i in range(len(cur)):
          if cur[rc_i] == 1:
             c = Constraint("C(Q{}{}, Q{}{})".format(i+1, rc_i+1, i+1, rc_i+2), [vars[i*dim+rc_i], vars[i*dim+rc_i+1]])
             tups = []
             for a in itertools.product(domain_dft, domain_dft):
                if abs(a[0]-a[1]) == 1:
                   tups.append(a)
             c.add_satisfying_tuples(tups)
             cons.append(c)
       
       # Row double
       cur = initial_kropki_board.double_row[i]
       for rc_i in range(len(cur)):
          if cur[rc_i] == 1:
             c = Constraint("C(Q{}{}, Q{}{})".format(i+1, rc_i+1, i+1, rc_i+2), [vars[i*dim+rc_i], vars[i*dim+rc_i+1]])
             tups = []
             for a in itertools.product(domain_dft, domain_dft):
                if a[0]*2 == a[1] or a[1]*2 == a[0]:
                   tups.append(a)
             c.add_satisfying_tuples(tups)
             cons.append(c)
    
    # Initiating the vertical constrains
    for i in range(dim):
       # Column NON-EQUAL
       for qi in range(dim):
          for qj in range (qi+1, dim):
             c = Constraint("C(Q{}{}, Q{}{})".format(qi+1, i+1, qj+1, i+1), [vars[i+qi*dim], vars[i+qj*dim]])
             tups = []
             for a in itertools.product(domain_dft, domain_dft):
                if a[0] != a[1]:
                   tups.append(a)
             c.add_satisfying_tuples(tups)
             cons.append(c)
             
       # Column consecutive
       cur = initial_kropki_board.consec_col[i]
       for rc_i in range(len(cur)):
          if cur[rc_i] == 1:
             c = Constraint("C(Q{}{}, Q{}{})".format(rc_i+1, i+1, rc_i+2, i+1), [vars[i+rc_i*dim], vars[i+(rc_i+1)*dim]])
             tups = []
             for a in itertools.product(domain_dft, domain_dft):
                if abs(a[0]-a[1]) == 1:
                   tups.append(a)
             c.add_satisfying_tuples(tups)
             cons.append(c)
       
       # Column double
       cur = initial_kropki_board.double_col[i]
       for rc_i in range(len(cur)):
          if cur[rc_i] == 1:
             c = Constraint("C(Q{}{}, Q{}{})".format(rc_i+1, i+1, rc_i+2, i+1), [vars[i+rc_i*dim], vars[i+(rc_i+1)*dim]])
             tups = []
             for a in itertools.product(domain_dft, domain_dft):
                if a[0]*2 == a[1] or a[1]*2 == a[0]:
                   tups.append(a)
             c.add_satisfying_tuples(tups)
             cons.append(c)
    
    # Subsqure NON-EQUAL only for 6x6 and 9x9
    if dim == 6:
       # divide 6x6 into 6 3x2
       for y in range(2):
          for x in range(3):
             
             # iterating over the 6 squares of the inner square
             # Get coordinates in the sub squares
             coord_list = []
             for qy in range(3):
                for qx in range(2):
                   coord_list.append((y*3+qy, x*2+qx))
                   
             # Iterating over the 6 coords to check they are not equal
             for i in range(6):
                for j in range(i+1, 6):
                   c = Constraint("C(Q{}{}, Q{}{})".format(coord_list[i][0]+1, coord_list[i][1]+1, coord_list[j][0]+1, coord_list[j][1]+1), [vars[coord_list[i][0]*6+coord_list[i][1]], vars[coord_list[j][0]*6+coord_list[j][1]]])
                   tups = []
                   for a in itertools.product(domain_dft, domain_dft):
                      if a[0] != a[1]:
                         tups.append(a)
                c.add_satisfying_tuples(tups)
                cons.append(c)           
    elif dim == 9:
       # divide 6x6 into 9 3x3
       for y in range(3):
          for x in range(3):
             
             # iterating over the 6 squares of the inner square
             # Get coordinates in the sub squares
             coord_list = []
             for qy in range(3):
                for qx in range(3):
                   coord_list.append((y*3+qy, x*2+qx))
                   
             # Iterating over the 6 coords to check they are not equal
             for i in range(9):
                for j in range(i+1, 9):
                   c = Constraint("C(Q{}{}, Q{}{})".format(coord_list[i][0]+1, coord_list[i][1]+1, coord_list[j][0]+1, coord_list[j][1]+1), [vars[coord_list[i][0]*6+coord_list[i][1]], vars[coord_list[j][0]*6+coord_list[j][1]]])
                   tups = []
                   for a in itertools.product(domain_dft, domain_dft):
                      if a[0] != a[1]:
                         tups.append(a)
                c.add_satisfying_tuples(tups)
                cons.append(c) 
    else:
       print("Invalid dimention provided") 
       
    game = CSP("{}x{} Kropki".format(dim, dim), vars)
    
    for c in cons:
       game.add_constraint(c)
   
    return game, vars #change this!

def kropki_csp_model_2(initial_kropki_board):
   '''Return a tuple containing a CSP object representing a Kropki Grid CSP problem along 
       with an array of variables for the problem. That is return

       kropki_csp, variable_array

       where kropki_csp is a csp representing Kropki grid of dimension N using model_2
       and variable_array is a list such that variable_array[i*N+j] is the Variable 
       (object) that you built to represent the value to be placed in cell i,j of
       the Kropki Grid.
              
       The input board is specified as a KropkiBoard (see the class definition above)
              
       This routine returns model_2 which consists of a variable for
       each cell of the board, with domain equal to {1-N} if the board
       has a -1 at that position, and domain equal {i} if the board has
       a non-negative number i at that cell.
       
       model_2 contains N-ARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all variables in the
       same row, etc.).

       model_2 also contains binary consecutive and double constraints for each 
       column and row, as well as sub-square constraints.

       Note that we will only test on boards of size 6x6, 9x9 and 12x12
       Subsquares on boards of dimension 6x6 are each 2x3.
       Subsquares on boards of dimension 9x9 are each 3x3.
       Subsquares on boards of dimension 12x12 are each 4x3.
    '''
   #IMPLEMENT
   domain_dft = []
    
   cons = []
   
   vars = []
   dim = initial_kropki_board.dim
    
   #The default domain
   for i in range(dim):
      domain_dft.append(i+1)
       
   # Initiating the Variables
   # Naming convention: Q {ROW}{COLUMN}
   for i in range(dim):
      for j in range(dim):
         dom_sel = domain_dft
         if initial_kropki_board.cell_values[i][j] != -1:
            dom_sel = [initial_kropki_board.cell_values[i][j]]
         temp = Variable("Q{}{}".format(i, j), dom_sel)
         if temp.domain_size() == 1:
            temp.assign(temp.domain()[0])
         vars.append(temp)
   
   # For the NON-EQUAL, the constrains are the same thus
   neq_cons = []
   for i in itertools.permutations(domain_dft, dim):
      neq_cons.append(i)
   
   # Initiating the horizontial constrains
   for i in range(dim):
      
      # Row NON-EQUAL
      l_var = []
      for qi in range (dim):
         l_var.append(vars[i*dim+qi])
            
      c = Constraint("Row{}".format(qi+1), l_var)
      c.add_satisfying_tuples(neq_cons)
      cons.append(c)
            
      # Row consecutive
      cur = initial_kropki_board.consec_row[i]
      for rc_i in range(len(cur)):
         if cur[rc_i] == 1:
            c = Constraint("C(Q{}{}, Q{}{})".format(i+1, rc_i+1, i+1, rc_i+2), [vars[i*dim+rc_i], vars[i*dim+rc_i+1]])
            tups = []
            for a in itertools.product(domain_dft, domain_dft):
               if abs(a[0]-a[1]) == 1:
                  tups.append(a)
            c.add_satisfying_tuples(tups)
            cons.append(c)
      
      # Row double
      cur = initial_kropki_board.double_row[i]
      for rc_i in range(len(cur)):
         if cur[rc_i] == 1:
            c = Constraint("C(Q{}{}, Q{}{})".format(i+1, rc_i+1, i+1, rc_i+2), [vars[i*dim+rc_i], vars[i*dim+rc_i+1]])
            tups = []
            for a in itertools.product(domain_dft, domain_dft):
               if a[0]*2 == a[1] or a[1]*2 == a[0]:
                  tups.append(a)
            c.add_satisfying_tuples(tups)
            cons.append(c)
    
    # Initiating the vertical constrains
   for i in range(dim):
   
      # Column NON-EQUAL
      l_var = []
      for qi in range (dim):
         l_var.append(vars[dim*qi+i])
            
      c = Constraint("Col{}".format(i+1), l_var)
      c.add_satisfying_tuples(neq_cons)
      cons.append(c)
             
      # Column consecutive
      cur = initial_kropki_board.consec_col[i]
      for rc_i in range(len(cur)):
         if cur[rc_i] == 1:
            c = Constraint("C(Q{}{}, Q{}{})".format(rc_i+1, i+1, rc_i+2, i+1), [vars[i+rc_i*dim], vars[i+(rc_i+1)*dim]])
            tups = []
            for a in itertools.product(domain_dft, domain_dft):
               if abs(a[0]-a[1]) == 1:
                  tups.append(a)
            c.add_satisfying_tuples(tups)
            cons.append(c)
       
      # Column double
      cur = initial_kropki_board.double_col[i]
      for rc_i in range(len(cur)):
         if cur[rc_i] == 1:
            c = Constraint("C(Q{}{}, Q{}{})".format(rc_i+1, i+1, rc_i+2, i+1), [vars[i+rc_i*dim], vars[i+(rc_i+1)*dim]])
            tups = []
            for a in itertools.product(domain_dft, domain_dft):
               if a[0]*2 == a[1] or a[1]*2 == a[0]:
                  tups.append(a)
            c.add_satisfying_tuples(tups)
            cons.append(c)
    
   # Subsqure NON-EQUAL only for 6x6 and 9x9
   if dim == 6:
      # divide 6x6 into 6 3x2
      for y in range(2):
         for x in range(3):
            # iterating over the 6 squares of the inner square
            subsq_list = [] 
            for i in range(3):
               for j in range(2):
                  subsq_list.append(vars[(y*3+i)*6+(x*2+j)])
            
            # Constraint
            c = Constraint("SS{}{}".format(y+1, x+1), subsq_list)     
            c.add_satisfying_tuples(neq_cons)
            cons.append(c)
   elif dim == 9:
      # divide 9x9 into 9 3x3
      for y in range(3):
         for x in range(3):
            # iterating over the 6 squares of the inner square
            subsq_list = [] 
            for i in range(3):
               for j in range(3):
                  subsq_list.append(vars[(y*3+i)*9+(x*3+j)])
            
            # Constraint
            c = Constraint("SS{}{}".format(y+1, x+1), subsq_list)     
            c.add_satisfying_tuples(neq_cons)
            cons.append(c)
   else:
      print("Invalid dimention provided")
      
   game = CSP("{}x{} Kropki".format(dim, dim), vars)
    
   for c in cons:
      game.add_constraint(c)
   
   return game, vars #change this!


    
