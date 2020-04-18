import copy
import json
from elasticsearch.helpers import bulk
from tqdm import tqdm
import os
from elasticsearch import Elasticsearch
import math
from collections import defaultdict
import random

import yaml

with open("config.yaml", "r") as ymlfile:
    config = yaml.load(ymlfile)

LOCALHOST = config['es']['localhost']
PORT = config['es']['port']
INDEX = config['es']['index']
QUERY = config['query']

es = Elasticsearch([{'host': LOCALHOST, 'port': PORT}])

def add_score(docno, model_scores, score):
    if docno in model_scores:
        model_scores[docno] += score
    else:
        model_scores[docno] = score

def compute_es_built_in(query):
    
    es_built_in_scores = defaultdict(lambda: 0.0)
    body = {
        'size': 100000,
        '_source': False,
        'query': {
                'match': {
                    'text': query
                }
        }
    }
    res = es.search(index=INDEX, body=body)
    for docno in res['hits']['hits']:
        add_score(docno['_id'], es_built_in_scores, docno['_score'])
    sorted_scores = sorted(es_built_in_scores.items(), key=lambda x: x[1], reverse=True)
    root_pages = [ sorted_scores[i][0] for i in range(1000) ]
    return set(root_pages)

def get_root_set():
    query = QUERY
    return compute_es_built_in(query)

def get_random_pages(inlinks, D):
    random_set = set()
    for i in range(D):
        pick = random.choice(list(inlinks.keys()))
        while pick in random_set:
            pick = random.choice(list(inlinks.keys()))
        random_set.add(pick)
    return random_set

def get_base_set(inlinks, outlinks, root_pages, D):
    expand_set = set()
    for page in root_pages:
        if page in outlinks:
            expand_set.update(set(outlinks[page]))
        if page in inlinks:
            if len(inlinks[page]) <= D:
                expand_set.update(set(inlinks[page]))
            else:
                expand_set.update(get_random_pages(inlinks, D))
    return expand_set

def get_inlinks(path):
    inlinks = defaultdict(list)
    with open(path, 'r') as f:
        inlinks = json.load(f)
    return inlinks

def get_outlinks(path):
    outlinks = defaultdict(list)
    with open(path, 'r') as f:
        outlinks = json.load(f)
    return outlinks

def get_all_pages(path):
    all_pages = []
    with open(path, 'r') as f:
        all_pages = json.load(f)
    return all_pages



if __name__ == "__main__":
    D = 200

    inlinks = get_inlinks('./info/inlinks.json')
    outlinks = get_outlinks('./info/outlinks.json')
    all_pages = get_all_pages('./info/docno_list.json')

    # A
    root_set = get_root_set()
    print('A: Get root set finish')

    # B
    base_set = get_base_set(inlinks, outlinks, root_set, D)
    print('B: Get base set finish')

    with open('./info/root_set.json', 'w') as f:
        json.dump(list(root_set), f)

    with open('./info/base_set.json', 'w') as f:
        json.dump(list(base_set), f)