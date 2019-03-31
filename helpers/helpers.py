import os


def find_in_array(arr, predicate):
    return next(x for x in arr if predicate(x))


def is_file_exists_in_dir(current_currency_pair_path, filename):
    files_in_current_directory = [f for f in os.listdir(current_currency_pair_path) if
                                  os.path.isfile(os.path.join(current_currency_pair_path, f))]

    for f in files_in_current_directory:
        if filename in f:
            return True

    return False

