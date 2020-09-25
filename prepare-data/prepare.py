import zipfile
from collections import defaultdict
import xlrd
from urllib.request import urlretrieve
from lingpy import *
from pathlib import Path
from tabulate import tabulate

def download_experiment():
    urlretrieve('https://github.com/lingpy/predict-khobwa/archive/v1.0.1.zip',
            'predict-khobwa')
    with open('predict-khobwa', 'rb') as f:
        with zipfile.ZipFile(f) as archive:
            archive.extract(
                str(
                    Path('').joinpath(
                    'predict-khobwa-1.0.1',
                    'predictions-automatic.tsv')))
            archive.extract(
                str(
                    Path('').joinpath(
                    'predict-khobwa-1.0.1',
                    'predictions-manual.tsv')))
            archive.extract(
                str(
                    Path('').joinpath(
                    'predict-khobwa-1.0.1',
                    'data',
                    'bodt-khobwa-cleaned.tsv')))


print('downloading data')
download_experiment()
manual = csv2list(
        str(Path('').joinpath(
            'predict-khobwa-1.0.1', 'predictions-manual.tsv')),
        strip_lines=False)
automatic = csv2list(
        str(Path('').joinpath(
            'predict-khobwa-1.0.1', 'predictions-automatic.tsv')),
        strip_lines=False)

manual = [dict(zip([h.lower() for h in manual[0]], row)) for row in manual[1:]]
automatic = [dict(zip([h.lower() for h in automatic[0]], row)) for row in automatic[1:]]

# check for automatic predictions
print(len(automatic))
print(len(manual))

# load word item data
M = {}
idx2line = {row['id']: i for i, row in enumerate(manual)}
idx2auto = {row['number']: i for i, row in enumerate(automatic)}
mappings = csv2list('mappings.tsv', strip_lines=False)
for row in mappings[1:]:
    for i, (item, best, guess) in enumerate(zip(row[0].split(), row[1].split(' + '),
            row[2].split(' + '))):
        M[item] = [guess, row[0], i]


# make morpheme-based list of predictions
predictions = {}
new_idx = max([int(row['number']) for row in automatic])+1
for row in manual:
    if row['id'] in M:
        predictions[int(row['id'])] = {
                "doculect": row['doculect'],
                "best": row['best'],
                "second": row['2best'],
                "third": row['3best'],
                "guess": M[row['id']][0],
                "notes": row['notes'],
                "cogid": row['cogid'], # modify
                "morpheme": automatic[idx2auto[row['id']]]['morpheme'],
                "order": M[row['id']][2],
                "word": M[row['id']][1],
                "concept": automatic[idx2auto[row['id']]]['concept']
                }
    else:# row['id'] != '888':
        if not '0' in row['pred']:
            predictions[int(row['id'])] = {
                    "doculect": row['doculect'],
                    "best": row['best'],
                    "second": row['2best'],
                    "third": row['3best'],
                    "guess": row['guess'],
                    "notes": row['notes'],
                    "cogid": row['cogid'],
                    "morpheme": automatic[idx2auto[row['id']]]['morpheme'],
                    "order": 0,
                    "word": row['id'],
                    "concept": automatic[idx2auto[row['id']]]['concept']
                    }
        elif row['pred'] == '0 1':
            for i, (a, b) in enumerate(zip(row['guess'].split(' + '),
                row['pred'].split())):
                if b == '0':
                    predictions[new_idx] = {
                        "doculect": row['doculect'],
                        "best": '?',
                        "second": '?',
                        "third": '?',
                        "guess": a,
                        "notes": row['notes'],
                        "cogid": 0,
                        "morpheme": '?',
                        "order": i,
                        "word": str(new_idx) + ' ' + row['id'],
                        }
                    new_idx += 1
                else:
                    predictions[int(row['id'])] = {
                        "doculect": row['doculect'],
                        "best": row['best'],
                        "second": row['2best'],
                        "third": row['3best'],
                        "guess": a,
                        "notes": row['notes'],
                        "cogid": row['cogid'],
                        "morpheme": automatic[idx2auto[row['id']]]['morpheme'],
                        "order": i,
                        "word": str(new_idx-1) + ' ' + row['id'],
                        "concept": automatic[idx2auto[row['id']]]['concept'],
                        }
                    predictions[new_idx-1]['concept'] = predictions[int(row['id'])]['concept']

        elif row['pred'] == '1 0':
            for i, (a, b) in enumerate(zip(row['guess'].split(' + '),
                row['pred'].split())):
                if b == '0':
                    predictions[new_idx] = {
                        "doculect": row['doculect'],
                        "best": '?',
                        "second": '?',
                        "third": '?',
                        "guess": a,
                        "notes": row['notes'],
                        "cogid": 0,
                        "morpheme": '?',
                        "order": i,
                        "word": row['id'] + ' ' + str(new_idx),
                        "concept": automatic[idx2auto[row['id']]]['concept'],
                        }
                    new_idx += 1
                else:
                    predictions[int(row['id'])] = {
                        "doculect": row['doculect'],
                        "best": row['best'],
                        "second": row['2best'],
                        "third": row['3best'],
                        "guess": a,
                        "notes": row['notes'],
                        "cogid": row['cogid'],
                        "morpheme": automatic[idx2auto[row['id']]]['morpheme'],
                        "order": i,
                        "word": row['id'] + ' ' + str(new_idx),
                        "concept": automatic[idx2auto[row['id']]]['concept']
                        }


from_auto = {}
for i, row in enumerate(automatic):
    from_auto[row['language'], row['cognateset']] = i
to_auto = {}
for i, row in enumerate(manual):
    to_auto[row['id']] = from_auto[
            {
                "Khis": "Khispi",
                "Duhum": "Duhumbi",
                }.get(row['doculect'],
        row['doculect']), row['cogid']]
idx2auto = to_auto


# load data with attested forms
D = {0: [
    'doculect',
    'concept',
    'concept_predicted',
    'doculect_in_source',
    'form',
    'tokens',
    'crossids',
    'cogids',
    'morphemes',
    'alignment',
    'note']}
number = 1
attested_values = csv2list('prediction-results.tsv', strip_lines=False)
for line in attested_values[1:]:
    row = dict(zip(
        ['id', 'cogid', 'doculect', 'concept', 'best', 'second', 'third', 
            'guess', 'attested', 'note', 'attested_2', 'note_2'],
        line))
    words = predictions[int(row['id'])]['word'].split()
    concept = ''
    morphemes, morphemes2 = [], []
    cogids, crossids, cogids2, crossids2 = [], [], [], []
    best, second, third = [], [], []
    guess = []
    attested = []
    for word in words:
        if word in idx2auto:
            concept = automatic[idx2auto[word]]['concept']
            doculect = automatic[idx2auto[word]]['language']
            break
    if not concept:
        print(line)
        input()
    
    for word in words:
        if word in idx2auto:
            best += [automatic[idx2auto[word]]['word1']]
            second += [automatic[idx2auto[word]]['word2']]
            third += [automatic[idx2auto[word]]['word3']]
            morphemes += [automatic[idx2auto[word]]['morpheme']]
            morphemes2 += [automatic[idx2auto[word]]['morpheme']]
            guess += [predictions[int(word)]['guess']]
            crossids += [automatic[idx2auto[word]]['cognateset']]
            cogids += [word]
            crossids2 += [automatic[idx2auto[word]]['cognateset']]
            cogids2 += [word]
        else:
            cogids2 += [str(word)]
            crossids2 += ['0']
            guess += [predictions[int(word)]['guess']]
            morphemes2 += ['?']

    D[number] = [
            doculect+' BEST',
            concept,
            '',
            doculect,
            ' + '.join(best),
            ' + '.join(best),
            ' '.join(crossids),
            ' '.join(cogids),
            ' '.join(morphemes),
            '', ''
            ]
    D[number+1] = [
            doculect+' GUESS',
            concept,
            '',
            doculect,
            ' + '.join(guess),
            ' + '.join(guess),
            ' '.join(crossids2),
            ' '.join(cogids2),
            ' '.join(morphemes2),
            '', ''
            ]
    D[number+3] = [
            doculect+' SECOND',
            concept,
            '',
            doculect,
            ' + '.join(second),
            ' + '.join(second),
            ' '.join(crossids),
            ' '.join(cogids),
            ' '.join(morphemes),
            '', ''
            ]
    D[number+4] = [
            doculect+' THIRD',
            concept,
            '',
            doculect,
            ' + '.join(third),
            ' + '.join(third),
            ' '.join(crossids),
            ' '.join(cogids),
            ' '.join(morphemes),
            '', ''
            ]
    if row['note'].startswith('c'):
        D[number+2] = [
                doculect+' ATTESTED',
                concept,
                concept,
                doculect,
                row['attested'],
                row['attested'],
                ' '.join(crossids2),
                ' '.join(cogids2),
                ' '.join(morphemes),
                '', row['note']]
    elif row['attested'].strip():
        D[number+2] = [
                doculect+' ATTESTED',
                concept,
                concept,
                doculect,
                row['attested'] or 'Ø',
                row['attested'] or 'Ø',
                len(row['attested'].replace('_', '+').split('+')) * ['?'],
                len(row['attested'].replace('_', '+').split('+')) * ['?'],
                len(row['attested'].replace('_', '+').split('+')) * ['?'],
                '', row['note']]

    if row['note_2'].startswith('c'):
        D[number+5] = [
                doculect+' ATTESTED',
                concept,
                concept,
                doculect,
                row['attested_2'],
                row['attested_2'],
                ' '.join(crossids2),
                ' '.join(cogids2),
                ' '.join(morphemes),
                '', row['note_2']]
    elif row['attested_2'].strip():
        D[number+5] = [
                doculect+' ATTESTED',
                concept,
                concept,
                doculect,
                row['attested_2'] or 'Ø',
                row['attested_2'] or 'Ø',
                len(row['attested_2'].replace('_', '+').split('+')) * ['?'],
                len(row['attested_2'].replace('_', '+').split('+')) * ['?'],
                len(row['attested_2'].replace('_', '+').split('+')) * ['?'],
                '', row['note_2']]


    number += 6

Wordlist(D).output('tsv', filename='predictions', prettify=False)


comps = []
for idxA, idxB in idx2auto.items():
    rowB = manual[idx2line[idxA]]
    rowA = automatic[idxB]

    comps += [[
        idxA,
        rowA['number'],
        rowA['language'],
        rowA['concept'],
        rowA['morpheme'],
        rowA['cognateset'],
        rowA['word1'],
        rowB['best'],
        rowA['word2'],
        rowB['2best'],
        rowA['word3'],
        rowB['3best'],
        rowB['guess'],
        rowB['notes'],
        '!' if rowA['word1'] != rowB['best'] else ''
        ]]
        
with open('comparison.tsv', 'w') as f:
    f.write('\t'.join([
        'AutoID', 'ManuID', 'Language', 'Concept', 'Morpheme', 'AutoBest',
        'ManuBest', 'Auto2', 'Manu2', 'Auto3', 'Manu3', 'Guess',
        'Notes'])+'\n')
    for row in comps:
        f.write('\t'.join(row)+'\n')
