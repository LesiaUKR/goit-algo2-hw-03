# import networkx as nx
# from colorama import Fore, Style
# from collections import defaultdict
# import matplotlib.pyplot as plt
#
#
# def build_logistics_graph():
#     """
#     Builds a directed graph representing the logistics network with given capacities.
#
#     Returns:
#         networkx.DiGraph: The logistics network graph.
#     """
#     G = nx.DiGraph()
#
#     # Додавання ребер до графа згідно з таблицею пропускних здатностей
#     edges = [
#         ("Terminal 1", "Warehouse 1", 25), ("Terminal 1", "Warehouse 2", 20),
#         ("Terminal 1", "Warehouse 3", 15),
#         ("Terminal 2", "Warehouse 3", 15), ("Terminal 2", "Warehouse 4", 30),
#         ("Terminal 2", "Warehouse 2", 10),
#         ("Warehouse 1", "Shop 1", 15), ("Warehouse 1", "Shop 2", 10),
#         ("Warehouse 1", "Shop 3", 20),
#         ("Warehouse 2", "Shop 4", 15), ("Warehouse 2", "Shop 5", 10),
#         ("Warehouse 2", "Shop 6", 25),
#         ("Warehouse 3", "Shop 7", 20), ("Warehouse 3", "Shop 8", 15),
#         ("Warehouse 3", "Shop 9", 10),
#         ("Warehouse 4", "Shop 10", 20), ("Warehouse 4", "Shop 11", 10),
#         ("Warehouse 4", "Shop 12", 15),
#         ("Warehouse 4", "Shop 13", 5), ("Warehouse 4", "Shop 14", 10)
#     ]
#
#     for u, v, capacity in edges:
#         G.add_edge(u, v, capacity=capacity)
#
#     return G
#
#
# def compute_max_flow(G, source, sink):
#     """
#     Computes the maximum flow in the logistics network using Edmonds-Karp algorithm.
#
#     Args:
#         G (networkx.DiGraph): The logistics network graph.
#         source (str): The source node.
#         sink (str): The sink node.
#
#     Returns:
#         tuple: Maximum flow value and the flow distribution.
#     """
#     return nx.maximum_flow(G, source, sink)
#
#
# def visualize_graph(G):
#     """
#     Visualizes the logistics network graph using matplotlib.
#
#     Args:
#         G (networkx.DiGraph): The logistics network graph.
#     """
#     pos = nx.spring_layout(G, seed=42)  # Позиціонування вузлів графа
#     labels = nx.get_edge_attributes(G, "capacity")  # Місткості на ребрах
#
#     # Створення візуалізації графа
#     plt.figure(figsize=(12, 8))
#     nx.draw(
#         G,
#         pos,
#         with_labels=True,
#         node_size=3000,
#         node_color="lightblue",
#         edge_color="gray",
#         font_size=10,
#     )
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
#
#     plt.title("Граф логістичної мережі")
#     plt.show()
#
#
# # Побудова графа логістичної мережі
# graph = build_logistics_graph()
#
# # Додавання "суперджерела" та "суперстоку" для обчислення максимального потоку
# graph.add_node("Super Source")
# graph.add_node("Super Sink")
#
# # З'єднання "суперджерела" з терміналами
# for terminal in ["Terminal 1", "Terminal 2"]:
#     graph.add_edge("Super Source", terminal, capacity=float("inf"))
#
# # З'єднання магазинів з "суперстоком"
# for shop in [f"Shop {i}" for i in range(1, 15)]:
#     graph.add_edge(shop, "Super Sink", capacity=float("inf"))
#
# # Обчислення максимального потоку
# max_flow_value, flow_distribution = compute_max_flow(graph, "Super Source", "Super Sink")
#
# # Вивід максимального потоку
# print(Fore.GREEN + "Maximum flow in the logistics network: " + Fore.YELLOW + str(max_flow_value) + Style.RESET_ALL)
#
# # Формування таблиці фактичних потоків
# print(Fore.CYAN + "\nFlow distribution from terminals to shops:" + Style.RESET_ALL)
#
# # Створюємо словник для зберігання потоків від терміналів до магазинів
# terminal_to_shop_flows = defaultdict(lambda: defaultdict(int))
#
# # Проходимо через всі вузли та їх потоки
# for u, v_dict in flow_distribution.items():
#     for v, flow in v_dict.items():
#         if flow > 0:
#             # Якщо потік йде від терміналу до складу
#             if u.startswith("Terminal") and v.startswith("Warehouse"):
#                 # Знаходимо всі магазини, які отримують товари з цього складу
#                 for shop, shop_flow in flow_distribution[v].items():
#                     if shop.startswith("Shop"):
#                         terminal_to_shop_flows[u][shop] += min(flow, shop_flow)
#             # Якщо потік йде безпосередньо від терміналу до магазину (якщо такі є)
#             elif u.startswith("Terminal") and v.startswith("Shop"):
#                 terminal_to_shop_flows[u][v] += flow
#
# # Виводимо потоки від терміналів до магазинів
# for terminal, shops in terminal_to_shop_flows.items():
#     for shop, flow in shops.items():
#         print(Fore.MAGENTA + f"{terminal} -> {shop}: " + Fore.YELLOW + str(flow) + Style.RESET_ALL)
#
# # Аналіз результатів
# print(Fore.BLUE + "\nDetailed Analysis:" + Style.RESET_ALL)
#
# # 1. Які термінали забезпечують найбільший потік?
# terminal_flows = {}
# for terminal in ["Terminal 1", "Terminal 2"]:
#     terminal_flows[terminal] = sum(flow_distribution[terminal].values())
# max_terminal = max(terminal_flows, key=terminal_flows.get)
# print(Fore.WHITE + f"1. The terminal providing the highest flow is {max_terminal} with {terminal_flows[max_terminal]} units." + Style.RESET_ALL)
#
# # 2. Які маршрути мають найменшу пропускну здатність?
# min_capacity = float('inf')
# weakest_route = None
# for u, v, data in graph.edges(data=True):
#     if data['capacity'] < min_capacity and data['capacity'] != float('inf'):
#         min_capacity = data['capacity']
#         weakest_route = (u, v)
# print(Fore.WHITE + f"2. The weakest route is {weakest_route} with a capacity of {min_capacity} units." + Style.RESET_ALL)
#
# # 3. Які магазини отримали найменше товарів?
# shop_flows = {}
# for shop in [f"Shop {i}" for i in range(1, 15)]:
#     shop_flows[shop] = sum(flow_distribution[u].get(shop, 0) for u in flow_distribution if u.startswith("Terminal"))
# min_shop = min(shop_flows, key=shop_flows.get)
# print(Fore.WHITE + f"3. The shop receiving the least goods is {min_shop} with {shop_flows[min_shop]} units." + Style.RESET_ALL)
#
# # 4. Чи є вузькі місця, які можна усунути?
# print(Fore.WHITE + "4. Bottlenecks can be removed by increasing the capacity of the following routes:" + Style.RESET_ALL)
# for u, v, data in graph.edges(data=True):
#     if data['capacity'] == min_capacity:
#         print(Fore.WHITE + f"   - {u} -> {v} (current capacity: {data['capacity']})" + Style.RESET_ALL)
#
# # Візуалізація графа
# visualize_graph(graph)

import networkx as nx
from colorama import Fore, Style
from collections import defaultdict
import matplotlib.pyplot as plt


def build_logistics_graph():
    """
    Builds a directed graph representing the logistics network with given capacities.

    Returns:
        networkx.DiGraph: The logistics network graph.
    """
    G = nx.DiGraph()

    # Додавання ребер до графа згідно з таблицею пропускних здатностей
    edges = [
        ("Terminal 1", "Warehouse 1", 25), ("Terminal 1", "Warehouse 2", 20),
        ("Terminal 1", "Warehouse 3", 15),
        ("Terminal 2", "Warehouse 3", 15), ("Terminal 2", "Warehouse 4", 30),
        ("Terminal 2", "Warehouse 2", 10),
        ("Warehouse 1", "Shop 1", 15), ("Warehouse 1", "Shop 2", 10),
        ("Warehouse 1", "Shop 3", 20),
        ("Warehouse 2", "Shop 4", 15), ("Warehouse 2", "Shop 5", 10),
        ("Warehouse 2", "Shop 6", 25),
        ("Warehouse 3", "Shop 7", 20), ("Warehouse 3", "Shop 8", 15),
        ("Warehouse 3", "Shop 9", 10),
        ("Warehouse 4", "Shop 10", 20), ("Warehouse 4", "Shop 11", 10),
        ("Warehouse 4", "Shop 12", 15),
        ("Warehouse 4", "Shop 13", 5), ("Warehouse 4", "Shop 14", 10)
    ]

    for u, v, capacity in edges:
        G.add_edge(u, v, capacity=capacity)

    return G


def compute_max_flow(G, source, sink):
    """
    Computes the maximum flow in the logistics network using Edmonds-Karp algorithm.

    Args:
        G (networkx.DiGraph): The logistics network graph.
        source (str): The source node.
        sink (str): The sink node.

    Returns:
        tuple: Maximum flow value and the flow distribution.
    """
    return nx.maximum_flow(G, source, sink)


def visualize_graph(G):
    """
    Visualizes the logistics network graph using matplotlib.

    Args:
        G (networkx.DiGraph): The logistics network graph.
    """
    pos = nx.spring_layout(G, seed=42)  # Позиціонування вузлів графа
    labels = nx.get_edge_attributes(G, "capacity")  # Місткості на ребрах

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue",
            edge_color="gray", font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title("Граф логістичної мережі")
    plt.show()


# Побудова графа логістичної мережі
graph = build_logistics_graph()

# Додавання "суперджерела" та "суперстоку" для обчислення максимального потоку
graph.add_node("Super Source")
graph.add_node("Super Sink")

for terminal in ["Terminal 1", "Terminal 2"]:
    graph.add_edge("Super Source", terminal, capacity=float("inf"))

for shop in [f"Shop {i}" for i in range(1, 15)]:
    graph.add_edge(shop, "Super Sink", capacity=float("inf"))

# Обчислення максимального потоку
max_flow_value, flow_distribution = compute_max_flow(graph, "Super Source",
                                                     "Super Sink")

# Вивід максимального потоку
print(
    Fore.GREEN + "Maximum flow in the logistics network: " + Fore.YELLOW + str(
        max_flow_value) + Style.RESET_ALL)

# Формування таблиці фактичних потоків
print(
    Fore.CYAN + "\nFlow distribution from terminals to shops:" + Style.RESET_ALL)

# Коректне визначення потоку від терміналів до магазинів
terminal_to_shop_flows = defaultdict(int)

for terminal in ["Terminal 1", "Terminal 2"]:
    for warehouse in flow_distribution[terminal]:
        terminal_to_warehouse_flow = flow_distribution[terminal][warehouse]
        for shop in flow_distribution[warehouse]:
            shop_flow = flow_distribution[warehouse][shop]
            terminal_to_shop_flows[(terminal, shop)] += min(
                terminal_to_warehouse_flow, shop_flow)

for (terminal, shop), flow in terminal_to_shop_flows.items():
    print(Fore.MAGENTA + f"{terminal} -> {shop}: " + Fore.YELLOW + str(
        flow) + Style.RESET_ALL)

# Візуалізація графа
visualize_graph(graph)

print(
    """
1. Які термінали забезпечують найбільший потік товарів до магазинів?
Terminal 1 забезпечує найбільший потік товарів до магазинів.

2. Які маршрути мають найменшу пропускну здатність і як це впливає на загальний 
потік?
Найменшу пропускну здатність має маршрут Warehouse 4 -> Shop 13, що обмежує 
загальний потік.

3. Які магазини отримали найменше товарів і чи можна збільшити їх постачання, 
збільшивши пропускну здатність певних маршрутів?
Магазини Shop 3, Shop 9, Shop 12, Shop 13 та Shop 14 отримали найменше товарів, 
але їх постачання можна збільшити, збільшивши пропускну здатність певних 
маршрутів.

4.  Чи є вузькі місця, які можна усунути для покращення ефективності 
логістичної мережі?
Вузькі місця, такі як Warehouse 4 -> Shop 13, можна усунути, збільшивши 
пропускну здатність або додавши нові маршрути.

Ці заходи дозволять покращити ефективність логістичної мережі та забезпечити 
рівномірне постачання товарів до всіх магазинів.
    """
)