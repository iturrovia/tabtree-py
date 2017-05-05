"""
The purpose of this module is to parse data formatted as tabbed tree

"""

import re
import string
import itertools
GENERAL_TABBED_LINE_REGEX = re.compile('([\\t ]*)(.*)')
SPACE_TABBED_LINE_REGEX = re.compile('( *)(.*)')

def spaces_to_tabs(line, spaces_per_tab):
	'''
	Replaces leading spaces with tabs, according to the spaces_per_tab equivalence
	
	:param string line: input line
 	:rtype: string
	
	'''
	m = GENERAL_TABBED_LINE_REGEX.match(line)
	space_tab = ' '*spaces_per_tab
	return string.replace(m.group(1), space_tab, '\t') + m.group(2)


def line_to_depth_and_text(line):
	'''
	Takes a line and returns a tuple containing:
	    - The number of tabs
	    - The text after those tabs
	'''
	m = GENERAL_TABBED_LINE_REGEX.match(line)
	depth = len(m.group(1))
	text = m.group(2)
	return (depth, text.rstrip('\r\n'))

def lines_to_dts(lines):
	'''
	Takes a stream of lines and yields, for each line, a (depth, text) tuple containing:
	    - The depth (number of tabs)
	    - The text found after the tabs
	
	'''
	return itertools.imap(line_to_depth_and_text, lines)

def text_to_dc_node(text):
	'''
	Takes a text string and returns a DC (Data and Children) node, which is a dictionary contaning the following elements:
		- data: data extracted from the text
		- children: list of children nodes, not extracted from the input text, but to be filled with subsquent nodes

	Note that this is an example of a "text_to_node" function that could be used with dts_to_node_trees()
	'''
	return {'data': text, 'children': []}

def dts_to_node_trees(dts, text_to_node=text_to_dc_node, node_children_key='children'):
	'''
	Takes a stream of (depth, text) tuples and yields a stream of node trees, which are trees composed of dictionary nodes

	It can also take the following optional parameters:
		- text_to_node: function that takes the text from the input (depth, text) tuple and returns a node, which is a dictionary that contains,
						among other fields, a "children" field set to an empty list (which will be filled later on).
						Note that it takes the text_to_dc_node function from this module as a default value, but you can provide your own text_to_node
						function if necessary
		- node_children_key: in case you provide a custom text_to_node function that, when creating the children field in the outpput dictionary, uses
						a key value different from "children", then you mmus specify such new key value in node_children_key, so the dts_to_node_trees 
						function will now know where to add children elements into your dictionary	
	'''
	node_stack = []
	depth_to_level = {}
	max_depth = -1
	min_depth = -1
	for depth_and_text in itertools.ifilter(lambda depth_and_text): depth_and_text[1] != '', dts):
		depth = depth_and_text[0]
		text = depth_and_text[1]
		if(depth <= min_depth):
			node = node_stack[0]
			node_stack = []
			depth_to_level = {}
			max_depth = -1
			min_depth = -1
			yield node
		if(len(node_stack) == 0):
			if(text != ''):
				# Initializing the stack
				depth_to_level[depth] = 0
				max_depth = depth
				min_depth = depth
				node = text_to_node(text)
				node_stack.append(node)
			else:
				print('once')
		else:
			if(depth > max_depth):
				node = text_to_node(text)
				# New node, we append it as children to the last one
				node_stack[depth_to_level[max_depth]][node_children_key].append(node)
				# Now appending the new node to the stack
				depth_to_level[depth] = len(node_stack)
				max_depth = depth
				node_stack.append(node)
			else:
				node = text_to_node(text)
				# Children of someone
				level = depth_to_level[depth]
				node_stack = node_stack[:level]
				parent = node_stack[level - 1]
				parent[node_children_key].append(node)
				depth_to_level[depth] = len(node_stack)
				max_depth = depth
				node_stack.append(node)
	if(len(node_stack) > 0):
		node = node_stack[0]
		yield node

def lines_to_node_trees(lines, text_to_node=text_to_dc_node, node_children_key='children', spaces_per_tab=None):
	'''
	Takes a stream of lines and yields a stream of node trees, which are trees composed of dictionary nodes

	It can also take the following optional parameters:
		- text_to_node: function that takes the text from the input (depth, text) tuple and returns a node, which is a dictionary that contains,
						among other fields, a "children" field set to an empty list (which will be filled later on).
						Note that it takes the text_to_dc_node function from this module as a default value, but you can provide your own text_to_node
						function if necessary
		- node_children_key: in case you provide a custom text_to_node function that, when creating the children field in the outpput dictionary, uses
						a key value different from "children", then you mmus specify such new key value in node_children_key, so the dts_to_node_trees 
						function will now know where to add children elements into your dictionary	
		- spaces_per_tab: in case the indent in the input lines combines both tabs and spaces, in which case you might want to set and equivalence other
						than one to one
	'''
	node_stack = []
	depth_to_level = {}
	max_depth = -1
	min_depth = -1
	if(spaces_per_tab != None):
		fix_spaces = lambda x: spaces_to_tabs(x, spaces_per_tab)
		preprocessed_lines = itertools.imap(fix_spaces, lines)
	else:
		preprocessed_lines = lines
	dts = itertools.imap(line_to_depth_and_text, preprocessed_lines)
	return dts_to_node_trees(dts, text_to_node=text_to_node, node_children_key=node_children_key)
