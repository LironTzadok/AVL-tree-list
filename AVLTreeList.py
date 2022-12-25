#username - talbentov1
#id1      - 208634766
#name1    - Tal Ben Tov
#id2      - 208005835
#name2    - Liron Tzadok
from printree import *
import random

"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 

	@type value: str
	@param value: data of your node
	time complexity: O(1)
	"""
	def __init__(self, value):
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		self.size = 0


	"""responsible printing node in specific format
	
	@rtype: None
	@returns: None
	time complexity: O(1)
	"""
	def __repr__(self):
		return "(" + str(self.value) + ")"


	"""returns the left child
	
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child
	time complexity: O(1)
	"""
	def getLeft(self):
		return self.left


	"""returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child
	time complexity: O(1)
	"""
	def getRight(self):
		return self.right


	"""returns the parent 

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	time complexity: O(1)
	"""
	def getParent(self):
		return self.parent


	"""return the value

	@rtype: str
	@returns: the value of self, None if the node is virtual
	time complexity: O(1)
	"""
	def getValue(self):
		if self.isRealNode():
			return self.value
		return None


	"""returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	time complexity: O(1)
	"""
	def getHeight(self):
		if self.isRealNode():
			return self.height
		return -1


	"""returns the size

	@rtype: int
	@returns: the size of self
	time complexity: O(1)
	"""
	def getSize(self):
		return self.size


	"""sets left child

	@type node: AVLNode
	@param node: a node
	time complexity: O(1)
	"""
	def setLeft(self, node):
		self.left = node
		node.setParent(self)


	"""sets right child

	@type node: AVLNode
	@param node: a node
	time complexity: O(1)
	"""
	def setRight(self, node):
		self.right = node
		node.setParent(self)


	"""sets parent

	@type node: AVLNode
	@param node: a node
	time complexity: O(1)
	"""
	def setParent(self, node):
		self.parent = node


	"""sets value

	@type value: str
	@param value: data
	time complexity: O(1)
	"""
	def setValue(self, value):
		self.value = value


	"""sets the balance factor of the node

	@type h: int
	@param h: the height
	time complexity: O(1)
	"""
	def setHeight(self, h):
		self.height = h


	"""sets the size of the node

	@type size: int
	@param size: the size
	time complexity: O(1)
	"""
	def setSize(self, size):
		self.size = size


	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	time complexity: O(1)
	"""
	def isRealNode(self):
		return self.height != -1 and self is not None

	"""returns whether self is a leaf

	@rtype: bool
	@returns: True if self is a leaf, False otherwise.
	time complexity: O(1)
	"""
	def isLeaf(self):
		return self.height==0


"""
A class implementing the ADT list, using an AVL tree.
"""

class AVLTreeList(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.size = 0
		self.root = None
		self.min = None
		self.max = None

	"""for the tester. remember to delete!"""
	def __repr__(self):
		out = ""
		for row in printree(self.root):
			out = out + row + "\n"
		return out

	"""for the tester. remember to delete!"""
	def append(self, val):
		self.insert(self.length(), val)

	"""returns whether the list is empty

	@rtype: bool
	@returns: True if the list is empty, False otherwise
	time complexity: O(1)
	"""
	def empty(self):
		return self.size == 0


	"""retrieves the value of the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: index in the list
	@rtype: str
	@returns: the the value of the i'th item in the list
	time complexity: O(log n)
	"""
	def retrieve(self, i):
		return self.treeSelect(self.root, i + 1).getValue()


	"""retrieves the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: index in the list
	@rtype: AVLNode
	@returns: the i'th item in the list
	time complexity: O(log n)
	"""
	def retrieveNode(self, i):
		return self.treeSelect(self.root, i + 1)


	"""retrieves the i'th item in the AVL Tree such that node is it's root

	@type i: int
	@type node: AVLNode
	@pre: 0 <= i < self.length()
	@param i: Rank in the Tree
	@rtype: AVLNode
	@returns: the i'th item in the tree such that node is it's root
	time complexity: O(log n)
	"""
	def treeSelect(self, node, i):
		if i > node.getSize():
			return None
		left_size = 0
		if node.getLeft() is not None and node.getLeft().isRealNode():
			left_size = node.getLeft().getSize() + 1
			if i == left_size:
				return node
			if i < left_size:
				return self.treeSelect(node.getLeft(), i)
		if node.getRight() is not None and node.getRight().isRealNode():
			return self.treeSelect(node.getRight(), i - left_size)


	"""inserts val at position i in the list

	@type i: int
	@pre: 0 <= i <= self.length()
	@param i: The intended index in the list to which we insert val
	@type val: str
	@param val: the value we inserts
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	time complexity: O(log n)
	"""
	def insert(self, i, val):
		new_node = self.createRealNode(val)
		if i == 0:
			self.min = new_node
		if self.empty():
			self.root = new_node
			self.max=new_node
			self.min=new_node
		elif i == self.size:
			self.max.setRight(new_node)
			self.max = new_node
		elif i < self.size:
			tmp_node = self.treeSelect(self.root, i + 1)
			# if temp.node has no left child
			if not tmp_node.getLeft().isRealNode():
				tmp_node.setLeft(new_node)
			else:
				predecessor_node = self.predecessor(tmp_node)
				predecessor_node.setRight(new_node)
		sum_rotations = self.rotateAndFixSizeField(new_node)
		self.size += 1
		return sum_rotations

	"""fixes height and size fields after insert / delete / concat, using rotations

	@type node_inserted: AVLNode
	@param node_inserted: the beginning node in the chain of rebalancing operations
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	time complexity: O(log n)
	"""
	def rotateAndFixSizeField(self, node_inserted):
		y = node_inserted.getParent()
		sum_rotations = 0
		while y is not None:
			new_BF = y.getLeft().getHeight() - y.getRight().getHeight()
			y.setHeight(max(y.getLeft().getHeight(), y.getRight().getHeight()) + 1)
			if new_BF == -2:
				right_child_BF = y.getRight().getLeft().getHeight() - y.getRight().getRight().getHeight()
				if right_child_BF == -1 or right_child_BF == 0:
					# if y is not the root
					if(y.getParent() is not None):
						self.leftRotate(y, False, y.getParent().getLeft() == y)
					else:
						self.leftRotate(y, True)
					sum_rotations += 1
				elif right_child_BF == 1:
					self.rightLeftRotate(y)
					sum_rotations += 2
			elif new_BF == 2:
				left_child_BF = y.getLeft().getLeft().getHeight() - y.getLeft().getRight().getHeight()
				if left_child_BF == 1 or left_child_BF == 0:
					# if y is not the root
					if(y.getParent() is not None):
						self.rightRotate(y, False, y.getParent().getRight() == y)
					else:
						self.rightRotate(y, True)
					sum_rotations += 1
				elif left_child_BF == -1:
					self.leftRightRotate(y)
					sum_rotations += 2
			else:
				y.setSize(y.getLeft().getSize() + y.getRight().getSize() + 1)
			y = y.getParent()
		return sum_rotations

	"""performs a right rotation on node

	@type node: AVLNode
	@param node: the node who's BF is not legal (not 1,0,-1)
	@type isRoot: boolean
	@param isRoot: True if node is a root, False otherwise
	@type isRightChild: boolean
	@param isRightChild: True if node is a right child, False otherwise
	time complexity: O(1)
	"""
	def rightRotate(self, node, isRoot, isRightChild = False):
		z = node
		y = node.getLeft()
		z.setLeft(y.getRight())
		y.setParent(z.getParent())
		y.setRight(z)
		if not isRoot:
			if isRightChild:
				y.getParent().setRight(y)
			else:
				y.getParent().setLeft(y)
		else:
			self.root = y
		z.setParent(y)
		y.setSize(y.getLeft().getSize() + y.getRight().getSize() + 1)
		z.setSize(z.getLeft().getSize() + z.getRight().getSize() + 1)
		z.setHeight(max(z.getLeft().getHeight(), z.getRight().getHeight()) + 1)
		y.setHeight(max(y.getLeft().getHeight(), y.getRight().getHeight()) + 1)

	"""performs a left rotation on node

	@type node: AVLNode
	@param node: the node who's BF is not legal (not 1,0,-1)
	@type isRoot: boolean
	@param isRoot: True if node is a root, False otherwise
	@type isRightChild: boolean
	@param isRightChild: True if node is a right child, False otherwise
	time complexity: O(1)
	"""
	def leftRotate(self, node, isRoot, isLeftChild = False):
		z = node
		y = node.getRight()
		z.setRight(y.getLeft())
		y.setParent(z.getParent())
		y.setLeft(z)
		if not isRoot:
			if isLeftChild:
				y.getParent().setLeft(y)
			else:
				y.getParent().setRight(y)
		else:
			self.root = y
		z.setParent(y)
		z.setSize(z.getLeft().getSize() + z.getRight().getSize() + 1)
		y.setSize(y.getLeft().getSize() + y.getRight().getSize() + 1)
		z.setHeight(max(z.getLeft().getHeight(), z.getRight().getHeight()) + 1)
		y.setHeight(max(y.getLeft().getHeight(), y.getRight().getHeight()) + 1)

	"""performs a "right then left" rotation on node

	@type node: AVLNode
	@param node: the node who's BF is not legal (not 1,0,-1)
	time complexity: O(1)
	"""
	def rightLeftRotate(self, node):
		self.rightRotate(node.getRight(), False, True)
		# if node is not the root
		if (node.getParent() is not None):
			self.leftRotate(node, False, node.getParent().getLeft() == node)
		else:
			self.leftRotate(node, True)

	"""performs a "left then right" rotation on node

	@type node: AVLNode
	@param node: the node who's BF is not legal (not 1,0,-1)
	time complexity: O(1)
	"""
	def leftRightRotate(self, node):
		self.leftRotate(node.getLeft(), False, True)
		# if node is not the root
		if (node.getParent() is not None):
			self.rightRotate(node, False, node.getParent().getRight() == node)
		else:
			self.rightRotate(node, True)


	"""creates a real (non virtual) AVLNode

	@type val: str
	@rtype: AVLNode
	@returns: a new AVLNode with value val
	time complexity: O(1)
	"""
	def createRealNode(self, val):
		new_node = AVLNode(val)
		new_node.setHeight(0)
		new_node.setSize(1)
		virtual_child1 = AVLNode(None)
		new_node.setLeft(virtual_child1)
		virtual_child2 = AVLNode(None)
		new_node.setRight(virtual_child2)
		return new_node


	"""deletes the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	time complexity: O(log n)
	"""
	def delete(self, i):
		if i >= self.size:
			return -1
		node_to_delete = self.retrieveNode(i)
		if node_to_delete == self.root:
			return self.deleteRoot(i)
		sum_rotations = 0
		if node_to_delete.isLeaf():
			if node_to_delete.getParent() is not None:
				if node_to_delete.getParent().getRight() == node_to_delete:
					#set node_to_delete's parent's child as a virtual node
					node_to_delete.getParent().setRight(node_to_delete.getRight())
				else:
					node_to_delete.getParent().setLeft(node_to_delete.getLeft())
			sum_rotations += self.rotateAndFixSizeField(node_to_delete)
		elif node_to_delete.getRight().isRealNode() and node_to_delete.getLeft().isRealNode():
			#two childrens
			successor_node = self.successor(node_to_delete)
			sum_rotations += self.delete(i+1)
			self.size += 1
			#putting succesor_node instead of node_to_delete:
			if node_to_delete.getParent() is not None:
				if node_to_delete.getParent().getRight() == node_to_delete:
					node_to_delete.getParent().setRight(successor_node)
				else:
					node_to_delete.getParent().setLeft(successor_node)
			successor_node.setRight(node_to_delete.getRight())
			successor_node.setLeft(node_to_delete.getLeft())
			successor_node.setSize(node_to_delete.getSize())
			successor_node.setHeight(node_to_delete.getHeight())
		elif node_to_delete.getRight().isRealNode(): #right child
			if node_to_delete.getParent().getRight() == node_to_delete:
				node_to_delete.getParent().setRight(node_to_delete.getRight())
			else:
				node_to_delete.getParent().setLeft(node_to_delete.getRight())
			sum_rotations += self.rotateAndFixSizeField(node_to_delete)
		elif node_to_delete.getLeft().isRealNode(): #left child
			if node_to_delete.getParent().getRight() == node_to_delete:
				node_to_delete.getParent().setRight(node_to_delete.getLeft())
			else:
				node_to_delete.getParent().setLeft(node_to_delete.getLeft())
			sum_rotations += self.rotateAndFixSizeField(node_to_delete)
		node_to_delete.setParent(None)
		self.size -= 1
		if(node_to_delete == self.min):
			self.min = self.minNode(self.root)
		elif(node_to_delete == self.max):
			self.max = self.maxNode(self.root)
		return sum_rotations


	"""deletes the root from the tree

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	time complexity: O(log n)
	"""
	def deleteRoot(self,i):
		node_to_delete = self.root
		sum_rotations = 0
		if node_to_delete.isLeaf():
			self.root = None
		if node_to_delete.getRight().isRealNode() and node_to_delete.getLeft().isRealNode():
			successor_node = self.successor(node_to_delete)
			sum_rotations = self.delete(i+1)
			self.size += 1
			if node_to_delete.getParent() is not None:
				if node_to_delete.getParent().getRight() == node_to_delete:
					node_to_delete.getParent().setRight(successor_node)
				else:
					node_to_delete.getParent().setLeft(successor_node)
			successor_node.setRight(node_to_delete.getRight())
			successor_node.setLeft(node_to_delete.getLeft())
			successor_node.setSize(node_to_delete.getSize())
			successor_node.setHeight(node_to_delete.getHeight())
			#self.root = successor_node
		elif node_to_delete.getRight().isRealNode(): #right child
			self.root = node_to_delete.getRight()
		elif node_to_delete.getLeft().isRealNode(): #left child
			self.root = node_to_delete.getLeft()
		if self.root != None:
			self.root.setParent(None)
		self.size -= 1
		return sum_rotations


	"""returns the biggest node in the tree if called from root.
	
	@type node: AVLNode
	@param node: the root of the subtree 
	@rtype: AVLNode
	@returns: returns the biggest node in the subtree of node. if node is the root, then returns the biggest node in the tree
	time complexity: O(log n)
	"""
	def maxNode(self, node):
		while node.getRight().isRealNode():
			node = node.getRight()
		return node


	"""returns the smallest node in the tree if called from root.
	
	@type node: AVLNode
	@param node: the root of the subtree 
	@rtype: AVLNode
	@returns: returns the smallest node in the subtree of node. if node is the root, then returns the smallest node in the tree
	time complexity: O(log n)
	"""
	def minNode (self,node):
		while node.getLeft().isRealNode():
			node = node.getLeft()
		return node


	"""returns the predecessor of node, in case node has a left child
	@type node: AVLNode
	@pre: node.getLeft() != None
	@param node: a node to calculate predecessor from
	@rtype: AVLNode
	@returns: the predecessor of node
	time complexity: O(log n)
	"""
	def predecessor(self, node):
		# method implements only "go left then all the way right" case for insertion.
		if not (node.isRealNode()):
			return None
		if node.getLeft().isRealNode():
			return self.maxNode(node.getLeft())


	"""returns the sucessor of node
	@type node: AVLNode
	@param node: a node to calculate sucessor to
	@rtype: AVLNode
	@returns: the sucessor of node
	time complexity: O(log n)
	"""
	def successor(self, node):
		if node.getRight() != None and node.getRight().isRealNode():
			return self.minNode(node.getRight())
		parent = node.getParent()
		while parent !=None and parent.isRealNode() and node == parent.getRight():
			node = parent
			parent = node.getParent()
		return parent


	"""returns the value of the first item in the list

	@rtype: str
	@returns: the value of the first item, None if the list is empty
	time complexity: O(1).
	"""
	def first(self):
		if self.empty():
			return None
		return self.min.getValue()


	"""returns the value of the last item in the list

	@rtype: str
	@returns: the value of the last item, None if the list is empty
	time complexity: O(1)
	"""
	def last(self):
		if self.empty():
			return None
		return self.max.getValue()


	"""returns an array representing the list 

	@rtype: array
	@returns: an array of strings representing the data structure
	time complexity: O(n)
	"""
	def listToArray(self):
		array = []
		return self.inOrder(self.root, array)


	"""scans the tree "in order" and adds each value to a given array

	@type node: AVLNode
	@param node: a root of an AVLTreeList
	@type array: array
	@param array: an array that will contain all the values in the tree
	@rtype: array
	@returns: an array of strings representing the data structure
	time complexity: O(n)
	"""
	def inOrder(self, node, array):
		if(node is not None and node.isRealNode()):
			self.inOrder(node.getLeft(), array)
			array.append(node.getValue())
			self.inOrder(node.getRight(), array)
		return array


	"""returns the size of the list 

	@rtype: int
	@returns: the size of the list
	time complexity: O(1)
	"""
	def length(self):
		return self.size


	"""sort the info values of the list

	@rtype: AVLTreeList
	@returns: an AVLTreeList where the values are sorted by the info of the original list.
	time complexity: O(n*log n)
	"""
	def sort(self):
		list=self.listToArray()
		sorted_list = self.mergeSort(list)
		sorted_AVL = self.makeAVLOutOfAList(sorted_list)
		return sorted_AVL

	"""sorts an array of values

	@rtype: array
	@returns: an array of string values sorted by lexicographic order
	time complexity: O(n*log n)
	"""
	def mergeSort(self, list):
		n=len(list)
		if n<=1:
			return list
		return self.merge(self.mergeSort(list[0:n//2]), self.mergeSort(list[n//2:n]))

	"""merges two sorted arrays into one sorted array

	@type list1: array
	@param list1: a sorted array at size n
	@type list2: array
	@param list2: a sorted array at size m
	@pre: both list1 and list2 are sorted
	@rtype: array
	@returns: a merged sorted array at size m+n
	time complexity: O(m+n)
	"""
	def merge(self, list1, list2):
		n = len(list1)
		m = len(list2)
		merged_list = [0 for i in range(n+m)]
		a=0; b=0; c=0
		while  a<n  and  b<m:
			if list1[a] < list2[b]:
				merged_list[c] = list1[a]
				a+=1
			else:
				merged_list[c] = list2[b]
				b+=1
			c+=1
		merged_list[c:] = list1[a:] + list2[b:]
		return merged_list

	"""permute the info values of the list 

	@rtype: AVLTreeList
	@returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
	time complexity:O(n)
	"""
	def permutation(self):
		list = self.listToArray()
		shuffled_list = self.shuffleList(list)
		shuffled_AVL = self.makeAVLOutOfAList(shuffled_list)
		return shuffled_AVL


	"""shuffles a list

	@rtype: list
	@returns: a list where the values are permuted randomly by the info of the original list. ##Use Randomness
	time complexity:O(n)
	"""
	def shuffleList(self, list):
		for i in range(len(list) - 1, 0, -1):
			# Pick a random index from 0 to i
			j = random.randint(0, i)
			# swap
			temp = list[i]
			list[i] = list[j]
			list[j] = temp
		return list


	""" makes an AVLTreeList from a given list

	@rtype: AVLTreeList
	@returns: an AVLTreeList that nodes in it are ordered by their index in the given list
	time complexity:O(n)
	"""
	def makeAVLOutOfAList(self, list):
		shuffled_tree = AVLTreeList()
		mid = (len(list)) // 2
		shuffled_tree.root = self.createRealNode(list[mid])
		shuffled_tree.root.setLeft(self.AVLOutOfAListInner(list, 0, mid - 1, shuffled_tree))
		shuffled_tree.root.setRight(self.AVLOutOfAListInner(list, mid + 1, len(list) - 1, shuffled_tree))
		shuffled_tree.root.setSize(shuffled_tree.root.getLeft().getSize() + shuffled_tree.root.getRight().getSize() + 1)
		shuffled_tree.root.setHeight(max(shuffled_tree.root.getLeft().getHeight(), shuffled_tree.root.getRight().getHeight()) + 1)
		shuffled_tree.size = len(list)
		return shuffled_tree


	""" creates a subtree from a given list

	@rtype: AVLNode
	@returns: an AVLNode with the value of the list[middle of start + end]. the AVLNode left's child is an AVL subtree
	made of the left side of the array (from middle index to 0 index) the right child is an AVL subtree made of the 
	right side of the array(from middle index to list.len()-1 index)
	time complexity:O(n)
	"""
	def AVLOutOfAListInner(self, list, start, end, tree):
		if start > end:
			return AVLNode(None)
		else:
			mid = start + (end - start) // 2
			new_node = self.createRealNode(list[mid])
			new_node.setLeft(self.AVLOutOfAListInner(list, start, mid - 1, tree))
			new_node.setRight(self.AVLOutOfAListInner(list, mid + 1, end, tree))
			new_node.setSize(new_node.getLeft().getSize() + new_node.getRight().getSize() + 1)
			new_node.setHeight(max(new_node.getLeft().getHeight(), new_node.getRight().getHeight()) + 1)
			# if new_node is the first node in the list make it the min of the tree
			if mid == 0:
				tree.min = new_node
			# if new_node is the last node in the list make it the max of the tree
			elif mid == len(list) - 1:
				tree.max = new_node
		return new_node


	"""concatenates lst to self

	@type lst: AVLTreeList
	@param lst: a list to be concatenated after self
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	time complexity:O(log n)
	"""
	def concat(self, lst):
		if lst.empty() and not self.empty():
			return self.root.getHeight()
		if self.empty() and not lst.empty():
			self.root = lst.getRoot()
			return lst.getRoot().getHeight()
		if self.empty() and lst.empty():
			return 0
		height_difference = abs(self.getRoot().getHeight()-lst.getRoot().getHeight())
		x = self.max
		self.delete(self.size - 1)
		joined_tree = self.join(self, lst, x)
		self.root = joined_tree
		self.max = self.maxNode(self.root)
		self.min = self.minNode(self.root)
		self.size = self.root.getSize()
		return height_difference


	"""joining T1,T2 into one tree, given a node x such that T1<x<T2

	@type T1: AVLTreeList
	@type T2: AVLTreeList
	@type x: AVLNode
	@param T1: a tree to be joined with T2
	@param T2: a tree to be joined with T1
	@rtype: AVLTreeList
	@returns: the root of a joined tree from two given trees
	time complexity:O(log n)
	"""
	def join(self, T1, T2 ,x):
		if T1.empty():
			T1_root = AVLNode(None)
		else:
			T1_root = T1.getRoot()
		if T2.empty():
			T2_root = AVLNode(None)
		else:
			T2_root = T2.getRoot()
		h1 = T1_root.getHeight()
		h2 = T2_root.getHeight()
		if abs(h1 - h2) <= 1:
			x.setLeft(T1_root)
			x.setRight(T2_root)
			root = x
		elif h1 < h2:
			a = T1_root
			b = T2_root
			while b.getHeight() > h1:
				b = b.getLeft()
			root = T2_root
			# start joining
			x.setLeft(a)
			c = b.getParent()
			c.setLeft(x)
			x.setRight(b)
		else:
			a = T2_root
			b = T1_root
			while b.getHeight() > h2:
				b = b.getRight()
			root = T1_root
			# start joining
			x.setRight(a)
			c = b.getParent()
			c.setRight(x)
			x.setLeft(b)
		self.rotateAndFixSizeField(x.getLeft())
		return root


	"""searches for a *value* in the list

	@type val: str
	@param val: a value to be searched
	@rtype: int
	@returns: the first index that contains val, -1 if not found.
	@time complexity: O(n)
	"""
	def search(self, val):
		if self.empty():
			return -1
		node=self.min
		index=0
		while node != None and node.isRealNode() and node.getValue()!=val:
			index+=1
			node=self.successor(node)
		if node != None and node.isRealNode() and node.getValue()==val:
			return index
		return -1


	"""returns the root of the tree representing the list

	@rtype: AVLNode
	@returns: the root of the tree, or None if the list is empty
	"""
	def getRoot(self):
		return self.root





