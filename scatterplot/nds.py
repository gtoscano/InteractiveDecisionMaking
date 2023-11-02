"""
nds.py
non dominated sorting
"""

from dominance import *
import numpy
import numpy as np
from matplotlib.pyplot import figure, show

def nds(objs, cnstrs, compare):
    """
    Non-Dominated Sorting
    
    input
    chroms      (pop_size, n_vars) matrix
    
    output
    fronts      list of lists of indices
    ranks       (pop_size, ) vector
    """
    
    n = objs.shape[0]
    
    sp      = [ []   for i in range(n) ]
    np      = [ 0    for i in range(n) ]
    ranks   = [ 10000  for i in range(n) ]
    
    fronts  = [[]]
    cnstrs_sum = cnstrs.copy()
    cnstr_feasible_idx = cnstrs_sum >= 0.0
    cnstr_infeasible_idx = cnstrs_sum < 0.0
    cnstrs_sum [cnstr_feasible_idx] = 0.0
    #min_values = numpy.min(cnstrs_sum, axis=0)
    #max_values = numpy.max(cnstrs_sum, axis=0)
    #cnstrs_sum = (cnstrs_sum - min_values)/(max_values-min_values)
    #cnstrs_sum = cnstrs_sum / -min_values
    #cnstrs_sum  = cnstrs_sum - 1.0
    #cnstrs_sum [cnstr_zero_idx] = 0.0
    cnstrs_sum = numpy.sum(cnstrs_sum, axis=1)
    #print cnstrs_sum

    for p in range(n):
        
        for q in range(n):
            if p == q: continue
            a = objs[p, :]
            b = objs[q, :]
            cnstr_a = cnstrs_sum[p]
            cnstr_b = cnstrs_sum[q]

            result = compare(a, b, cnstr_a, cnstr_b)
            
            if result == A_DOM_B:
                sp[p].append(q)     # add q-th solution dominated by p-th solution
                
            elif result == A_IS_DOM_BY_B:
                np[p] += 1          # increment the domination counter of p-th solution

        if np[p] == 0:
            ranks[p] = 0
            fronts[0].append(p)
    
    
    #import ipdb; ipdb.set_trace()
    i = 0
    while len(fronts[i]) > 0:
        
        Q = []
        
        for p in fronts[i]:
            
            for q in sp[p]:
                
                np[q] -= 1
                
                if np[q] == 0:
                    ranks[q] = i+1
                    Q.append(q)
        i += 1
        
        if len(Q) > 0:
            fronts.append(list(Q))
        else:
            break
        
    return fronts, numpy.array(ranks)
        
if __name__ == "__main__":
    
    fig = figure("nds")
    ax = fig.add_subplot(111)
    ax.cla()
    ax.set_xlabel("$f_1$")
    ax.set_ylabel("$f_2$")
    #hold(True)
    objs = genfromtxt("combined-lc.txt")
    objs_len = len(objs)
    cnstrs = np.zeros((objs_len,1))
    fronts, ranks = nds(objs, cnstrs, compare_min)
    first_front = objs[fronts[0], :]
    savetxt('first_front.txt', first_front, delimiter=' ')
    print (fronts,ranks)
    ax.plot(objs[:, 0], objs[:, 1], "bo")
    ax.plot(objs[fronts[0], 0], objs[fronts[0], 1], "ro")
    for idx, p in enumerate(objs):
        x, y = p
        print (idx, ranks[idx])
        ax.text(x+.01, y, "%s" % (ranks[idx], )) 
                
    show()
