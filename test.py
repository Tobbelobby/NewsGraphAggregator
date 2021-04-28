from rdflib import Graph, XSD
import os
import threading
import time

knowledge_bank = 'knowledge_graph'

object_dict = {}
object_list = []
knowledge_path = []
fil_list = []

def the_banker():
    global filename
    for filename in os.listdir(knowledge_bank):
        graphs = os.path.join(knowledge_bank, filename)
        if os.path.isfile(graphs):
            knowledge_path.append(graphs)
            the_handler()



def the_handler():
    global g
    if len(knowledge_path) > 0:
        g = knowledge_path[-1]
        g = Graph()
        g.parse(location=knowledge_path[-1], format="turtle")
        graph_shredder()


def graph_shredder():
    global g
    if len(knowledge_path) > 0:
        object_dict[knowledge_path[-1]] = []
        for subject, predicate, object in g:
            object_list.append(object[:])
        for num in object_list:
            object_dict[knowledge_path[-1]].append(num)
        knowledge_path.pop(-1)
        the_handler()

def main():
    if len(object_dict) == 0:
        the_banker()
    if len(knowledge_path) == 0:
        print('All graph are reddy for proses ')
        print(object_dict.keys())



if __name__ == "__main__":
    main()
