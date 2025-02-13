import csv
import timeit
from BTrees.OOBTree import OOBTree
from colorama import Fore, Style


def load_data(filename):
    """Load item data from a CSV file.

    Args:
        filename (str): Path to the CSV file.

    Returns:
        list: A list of dictionaries containing item data.
    """
    items = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['ID'] = int(row['ID'])
            row['Price'] = float(row['Price'])
            items.append(row)
    return items


def add_item_to_tree(tree, item):
    """Add an item to an OOBTree.

    Args:
        tree (OOBTree): The OOBTree structure.
        item (dict): Item data with ID as key.
    """
    tree[item['ID']] = item


def add_item_to_dict(dictionary, item):
    """Add an item to a dictionary.

    Args:
        dictionary (dict): The dictionary structure.
        item (dict): Item data with ID as key.
    """
    dictionary[item['ID']] = item


def range_query_tree(tree, min_price, max_price):
    """Perform a range query on an OOBTree.

    Args:
        tree (OOBTree): The OOBTree structure.
        min_price (float): Minimum price.
        max_price (float): Maximum price.

    Returns:
        list: Items within the specified price range.
    """
    return [item for _, item in tree.items() if
            min_price <= item['Price'] <= max_price]


def range_query_dict(dictionary, min_price, max_price):
    """Perform a range query on a dictionary.

    Args:
        dictionary (dict): The dictionary structure.
        min_price (float): Minimum price.
        max_price (float): Maximum price.

    Returns:
        list: Items within the specified price range.
    """
    return [item for item in dictionary.values() if
            min_price <= item['Price'] <= max_price]


def measure_time(func, *args):
    """Measure execution time of a function over 100 runs.

    Args:
        func (function): The function to measure.
        *args: Arguments to pass to the function.

    Returns:
        float: The total execution time.
    """
    return timeit.timeit(lambda: func(*args), number=100)


if __name__ == "__main__":
    # Завантаження даних з файлу
    filename = "generated_items_data.csv"
    items = load_data(filename)

    # Створення структур даних
    tree = OOBTree()
    dictionary = {}

    # Додавання товарів у структури
    for item in items:
        add_item_to_tree(tree, item)
        add_item_to_dict(dictionary, item)

    # Визначення діапазону цін
    min_price, max_price = 10, 50

    # Вимірювання продуктивності діапазонних запитів
    tree_time = measure_time(range_query_tree, tree, min_price, max_price)
    dict_time = measure_time(range_query_dict, dictionary, min_price,
                             max_price)

    # Виведення результатів у кольорі
    print(
        Fore.GREEN + f"Total range_query time for OOBTree: {tree_time:.6f} seconds" + Style.RESET_ALL)
    print(
        Fore.BLUE + f"Total range_query time for Dict: {dict_time:.6f} seconds" + Style.RESET_ALL)
