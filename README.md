# Enusearch

A collection of enumerative search algorithms for combinatorial optimization

## Instalation
To use enusearch directly from this repository use:
```
$ python setup.py install
# or
$ pip install -e .
```

If you want to contribute to this repository use instead:
```
$ python setup.py develop
# or
$ pip install -e .[dev]
# or even
$ make install
```

## How to use
```python
from enusearch import branch_and_bound, exaustive

# define an objective function to optimize
def obj_func(x):
    return sum([a / (i + 1) for i, a in enumerate(x)])

# list of possible candidates
candidates = list(range(1, 11))

# minimize the obj function
result = branch_and_bound.solve(obj_func, candidates, order=True, selection_size=5)
print(result, obj_func(result))
result = exaustive.solve(obj_func, candidates, order=True, selection_size=5)
print(result, obj_func(result))
```