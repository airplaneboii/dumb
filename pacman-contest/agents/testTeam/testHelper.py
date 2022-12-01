from helper import *

# used for testing helper.py file (functions, classes ...)

def test1():
    node1 = Node((3,3))
    node2 = Node((5, 56, 'a'))
    #print(node1.value)
    node1.add_neighbor(node2)
    node2.add_neighbor(node1)
    print(str(node1))
    print(str(node2))


def test2():
    ''' Graph with structure (similr structure will be used)
            x - x
            |   |
            x - x
    '''
    node1 = Node((1,4))
    #print("node1:" + str(node1))
    node2 = Node((1,5))
    node3 = Node((2,4))
    node4 = Node((2,5))

    graph = Graph([node1, node2, node3, node4])
    graph.add_edge((1,4), (1,5), 7)
    graph.add_edge((2,4), (2,5))
    graph.add_edge((1,4), (2,4))
    graph.add_edge((1,5), (2,5))

    print("node1: " + str(node1))
    print("node2: " + str(node2))
    print("node3: " + str(node3))
    print("node4: " + str(node4))

    print(str(graph))

    '''
    (1, 4):  [(1, 5),7] ->  [(2, 4),1] -> None
    (1, 5):  [(1, 4),1] ->  [(2, 5),1] -> None
    (2, 4):  [(2, 5),1] ->  [(1, 4),1] -> None
    (2, 5):  [(2, 4),1] ->  [(1, 5),1] -> None
    '''


# will be used ...
'''%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   %. %.%.%       %     %.%.%4%
% % %%       %%  %   %%%   %.%2%
% % %. % %%%    %%%% .%..% % % %
% % %% % ..% %   %   %%%%% % % %
% %    %%%%% %%%   %%%.% o % % %
% %% % ..%.  %.%%%       %   % %
% %. %%.%%%%        %.%%%%  %% %
% %%  %%%%.%        %%%%.%% .% %
% %   %       %%%.%  .%.. % %% %
% % % o %.%%%   %%% %%%%%    % %
% % % %%%%%   %   % %.. % %% % %
% % % %..%. %%%%    %%% % .% % %
%1%.%   %%%   %  %%       %% % %
%3%.%.%     %       %.%.% .%   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%'''

def test3():
    layout = ["%%%%%%%%%%%%",
            "%        24%",
            "%      %%%%%",
            "%%%%%      %",
            "%13     o  %",
            "%%%%%%%%%%%%"]
    graph = generate_graph_from_layout(layout)
    print(graph)

    print(graph.get_nodes()[3])

test3()