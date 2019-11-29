import networkx as nx

from sql import SqlHandler


def get_lineups(sql_handler):
    sql_handler.connect()
    data = sql_handler.query('''
    select * from nba.lineups 
    where season_id_custom in ('2018-19', '2017-18', '2016-17', '2015-16', '2014-15', '2013-14')
    #where team_abbreviation = 'WAS'
    and gp > 40
    ''')
    sql_handler.close()
    return data


def get_players(sql_handler):
    sql_handler.connect()
    data = sql_handler.query('select * from nba.players')
    return data


def get_name_from_id(id, player_data):
    for row in player_data:
        if id == str(row['id']):
            return row['full_name']


def generate_edges_nodes(player_id_list, player_data):
    edges = []
    nodes = []
    for player_id in player_id_list:
        nodes.append(get_name_from_id(player_id, player_data))
        teammate_ids = [teammate_id for teammate_id in player_id_list if player_id != teammate_id]
        for teammate_id in teammate_ids:
            edges.append((player_id, teammate_id))
    return edges, nodes

def generate_network(player_data, lineup_data):
    G = nx.Graph()
    for row in lineup_data:
        player_ids = [player_id for player_id in row['GROUP_ID'].split('-') if player_id]
        player_names = [get_name_from_id(player_id, player_data) for player_id in player_ids]
        edges, nodes = generate_edges_nodes(player_names, player_data)
        G.add_edges_from(edges)
        G.add_nodes_from(nodes)
    return G


def get_graph():
    sql = SqlHandler()
    lineup_data = get_lineups(sql)
    player_data = get_players(sql)
    G = generate_network(player_data, lineup_data)
    G.remove_node(None)
    return(G)