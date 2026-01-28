# Genetic Algorithm Optimization Framework

This project implements a **modular Genetic Algorithm (GA) framework in Python**, designed to experiment with different evolutionary strategies such as initialization methods, selection mechanisms, crossover operators, and mutation operators.  
It also includes **grid search utilities** for hyperparameter tuning and visualization support.

---

## Project Structure

```
genetic-algorithm-optimization/
│
├── algorithm/
│   ├── algorithm.py        # Core genetic algorithm logic
│   ├── grid_search.py      # Hyperparameter tuning using grid search
│
├── initializers/
│   ├── individual.py       # Individual representation
│   ├── population.py      # Population initialization
│   ├── test_data.py        # Test datasets / fitness functions
│
├── operators/
│   ├── crossovers.py       # Crossover operators
│   ├── mutators.py         # Mutation operators
│   ├── selectors.py        # Selection strategies
│
├── results/
│   └── ...                 # Output files, plots, or CSV results
│
└── README.md
```

---

## Features

- Modular **Genetic Algorithm** implementation  
- Customizable:
  - Population initialization
  - Selection strategies
  - Crossover operators
  - Mutation operators
- **Grid search** for hyperparameter optimization
- Fitness tracking and result logging
- Plotting and CSV export support

---

## Requirements

- Python **3.9+**
- Required library:
  - `matplotlib`

Install dependencies with:

```bash
pip install matplotlib
```

---

## How to Run

### Run the Genetic Algorithm

You can run the genetic algorithm by importing and configuring it from `algorithm.py`:

```python
from algorithm.algorithm import genetic_algorithm
```

Configure parameters such as:
- Population size
- Number of generations
- Crossover probability
- Mutation probability
- Selection method

---

### Run Grid Search

To perform hyperparameter tuning using grid search:

```bash
python algorithm/grid_search.py
```

This will test multiple configurations and store the results for comparison.

---

## Output

The framework produces:
- Fitness evolution plots
- CSV files with experiment results
- Best individual and fitness score per run

Results are stored in the `results/` directory.

 Rapid prototyping of evolutionary strategies

---

## Notes

- The framework is intentionally modular and easy to extend.
- New operators or fitness functions can be added with minimal changes.

---

## License

This project is provided for **educational purposes**.  
You are free to use, modify, and extend it.
