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
