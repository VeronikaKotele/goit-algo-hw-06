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

    fig = go.Figure()

    # Add nodes as scatter points on the map
    fig.add_trace(go.Scattermapbox(
        lat=lats,
        lon=lons,
        mode="markers",
        marker=dict(size=sizes),
        text=labels,
        hoverinfo="text"
    ))

    fig = add_edges_to_figure(G, fig)

    # Base map settings
    fig.update_layout(
        mapbox_style="open-street-map",   # No token needed
        mapbox_zoom=1.5,                  # World-level zoom
        mapbox_center={"lat": 20, "lon": 0},
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig

def add_edges_to_figure(G, fig, weight_attribute="weight"):
    for u, v, attrs in G.edges(data=True):
        lat_u = G.nodes[u]["lat"]
        lon_u = G.nodes[u]["lon"]
        lat_v = G.nodes[v]["lat"]
        lon_v = G.nodes[v]["lon"]

        weight = attrs.get(weight_attribute, 1)

        # Normalize weight for display
        min_width, max_width = 1, 8
        width = min_width + (weight - 1) / 10 * (max_width - min_width)
        width = min(max(width, min_width), max_width)

        fig.add_trace(go.Scattermapbox(
            lat=[lat_u, lat_v],
            lon=[lon_u, lon_v],
            mode="lines",
            line=dict(width=width),
            hoverinfo="none"
        ))

    return fig

