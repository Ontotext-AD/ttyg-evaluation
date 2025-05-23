# Contribution Guide

Please make sure your code passes tests and includes coverage for new logic.

## Set up an environment with conda and poetry

### Prerequisites

You should install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html). `miniconda`
will suffice.

#### First time setup (if conda lock and poetry lock are not present)

To create conda environment and install dependencies:

```bash
conda env create -f environment.yml
conda activate ttyg-evaluation
conda-lock -k explicit --conda mamba
poetry lock
conda deactivate
conda remove --name ttyg-evaluation --all
git add environment.yml conda-*.lock
git add pyproject.toml poetry.lock
git commit
```

### Create the environment

```bash
conda create --name ttyg-evaluation --file conda-linux-64.lock
conda activate ttyg-evaluation
poetry install
```

## Run tests

```sh
conda activate ttyg-evaluation
poetry install --with test
poetry run pytest --cov=ttyg_evaluation --cov-report=term-missing tests/
```
