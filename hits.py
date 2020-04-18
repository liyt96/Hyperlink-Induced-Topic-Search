#!/usr/bin/env python
__author__ = "Yuetian Li"

import copy
import json
from elasticsearch.helpers import bulk
from tqdm import tqdm
import os
from elasticsearch import Elasticsearch
import math
from collections import defaultdict
import random

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

def authority_hub_init(all_pages):
    authority = defaultdict(float)
    hub = defaultdict(float)
    for page in all_pages:
        authority[page] = 1
        hub[page] = 1
    return authority, hub

def hits_iter(root_set, base_set, authority, hub, inlinks, outlinks):
    new_authority = defaultdict(float)
    new_hub = defaultdict(float)

    # Calculate the scores
    for page in root_set:
        if page in inlinks:
            new_authority[page] = 0
            for inlink in inlinks[page]:
                if inlink in authority:
                    new_authority[page] += hub[inlink]
        else:
            new_authority[page] = 0

    for page in base_set:
        if page in outlinks:
            new_hub[page] = 0
            for outlink in outlinks[page]:
                if outlink in hub:
                    new_hub[page] += authority[outlink]
        else:
            new_hub[page] = 0
    
    # Normalization
    auth_norm = math.sqrt( sum([ ( new_authority[page] ) ** 2 for page in new_authority ]) )
    hub_norm = math.sqrt( sum([ ( new_hub[page] ) ** 2 for page in new_hub ]) )
    for page in new_authority:
        new_authority[page] = new_authority[page] / auth_norm
    for page in new_hub:
        new_hub[page] = new_hub[page] / hub_norm
    
    return new_authority, new_hub

def update_auth_hub(authority, hub, new_authority, new_hub):
    for page in new_authority:
        if page in authority:
            authority[page] = new_authority[page]
    for page in new_hub:
        if page in hub:
            hub[page] = new_hub[page]
    return authority, hub
        
def check_convergence(authority, hub, new_authority, new_hub, epsilon_auth, epsilon_hub):

    authority_total = 0
    new_authority_total = 0
    for count, page in enumerate(new_authority):
        authority_total += authority[page]
        new_authority_total += new_authority[page]

    hub_total = 0
    new_hub_total = 0
    for count, page in enumerate(new_hub):
        hub_total += hub[page]
        new_hub_total += new_hub[page]
    
    print( 'Authority gap:', math.fabs(authority_total - new_authority_total ) )
    print( 'Hub gap:', math.fabs(hub_total - new_hub_total ) )

    if ( math.fabs(authority_total - new_authority_total ) < epsilon_auth ) and \
        ( math.fabs(hub_total - new_hub_total ) < epsilon_hub ):
        return True
    return False


def run_hits(root_set, base_set, all_pages, inlinks, outlinks):
    epsilon_auth = 10 ** -9
    epsilon_hub = 10 ** -9
    authority, hub = authority_hub_init(all_pages)
    new_authority, new_hub = hits_iter(root_set, base_set, authority, hub, inlinks, outlinks)
    iter_count = 0
    complete_converge_count = 0
    while True:
        if iter_count > 100000:
            print('Exceeded iteration limit of', str(iter_count))
            break
        if check_convergence(authority, hub, new_authority, new_hub, epsilon_auth, epsilon_hub):
            complete_converge_count += 1
            if complete_converge_count == 4:
                print('HITS score converged.')
                break
        else:
            complete_converge_count = 0
        authority, hub = update_auth_hub(authority, hub, new_authority, new_hub)
        new_authority, new_hub = hits_iter(root_set, base_set, authority, hub, inlinks, outlinks)
        iter_count += 1
    return new_authority, new_hub

if __name__ == "__main__":

    D = 200

    print('Loading link graph...')
    inlinks = get_inlinks('./info/inlinks.json')
    print('inlinks loaded')
    outlinks = get_outlinks('./info/outlinks.json')
    print('outlinks loaded')
    all_pages = get_all_pages('./info/docno_list.json')
    print('url loaded')

    with open('./info/root_set.json', 'r') as f:
        root_set = json.load(f)
    print('A: Get root set finish')

    with open('./info/base_set.json', 'r') as f:
        base_set = json.load(f)
    print('B: Get base set finish')

    print('C: Start to run HITS')
    authority, hub = run_hits(root_set, base_set, all_pages, inlinks, outlinks)

    # Dump result
    sorted_authority = sorted(authority.items(), key=lambda x: x[1], reverse=True)
    sorted_hub = sorted(hub.items(), key=lambda x: x[1], reverse=True)

    sorted_authority_all = []
    sorted_hub_all = []

    for page in sorted_authority:
        if ( page[0] in outlinks ) and ( page[0] in inlinks ):
            sorted_authority_all.append( [ page[0], page[1], len(outlinks[page[0]]), len(inlinks[page[0]]) ] )
        elif ( page[0] in outlinks ):
            sorted_authority_all.append( [ page[0], page[1], len(outlinks[page[0]]), 0 ] )
        elif ( page[0] in inlinks ):
            sorted_authority_all.append( [ page[0], page[1], 0, len(inlinks[page[0]]) ] )
        else:
            sorted_authority_all.append( [ page[0], page[1], 0, 0 ] )
    
    for page in sorted_hub:
        if ( page[0] in outlinks ) and ( page[0] in inlinks ):
            sorted_hub_all.append( [ page[0], page[1], len(outlinks[page[0]]), len(inlinks[page[0]]) ] )
        elif ( page[0] in outlinks ):
            sorted_hub_all.append( [ page[0], page[1], len(outlinks[page[0]]), 0 ] )
        elif (page[0] in inlinks):
            sorted_hub_all.append( [ page[0], page[1], 0, len(inlinks[page[0]]) ] )
        else:
            sorted_hub_all.append( [ page[0], page[1], 0, 0 ] )

    with open('./result/authority.json', 'w') as f:
        json.dump(sorted_authority_all[:1000], f)
    
    with open('./result/hub.json', 'w') as f:
        json.dump(sorted_hub_all[:1000], f)

    