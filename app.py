from flask import Flask, render_template, request
import networkx as nx
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Friend Network
graph = {
    "Pratham": ["Rahul", "Priya"],
    "Rahul": ["Pratham", "Karan", "Aman"],
    "Priya": ["Pratham", "Sneha"],
    "Karan": ["Rahul"],
    "Aman": ["Rahul"],
    "Sneha": ["Priya"]
}

@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = {}

    if request.method == "POST":
        user = request.form["username"]

        if user in graph:

            highlight_edges = []

            # Find mutual friends
            for friend in graph[user]:
                for mutual in graph[friend]:

                    if mutual != user and mutual not in graph[user]:

                        recommendations[mutual] = friend

                        highlight_edges.append((user, friend))
                        highlight_edges.append((friend, mutual))

            # Create graph
            G = nx.Graph()

            for person in graph:
                for friend in graph[person]:
                    G.add_edge(person, friend)

            plt.figure(figsize=(10, 7))
            pos = nx.spring_layout(G, seed=42)

            # Draw nodes
            nx.draw_networkx_nodes(
                G,
                pos,
                node_color="lightblue",
                node_size=2500
            )

            # Draw labels
            nx.draw_networkx_labels(
                G,
                pos,
                font_size=10,
                font_weight="bold"
            )

            # Draw normal edges
            nx.draw_networkx_edges(
                G,
                pos,
                edge_color="gray"
            )

            # Highlight recommendation paths
            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=highlight_edges,
                edge_color="red",
                width=4
            )

            plt.title(
                f"Friend Recommendations for {user}\n(Red = Mutual Friend Path)"
            )

            plt.axis("off")

            # Ensure static folder exists
            os.makedirs("static", exist_ok=True)

            plt.savefig("static/graph.png")
            plt.close()

        else:
            recommendations["User Not Found"] = "Please enter a valid name."

    return render_template(
        "index.html",
        recommendations=recommendations
    )

if __name__ == "__main__":
    app.run(debug=True)