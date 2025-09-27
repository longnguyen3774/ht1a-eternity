# ============ Import & setup =============
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
from operator import itemgetter

# ============ Bước 1: Load đồ thị =============
# Bạn cần có file đồ thị từ Project 1A, ví dụ lưu dưới dạng gpickle hoặc edge list
G = nx.read_graphml("graph_coursera.graphml")
print("Số giảng viên:", G.number_of_nodes())
print("Số mối quan hệ:", G.number_of_edges())

# Tính toán các chỉ số centrality
degree_cent = nx.degree_centrality(G)
betweenness_cent = nx.betweenness_centrality(G)
closeness_cent = nx.closeness_centrality(G)
pagerank_cent = nx.pagerank(G)

# Tìm top 3 node quan trọng nhất theo từng chỉ số
def get_top_nodes(centrality_dict, k=3):
    return sorted(centrality_dict.items(), key=lambda x: x[1], reverse=True)[:k]

print("\n=== PHÂN TÍCH KẾT QUẢ ===")
print("\nTop 3 Degree Centrality:")
for node, score in get_top_nodes(degree_cent):
    print(f"  Node {node}: {score:.3f}")

print("\nTop 3 Betweenness Centrality:")
for node, score in get_top_nodes(betweenness_cent):
    print(f"  Node {node}: {score:.3f}")

print("\nTop 3 Closeness Centrality:")
for node, score in get_top_nodes(closeness_cent):
    print(f"  Node {node}: {score:.3f}")

print("\nTop 3 PageRank:")
for node, score in get_top_nodes(pagerank_cent):
    print(f"  Node {node}: {score:.3f}")

# Vẽ 4 biểu đồ khác nhau theo 4 chỉ số
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('Coursera Teachers Network - Phân tích theo các chỉ số Centrality', fontsize=16)

# Tạo layout cố định để so sánh
pos = nx.spring_layout(G, seed=42, k=2.5)

# 1. Degree Centrality
ax1 = axes[0, 0]
node_colors = [degree_cent[node] for node in G.nodes()]
nx.draw(G, pos, ax=ax1, node_color=node_colors, cmap='Reds',
        node_size=100, with_labels=True, font_size=8)
ax1.set_title('Degree Centrality\n(Đỏ đậm = Nhiều kết nối)')

# 2. Betweenness Centrality
ax2 = axes[0, 1]
node_colors = [betweenness_cent[node] for node in G.nodes()]
nx.draw(G, pos, ax=ax2, node_color=node_colors, cmap='Blues',
        node_size=100, with_labels=True, font_size=8)
ax2.set_title('Betweenness Centrality\n(Xanh đậm = Cầu nối quan trọng)')

# 3. Closeness Centrality
ax3 = axes[1, 0]
node_colors = [closeness_cent[node] for node in G.nodes()]
nx.draw(G, pos, ax=ax3, node_color=node_colors, cmap='Greens',
        node_size=100, with_labels=True, font_size=8)
ax3.set_title('Closeness Centrality\n(Xanh lá đậm = Tiếp cận nhanh)')

# 4. PageRank
ax4 = axes[1, 1]
node_colors = [pagerank_cent[node] for node in G.nodes()]
nx.draw(G, pos, ax=ax4, node_color=node_colors, cmap='Purples',
        node_size=100, with_labels=True, font_size=8)
ax4.set_title('PageRank\n(Tím đậm = Ảnh hưởng cao)')

plt.tight_layout()
plt.show()

# Phân tích node quan trọng nhất
most_important_nodes = {
    'degree': max(degree_cent, key=degree_cent.get),
    'betweenness': max(betweenness_cent, key=betweenness_cent.get),
    'closeness': max(closeness_cent, key=closeness_cent.get),
    'pagerank': max(pagerank_cent, key=pagerank_cent.get)
}

print("\n=== NODE QUAN TRỌNG NHẤT THEO TỪNG CHỈ SỐ ===")
for metric, node in most_important_nodes.items():
    print(f"{metric.capitalize()}: Node {node}")

# Phân tích node 3152
key_nodes = ["3152"]
print(f"\n=== NODE QUAN TRỌNG: {key_nodes} ===")

for node in key_nodes:
    print(f"\nNode {node}:")
    print(f"  Degree Centrality: {degree_cent[node]:.3f}")
    print(f"  Betweenness Centrality: {betweenness_cent[node]:.3f}")
    print(f"  Closeness Centrality: {closeness_cent[node]:.3f}")
    print(f"  PageRank: {pagerank_cent[node]:.3f}")
    print(f"  Số bạn bè trực tiếp: {G.degree[node]}")