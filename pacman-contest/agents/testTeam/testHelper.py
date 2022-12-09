from helper import *

# used for testing helper.py file (functions, classes ...)


def test2():
    ''' Graph with structure (similr structure will be used)
            x - x
            |   |
            x - x
    '''
    values = [(1,4), (1,5), (2,4), (2,5)]
    nodes = [Node(value) for value in values]

    graph = Graph(values)
    graph.add_edge(values[0], values[1], 7)
    graph.add_edge(values[2], values[3])
    graph.add_edge(values[0], values[2])
    graph.add_edge(values[1], values[3])

    print("node1: " + str(nodes[0]))


    print(str(graph))



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
    #print(type(graph) == Graph)
    
def test4():
    l1 = [3,5]
    n1 = Node(l1)
    n2 = n1.get_copy()
    l1[0] = 7
    print(n1)
    print(n2)

def test5():
    values = [(i//3+1, i%3+1) for i in range(9)]
    #print(values)

    graph = Graph(values)
    for i in range(1,4):
        for j in range(1,4):
            if (i < 3):
                graph.add_edge((i,j), (i+1,j))
            if (j < 3):
                graph.add_edge((i,j), (i,j+1))
    #print(graph)

    print(graph.edges[(1,1)])
    #print(graph.edges)
    print("\n")
    graph2 = graph.get_subgraph([(1,1)])
    print(graph2)
    graph2.clean()
    print(graph2)

    print("\n")
    graph3 = expand_subgraph(graph, graph2)
    #graph3 = expand_subgraph(graph, expand_subgraph(graph, graph2))
    print(graph3)
    graph3.clean()
    print(graph3)

    #print(type(graph.get_nodes()) == list)

    '''graph4 = graph.get_subgraph([(1,1), (1,2), (2,2)])

    print(graph4)'''
            

def test6():
    layout = ["%%%%%%%%%%%%",
            "%        24%",
            "%      %%%%%",
            "%%%%%      %",
            "%13     o  %",
            "%%%%%%%%%%%%"]
    graph1 = generate_graph_from_layout(layout)
    print(graph1)

def test7():
    layout = ["%%%%%%%%%%%%",
            "%        24%",
            "%      %%%%%",
            "%%%%%      %",
            "%13     o  %",
            "%%%%%%%%%%%%"]

    graph = generate_graph_from_layout(layout)
    print(graph)

    print("\n")
    graph2 = graph.get_subgraph([(2,4), (2,5)])
    print(graph2)
    graph2.clean()
    print(graph2)

    print("\n")
    graph3 = expand_subgraph(graph, graph2)
    graph3.clean()
    print(graph3)
    graph3 = expand_subgraph(graph, graph3)
    graph3.clean()
    print(graph3)
    #visualize(layout, graph2)

def test8():
    layout = ["%%%%%%%%%%%%",
            "%        24%",
            "%      %%%%%",
            "%%%%%      %",
            "%13     o  %",
            "%%%%%%%%%%%%"]

    graph = generate_graph_from_layout(layout)
    #print()
    print(is_trap(graph, (2,1), (3,1)))     # bottom left to right -> not trap (actually in trap, but going away)
    #print()
    print(is_trap(graph, (3,1), (2,1)))     # botton left to left -> going deeper into trap


def test9():
    layout = ["%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
            "%   %. %.%.%       %     %.%.%4%",
            "% % %%       %%  %   %%%   %.%2%",
            "% % %. % %%%    %%%% .%..% % % %",
            "% % %% % ..% %   %   %%%%% % % %",
            "% %    %%%%% %%%   %%%.% o % % %",
            "% %% % ..%.  %.%%%       %   % %",
            "% %. %%.%%%%        %.%%%%  %% %",
            "% %%  %%%%.%        %%%%.%% .% %",
            "% %   %       %%%.%  .%.. % %% %",
            "% % % o %.%%%   %%% %%%%%    % %",
            "% % % %%%%%   %   % %.. % %% % %",
            "% % % %..%. %%%%    %%% % .% % %",
            "%1%.%   %%%   %  %%       %% % %",
            "%3%.%.%     %       %.%.% .%   %",
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"]
    graph = generate_graph_from_layout(layout)
    print(graph)
    previous_nodes, shortest_path = dijkstra_algorithm(graph, (1,1))
    for path in shortest_path:
        print(str(path) + ": " + str(shortest_path[path]))

def test10():
    layout = ["%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
            "%   %. %.%.%       %     %.%.%4%",
            "% % %%       %%  %   %%%   %.%2%",
            "% % %. % %%%    %%%% .%..% % % %",
            "% % %% % ..% %   %   %%%%% % % %",
            "% %    %%%%% %%%   %%%.% o % % %",
            "% %% % ..%.  %.%%%       %   % %",
            "% %. %%.%%%%        %.%%%%  %% %",
            "% %%  %%%%.%        %%%%.%% .% %",
            "% %   %       %%%.%  .%.. % %% %",
            "% % % o %.%%%   %%% %%%%%    % %",
            "% % % %%%%%   %   % %.. % %% % %",
            "% % % %..%. %%%%    %%% % .% % %",
            "%1%.%   %%%   %  %%       %% % %",
            "%3%.%.%     %       %.%.% .%   %",
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"]
    graph = generate_graph_from_layout(layout)
    print(get_bordering_fields(graph, layout, is_red=True, my_border=True))
    print(get_bordering_fields(graph, layout, True, False))
    print(get_bordering_fields(graph, layout, False, True))
    print(get_bordering_fields(graph, layout, False, False))

def test11():
    layout = ["%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%",
            "%   %. %.%.%       %     %.%.%4%",
            "% % %%       %%  %   %%%   %.%2%",
            "% % %. % %%%    %%%% .%..% % % %",
            "% % %% % ..% %   %   %%%%% % % %",
            "% %    %%%%% %%%   %%%.% o % % %",
            "% %% % ..%.  %.%%%       %   % %",
            "% %. %%.%%%%        %.%%%%  %% %",
            "% %%  %%%%.%        %%%%.%% .% %",
            "% %   %       %%%.%  .%.. % %% %",
            "% % % o %.%%%   %%% %%%%%    % %",
            "% % % %%%%%   %   % %.. % %% % %",
            "% % % %..%. %%%%    %%% % .% % %",
            "%1%.%   %%%   %  %%       %% % %",
            "%3%.%.%     %       %.%.% .%   %",
            "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"]
    graph = generate_graph_from_layout(layout)
    fields = get_bordering_fields(graph, layout, True, True)
    print(return_min_len_to_fields(graph, (1,1), fields))

test11()