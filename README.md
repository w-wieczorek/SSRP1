# New Approaches for String Site-Removal Problem

## Exact algorithms

### QCP

#### Requirements

1. Python 3
2. [Gurobi + Python extension](https://www.gurobi.com/documentation/9.5/quickstart_mac/cs_manual_installation.html#subsubsection:manualinstall)

#### Running

```
usage: experiments.py [-h] [--file FILE] [--k K]

optional arguments:
  -h, --help   show this help message and exit
  --file FILE
  --k K
```

Example:

```
python .\experiments.py --file ..\data\words_100_0100_12_0.010.dat --k 5
```

### ILP

#### Requirements

1. Python 3
2. [CPLEX](https://www.ibm.com/products/ilog-cplex-optimization-studio/cplex-optimizer)
3. [docplex](https://pypi.org/project/docplex/)

#### Running

```
usage: experiments.py [-h] [--file FILE] [--k K]

optional arguments:
  -h, --help   show this help message and exit
  --file FILE
  --k K
```

Example:

```
python .\experiments.py --file ..\data\words_100_0100_12_0.010.dat --k 5
```

## Heuristic algorithms

### Hybrid (QCP + GA)

#### Requirements

1. Python 3
2. [Gurobi + Python extension](https://www.gurobi.com/documentation/9.5/quickstart_mac/cs_manual_installation.html#subsubsection:manualinstall)
3. [Mealpy](https://pypi.org/project/mealpy/)


#### Running

```
usage: experiments.py [-h] [--file FILE] [--k K] [--time_limit_sec TIME_LIMIT_SEC] [--repeats REPEATS]

optional arguments:
  -h, --help            show this help message and exit
  --file FILE
  --k K
  --time_limit_sec TIME_LIMIT_SEC
  --repeats REPEATS
```

Example:

```
python .\experiments.py --file ..\data\words_500_5000_12_0.015.dat --k 10 --time_limit_sec 30 --repeats 1

```

### LNS

#### Requirements

1. Python 3
2. [CPLEX](https://www.ibm.com/products/ilog-cplex-optimization-studio/cplex-optimizer)
3. [docplex](https://pypi.org/project/docplex/)

#### Running

```
python .\experiments.py
```
