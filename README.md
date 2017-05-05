## tabtree - Parsing tabbed tree formatted text files into dict node trees
[![PyPI](http://img.shields.io/pypi/v/tabtree.svg)](http://img.shields.io/pypi/v/tabtree.svg)

1. tabtree is a tiny package to convert tabbed trees from text files into dict trees.
2. The functions in this module use lazy evaluation (take line iterators as input and return record iterators as output), so they can be used with very large files without becoming a memory hog.
3. Although there is a default format for the dict nodes in the output node trees, it can be fully customized by passing a node generating function as an optional argument

## How to use tabtree?

Lets assume we have a file (name data.txt) with the following content:

```
item 0
	item 0 0
	item 0 1
		item 0 1 0
		item 0 1 1
	item 0 2 
item 1 
	item 1 0
	item 1 1
		item 1 1 0
		item 1 1 1
	item 1 2
```

then the following code:

```
from tabtree import parser
with open('data.txt', 'r') as lines:
	node_trees = parser.lines_to_node_trees(lines)
	for node_tree in node_trees:
		print(node_tree)
```

will print the following two trees:

```
{'data': 'item 0', 'children': [
	{'data': 'item 0 0', 'children': []},
	{'data': 'item 0 1', 'children': [
		{'data': 'item 0 1 0', 'children': []},
		{'data': 'item 0 1 1', 'children': []}
	]},
	{'data': 'item 0 2', 'children': []}
]}
{'data': 'item 1', 'children': [
	{'data': 'item 1 0', 'children': []},
	{'data': 'item 1 1', 'children': [
		{'data': 'item 1 1 0', 'children': []},
		{'data': 'item 1 1 1', 'children': []}
	]},
	{'data': 'item 1 2', 'children': []}
]}
```

## Why implementing this module?

Although this is actually a tiny piece of code, it is a functionality I need quite often. However, I found very few existing python implementations of it (mostly code snippets), and none of which was entirely suitable for my needs:
   * Lazy evaluation (I am working with very big files, so I cannot afford to load all the data into a big tree in memory).
   * Ability to use customized node formats. I'm parsing different types of data that require different representations, so customizing the node format at tree creation time is a big plus (otherwise you need to stick with one-and-only-library-defined-node-class or either apply a traverse-the-trees-and-transform-node process)
