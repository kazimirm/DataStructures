#!/usr/bin/env python3

class Node:
    """Node in a binary tree `Tree`"""

    def __init__(self, key, left=None, right=None, parent=None):
        self.key = key
        self.parent = parent
        self.left = left
        self.right = right
        if left is not None: left.parent = self
        if right is not None: right.parent = self

class Tree:
    """A simple binary search tree"""

    def __init__(self, root=None):
        self.root = root

    def rotate(self, node):
        """ Rotate the given `node` up.

        Performs a single rotation of the edge between the given node
        and its parent, choosing left or right rotation appropriately.
        """
        if node.parent is not None:
            if node.parent.left == node:
                if node.right is not None: node.right.parent = node.parent
                node.parent.left = node.right
                node.right = node.parent
            else:
                if node.left is not None: node.left.parent = node.parent
                node.parent.right = node.left
                node.left = node.parent
            if node.parent.parent is not None:
                if node.parent.parent.left == node.parent:
                    node.parent.parent.left = node
                else:
                    node.parent.parent.right = node
            else:
                self.root = node
            node.parent.parent, node.parent = node, node.parent.parent

    def lookup(self, key):
        """Look up the given key in the tree.

        Returns the node with the requested key or `None`.

        We check the lastly visited node and splay it to the root
        """
        node = self.root
        last = node
        while node is not None:
            last = node
            if node.key == key:
                self.splay(node)
                return node
            if key < node.key:
                node = node.left
            else:
                node = node.right
        self.splay(last)
        return None

    def insert(self, key):
        """Insert key into the tree.

        If the key is already present, nothing happens.

        After the node with a given key is inserted, we splay it to the root
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
        self.splay(node)

    def remove(self, key):
        """Remove given key from the tree.

        It the key is not present, nothing happens.

        The implementation firstly finds the node, in case such node does not exist - we splay the lastly visited node.
        Otherwise, we make some replacements and splay the parent of the given node
        """
        node = self.root
        last = node
        while node is not None and node.key != key:
            last = node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        if node is not None:
            if node.left is not None and node.right is not None:
                replacement = node.right
                while replacement.left is not None:
                    replacement = replacement.left
                node.key = replacement.key
                node = replacement

            replacement = node.left if node.left is not None else node.right
            if node.parent is not None:
                if node.parent.left == node: node.parent.left = replacement
                else: node.parent.right = replacement
            else:
                self.root = replacement
            if replacement is not None:
                replacement.parent = node.parent
            self.splay(node.parent)
        else:
            self.splay(last)

    def splay(self, node):
        """Splay the given node.

        If a single rotation needs to be performed, perform it as the last rotation
        (i.e., to move the splayed node to the root of the tree).
        """
        # While the desired node is not in the root, we perform the suitable splay steps
        if node is None:
            return
        while node.parent is not None:
            current = node
            # check if parent and grandparent exist
            cp_not_null = current.parent is not None
            cpp_not_null = current.parent.parent is not None
            cp_and_cpp_not_null = cp_not_null and cpp_not_null
            # LL & PP suitable
            ll = cp_and_cpp_not_null and current.parent.left == current and current.parent.parent.left == current.parent
            pp = cp_and_cpp_not_null and current.parent.right == current and current.parent.parent.right == current.parent
            # LP and PL suitable
            lp = cp_and_cpp_not_null and current.parent.right == current and current.parent.parent.left == current.parent
            pl = cp_and_cpp_not_null and current.parent.left == current and current.parent.parent.right == current.parent
            # L and P suitable
            l = cp_not_null and current.parent.left == current and current.parent.parent is None
            p = cp_not_null and current.parent.right == current and current.parent.parent is None

            # We perform the correct operation according to conditions - no need to distinguish right and left as the
            # rotate method handles that
            if ll or pp:
                self.rotate(current.parent)
                self.rotate(current)
            elif lp or pl:
                self.rotate(current)
                self.rotate(current)
            elif l or p:
                self.rotate(current)


