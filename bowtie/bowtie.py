import numpy as np
import datetime as dt
import igraph
from tqdm import trange, tqdm


class bowtie:
    '''
    the class extract the greatest bow-tie structure in the network.
    it returns istances for each class of nodes, according to Yang and others
    

    '''

    def __init__(self, igraph_network, verbose=False):
        self.verbose=verbose
        self.membership=np.zeros(len(igraph_network.vs), dtype='U12')
        self.SCC(igraph_network)
        self.IN_and_OUT(igraph_network)
        self.other_stuff(igraph_network)
        
    def SCC(self, igraph_network):
        bow_tie_sccs=igraph_network.components(mode='Strong')
        # get all SCCs
        l_bow_tie_sccs=np.array([len(_cl) for _cl in bow_tie_sccs])
        # get the lenght of all SCCs
        _mask=l_bow_tie_sccs==max(l_bow_tie_sccs)
        # get a proper mask
        _how_may=np.sum(_mask)
        # get the number of the largest SCCs
        if _how_may==1:
            where_scc=[_im for _im, _m in enumerate(_mask) if _m][0]
        else:
            which_one=np.random.choice(_how_may)
            where_scc=[_im for _im, _m in enumerate(_mask) if _m][which_one]
            
        self.SCC=bow_tie_sccs[where_scc]
        self.SCC.sort()
        self.membership[self.SCC]='SCC'
        if self.verbose:
            print('{:%H:%M:%S:%f}\tSCC'.format(dt.datetime.now()))
        
    def IN_and_OUT(self, igraph_network):
        # bfsiter finds the nodes reachable from the node under analysis (mode='OUT')
        # or that can reach the node under analysis (mode='IN')
        
        self.BFS_G=[nn.index for nn in igraph_network.bfsiter(self.SCC[0], mode='OUT')]
        self.OUT=[nn for nn in self.BFS_G if nn not in self.SCC]
        self.OUT.sort()
        self.membership[self.OUT]='OUT'
        #print('{:%H:%M:%S:%f}\tOUT found'.format(dt.datetime.now()))
        
        self.BFS_GT=[nn.index for nn in igraph_network.bfsiter(self.SCC[0], mode='IN')]
        self.IN=[nn for nn in self.BFS_GT if nn not in self.SCC]
        self.IN.sort()
        self.membership[self.IN]='IN'
        if self.verbose:
            print('{:%H:%M:%S:%f}\tIN'.format(dt.datetime.now()))
        
        
    def other_stuff(self, igraph_network):
        
        bow_tie_not_in_out_scc=[i for i in range(len(igraph_network.vs)) if (i not in self.OUT) and (i not in self.IN) and (i not in self.SCC)]
        
        self.TUBES=[]
        self.INTENDRILS=[]
        self.OUTTENDRILS=[]
        self.OTHERS=[]
        
        for i in bow_tie_not_in_out_scc:
            i_IRV=[v.index for v in igraph_network.bfsiter(igraph_network.vs[i], mode='IN') if v.index in self.IN]
            i_ORV=[v.index for v in igraph_network.bfsiter(igraph_network.vs[i], mode='OUT') if v.index in self.OUT]
            i_IRV_bool=len(i_IRV)>0
            i_ORV_bool=len(i_ORV)>0
            if i_IRV_bool and i_ORV_bool:
                self.TUBES.append(i)
            elif i_IRV_bool:
                self.INTENDRILS.append(i)
            elif i_ORV_bool:
                self.OUTTENDRILS.append(i)
            else:
                self.OTHERS.append(i)
        self.membership[self.TUBES]='TUBES'
        self.membership[self.INTENDRILS]='INTENDRILS'
        self.membership[self.OUTTENDRILS]='OUTTENDRILS'
        self.membership[self.OTHERS]='OTHERS'
        if self.verbose:
            print('{:%H:%M:%S:%f}\tOther stuff'.format(dt.datetime.now()))
        
