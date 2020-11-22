# Data and Code Accompanying the Study on "Benefits of reflex prediction: A case study of Western Kho-Bwa" 

## Source of the Dataset

Cite the source of the dataset as:

> Timotheus A. Bodt and Johann-Mattis List (to appear): Benefits of reflex prediction: A case study of Western Kho-Bwa. Diachronica.

## Overview

The main data we submit in this repository is an extensively annotated file named `predictions.tsv`. This file itself was automatically generated from double-checking the original predictions we made (both automatic and manual) and merging it with the attested forms, which were for convenience stored in a single spreadsheet. Since the comparison itself requires to align the data and also identify to which degree attested forms coincide with predicted ones, this work was *manually* carried out in the [EDICTOR](https://digling.org/edictor/) tool and then stored in the form of a simple TSV file (named file `predictions.tsv`). 

In order to allow for a convenient editing of the data, we have used a server-based version of the EDICTOR, by which the data can be accessed online without uploading the file. This version is accessible from the link:

```
http://digling.org/edictor/?remote_dbase=predictions&file=predictions&basics=DOCULECT|CONCEPT|CONCEPT_PREDICTED|FORM|TOKENS|COGIDS|MORPHEMES|NOTE&columns=DOCULECT|CONCEPT|CONCEPT_PREDICTED|DOCULECT_IN_SOURCE|FORM|TOKENS|CROSSIDS|COGIDS|MORPHEMES|ALIGNMENT|NOTE&split_on_tones=false&async=true&root_formatter=COGIDS
```

## Dependencies

In order to run the code, you will need the following packages:

* lingpy
* tabulate

To install these, provided you have Python (version 3.5 or higher) and PIP installed, you can just type:

```
$ pip install tabulate
$ pip install lingpy
```

## Running the code for evaluating the predictions

The code uses the specific annotation of partial cognates as mentioned in the study in order to trace both those cases where lexemes have been perfectly predicted and those individual cases where successfully predicted morphemes are compared phonetically with their attested counterparts. To run the code, just type:

```
$ python evaluate.py
```

The output will first produce various tables which are for conveniency encoded in HTML (to allow for a quick pasting of the tables into spreadsheets and DOC formats), and also printed onto the terminal. The output looks as follows.

```
### 1. Lexical Predictions

| doculect   |   predictions |   verified |   full |   part |   semi |   missing |   proportion |
|:-----------|--------------:|-----------:|-------:|-------:|-------:|----------:|-------------:|
| Duhumbi    |            19 |         19 |      3 |      1 |      7 |         8 |       0.5789 |
| Jerigaon   |           109 |         80 |     53 |      3 |      6 |        18 |       0.7750 |
| Khispi     |            39 |         37 |     18 |      3 |      5 |        11 |       0.7027 |
| Khoina     |            72 |         66 |     30 |      4 |      4 |        28 |       0.5758 |
| Khoitam    |            53 |         49 |     26 |      8 |      5 |        10 |       0.7959 |
| Rahung     |            65 |         56 |     28 |     11 |      6 |        11 |       0.8036 |
| Rupa       |            46 |         40 |     15 |      6 |      4 |        15 |       0.6250 |
| Shergaon   |           116 |        107 |     62 |     12 |      7 |        26 |       0.7570 |
| total      |           519 |        454 |    235 |     48 |     44 |       127 |       0.7203 |

### 2. Human Predictions

| doculect   |   words |   morphemes |   perfect |   proportion |   score |
|:-----------|--------:|------------:|----------:|-------------:|--------:|
| Duhumbi    |      11 |          14 |        10 |       0.7143 |  0.8690 |
| Jerigaon   |      62 |          83 |        51 |       0.6145 |  0.7992 |
| Khispi     |      26 |          33 |        19 |       0.5758 |  0.7828 |
| Khoina     |      38 |          48 |        20 |       0.4167 |  0.6875 |
| Khoitam    |      39 |          54 |        28 |       0.5185 |  0.7685 |
| Rahung     |      45 |          53 |        29 |       0.5472 |  0.7453 |
| Rupa       |      25 |          33 |        15 |       0.4545 |  0.6616 |
| Shergaon   |      81 |          99 |        49 |       0.4949 |  0.7340 |
| total      |     327 |         417 |       221 |       0.5300 |  0.7560 |

### 3. Predictions (Automated, one candidate)

| doculect   |   words |   morphemes |   perfect |   proportion |   score |
|:-----------|--------:|------------:|----------:|-------------:|--------:|
| Duhumbi    |      11 |          13 |         6 |       0.4615 |  0.6923 |
| Jerigaon   |      62 |          73 |        34 |       0.4658 |  0.6963 |
| Khispi     |      26 |          31 |        13 |       0.4194 |  0.7097 |
| Khoina     |      38 |          45 |        16 |       0.3556 |  0.6593 |
| Khoitam    |      39 |          47 |        23 |       0.4894 |  0.7340 |
| Rahung     |      45 |          48 |        24 |       0.5000 |  0.7153 |
| Rupa       |      25 |          31 |        13 |       0.4194 |  0.6505 |
| Shergaon   |      81 |          91 |        40 |       0.4396 |  0.6923 |
| total      |     327 |         379 |       169 |       0.4459 |  0.6937 |

### 4. Predictions (Automated, up to two candidates)

| doculect   |   words |   morphemes |   perfect |   proportion |   score |
|:-----------|--------:|------------:|----------:|-------------:|--------:|
| Duhumbi    |      11 |          13 |         6 |       0.4615 |  0.6923 |
| Jerigaon   |      62 |          73 |        34 |       0.4658 |  0.7169 |
| Khispi     |      26 |          31 |        13 |       0.4194 |  0.7151 |
| Khoina     |      38 |          45 |        16 |       0.3556 |  0.6667 |
| Khoitam    |      39 |          47 |        23 |       0.4894 |  0.7447 |
| Rahung     |      45 |          48 |        24 |       0.5000 |  0.7292 |
| Rupa       |      25 |          31 |        13 |       0.4194 |  0.6559 |
| Shergaon   |      81 |          91 |        40 |       0.4396 |  0.7051 |
| total      |     327 |         379 |       169 |       0.4459 |  0.7032 |

### 5. Predictions (Automated, up to three candidates)

| doculect   |   words |   morphemes |   perfect |   proportion |   score |
|:-----------|--------:|------------:|----------:|-------------:|--------:|
| Duhumbi    |      11 |          13 |         6 |       0.4615 |  0.7179 |
| Jerigaon   |      62 |          73 |        34 |       0.4658 |  0.7192 |
| Khispi     |      26 |          31 |        13 |       0.4194 |  0.7151 |
| Khoina     |      38 |          45 |        16 |       0.3556 |  0.6728 |
| Khoitam    |      39 |          47 |        23 |       0.4894 |  0.7482 |
| Rahung     |      45 |          48 |        24 |       0.5000 |  0.7292 |
| Rupa       |      25 |          31 |        13 |       0.4194 |  0.6649 |
| Shergaon   |      81 |          91 |        40 |       0.4396 |  0.7088 |
| total      |     327 |         379 |       169 |       0.4459 |  0.7095 |

```



