#username - talbentov1
#id1      - 208634766
#name1    - Tal Ben Tov
#id2      - 208005835
#name2    - Liron Tzadok


"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 

	@type value: str
	@param value: data of your node
	"""
	def __init__(self, value):
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		self.size = 0


	def setSize(self, size):
		self.size = size


	"""returns the left child
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child
	"""
	def getLeft(self):
		return self.left


	"""returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child
	"""
	def getRight(self):
		return self.right

	"""returns the parent 

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	"""
	def getParent(self):
		return self.parent

	"""return the value

	@rtype: str
	@returns: the value of self, None if the node is virtual
	"""
	def getValue(self):
		if self.isRealNode():
			return self.value
		return None

	"""returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""
	def getHeight(self):
		if self.isRealNode():
			return self.height
		return -1

	"""sets left child

	@type node: AVLNode
	@param node: a node
	"""
	def setLeft(self, node):
		self.left = node
		node.setParent(self)

	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def setRight(self, node):
		self.right = node
		node.setParent(self)

	"""sets parent

	@type node: AVLNode
	@param node: a node
	"""
	def setParent(self, node):
		self.parent = node

	"""sets value

	@type value: str
	@param value: data
	"""
	def setValue(self, value):
		self.value = value

	"""sets the balance factor of the node

	@type h: int
	@param h: the height
	"""
	def setHeight(self, h):
		self.height = h

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def isRealNode(self):
		return self.height != -1 and self is not None



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
		# add your fields here


	"""returns whether the list is empty

	@rtype: bool
	@returns: True if the list is empty, False otherwise
	"""
	def empty(self):
		return self.size == 0


	"""retrieves the value of the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: index in the list
	@rtype: str
	@returns: the the value of the i'th item in the list
	"""
	def retrieve(self, i):
		return self.treeSelect(i + 1).value

	"""retrieves the value of the i'th item in the AVL Tree

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: Rank in the Tree
	@rtype: AVLNode
	@returns: value of the i'th smallest element in the Tree
	"""
	def treeSelect(self, i):
		x = self.root
		if i > x.size:
			return None
		left_size = x.left.size + 1
		if i == left_size :
			return x
		if i < left_size :
			return self.treeSelect(x.left,i)
		return self.treeSelect(x.right,i - left_size)


	"""inserts val at position i in the list

	@type i: int
	@pre: 0 <= i <= self.length()
	@param i: The intended index in the list to which we insert val
	@type val: str
	@param val: the value we inserts
	@rtype: list
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def insert(self, i, val):
		new_node = self.createRealNode(val)
		if self.empty():
			self.root = new_node
		elif i == self.size:
			max_node = self.maxNode()
			max_node.right = new_node
		elif i < self.size:
			tmp_node = self.treeSelect(i + 1)
			# if temp.node has no left child
			if not tmp_node.left.isRealNode():
				tmp_node.setLeft(new_node)
			else:
				predecessor_node = self.predecessor(tmp_node)
				predecessor_node.setRight(new_node)
		self.rotateAndFixSizeField(new_node)


	def rotateAndFixSizeField(self, node_inserted):
		y = node_inserted.getParent()
		while y is not None:
			new_BF = y.getLeft().getHeight() - y.getRight().getHeight()
			y.setHeight(max(y.getLeft, y.getRight) + 1)
			y.setSize(y.getLeft.getSize + y.getLeft.getSize + 1)
			if new_BF == -2:
				right_child_BF = y.getRight.getLeft().getHeight() - y.getRight.getRight().getHeight()
				if right_child_BF == -1 or right_child_BF == 0:
					self.leftRotate(y, y.getParent().getLeft == y)
				elif right_child_BF == 1:
					self.rightLeftRotate(y)
			elif new_BF == 2:
				left_child_BF = y.getLeft.getLeft().getHeight() - y.getLeft.getRight().getHeight()
				if left_child_BF == 1 or right_child_BF == 0:
					self.rightRotate(y, y.getParent().getRight == y)
				elif left_child_BF == -1:
					self.leftRightRotate(y)
			# check y.setHeight(max(y.getLeft, y.getRight) + 1)
			# check y.setSize(y.getLeft.getSize + y.getLeft.getSize + 1)



	def leftRotate(self, node, isLeftChild):
		b = node
		a = node.getRight()
		b.setRight(a.getLeft())
		b.getRight.setParent(b)
		a.setLeft(b)
		a.setParent(b.getParent)
		if isLeftChild:
			a.getParent().setLeft(a)
		else:
			a.getParent().setRight(a)
		b.setParent(a)
		b.setHeight(max(b.getLeft, b.getRight) + 1)
		a.setHeight(max(a.getLeft, a.getRight) + 1)

	def rightLeftRotate(self, node):
		self.rightRotate(node.getRight(), True)
		self.leftRotate(node, node.getParent().getRight == node)

	def rightRotate(self, node, isRightChild):
		b = node
		a = node.getLeft()
		b.setLeft(a.getRight())
		b.getLeft.setParent(b)
		a.setRight(b)
		a.setParent(b.getParent)
		if isRightChild:
			a.getParent().setRight(a)
		else:
			a.getParent().setLeft(a)
		b.setParent(a)
		b.setHeight(max(b.getLeft, b.getRight) + 1)
		a.setHeight(max(a.getLeft, a.getRight) + 1)



	def leftRightRotate(self, node):
		self.leftRotate(node.getLeft(), True)
		self.rightRotate(node, node.getParent().getRight == node)


	def createRealNode(self, val):
		new_node = AVLNode(val)
		new_node.setHeight(0)
		new_node.setSize(1)
		virtual_child1 = AVLNode(None)
		new_node.setLeft(virtual_child1)
		virtual_child2 = AVLNode(None)
		new_node.setRight(virtual_child2)
		virtual_child1.setParent(new_node)
		virtual_child2.setParent(new_node)
		return new_node


	"""deletes the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""

	def delete(self, i):
		return -1

	"""returns the biggest node in the tree if called from root
	@rtype: AVLNode
	"""
	def maxNode(self, node):
		while node.right.isRealNode:
			node = node.getRight()
		return node


	"""returns the node's left node's most right node
	@rtype: AVLNode
	"""
	def predecessor(self, node):
		# method implements only "go left then all the way right" case for insertion.
		if not (node.isRealNode()):
			return None
		if node.getLeft().isRealNode():
			return self.maxNode(node.getLeft())


	"""returns the value of the first item in the list

	@rtype: str
	@returns: the value of the first item, None if the list is empty
	"""
	def first(self):
		return None

	"""returns the value of the last item in the list

	@rtype: str
	@returns: the value of the last item, None if the list is empty
	"""
	def last(self):
		return None

	"""returns an array representing list 

	@rtype: list
	@returns: a list of strings representing the data structure
	"""
	def listToArray(self):
		return None

	"""returns the size of the list 

	@rtype: int
	@returns: the size of the list
	"""
	def length(self):
		return None

	"""sort the info values of the list

	@rtype: list
	@returns: an AVLTreeList where the values are sorted by the info of the original list.
	"""
	def sort(self):
		return None

	"""permute the info values of the list 

	@rtype: list
	@returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
	"""
	def permutation(self):
		return None

	"""concatenates lst to self

	@type lst: AVLTreeList
	@param lst: a list to be concatenated after self
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def concat(self, lst):
		return None

	"""searches for a *value* in the list

	@type val: str
	@param val: a value to be searched
	@rtype: int
	@returns: the first index that contains val, -1 if not found.
	"""
	def search(self, val):
		return None




	"""returns the root of the tree representing the list

	@rtype: AVLNode
	@returns: the root, None if the list is empty
	"""
	def getRoot(self):
		return None


