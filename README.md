# Graphene Sql Alchemy Optmizer
(WIP)
inspired by https://github.com/tfoxy/graphene-django-optimizer

[![Build Status](https://travis-ci.org/colanconnon/graphene_sa_optimizer.svg?branch=master)](https://travis-ci.org/colanconnon/graphene_sa_optimizer)

Uses graphql schema to generate efficient database access using sql alchemy joins
## How to use 
```python
from graphene_sa_optimizer import get_optimized_joins

# This will generate all our options
# to optimize this query
get_optimized_joins(ModelClass, info)

# pass those optimizations into our query
query.options(*get_optimized_joins)
```
## Setup for dev
* Install `pipenv`
* run `pipenv install`
* run `pipenv shell`
* run `pytest`

