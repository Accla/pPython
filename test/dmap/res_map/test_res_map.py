##
# Test a res map #
import pPython as GPC
from Dmap import *
from rand import *
from size import *
from zeros import *

Np = GPC.Np
Pid = GPC.Pid

mapA = Dmap([Np,1],'b',range(Np));
mapB = Dmap([1,Np],'b',range(Np));

N = 8
A = rand(N,N,map=mapA);
B = rand(N,N,map=mapB);

print('mapA:')
mapA.show()


print(' Now ith row of B to the top node in ith column of A ');
print(' ');

# map B's ith row to the top node in A's ith column
res_gridspec = [size(mapA['grid'], 0)[0], 1];
print('--> res_gridspec = %s'%(str(res_gridspec)))
res_distspec = dict()
res_distspec[0]= mapA['dist_spec'][0]
res_distspec[1] = dict()
res_distspec[1]['dist'] = 'b'
my_idx = 1
res = dict()
for i in range(size(mapA['grid'], 1)[0]):
  res_map = Dmap(res_gridspec, res_distspec, mapA['grid'][:, i])
  print('Iter = %d'%(i))
  print('--> res_proclist = ')
  print(mapA['grid'][:, i]) 
  res[i] = zeros(size(A, 0)[0], size(B, 1)[0], map=res_map)
  # store which result matrix this processor will use
  res_map.show()
  if inmap(res_map, Pid):
    my_idx = i
    print('Pid = %d found in res_map  my_idx = %d'%(Pid,i))


