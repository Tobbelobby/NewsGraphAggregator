from rdflib import Graph, Namespace, URIRef, BNode, Literal
from rdflib.namespace import RDF, FOAF, XSD
from rdflib.collection import Collection
import owlrl

g = Graph()
g_parsd = g.parse(location="dataset36.ttl", format="turtle")
ex = Namespace("http://example.org/")

'''
rdfs = owlrl.RDFSClosure.RDFS_Semantics(g, False, False, False)
rdfs.closure()
rdfs.flush_stored_triples()
'''

g_parsd.add((ex.Magnus, ex.tried, ex.fuckywucky))
g_parsd.add((ex.Magnus, ex.age, Literal("21", datatype=XSD.integer)))

g_parsd.serialize("data2", format="turtle")