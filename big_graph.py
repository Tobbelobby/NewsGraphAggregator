from rdflib import Graph, XSD
import os
import time
import threading

knowledge_bank = 'knowledge_graph'

object_dict = {}
object_list = []
knowledge_path = []


#def graph_shredder():
for filename in os.listdir(knowledge_bank):
    graphs = os.path.join(knowledge_bank, filename)
    if os.path.isfile(graphs):
        knowledge_path.append(graphs)
    for path in knowledge_path:
        g = Graph()
        graph = g.parse(location=path, format="turtle")


        name = hash(filename)
        object_dict[name] = []
        for subject,predicate,object in graph:
            object_list.append(object[:])
        for num in object_list:
            object_dict[name].append(num)



'''    
    for x, y in object_dict.items():
        print(y)

def main():
    thread = threading.Thread(target=graph_shredder)
    thread.start()


if __name__ == '__main__':
    main()
'''

