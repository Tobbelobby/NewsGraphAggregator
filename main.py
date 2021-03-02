# Todo : Make graph, make function to read graph, make function to merge small graphs to big

from rdflib import Graph, URIRef

g = Graph()
graph = g.parse(location="knowledge_graph/dataset36.ttl", format="turtle")

print(graph.serialize(format='turtle').decode('utf-8'))





