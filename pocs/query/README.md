Query POC
=========

Overview
--------

This poc will query an Azure Cognitive Search for relevant documents using a
vector search (set to 3) and then passes the documents and a prompt to Azure
OpenAI to construct an answer.

`index.py` is an example using the Langchain library\
`index_raw.py` is an example using raw commands and our own custom prompt which
is useful for learning.

Requirements
------------

 - Python 3.11
 - Pip
 - Pipenv

Install
-------

`pipenv install`

Copy `.env.example` to `.env` and enter the required values.

How To Use
----------

```bash
pipenv run python index.py
```
or
```bash
pipenv run python index_raw.py
```

`.env` will be automatically loaded by pipenv.
