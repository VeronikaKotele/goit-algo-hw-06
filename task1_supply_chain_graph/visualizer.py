import plotly.graph_objects as go

def plot_graph_nodes(G):
    lats = []
    lons = []
    labels = []
    sizes = []

    for node_id, attrs in G.nodes(data=True):
        lats.append(attrs["lat"])
        lons.append(attrs["lon"])
        labels.append(attrs.get("name", node_id))
        sizes.append(attrs.get("size", 10))

    fig = go.Figure()

    # Add nodes as scatter points on the map
    fig.add_trace(go.Scattermapbox(
        lat=lats,
        lon=lons,
        mode="markers",
        marker=dict(size=sizes),
        text=labels,
        hoverinfo="text",
    ))

    for u, v, attrs in G.edges(data=True):
        weight = attrs.get("weight", 1)
        lat_u = G.nodes[u]["lat"]
        lon_u = G.nodes[u]["lon"]
        lat_v = G.nodes[v]["lat"]
        lon_v = G.nodes[v]["lon"]
        fig.add_trace(go.Scattermapbox(
            lat=[lat_u, lat_v],
            lon=[lon_u, lon_v],
            mode="lines",
            line=dict(width=weight),
            hoverinfo="none"
        ))

    # Base map settings
    fig.update_layout(
        mapbox_style="open-street-map",   # No token needed
        mapbox_zoom=1.5,                  # World-level zoom
        mapbox_center={"lat": 20, "lon": 0},
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig

def highlight_path(G, fig, path):
    # Iterate through consecutive node pairs in path
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]

        lat_u = G.nodes[u]["lat"]
        lon_u = G.nodes[u]["lon"]
        lat_v = G.nodes[v]["lat"]
        lon_v = G.nodes[v]["lon"]

        fig.update_traces(go.Scattermapbox(
            lat=[lat_u, lat_v],
            lon=[lon_u, lon_v],
            mode="lines",
            line=dict(width=6, color="red"),  # Highlighting
            hoverinfo="none"
        ))

    return fig
