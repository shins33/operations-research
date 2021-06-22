import numpy as np

def valGen():
    m,n  = [int(x) for x in (input("Transportation Table Size (m,n) ").split(","))]
    
    column = list()
    dem_in = list()
    supl_in = list()

    for j in range(m):
        row = list()
        for i in range(n):
            a = int(input("Matrix Element[{}{}]: ".format(j+1,i+1)))
            row.append(a)
        column.append(row)

    arr = np.array(column, dtype = float)

    for k in range(m):
        
        s = int(input("Supply[{}]: ".format(k+1)))
        supl_in.append(s)

    for l in range(n):
        
        d = int(input("Demand[{}]: ".format(l+1)))
        dem_in.append(d)

    
    return arr,m,n,supl_in,dem_in
  
def NW_ifs(trans_t_o,supl_o,dem_o,cost_mat):

  supl,dem = supl_o.copy(),dem_o.copy()
  trans_t = trans_t_o.copy()

  ## Processing
  m,n = trans_t.shape[0], trans_t.shape[1]
  assign_mat = np.zeros(shape=(m,n))

  for i in range(m+n-1):
      max_pos = min(supl[0],dem[0])        
      supl[0] -= max_pos
      dem[0] -= max_pos
      s = len(supl)
      d = len(dem)


      if supl[0] == 0 :
          itrT = np.delete(trans_t,0,0)
          del supl[0]

      elif dem[0] == 0 :
          itrT = np.delete(trans_t,0,1)
          del dem[0]

      assign_mat[m-s,n-d]  = max_pos
      trans_t = itrT

  print("cost\n",cost_mat,"\nAssignment\n",assign_mat)
  final_mat = np.multiply(assign_mat,cost_mat)

  cost = np.sum(final_mat)
  print("Initial Feasible solution by NWC = ",cost)
    
def LCost(mat):
    lowCst = np.argmin(mat)
    lc_pos = np.unravel_index(lowCst,mat.shape)
    return lc_pos, mat[lc_pos]

def LC_ifs(trans_t_o,supl_o,dem_o,cost_mat):
    supl,dem = supl_o.copy(),dem_o.copy()
    trans_t = trans_t_o.copy()

    ## Processing
    m,n = trans_t.shape[0], trans_t.shape[1]
    assign_mat = np.zeros(shape=(m,n))
    
    for i in range(m+n-1):
        pos,val = LCost(trans_t)
        max_pos = min(supl[pos[0]],dem[pos[1]])
        supl[pos[0]] -= max_pos
        dem[pos[1]] -= max_pos

        if supl[pos[0]] == 0 :
            trans_t[pos[0],:] = trans_t[np.unravel_index(np.argmax(trans_t),trans_t.shape)]+1
            
        elif dem[pos[1]] == 0 :
            trans_t[:,pos[1]] = trans_t[np.unravel_index(np.argmax(trans_t),trans_t.shape)]+1
        assign_mat[pos[0],pos[1]]  = max_pos  

    print("cost\n",cost_mat,"\nAssignment\n",assign_mat)
    final_mat = np.multiply(assign_mat,cost_mat)
    cost = np.sum(final_mat)
    print("Initial Feasible Solution by LC = ",cost)
    
    
def penalty(arr):
    r_lst = []
    c_lst = []

    for m in arr.copy():
        m.sort()
        if not len(m) > 1:
            r_lst.append(m[0])
        else:r_lst.append(m[1]-m[0])

    for n in np.transpose(arr):
        n.sort()
        if not len(n) > 1:
            c_lst.append(n[0])
        else:c_lst.append(n[1]-n[0])
    return r_lst,c_lst

def vam_asgn(trans_t):
    idx0,idx1 = None,None
    pen_row, pen_col = penalty(trans_t.copy())
    if max(pen_row) > max(pen_col):
        idx0 = pen_row.index(max(pen_row))
        idx1 = list(trans_t[idx0]).index(min(trans_t[idx0, :]))

    elif max(pen_col) > max(pen_row):
        idx1 = pen_col.index(max(pen_col))
        idx0 = list(trans_t[:,idx1]).index(min(trans_t[:,idx1]))

    else:
        idx0 = pen_row.index(max(pen_row))
        idx1 = list(trans_t[idx0]).index(min(trans_t[idx0, :]))

    pos = [idx0,idx1]
    val = trans_t[idx0,idx1]
    return pos ,val

def vam_ifs(trans_t_o,supl_o,dem_o,cost_mat):
    supl,dem= supl_o.copy(),dem_o.copy()
    trans_t = trans_t_o.copy()
    
    ## Processing
    m,n = trans_t.shape[0], trans_t.shape[1]
    assign_mat = np.zeros(shape=(m,n))
    r_check_mat = np.zeros(m)
    c_check_mat = np.zeros(n)
    
    
    
    for i in range(m+n-1):
        pos,val = vam_asgn(trans_t)
        pos_check = list(pos).copy()
        max_pos = min(supl[pos[0]],dem[pos[1]])
        
        supl[pos[0]] -= max_pos
        dem[pos[1]] -= max_pos

        supl_ch = supl.copy()
        dem_ch = dem.copy()
    
        if supl[pos[0]] == 0 :
            itrT = np.delete(trans_t,pos[0],0)
            del supl[pos[0]]
            
        elif dem[pos[1]] == 0 :
            itrT = np.delete(trans_t,pos[1],1)
            del dem[pos[1]]

        if r_check_mat[pos[0]] == 1:
            r_inc = list(r_check_mat[:pos[0]]).count(1)   
            while r_check_mat[pos[0]] == 1:
                pos[0] += 1
            pos[0] += r_inc

        elif r_check_mat[pos[0]] == 0:
            r_inc = list(r_check_mat[:pos[0]]).count(1)
            pos[0] += r_inc
         
        if c_check_mat[pos[1]] == 1:
            c_inc = list(c_check_mat[:pos[1]]).count(1)
            while c_check_mat[pos[1]] == 1:
                pos[1] += 1
            pos[1] += c_inc
        

        elif c_check_mat[pos[1]] == 0:
            c_inc = list(c_check_mat[:pos[1]]).count(1)
            pos[1] += c_inc
        
        assign_mat[pos[0],pos[1]]  = max_pos  
        trans_t = itrT


        if supl_ch[pos_check[0]] == 0 :
            if r_check_mat[pos[0]] == 0:
                r_check_mat[pos[0]] = 1
            else:
                r_check_mat[pos[0]+1] = 1
            
        elif dem_ch[pos_check[1]] == 0 :
            if c_check_mat[pos[1]] == 0:
                c_check_mat[pos[1]] = 1
            else:
                c_check_mat[pos[1]+1] = 1

    print("cost\n",cost_mat,"\nAssignment\n",assign_mat)  
    final_mat = np.multiply(assign_mat,cost_mat)

    cost = np.sum(final_mat)
    print("Initial Feasible Solution by VAM = ",cost)
