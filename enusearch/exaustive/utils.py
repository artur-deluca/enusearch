def wrapper(candidate, obj_func, m):
    return {"value": m * obj_func(candidate), "position": candidate}