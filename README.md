# Anu

> This project is not completed.

Predicting interactions among protein, DNA and RNA.

## Getting Started

### Requirement
* git
* python 3.8 or above

## Developing

### Clone this repository

```bash
git clone https://github.com/ankitskvmdam/anu.git
```

### Create a python virtual env

```bash
python -m venv venv     # create python environment
. ./venv/bin/activate    # activate python enviroment
```

### Install poetry

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```
or

```bash
pipx install poetry
```

For more information about poetry visit [poetry docs](https://python-poetry.org/docs/)

### Install nox

```bash
pip install nox
```
### Nox

Run tests, lint check, type check, doc tests, coverage
```bash
nox
```

For more information visit [nox tutorial](https://nox.thea.codes/en/stable/tutorial.html)

## Using
In order to use this tool. First few steps are similar to developing step.

### Clone this repository

```bash
git clone https://github.com/ankitskvmdam/anu.git
```


### Install poetry

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```
or

```bash
pipx install poetry
```

### Install anu
Now you have to run the following command
```bash
# First move to the directory
cd anu

# Installing anu
poetry install
```


### Initial steps

#### Step 1: Download the databases.
* Pickle - Interacting protein database
* Negatome - Non-interacting protein database
> Currently there is no way to specify anu to download only one databases. This feature will be implemented in future release.
```bash
# Download both databases
anu data fetch databases

# For help/more information
anu data fetch databases --help
```

#### Step 2: Prepare dataframe
* Pickle dataset dataframe (vaex dataframes)
* Negatome dataset dataframe (vaex dataframes)
> Currently there is no way to specify anu to make individual dataframes. This feature will be implemented in future release.
```bash
# Prepare pickle and negatome dataframe
anu data prepare dataframes

# For help/more information
anu data prepare dataframes -- help
```

#### Step 3: Fetch PDB files
Now we have to fetch the PDB file.
> Since there are almost 30,000 proteins in pickle database and around 10,000 in negative database. It is hard to fetch them all at once. The fetching process is resumable. And for testing only 300 to 400 files for each dataset is enough. So once you have downloaded enough file you can press ctrl+c to exit.
```bash
# For help/more information
anu data fetch pdb --help

# Fetch pdb files for protein present in pickle dataset
anu data fetch pdb -p
# or
anu data fetch pdb --pickle

# Fetch pdb file for protein present in negatome dataset
anu data fetch pdb -n
# or
anu data fetch pdb --negatome

# Fetch pdb file from both data set
anu data fetch pdb
```

If the pdb file is already downloaded it will not be downloaded again. Downloading of pdb files is sync between both datasets.

#### Step 4: Prepare input for train
This is also a time taking process.

```bash
# For help/more information
anu data prepare inputs --help

# Prepare interacting protein dataframe
anu data prepare inputs -i
# or
anu data prepare inputs --interacting

# Prepare non interacting protein dataframe
anu data prepare inputs -n
# or
anu data prepare inputs --non-interacting

# Prepare both input dataframes
anu data prepare inputs
```

#### Step 5: Train model
Currently cnn model is only available.

```bash
anu train cnn
```

#### Step 6: Predict
Before prediction you have to train the model.

```bash
# For help/more information
anu predict protein --help

# given pdb id as input
anu predict protein -p "1gzx" "4hh3"

# give uniprot id as input
anu predict protein -u "F4JRB0" "Q8RX29"

# give path as input
anu predict protein "path/to/protein/a.pdb" "path/to/protein/b.pdb"
```
