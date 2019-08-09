import itertools
import functools

from collections import Counter

def get_min_node_index(stack):
    values = [x["value"] for x in stack]
    return values.index(min(values))

def find_initial_bound(stack, get_subspaces, selection_size, obj_func, m):
    if selection_size != len(stack[0]["position"]):

        index = get_min_node_index(stack)
        stack = generate_branches(obj_func, get_subspaces(space=stack[index]["position"]), m)
        best_candidate, bound = find_initial_bound(stack, get_subspaces, selection_size, obj_func, m)

    else:

        solution = stack[get_min_node_index(stack)]
        best_candidate, bound = solution["position"], solution["value"]

    return best_candidate, bound

def subspace_builder(order, candidates):
    if order:
        def _get_subspaces(candidates, space):
            candidates = list(
                itertools.chain.from_iterable(
                    [
                        x*[k]
                        for k, x in (Counter(candidates)-Counter(space)).items()
                        if x > 0]
                )
            )
            return [space + [x] for x in candidates]
        get_subspaces = functools.partial(_get_subspaces, candidates=candidates)

    else:
        def get_subspaces(self, space):
            return list(itertools.combinations(space, len(space)-1))
    
    return get_subspaces

def generate_branches(obj_func, splits, m):
        stack = [{"position": i, "value": m * obj_func(i)} for i in splits]    
        stack.sort(reverse=True, key=lambda x: x["value"])
        return stack

