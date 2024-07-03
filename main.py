import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLineEdit, QLabel
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if root is None:
            return TreeNode(key)
        else:
            if root.val < key:
                root.right = self.insert(root.right, key)
            else:
                root.left = self.insert(root.left, key)
        return root

    def delete(self, root, key):
        if root is None:
            return root
        if key < root.val:
            root.left = self.delete(root.left, key)
        elif key > root.val:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = self.minValueNode(root.right)
            root.val = temp.val
            root.right = self.delete(root.right, temp.val)
        return root

    def minValueNode(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.val, end=" ")
            self.inorder(root.right)

class AVLTreeNode(TreeNode):
    def __init__(self, key):
        super().__init__(key)
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if not root:
            return AVLTreeNode(key)
        elif key < root.val:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and key < root.left.val:
            return self.rightRotate(root)
        if balance < -1 and key > root.right.val:
            return self.leftRotate(root)
        if balance > 1 and key > root.left.val:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
        if balance < -1 and key < root.right.val:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def delete(self, root, key):
        if not root:
            return root
        elif key < root.val:
            root.left = self.delete(root.left, key)
        elif key > root.val:
            root.right = self.delete(root.right, key)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.minValueNode(root.right)
            root.val = temp.val
            root.right = self.delete(root.right, temp.val)

        if root is None:
            return root

        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)
        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)
        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)
        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def minValueNode(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def leftRotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.getHeight(z.left), self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        return y

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(root.val, end=" ")
            self.inorder(root.right)

class TreeVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.tree = None
        self.root = None
        self.search_key = None  # Track the search key

        layout = QVBoxLayout()

        self.tree_type_label = QLabel("Select Tree Type:")
        layout.addWidget(self.tree_type_label)

        self.tree_type_combo = QComboBox()
        self.tree_type_combo.addItem("Binary Search Tree")
        self.tree_type_combo.addItem("AVL Tree")
        layout.addWidget(self.tree_type_combo)

        self.input_label = QLabel("Enter numbers (comma-separated):")
        layout.addWidget(self.input_label)

        self.input_line = QLineEdit()
        layout.addWidget(self.input_line)

        self.create_button = QPushButton("Create Tree")
        self.create_button.clicked.connect(self.create_tree)
        layout.addWidget(self.create_button)

        self.add_delete_layout = QHBoxLayout()
        self.add_delete_label = QLabel("Enter number to add/delete:")
        self.add_delete_layout.addWidget(self.add_delete_label)

        self.add_delete_line = QLineEdit()
        self.add_delete_layout.addWidget(self.add_delete_line)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_node)
        self.add_delete_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_node)
        self.add_delete_layout.addWidget(self.delete_button)

        layout.addLayout(self.add_delete_layout)

        self.search_layout = QHBoxLayout()
        self.search_label = QLabel("Search node:")
        self.search_layout.addWidget(self.search_label)

        self.search_line = QLineEdit()
        self.search_layout.addWidget(self.search_line)

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_node)
        self.search_layout.addWidget(self.search_button)

        layout.addLayout(self.search_layout)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def create_tree(self):
        numbers = list(map(int, self.input_line.text().split(',')))
        tree_type = self.tree_type_combo.currentText()

        if tree_type == "Binary Search Tree":
            self.tree = BinarySearchTree()
        elif tree_type == "AVL Tree":
            self.tree = AVLTree()

        self.root = None
        for number in numbers:
            self.root = self.tree.insert(self.root, number)

        self.plot_tree(self.root)

    def add_node(self):
        number = int(self.add_delete_line.text())
        self.root = self.tree.insert(self.root, number)
        self.plot_tree(self.root)

    def delete_node(self):
        number = int(self.add_delete_line.text())
        self.root = self.tree.delete(self.root, number)
        self.plot_tree(self.root)

    def search_node(self):
        self.search_key = int(self.search_line.text())
        self.plot_tree(self.root, search_key=self.search_key)

    def plot_tree(self, root, x=0, y=0, dx=20, animate=False, search_key=None):
        self.ax.clear()

        def plot_node(node, x, y, dx, path=[]):
            if node:
                current_path = path + [node]
                if search_key is not None and node.val == search_key:
                    color = 'green'  # Highlight searched node in green
                    for n in current_path[:-1]:
                        n.color = 'green'
                else:
                    color = 'white'
                    for n in current_path:
                        if not hasattr(n, 'color'):
                            n.color = 'red'

                bbox_props = dict(facecolor=color, edgecolor='black', boxstyle='circle')
                self.ax.text(x, y, str(node.val), ha='center', va='center', bbox=bbox_props)

                if node.left:
                    self.ax.plot([x, x - dx], [y, y - 20], color=node.left.color if hasattr(node.left, 'color') else 'black')
                    plot_node(node.left, x - dx, y - 20, dx // 2, current_path)

                if node.right:
                    self.ax.plot([x, x + dx], [y, y - 20], color=node.right.color if hasattr(node.right, 'color') else 'black')
                    plot_node(node.right, x + dx, y - 20, dx // 2, current_path)

        plot_node(root, x, y, dx)
        self.ax.axis('off')

        if animate:
            self.canvas.draw()
        else:
            self.canvas.draw_idle()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TreeVisualizer()
    ex.setWindowTitle('Tree Visualizer')
    ex.setGeometry(100, 100, 800, 600)
    ex.show()
    sys.exit(app.exec_())

# 29,88,97,25,83,43,33,24,32,85,100,86,12,23,27,41