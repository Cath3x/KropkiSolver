#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.
'''
This file will contain different constraint propagators to be used within
bt_search.

propagator == a function with the following template
    propagator(csp, newly_instantiated_variable=None)
        ==> returns (True/False, [(Variable, Value), (Variable, Value) ...])

    csp is a CSP object---the propagator can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    newly_instaniated_variable is an optional argument.
    if newly_instantiated_variable is not None:
        then newly_instantiated_variable is the most
        recently assigned variable of the search.
    else:
        propagator is called before any assignments are made
        in which case it must decide what processing to do
        prior to any variables being assigned. SEE BELOW

    The propagator returns True/False and a list of (Variable, Value) pairs.

    Returns False if a deadend has been detected by the propagator.
        in this cas e bt_search will backtrack
    Returns True if we can continue.

    The list of variable values pairs are all of the values
    the propagator pruned (using the variable's prune_value method).
    bt_search NEEDS to know this in order to correctly restore these
    values when it undoes a variable assignment.

    NOTE propagator SHOULD NOT prune a value that has already been
    pruned! Nor should it prune a value twice.

    IF PROPAGATOR is called with newly_instantiated_variable = None
        PROCESSING REQUIRED:
            for plain backtracking (where we only check fully instantiated
            constraints) we do nothing...return (true, [])

            for forward checking (where we only check constraints with one
            remaining variable) we look for unary constraints of the csp
            (constraints whose scope contains only one variable) and we
            forward_check these constraints.

            for gac we establish initial GAC by initializing the GAC queue with
            all constaints of the csp

    IF PROPAGATOR is called with newly_instantiated_variable = a variable V
        PROCESSING REQUIRED:
            for plain backtracking we check all constraints with V (see csp
            method get_cons_with_var) that are fully assigned.

            for forward checking we forward check all constraints with V that
            have one unassigned variable left

            for gac we initialize the GAC queue with all constraints containing
            V.
'''
def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
    #IMPLEMENT
    bookKeeping = []
    if not newVar:
        for v in csp.get_all_unasgn_vars():
            for c in csp.get_cons_with_var(v):
                if c.get_n_unasgn() == 1:
                    unSigned = c.get_unasgn_vars()[0]
                    for d in unSigned.cur_domain():
                        unSigned.assign(d)
                        vals = []
                        vars = c.get_scope()
                        for var in vars:
                            vals.append(var.get_assigned_value())
                        unSigned.unassign()
                        if not c.check(vals):
                            unSigned.prune_value(d)
                            bookKeeping.append((unSigned, d))
                    #DWO
                    if unSigned.cur_domain_size() == 0:
                        return False, bookKeeping
    else:    
        for c in csp.get_cons_with_var(newVar):
            if c.get_n_unasgn() == 1:
                unSigned = c.get_unasgn_vars()[0]
                for d in unSigned.cur_domain():
                    unSigned.assign(d)
                    vals = []
                    vars = c.get_scope()
                    for var in vars:
                        vals.append(var.get_assigned_value())
                    unSigned.unassign()
                    if not c.check(vals):
                        unSigned.prune_value(d)
                        bookKeeping.append((unSigned, d))
                #DWO
                if unSigned.cur_domain_size() == 0:
                    return False, bookKeeping
    return True, bookKeeping
                
    

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT
    bookKeeping = []
    GACqueue = []
    #Enqueue all constrains
    if not newVar:
        for v in csp.get_all_unasgn_vars():
            GACqueue = GACqueue + csp.get_cons_with_var(v)            
    #Enqueue constrains for newVar
    else:
        GACqueue = csp.get_cons_with_var(newVar)
    
    found = False    
    while(len(GACqueue) > 0):
        c = GACqueue.pop()
        cScope = c.get_scope()
        for var in cScope:
            if not var.is_assigned():
                for d in var.cur_domain():
                    found = c.has_support(var, d)
                    if not found:
                        var.prune_value(d)
                        bookKeeping.append((var, d))
                        #DWO
                        if var.cur_domain_size() == 0:
                            GACqueue.clear()
                            return False, bookKeeping
                        else:
                            #add to the queue
                            temp = csp.get_cons_with_var(var)
                            GACqueue = GACqueue + temp
    return True, bookKeeping
            
def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    #IMPLEMENT
    mrv, heur = None, 100000
    
    for v in csp.get_all_unasgn_vars():
        l = len(csp.get_cons_with_var(v))
        if l < heur:
            mrv = v
            heur = l
	
    return mrv