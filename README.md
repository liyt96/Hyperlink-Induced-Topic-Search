# Hyperlink-Induced Topic Search
An implementation of Hyperlink-Induced-Topic-Search (HITS) algorithm with Python 3.

## Usage

#### 1. Get the web graph

HITS computes on a web graph. In this implementation, the graph expressed as 
⋅⋅* `inlinks.json`: A JSON that maps a URL to its inlink URLs.
⋅⋅* `outlinks.json`: A JSON that maps a URL to its outlink URLs.
⋅⋅* `docno_list.json`: A JSON that contains all URLs.

The web graph I crawled is [here].

### 2. Get Root Set and Base Set

You may modify `hits_get_root_base.py` and `config.yaml` to compute Root Set and Base Set if you use [Elasticsearch](https://www.elastic.co/products/elasticsearch)

The root set and base set I get is [here]

2. Run `python hits.py` to run the algorithm when you are ready with `inlinks.json`, `outlinks.json`, `docno_list.json`, `root_set.json` and `base_set.json`.

## More on HITS algorithm

1. [HITS algorithm - Wikipedia](https://en.wikipedia.org/wiki/HITS_algorithm)
2. [Hubs, Authorities, and Communities, Kleinberg, Jon (1999)](http://www.cs.brown.edu/memex/ACM_HypertextTestbed/papers/10.html)
