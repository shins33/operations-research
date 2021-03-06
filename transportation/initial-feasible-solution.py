import numpy as np
from utilis import *
## Feasible Solution
## Data Collection

trans_t_in, m ,n, supl_in,dem_in = valGen()
m,n = trans_t_in.shape[0], trans_t_in.shape[1]
oprtn = int(input("Select Objective: \n0 >> Minimisation\n1 >> Maximisation : "))
print(trans_t_in)
print("supply ",supl_in," || Demand ",dem_in)

cost_mat_in = trans_t_in


if sum(supl_in) == sum(dem_in):
    print("Balanced Problem")
    if oprtn == 1:
        max = trans_t_in[np.unravel_index(np.argmax(trans_t_in),trans_t_in.shape)]
        trans_t_in = max - trans_t_in
    NW_ifs(trans_t_in,supl_in,dem_in,cost_mat_in)
    LC_ifs(trans_t_in,supl_in,dem_in,cost_mat_in)
    vam_ifs(trans_t_in,supl_in,dem_in,cost_mat_in)

else:
    print("Unbalanced Problem")
    if sum(supl_in) > sum(dem_in):
        print("adding dummy column")
        dumCol = np.zeros(shape=(m,1))
        trans_t_in = np.append(trans_t_in,dumCol,1)
        cost_mat_in = np.append(cost_mat_in,dumCol,1)
        if oprtn == 1:
            max = trans_t_in[np.unravel_index(np.argmax(trans_t_in),trans_t_in.shape)]
            trans_t_in = max - trans_t_in
        diff = sum(supl_in)-sum(dem_in)
        dem_in.append(diff)
        NW_ifs(trans_t_in,supl_in,dem_in,cost_mat_in)
        LC_ifs(trans_t_in,supl_in,dem_in,cost_mat_in)
        vam_ifs(trans_t_in,supl_in,dem_in,cost_mat_in)
        
    else:
        print("adding dummy row")
        dumCol = np.zeros(shape=(1,n))
        trans_t_in = np.append(trans_t_in,dumCol,0)
        cost_mat_in = np.append(cost_mat_in,dumCol,0)
        if oprtn == 1:
            max = trans_t_in[np.unravel_index(np.argmax(trans_t_in),trans_t_in.shape)]
            trans_t_in = max - trans_t_in
        diff = sum(dem_in)-sum(supl_in)
        supl_in.append(diff)
        NW_ifs(trans_t_in,supl_in,dem_in,cost_mat_in)
        LC_ifs(trans_t_in,supl_in,dem_in,cost_mat_in)
        vam_ifs(trans_t_in,supl_in,dem_in,cost_mat_in)
