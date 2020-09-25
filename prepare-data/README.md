# Prepare the Data for Evaluation

## Requirements

* lingpy

## Usage

This code was used to prepare the prediction data, which was then manually updated. To run the code, just type:

```
$ python prepare.py
```

It combines the previous predictions which were done manually with those which were done automatically by downloading them from the GitHub repository where they are versionized, along with the attested forms and then creates a file `predictions.tsv`, which we submit in *manually edited form* in the main folder of the repository. 
