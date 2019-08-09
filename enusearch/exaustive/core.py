import functools
import itertools
import logging
import multiprocessing
import time

from .utils import wrapper

def solve(obj_func, candidates, order, f_min=True, selection_size=None, n_jobs=None, verbose=False):
    """
    Solver to find the optimal combination or permutation of candidates using exaustive enumeration

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

        n_jobs: int default 1
            The number of jobs to run in parallel.
                If n_jobs is -1 all CPUs are used
                If n_jobs is -2 all but one CPU are used
        
        verbose: bool, default False
            Sets the verbosity of the solver

    Returns:
        a list with the optimal solution

    Example:

        >>> candidates = [2,4,5,6,3,1,7]

        >>> # e.g. obj_func([a, b, c, d, e]) ==> a + b + c + d + e
        >>> def obj_func(x): return sum(x)

        >>> # maximize the obj function
        >>> solution = exaustive.solve(obj_func, candidates, order=False, f_min=False, selection_size=5)

    TODO:
        - Implement constraint system
    """
    if verbose:
        logging.basicConfig(format="%(message)s", level=logging.INFO)
    
    start = time.time()
    selection_size = selection_size or len(candidates)
    m = 2 * f_min - 1

    n_jobs = n_jobs or 1
    if n_jobs == -1:
        n_jobs = None
    elif n_jobs == -2:
        n_jobs = multiprocessing.cpu_count() - 1

    if order:
        iterable = itertools.permutations(candidates, selection_size)
    else:
        iterable = itertools.combinations(candidates, selection_size)
    
    wrapped = functools.partial(wrapper, obj_func=obj_func, m=m)
    
    pool = multiprocessing.Pool(n_jobs)
    results = sorted(pool.map(wrapped, iterable), key=lambda x: x["value"])
    iterations = len(results)
    best_candidate = results[0]["position"]

    logging.info("Evaluations: {}".format(iterations))
    logging.info("Duration: {:.3f}s".format(time.time() - start))
    
    return best_candidate