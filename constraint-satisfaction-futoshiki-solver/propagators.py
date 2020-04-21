#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.  

'''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated 
        constraints) 
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope 
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
		 
		 
var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''
import collections as collections


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
    if not newVar:
        return FC_Helper(csp, None)
    else:    
        return FC_Helper(csp, newVar)              
    return True, []

def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT

    if not newVar:
        return GAC_helper(csp, None)
    else:
        return GAC_helper(csp, newVar)
        
def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    save_mrv = collections.OrderedDict()

    for var in csp.get_all_unasgn_vars():
        save_mrv[var] = var.cur_domain_size() 

    if save_mrv:
        return min(save_mrv, key=save_mrv.get)
   
    return None

def FC_Helper(csp, newVar):

    if newVar == None:
        all_constraints = csp.get_all_cons()
    else:
        all_constraints = csp.get_cons_with_var(newVar)

    state_found = False
    current_search_state = False
    pruned = []

    for c in all_constraints:
        if c.get_n_unasgn() == 1: 
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            
            current_var_pos = 0
            current_search_state = True
            for var in vars:
                if var.get_assigned_value():
                    current_var_pos = current_var_pos + 1
                else:
                    for var_dom_val in var.cur_domain():
                        temp = vals.copy()
                        temp[current_var_pos] = var_dom_val
                        if c.check(temp):
                            state_found = True
                        else:
                            pruned.append((var, var_dom_val))
                            var.prune_value(var_dom_val)
                    if not state_found:
                        break
            if state_found:
                continue
            else: 
                break

    if current_search_state:
        if not state_found:
            return False, pruned
        else:
            return True, pruned 


def GAC_helper(csp, newVar):

    gac_queue = []
    if newVar == None:
        for c in csp.get_all_cons():
            gac_queue.append(c) 
    else:
        gac_queue =  csp.get_cons_with_var(newVar)

    pruned = []

    while len(gac_queue) != 0 :
        c = gac_queue.pop(0)
        vars = c.get_scope()
        for var in vars:
            for var_value in var.cur_domain():
                if c.has_support(var, var_value):
                    continue
                else:
                    var.prune_value(var_value)
                    pruned.append((var, var_value))
                
                    temp_constraint = csp.get_cons_with_var(var)
                    for constraint in gac_queue:
                        if constraint not in temp_constraint:
                            continue
                        else:
                            temp_constraint.remove(constraint)
                    gac_queue = gac_queue + temp_constraint

                if var.cur_domain_size() == 0:
                    return False, pruned
            
    return True, pruned