import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_node("A", color='red')
G.add_nodes_from(["B", "C", "D"])
G.add_edge("A", "B", weight=2.5, label="connection")
G.add_edges_from([("A", "C"), ("B", "C"), ("B", "D")])
G.nodes["B"]["color"] = "red" # don't work
G.edges["B", "C"]["label"] = "bridge"
print(list(G.neighbors("A")))  # ['B', 'C']
options = {
    "node_color": "yellow",
    "edge_color": "lightblue",
    "node_size": 500,
    "width": 3,
    "with_labels": True,
    "arrowstyle": "-|>",
    "arrowsize": 20,
}
nx.draw(G, **options)
labels = nx.get_edge_attributes(G,'label')
pos=nx.spring_layout(G) # or circular_layout, shell_layout, random_layout
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
nx.apply_matplotlib_colors(G, "color", "node")
plt.show()
#plt.savefig(<wherever>)


degree_centrality = nx.degree_centrality(G)  # {'A': 0.6666666666666666, 'B': 1.0, 'C': 0.6666666666666666, 'D': 0.3333333333333333}
closeness_centrality = nx.closeness_centrality(G)  # {'A': 0.75, 'B': 1.0, 'C': 0.75, 'D': 0.6}
betweenness_centrality = nx.betweenness_centrality(G)  # {'A': 0.0, 'B': 0.6666666666666666, 'C': 0.0, 'D': 0.0}

# Ступінь центральності (Degree Centrality) визначається як кількість з'єднань, які має вузол. Чим більше з'єднань має вузол, тим більш центральним він є. У ненаправлених графах це просто кількість сусідів вузла. У направлених графах можна розглядати вхідний і вихідний ступені окремо. У нашому випадку результат — {'A': 0.6666666666666666, 'B': 1.0, 'C': 0.6666666666666666, 'D': 0.3333333333333333}
# Близькість вузла (Closeness Centrality) визначається як обернене значення середньої відстані від вузла до всіх інших вузлів у графі. Вузли, які знаходяться ближче до інших вузлів, мають вищу центральність близькості. Для нашого графа — {'A': 0.75, 'B': 1.0, 'C': 0.75, 'D': 0.6}
# Посередництво вузла (Betweenness Centrality) визначається як кількість найкоротших шляхів між усіма парами вузлів, які проходять через даний вузол. Ця метрика відображає, наскільки вузол є "мостом" між іншими вузлами у графі. У нашому випадку це вузол B, що і підтверджує результат — {'A': 0.0, 'B': 0.6666666666666666, 'C': 0.0, 'D': 0.0}
# Ви також можете знайти найкоротший шлях між двома вузлами або розрахувати середню довжину шляху у графі.

path = nx.shortest_path(G, source="A", target="D")  # ['A', 'B', 'D']
avg_path_length = nx.average_shortest_path_length(G)  # 1.3333333333333333

#Функція nx.average_shortest_path_length працює таким чином:
# 1. Для кожної пари вузлів у графі вона знаходить найкоротший шлях між ними.
# 2. Сумує довжини всіх цих найкоротших шляхів.
# 3. Ділить суму на кількість всіх можливих пар вузлів (не враховуючи пари, що складаються з одного й того самого вузла).