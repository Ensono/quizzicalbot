Re-Index POC
============

Overview
--------

This poc takes all the files in a Blob storage container and prefix and uploads
them to Azure Cognitive Search with vectors.

NOTE: If this is run more than once you'll end up with duplicate uploads which
is obviously less than ideal.

Requirements
------------

 - Python 3.11
 - Pip

Install
-------

`pip install -r requirements.txt`

Copy `.env.example` to `.env` and enter the required values.

How To Use
----------

```bash
. .env
python index.py
```
