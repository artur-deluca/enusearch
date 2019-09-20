import logging
import time

from .utils import find_initial_bound, generate_branches, get_min_node_index, subspace_builder


def solve(obj_func, candidates, order, f_min=True, selection_size=None, verbose=False):
    """
    Solver to find the optimal combination or permutation of candidates using Branch and Bound.

    Implementation based on:
        Narendra, P. M. and Fukunaga, K. (1977)
            A Branch and Bound Algorithm for Feature Subset Selection

    Args:
        obj_func: objective function (or method) to be optimized.
            Must only accept the candidates as input.
            If the inherited structure does not allow it,
            use `functools.partial` to comply

        candidates: list of available candidates to the objective function

        order: bool that indicates whether the order of choice matters.
            If order is True, the solver seeks the best permutation of candidates.
            If False, it seeks the best combination of candidates.

        f_min: bool, default True
            Minimize or maximize the objective function
        
        selection_size: int, default None
            Number of candidates to compose a solution.
            If not provided, the selection size will be equal to the number of candidates
        
        verbose: bool, sets the verbosity of the solver

    Returns:
        a list with the optimal solution

    Example:

        >>> candidates = [2,4,5,6,3,1,7]

        >>> # e.g. obj_func([a, b, c, d, e]) ==> a + b + c + d + e
        >>> def obj_func(x): return sum(x)

        >>> # maximize the obj function
        >>> solution = branch_and_bound(obj_func, candidates, order=False, f_min=False, selection_size=5)

    TODO:
        - Implement constraint system
    """

    start = time.time()
    selection_size = selection_size or len(candidates)
    m = 2 * f_min - 1
    get_subspaces = subspace_builder(order, candidates)
    
    if verbose:
        logging.basicConfig(format="%(message)s", level=logging.INFO)

    if order:
        splits = [[i] for i in candidates]
        stack = generate_branches(obj_func, splits, m)
    else:
        stack = generate_branches(obj_func, [candidates], m)
    
    # best_candidate, bound = find_initial_bound(stack, get_subspaces, selection_size, obj_func, m)
    bound = float("inf")
    iteration = 0
    while stack:
        node = stack.pop()
        iteration += 1
        # the smaller the opt_value the better
        if bound > node["value"]:
            if iteration % 1000 == 0:
                logging.info(
                    (
                        "Iteration {}"
                        "Elapsed time: {:.3f}"
                        "Best value found: {}"
                    ).format(iteration, time.time() - start, bound)
                )
            children = generate_branches(obj_func, get_subspaces(space=node["position"]), m)
            if children and len(children[0]["position"]) == selection_size:
                if children[-1]["value"] < bound:
                    bound = children[-1]["value"]
                    best_candidate = children[-1]["position"]
                    
            else:
                # it wont extend them to the list because they were already analyzed
                # and if they were included it would make the algorithm run slower
                stack.extend(children)
                stack.sort(reverse=True, key=lambda x: x["value"]) # push lowest opt_value last

    logging.info("Evaluations: {}".format(iteration))
    logging.info("Duration: {:.3f}".format(time.time() - start))
    return best_candidate