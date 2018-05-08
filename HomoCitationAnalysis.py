import numpy as np
import networkx as nx


class HomoCitationAnalysis:

    def __init__(self, network_path):
        self.network_path = network_path

    '''
    初始化引用链接遍历数
    需要注意的是同时保存了遍历数的倒数，便于将主路径查找转化为最小路径的查找
    '''
    def init_iter_num(self, network):
        for edge in network.edges():
            network[edge[0]][edge[1]]['iter_num_nppc'] = 0
            network[edge[0]][edge[1]]['iter_num_back_nppc'] = 999
            network[edge[0]][edge[1]]['iter_num_splc'] = 0
            network[edge[0]][edge[1]]['iter_num_back_splc'] = 999
            network[edge[0]][edge[1]]['iter_num_spnp'] = 0
            network[edge[0]][edge[1]]['iter_num_back_spnp'] = 999
            network[edge[0]][edge[1]]['iter_num_spc'] = 0
            network[edge[0]][edge[1]]['iter_num_back_spc'] = 999
        return network

    '''
    用于确定引文网络中的源点集合与终点集合
    确定源点集合与终点的规则如下：
    1、如果该节点只有出度没有入度，则该节点为源点集合
    2、如果该节点只有入度没有出度，则该节点为终点结合
    3、如果不满足上述两个条件的都为中间节点
    '''
    def find_source_and_terminus(self, network):
        in_degree = network.in_degree(weight=None)
        out_degree = network.out_degree(weight=None)
        source_list = []
        terminus_list = []
        for node in network.nodes():
            if out_degree[node] == 0:
                terminus_list.append(node)
            if in_degree[node] == 0:
                source_list.append(node)
        return source_list, terminus_list

    '''
    局部主路径（nppc,splc,spnp,spc）
    '''
    def local_main_path_analysis(self):
        academic_network = nx.read_gpickle(self.network_path)
        academic_network = self.init_iter_num(academic_network)
        source_list, terminus_list = self.find_source_and_terminus(academic_network)
        for s in source_list:
            for t in terminus_list:
                paths = list(nx.all_simple_paths(academic_network, s, t))
                if len(paths) == 0:
                    continue
                else:
                    for path in paths:
                        for i in range(len(path) - 1):
                            # spc
                            academic_network[path[i]][path[i+1]]['iter_num_spc'] = academic_network[path[i]][path[i+1]]['iter_num_spc'] + 1
                            academic_network[path[i]][path[i+1]]['iter_num_back_spc'] = 1.0 / academic_network[path[i]][path[i+1]]['iter_num_spc']
                            # nppc
                            academic_network[path[i]][path[i + 1]]['iter_num_nppc'] = academic_network[path[i]][path[i + 1]]['iter_num_nppc'] + len(path) - i - 1
                            academic_network[path[i]][path[i + 1]]['iter_num_back_nppc'] = 1.0 / academic_network[path[i]][path[i + 1]]['iter_num_nppc']
                            # splc
                            academic_network[path[i]][path[i + 1]]['iter_num_splc'] = academic_network[path[i]][path[i + 1]]['iter_num_splc'] + len(path) - 1
                            academic_network[path[i]][path[i + 1]]['iter_num_back_splc'] = 1.0 / academic_network[path[i]][path[i + 1]]['iter_num_splc']
                            # spnp
                            academic_network[path[i]][path[i + 1]]['iter_num_spnp'] = academic_network[path[i]][path[i + 1]]['iter_num_spnp'] + len(path) + i
                            academic_network[path[i]][path[i + 1]]['iter_num_back_spnp'] = 1.0 / academic_network[path[i]][path[i + 1]]['iter_num_spnp']
        spc_main_path = nx.shortest_path()
        nx.write_gpickle(nx.write_gpickle(academic_network, 'data/homo_academic_network_local.gpickle'))



hca = HomoCitationAnalysis('data/homo_academic_network.gpickle')
hca.NPPC()