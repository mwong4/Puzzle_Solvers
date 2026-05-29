# Wordle Solver

This is a tool used to solve Wordle

## How to Use

### Dependencies

Install Pandas

```python
pip install pandas
```

### Pre-Processor

Run this to train the model

```python
py pre_process.py
```

### Solving

This is for typical use, it solving the daily Wordle

Main (defined at the bottom of solver.py) should look like the following
`

```python
if __name__ == '__main__':
    words = pre_solver(False)
    solver_wrapper("somereallylongwordover5letters", False, False, words, INITIAL_GUESSES)
```

```python
py solver.py # Run the script in terminal like this
```

### Evaluating Model

This is for evaluating the present model/inputs. Will output metrics like the following:

```
Average Attempt Count: 4.552406597105351
Number of 7+'s: 1332 (8.97%)
```

Use this tool in order to optimize the solver.

Main (defined at the bottom of solver.py) should look like the following

```python
if __name__ == '__main__':
    words = pre_solver(False)
    testing_runner()
```

Run via

```python
py solver.py  # Run the script in terminal like this
```

## Additional Resources

You can play this with the original new york times version, or Wordle Unlimited:

- https://www.nytimes.com/games/wordle/index.html
- https://wordleunlimited.org/
