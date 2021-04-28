import os
import sys
import uuid
import spacy
import time
from rdflib import Graph
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# Setting the recursion limit for lager files
sys.setrecursionlimit(5000)

# Models for processing. Here we are using the large model from spacy. If you will like a faster model use en_core_web_sm.
# If you want to use the smaller model the accuracy will be reduced.
nlp = spacy.load('en_core_web_lg')

# We use Sklearn model TfidfVectorizer to give a score on the text element in the graph as well as the spacy model.
# We found out that by combining models we can classify the graph more accurately.
# We are also using the punk
vectorization = TfidfVectorizer(stop_words='english')
# knowledge_directory is currently sett to knowledge_graph. This can be edited without effecting the code.
knowledge_directory = 'knowledge_graph'

corpus_dict = {}
object_dict = {}
text = []
object_list = []
knowledge_path = []
temp_sim_graph = []


# The function will get all the paths to all files from the path to knowledge_graph, and remove empty files.
# knowledge_directory is currently sett to knowledge_graph. This can be edited without effecting the code.
def file_handler():
    for filename in os.listdir(knowledge_directory):
        graphs = os.path.join(knowledge_directory, filename)
        filesize = os.path.getsize(graphs)
        # Removing empty files
        if filesize == 2:
            pass
        elif os.path.isfile(graphs):
            knowledge_path.append(graphs)
            graph_maker()


def graph_maker():
    global g
    if len(knowledge_path) > 0:
        g = knowledge_path[-1]
        g = Graph()
        g.parse(location=knowledge_path[-1], format="turtle")
        graph_shredder()


# Parsing all element of the graph, and filtering out what we do not want.
# The elements is added to a hash table for fast accessibility.
def graph_shredder():
    global g
    if len(knowledge_path) > 0:
        object_dict[knowledge_path[-1]] = []
        for subject, predicate, object in g:
            if format(predicate) == "https://newshunter.uib.no/term#originalText":
                text.append(object[:])
                continue
            object_list.append(object[:])
            object_list.sort()
        for element in object_list:
            if element.startswith('ub') or element.startswith('https://newshunter'):
                continue
            else:
                object_dict[knowledge_path[-1]].append(element)
        for str_element in text:
            corpus_dict.update({knowledge_path[-1]: str_element})
        knowledge_path.pop(-1)
        object_list.clear()
        graph_maker()


# Checking if all graphs is ready for processing.
def checker():
    global element_count
    if len(object_dict) == 0:
        file_handler()
    if len(knowledge_path) == 0:
        element_count = len(object_dict.keys())
        print(f'All graph are reddy for processing. We have a total of {len(object_dict.keys())} graph')
        divider()


# Retrieving all keys from the two hash tables, this make it easier to compare the element without changing the hash tables.
def divider():
    global elementToCompare, elementToCompare2, textElementToCompare, textElementToCompare2
    elementToCompare = []
    elementToCompare2 = []

    for keys, value in object_dict.items():
        elementToCompare2.append(keys)

    elementToCompare.append(elementToCompare2.pop(0))

    textElementToCompare = []
    textElementToCompare2 = []

    for keys, value in corpus_dict.items():
        textElementToCompare2.append(keys)

    textElementToCompare.append(textElementToCompare2.pop(0))

    processing_model()


# This is the main function it checks all combination against the models.
def processing_model():
    for x in elementToCompare:
        for y in elementToCompare2:
            entity = object_dict.get(x)
            entity2 = object_dict.get(y)
            spacer = ' '.join(entity)
            spacer2 = ' '.join(entity2)
            elementToCompare.pop(0)
            elementToCompare.append(elementToCompare2[0])
            graph = nlp(spacer)
            graph2 = nlp(spacer2)
            entity_similarity = graph.similarity(graph2)
            if entity_similarity >= 0.75:
                text_element = corpus_dict.get(x)
                text_element2 = corpus_dict.get(y)
                textElementToCompare.pop(0)
                textElementToCompare.append(textElementToCompare2[0])
                corpus = nlp(text_element)
                corpus2 = nlp(text_element2)
                text_similarity = corpus.similarity(corpus2)
                if text_similarity >= 0.78:
                    tfidf = vectorization.fit_transform([text_element, text_element2])
                    tfidf_similarity = (tfidf * tfidf.T)[0, 1]
                    if tfidf_similarity >= 0.18:
                        print(f'The graph that are being compared {x, y}')
                        print(
                            f'{corpus}\n{corpus2}\nEntity score: {entity_similarity}'
                            f' Text spacy score: {text_similarity} Tf-idf model score:{tfidf_similarity}')
                        temp_sim_graph.extend([(x, y)])
        if len(elementToCompare2) == 0:
            tuple_joiner()
            end_print()
            break
        else:
            print(f'There are {len(elementToCompare2)} element left')
            elementToCompare2.pop(0)
            tuple_joiner()
            processing_model()


def end_print():
    num_of_graph = (len([item for item in os.listdir('./MergingGraph') if
                         os.path.isfile(os.path.join('./MergingGraph', item))]))
    print(f"The total amount of files processed: {element_count}")
    print('Total new graph:', num_of_graph, 'and can now be found in the MergingGraph folder')


# Joining tuples whit the correspondent path. This function was inspired by:
# https://www.geeksforgeeks.org/python-join-tuples-if-similar-initial-element/
def tuple_joiner():
    global similar_graph
    similar_graph = []
    for element in temp_sim_graph:
        if similar_graph and similar_graph[-1][0] == element[0]:
            similar_graph[-1].extend(element[1:])
        else:
            similar_graph.append([item for item in element])
    similar_graph = list(map(tuple, similar_graph))
    temp_sim_graph.clear()
    for num in range(len(similar_graph)):
        graph_creator(similar_graph[num])


# Storing the new graph with the current time and date, and a random name.
def graph_merging(var):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S").replace(" ", "-")
    g = Graph()
    for new in var:
        g += new
        name_random = str(uuid.uuid4())
    g.serialize(f'./MergingGraph/{current_time}-{name_random}.ttl', format='turtle')


# We cant know how manny graph that are matched, so by doing it this way we can creat dynamic variables/graph.
def graph_creator(*args):
    global location
    location = []
    for path in args:
        for loc in path:
            g = Graph()
            g.parse(location=loc, format="turtle")
            location.append(g)
        graph_merging(location)


element = (len([item for item in os.listdir(knowledge_directory) if
                os.path.isfile(os.path.join(knowledge_directory, item))]))

# http://thepythoncorner.com/dev/how-to-create-a-watchdog-in-python-to-look-for-filesystem-changes/
# https://pypi.org/project/watchdog/
# To monitor the folder we use watchdog, in the link above you can find the inspiration for this code lines.
if __name__ == "__main__":
    monitor_handler = PatternMatchingEventHandler(patterns='*', ignore_patterns='',
                                                  ignore_directories=False, case_sensitive=True)


def file_added(event):
    global element
    print('This file has been added', event.src_path)
    element = (len([item for item in os.listdir(knowledge_directory) if
                    os.path.isfile(os.path.join(knowledge_directory, item))]))
    print(len([item for item in os.listdir(knowledge_directory) if
               os.path.isfile(os.path.join(knowledge_directory, item))]))
    return element


def news_dog(lim, my_wacther=None):
    monitor_handler.on_created = file_added

    my_watcher = Observer()
    my_watcher.schedule(monitor_handler, knowledge_directory, recursive=True)

    my_watcher.start()

    try:
        while True:
            time.sleep(1)
            if lim <= element:
                checker()
                break
    except KeyboardInterrupt:
        my_wacther.stop()
        my_wacther.join()


def terminal_menu():
    global user_input
    print('-' * 10, 'Welcome to NEWS SQUIRREL', '-' * 76)
    print(f"The purpose of this program is the parse smaller knowledge graph, and merging them in to bigger graph's. \n"
          'The program reads form the (knowledge_graph) directory, and will parse the new and bigger graph to the folder(MergingGraph) \n'
          'For every iteration, the new graph will be stored. Please make sure that (Merging Graph) is empty. This is to ensure that the end feedback is correct\n'
          'WARNING: The recursion limit is currently sett to 5000, the recursion depth is proportional to the amount of files in your folder. \n\n'
          '- If this is a problem you will have to change it manually in the code - \n '
          '- The format for the files, is currently sett to turtle(.ttl). - \n\n'
          'The program has currently 2 features. \n \n'
          '(1. Monitor folder) - By selecting this feature the program will start monitor the amount of files in the knowledge_graph folder.\n'
          'You can then specify the amount of files the program, should start at.\n'
          '(2. Start now) - By selecting this feature the program will start immediately.\n'
          )
    print('-' * 50, 'Menu', '-' * 50)
    print(
        f'The current size of the folder is: {element} elements. If there are some empty files, they will be removed.\n')
    print('1. Monitor folder')
    print('2. Start now')
    print('3. Exit')
    while True:
        try:
            user_input = int(input('Enter her (1-3): '))
            if user_input == 1:
                while True:
                    try:
                        size_input = input('Enter the folder size you wont to start at or press ENTER to return: ')
                        if size_input == '':
                            print('Returning to main menu...')
                            time.sleep(1)
                            terminal_menu()
                        else:
                            news_dog(int(size_input))
                            break
                    except ValueError:
                        print('VALUE NOT ACCEPTED: Pleas enter the amount of files you would like to start at')
                break
            if user_input == 2:
                checker()
                break
            if user_input == 3:
                exit()
                break
        except ValueError:
            print('String is not accepted. Pleas type in a number between 1-3')
        if user_input > 3:
            print('Pleas enter a number between 1-3')


terminal_menu()
