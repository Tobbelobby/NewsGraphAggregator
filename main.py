#Gennerer nøkkler som er unike, lurt å bruker en hash function kanskje

from rdflib import Graph, XSD
#import threading
import time

g = Graph()
graph = g.parse(location="knowledge_graph/Test.ttl", format="turtle")

object_list = []

for subject,predicate,object in graph:
     object_list.append(object)


object_list.sort()
print(object_list[5])
print(object_list)


# for x in object_list:
#      print(x)








#print(graph.serialize(format='turtle').decode('utf-8'))


#Dette vil vi ha ut 'https://twitter.com/i/status/1310747766067527686,
# http://dbpedia.org/resource/Coronavirus, https://www.wikidata.org/entity/Q918




