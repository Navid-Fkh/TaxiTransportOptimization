from os import name
import plotly.offline as py
import plotly.graph_objects as go


def make_edge(x, y, text, width, color="cornflowerblue"):
    return go.Scatter(
        x=x,
        y=y,
        line=dict(width=width, color=color),
        hoverinfo="text",
        text=([text]),
        mode="lines",
        name=text
    )


def draw_graph(edges, nodes, pos, flowDict):
    edge_trace = []
    for edge in edges:
        char_1 = edge[0]
        char_2 = edge[1]

        x0, y0 = pos[char_1]
        x1, y1 = pos[char_2]

        flow = flowDict[char_1][char_2]
        if (char_1, char_2) == ("A_start", "A_end"):
            continue
        text = f"{char_1} -> {char_2}"
        if flow :
            trace = make_edge([x0, x1, None], [y0, y1, None], text, flow * 3, "orange")
        else:
            trace = make_edge([x0, x1, None], [y0, y1, None], text, 1)

        edge_trace.append(trace)

    # Make a node trace
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        textposition="top center",
        textfont_size=10,
        mode="markers+text",
        hoverinfo="none",
        marker=dict(color=[], size=[], line=None),
    )

    # For each node in G, get the position and size and add to the node_trace
    for node in nodes:
        x, y = pos[node]
        node_trace["x"] += tuple([x])
        node_trace["y"] += tuple([y])
        node_trace["marker"]["color"] += tuple(["cornflowerblue"])
        node_trace["marker"]["size"] += tuple([20])
        node_trace["text"] += tuple(["<b>" + node + "</b>"])

    # Customize layout
    layout = go.Layout(
        paper_bgcolor="rgba(0,0,0,0)",  # transparent background
        plot_bgcolor="rgba(0,0,0,0)",  # transparent 2nd background
        xaxis={"showgrid": False, "zeroline": False},  # no gridlines
        yaxis={"showgrid": False, "zeroline": False},  # no gridlines
    )

    # Create figure
    fig = go.Figure(layout=layout)
    # Add all edge traces
    for trace in edge_trace:
        fig.add_trace(trace)
    # Add node trace
    fig.add_trace(node_trace)
    # Remove legend
    fig.update_layout(showlegend=True)
    # Remove tick labels
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    return fig
