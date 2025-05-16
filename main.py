import random
import logging


def generate_random_sequence():
    size = random.randint(1, 20)
    sequence = [random.randint(0, 1000) for _ in range(size)]
    return sequence


class BinaryTreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = BinaryTreeNode(value)
        if self.root is None:
            self.root = new_node
        else:
            self._insert_recursive(self.root, new_node)

    def _insert_recursive(self, current_node, new_node):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        if new_node.value < current_node.value:
            if current_node.left is None:
                current_node.left = new_node
                new_node.parent = current_node
                logger.info(
                    f"Inserted {new_node.value} as left child of {current_node.value}")
            else:
                self._insert_recursive(current_node.left, new_node)
        else:
            if current_node.right is None:
                current_node.right = new_node
                new_node.parent = current_node
                logger.info(
                    f"Inserted {new_node.value} as right child of {current_node.value}")
            else:
                self._insert_recursive(current_node.right, new_node)

    def print_tree(self):
        if self.root is not None:
            self._print_tree_recursive(self.root)

    def _print_tree_recursive(self, node, prefix="", is_left=True):
        if node is not None:
            if node.right:
                new_prefix = prefix + ("│   " if is_left else "    ")
                self._print_tree_recursive(node.right, new_prefix, False)
            print(
                prefix + ("└── " if is_left else "┌── ") + str(node.value))
            if node.left:
                new_prefix = prefix + ("    " if is_left else "│   ")
                self._print_tree_recursive(node.left, new_prefix, True)

    def print_tree(self):
        if self.root is not None:
            self._print_tree_recursive(self.root)

    def delete(self, value):
        node_to_delete = self._find(self.root, value)
        if node_to_delete is None:
            print(f"Ошибка: узел со значением {value} не найден.")
            return False
        self._delete_node(node_to_delete)
        print(f"Узел со значением {value} успешно удалён.")
        return True

    def _find(self, node, value):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        if node is None:
            logger.info(f"Поиск: узел со значением {value} не найден.")
            return None
        if value == node.value:
            logger.info(f"Поиск: найден узел со значением {value}.")
            return node
        elif value < node.value:
            logger.info(
                f"Поиск: идём влево от {node.value} для поиска {value}.")
            return self._find(node.left, value)
        else:
            logger.info(
                f"Поиск: идём вправо от {node.value} для поиска {value}.")
            return self._find(node.right, value)

    def _delete_node(self, node):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        if node.left is None:
            logger.info(
                f"Удаление узла {node.value}, у него нет левого потомка.")
            self._transplant(node, node.right)
        elif node.right is None:
            logger.info(
                f"Удаление узла {node.value}, у него нет правого потомка.")
            self._transplant(node, node.left)
        else:
            successor = self._minimum(node.right)
            logger.info(
                f"Удаление узла {node.value}, у него два потомка. Следующий по порядку: {successor.value}")
            if successor.parent != node:
                self._transplant(successor, successor.right)
                successor.right = node.right
                if successor.right:
                    successor.right.parent = successor
                logger.info(
                    f"Трансплантация преемника {successor.value} на место правого потомка.")
            self._transplant(node, successor)
            successor.left = node.left
            if successor.left:
                successor.left.parent = successor
            logger.info(
                f"Узел {successor.value} теперь на месте удалённого узла {node.value}.")

    def _transplant(self, u, v):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        if u.parent is None:
            self.root = v
            logger.info(
                f"Трансплантация: корень дерева теперь {v.value if v else None}")
        elif u == u.parent.left:
            u.parent.left = v
            logger.info(
                f"Трансплантация: {u.value} заменён на {v.value if v else None} в качестве левого потомка")
        else:
            u.parent.right = v
            logger.info(
                f"Трансплантация: {u.value} заменён на {v.value if v else None} в качестве правого потомка")
        if v is not None:
            v.parent = u.parent

    def _minimum(self, node):
        while node.left is not None:
            node = node.left
        return node

    def add(self, value):
        if self._find(self.root, value):
            print(f"Ошибка: узел со значением {value} уже существует.")
            return False
        self.insert(value)
        print(f"Узел со значением {value} успешно добавлен.")
        return True


if __name__ == "__main__":
    random_sequence = generate_random_sequence()
    print("Сгенерированная последовательность:", random_sequence)

    binary_tree = BinaryTree()
    for value in random_sequence:
        binary_tree.insert(value)

    print("Элементы вставлены в бинарное дерево.")
    binary_tree.print_tree()
    print("Выберите функцию\n1.Добавить\n2.Удалить\n3.Поиск")
    choice = input("Введите номер функции: ")
    if choice == "1":
        value = int(input("Введите значение для добавления: "))
        binary_tree.add(value)
        binary_tree.print_tree()
    elif choice == "2":
        value = int(input("Введите значение для удаления: "))
        binary_tree.delete(value)
        binary_tree.print_tree()
    elif choice == "3":
        value = int(input("Введите значение для поиска: "))
        node = binary_tree._find(binary_tree.root, value)
        if node:
            print(f"Узел со значением {value} найден.")
        else:
            print(f"Узел со значением {value} не найден.")
    else:
        print("Некорректный выбор.")
