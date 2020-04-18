# Hyperlink-Induced Topic Search
An implementation of Hyperlink-Induced-Topic-Search (HITS) algorithm with Python 3. 

HITS ranks web pages according to users' query, just like Page Rank.

## Usage

#### 1. Get the web graph

HITS computes on a web graph. In this implementation, the graph expressed as 
* `inlinks.json`: A JSON that maps a URL to its inlink URLs.
* `outlinks.json`: A JSON that maps a URL to its outlink URLs.
* `docno_list.json`: A JSON that contains all URLs.

The web graph I crawled is [here](https://drive.google.com/file/d/14A8-z8lJxU-VmV6gIN0qUEd740VS9I80/view?usp=sharing).

### 2. Get Root set and Base set

To compute HITS, we also need a Root set `root_set.json` and a Base set `base_set.json`.

You may modify `hits_get_root_base.py` and `config.yaml` to compute Root set and Base set by `python hits_get_root_base.py` if you use [Elasticsearch](https://www.elastic.co/products/elasticsearch).

The Root set and Base set I get form my web graph is [here](https://drive.google.com/file/d/1jpB7T08sl8z-PqRK4Pjyx-tUKlZEGqwx/view?usp=sharing).

### 3. Run HITS

Run `python hits.py` to run the algorithm when you are ready with `inlinks.json`, `outlinks.json`, `docno_list.json`, `root_set.json` and `base_set.json` and put them under the `info` directory.

The result will be under `result` directory, where `authority.json` contains authority pages and `hub.json` contains hub pages.

## More on HITS algorithm

1. [Hubs, Authorities, and Communities, Kleinberg, Jon (1999)](http://www.cs.brown.edu/memex/ACM_HypertextTestbed/papers/10.html)
2. [HITS algorithm - Wikipedia](https://en.wikipedia.org/wiki/HITS_algorithm)
