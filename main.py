# Todo : Make graph, make function to read graph, make function to merge small graphs to big

from rdflib import Graph, XSD
import os
import threading
import time

knowledge_bank = 'knowledge_graph'

object_dict = {}
object_list = []
knowledge_path = []


def banker():
     global filename, graph
     for filename in os.listdir(knowledge_bank):
          graphs = os.path.join(knowledge_bank, filename)
          if os.path.isfile(graphs):
               knowledge_path.append(graphs)
          for path in knowledge_path:
               g = Graph()
               graph = g.parse(location=path, format="turtle")

def graph_shreddar():
     banker()
     name = hash(filename)
     object_dict[name] = []
     for subject,predicate,object in graph:
          # time.sleep(0.35)
          object_list.append(object[:])
     for num in object_list:
          object_dict[name].append(num)
     print(object_dict)


graph_shreddar()

# def main():
#      thread = threading.Thread(target = graph_shredder())
#      thread.start()
#      thread.join()
#
#      for x, y in object_dict.items():
#           print(x,y)
#
# if name == 'main':
#      main()
#

     # object_list.append(object)



# object_list.sort()
# print(object_list[5])
# print(object_list)


# for x in object_list:
#      print(x)



#print(graph.serialize(format='turtle').decode('utf-8'))


#Dette vil vi ha ut 'https://twitter.com/i/status/1310747766067527686,
# http://dbpedia.org/resource/Coronavirus, https://www.wikidata.org/entity/Q918



