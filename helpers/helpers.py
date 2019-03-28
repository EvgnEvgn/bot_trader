def find_in_array(arr, predicate):
    return next(x for x in arr if predicate(x))

