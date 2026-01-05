import osmnx as ox
import matplotlib.pyplot as plt
from math import atan, atan2, sin, cos, sqrt, tan, pi
from geopy.geocoders import Nominatim
from heapq import heappop, heappush
from math import radians, cos, sin, asin, sqrt

# Região geográfica. AVISO: Regiões grandes (cidades grandes ou estados) utilizam MUITA memória (40GB+) 
place_name = "Lages, Santa Catarina, Brasil"

# Endereços de destino
origin_address = "Tanque, Lages, Santa Catarina, Brasil"
destination_address = "Catedral Diocesana, Lages, Santa Catarina, Brasil"

# Dimensões e resolução das figuras. Figuras mais bonitas -> Maior consumo de memória
figsize=(128,128)
#figsize=(8,8)
dpi=2000
#dpi=200

# Flag para salvar as figuras. Deixe em True para salvá-las em disco
savefig = True

# Formato para salvar as figuras
fig_format = 'svg'

#Mapa from now on!

graph = ox.graph_from_place(place_name, network_type="drive")

fig, ax = ox.plot_graph(
    graph,
    bgcolor="black",
    node_color="white",
    node_edgecolor="white",
    edge_color="white",
    figsize=figsize,
    dpi=dpi,
    save=False,
    show=False,
    close=False,
)


fig.patch.set_facecolor("black")
ax.set_facecolor("black")

fig.tight_layout(pad=0)
ax.margins(0)

if savefig:
    filepath = "data/" + place_name + "." + fig_format
    fig.savefig(
        filepath,
        format=fig_format,
        facecolor="black",
        bbox_inches="tight",
        pad_inches=0,
    )


plt.close(fig)

geolocator = Nominatim(user_agent="TrabalhoCal")

print("Origem:")
origin_location = geolocator.geocode(origin_address)
print(origin_location.raw)
origin_point = (origin_location.latitude, origin_location.longitude)
print(origin_point)
print("\n")


print("Destino:")
destination_location = geolocator.geocode(destination_address)
print(destination_location.raw)
destination_point = (destination_location.latitude, destination_location.longitude)
print(destination_point)
print("\n")

origin_node = ox.nearest_nodes(graph, origin_point[1],origin_point[0])
destination_node = ox.nearest_nodes(graph, destination_point[1],destination_point[0])

print("Nós de destino e origem encontrados após geocoding: "+str(origin_node)+" -> "+str(destination_node))

def vincenty_inverse(p1, p2):
    #given 2 points find the ellipsoidal distance s
    #https://en.wikipedia.org/wiki/Vincenty%27s_formulae
    lat1, lon1 = p1
    lat2, lon2 = p2
    a=6378137.0
    f=1/298.257223563

    b = (1 - f) * a
    L = radians(lon2 - lon1)
    U1 = atan((1 - f) * tan(radians(lat1)))
    U2 = atan((1 - f) * tan(radians(lat2)))
    sinU1 = sin(U1)
    cosU1 = cos(U1)
    sinU2 = sin(U2)
    cosU2 = cos(U2)
    lamb = L

    for _ in range(100):
        sinλ = sin(lamb)
        cosλ = cos(lamb)
        sinσ = sqrt((cosU2*sinλ)**2 + (cosU1*sinU2 - sinU1*cosU2*cosλ)**2)
        if sinσ == 0:
            return 0  # coincident points
        cosσ = sinU1*sinU2 + cosU1*cosU2*cosλ
        σ = atan2(sinσ, cosσ)
        sinα = cosU1*cosU2*sinλ / sinσ
        cos2α = 1 - sinα*sinα
        if cos2α != 0:
            cos2σm = cosσ - 2*sinU1*sinU2/cos2α
        else:
            cos2σm = 0
        C = f/16*cos2α*(4+f*(4-3*cos2α))
        λ_prev = lamb
        lamb = L + (1 - C) * f * sinα * (
            σ + C*sinσ*(cos2σm + C*cosσ*(-1 + 2*cos2σm**2))
        )
        if abs(lamb - λ_prev) < 1e-12:
            break

    u2 = cos2α * (a*a - b*b) / (b*b)
    A = 1 + u2/16384*(4096 + u2*(-768 + u2*(320 - 175*u2)))
    B = u2/1024*(256 + u2*(-128 + u2*(74 - 47*u2)))
    Δσ = B*sinσ*(cos2σm + B/4*(cosσ*(-1 + 2*cos2σm**2) -
              B/6*cos2σm*(-3 + 4*sinσ*sinσ)*(-3 + 4*cos2σm*cos2σm)))

    s = b*A*(σ - Δσ)
    return s  # meters

def custom_heuristic(node1, node2):
    point1 = (graph.nodes[node1]["y"], graph.nodes[node1]["x"])
    point2 = (graph.nodes[node2]["y"], graph.nodes[node2]["x"])
    return vincenty_inverse(point1, point2)


def a_star_search(graph, start, goal):
    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float("inf") for node in graph.nodes}
    g_score[start] = 0
    f_score = {node: float("inf") for node in graph.nodes}
    f_score[start] = custom_heuristic(start, goal)

    while open_set:
        current = heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor in graph.neighbors(current):
            tentative_g_score = g_score[current] + graph[current][neighbor][0]["length"]
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + custom_heuristic(neighbor, goal)
                heappush(open_set, (f_score[neighbor], neighbor))

    return []


path = a_star_search(graph, origin_node, destination_node)

fig, ax = ox.plot_graph_route(
    graph,
    path,
    bgcolor="black",
    node_color="white",
    node_edgecolor="white",
    edge_color="white",
    figsize=figsize,
    dpi=dpi,
    save=False,
    show=False,
    close=False,
)


fig.patch.set_facecolor("black")
ax.set_facecolor("black")

fig.tight_layout(pad=0)
ax.margins(0)

if savefig:
    filepath = (
        "data/"
        + place_name
        + " "
        + origin_address
        + " "
        + destination_address
        + "."
        + fig_format
    )
    fig.savefig(
        filepath,
        format=fig_format,
        facecolor="black",
        bbox_inches="tight",
        pad_inches=0,
    )

plt.close(fig)