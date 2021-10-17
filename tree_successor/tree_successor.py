#!/usr/bin/env python3

class Node:
    """Node in a binary tree `Tree`"""

    def __init__(self, key, left=None, right=None, parent=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent


class Tree:
    """A simple binary search tree"""

    def __init__(self, root=None):
        self.root = root

    def insert(self, key):
        """Insert key into the tree.

        If the key is already present, do nothing.
        """
        if self.root is None:
            self.root = Node(key)
            return

        node = self.root
        while node.key != key:
            if key < node.key:
                if node.left is None:
                    node.left = Node(key, parent=node)
                node = node.left
            else:
                if node.right is None:
                    node.right = Node(key, parent=node)
                node = node.right

    def successor(self, node=None):
        """Return successor of the given node.

        The successor of a node is the node with the next greater key.
        Return None if there is no such node.
        If the argument is None, return the node with the smallest key.
        """

        # Check if the given node is null. If yes, traverse the tree by leftmost path to get the minimal node
        if node is None:
            current = self.root
            while current.left is not None:
                current = current.left
            return current

        # As the given node is not null we want to find its successor. Firstly check for the right son - higher node.
        # If there exists such node we take the leftmost path from him and in the end we have a successor
        # In case there is no right son, we go through parents until we find a first parent with higher key. Otherwise,
        # no higher value exists so we return null
        current = node
        if current.right is not None:
            current = current.right
            while current.left is not None:
                current = current.left
            return current
        else:
            while current.parent is not None:
                current = current.parent
                if current.key > node.key:
                    return current
        return None

