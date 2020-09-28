from lingpy import *
from collections import defaultdict
from itertools import combinations, product
from tabulate import tabulate
from pathlib import Path

lex = Wordlist('predictions.tsv')

for idx in lex:
    lex[idx, 'cogids'] = basictypes.ints(lex[idx, 'cogids'])
    lex[idx, 'tokens'] = basictypes.lists(lex[idx, 'tokens'])
    if lex[idx, 'alignment']:
        lex[idx, 'alignment'] = basictypes.lists(lex[idx, 'alignment'])
    else:
        lex[idx, 'alignment'] = lex[idx, 'tokens']

etd = lex.get_etymdict(ref='cogids')

# search for direct matches
docs = sorted(set([d.split(' ')[0] for d in lex.cols]))
table = []
missing = 0
PREDICTED, AUTOMATED, SECOND, THIRD = {}, {}, {}, {}
for doc in docs:
    predicted = {k: v for k, v in lex.get_dict(
            col=doc+' GUESS',
            ).items() if v}
    automated = {k: v for k, v in lex.get_dict(
        col=doc+' BEST').items() if v}
    second = {k: v for k, v in lex.get_dict(
        col=doc+' SECOND').items() if v}
    third = {k: v for k, v in lex.get_dict(
        col=doc+' THIRD').items() if v}

    attested = lex.get_dict(
            col=doc+' ATTESTED')
    totals = sum([len(x) for x in predicted.values()])

    full, part, semi, miss = 0, 0, 0, 0
    now_predicted = 0
    PREDICTED[doc], AUTOMATED[doc] = [], []
    SECOND[doc], THIRD[doc] = [], []
    for concept, idxsA in predicted.items():
        parts, fulls = [], []
        for i, idxAi in enumerate(idxsA):
            missing = False
            for idxA, idxB in product([idxAi], attested[concept]):
                cogidsA, cogidsB = lex[idxA, 'cogids'], lex[idxB, 'cogids']
                if str(cogidsA) == str(cogidsB):
                    fulls += [1]
                elif [c for c in cogidsA if c in cogidsB]:
                    parts += [1]
                if str(lex[idxB, 'tokens']) == 'Ø':
                    missing = True
                    
            if not missing:
                now_predicted += 1
                if 1 in fulls:
                    full += 1
                    PREDICTED[doc] += [idxAi]
                    AUTOMATED[doc] += [automated[concept][i]]
                    SECOND[doc] += [second[concept][i]]
                    THIRD[doc] += [third[concept][i]]
                elif 1 in parts:
                    part += 1
                    PREDICTED[doc] += [idxAi]
                    AUTOMATED[doc] += [automated[concept][i]]
                    SECOND[doc] += [second[concept][i]]
                    THIRD[doc] += [third[concept][i]]
                else:
                    # get index of doculect
                    docIdx = lex.cols.index(doc+' ATTESTED')
                    # search for divergent matches
                    semis = []
                    for idxA in idxsA:
                        cogidsA = lex[idxA, 'cogids']
                        counterparts = [etd[cogid][docIdx] for cogid in cogidsA if \
                                etd[cogid][docIdx]]
                        if counterparts:
                            semis += [1]
                    if 1 in semis:
                        semi += 1
                        PREDICTED[doc] += [idxAi]
                        AUTOMATED[doc] += [automated[concept][i]]
                        SECOND[doc] += [second[concept][i]]
                        THIRD[doc] += [third[concept][i]]
                    else:
                        miss += 1

    table += [[doc, totals, now_predicted, full, part, semi, miss,
        (full+part+semi)/now_predicted]]
table += [['total',
    sum([row[1] for row in table]),
    sum([row[2] for row in table]),
    sum([row[3] for row in table]),
    sum([row[4] for row in table]),
    sum([row[5] for row in table]),
    sum([row[6] for row in table]),
    (
        sum([row[3] for row in table])+
        sum([row[4] for row in table])+
        sum([row[5] for row in table])
    )/sum([row[2] for row in table])
    ]]

print('### 1. Lexical Predictions\n')
print(tabulate(table,
    headers=[
        'doculect',
        'predictions',
        'verified',
        'full',
        'part',
        'semi',
        'missing',
        'proportion'],
    tablefmt='pipe',
    floatfmt='.4f'
    ))

# count accuracy of 
atable = []
errors = defaultdict(list)
S = {d: {} for d in docs}
for doc in docs:
    #print('[i] analysing {0} ({1} concepts)'.format(doc, len(predicted)))
    docIdx = lex.cols.index(doc+' ATTESTED')
    for idx in PREDICTED[doc]:
        cogids = lex[idx, 'cogids']
        words = lex[idx, 'alignment'].n
        if len(cogids) != len(words):
            print(idx, doc, lex[idx, 'concept'])
            raise ValueError
        for wordA, cogid in zip(words, cogids):
            attIdx = etd[cogid][docIdx]
            if attIdx:
                scores = []
                wordB = lex[attIdx[0], 'alignment'].n[lex[attIdx[0],
                    'cogids'].index(cogid)]
                if len(wordA) != len(wordB):
                    print(idx, doc, lex[idx, 'concept'], wordA, wordB)
                for charA, charB in zip(wordA, wordB):
                    if charA == charB:
                        scores += [1]
                    else:
                        scores += [0]
                        errors[charA, charB, doc] += [(wordA, wordB)]
                score = sum(scores)/len(scores)
                S[doc][cogid] = [score, wordA, wordB, idxA, attIdx[0]]
    atable += [[
        doc,
        len(PREDICTED[doc]),
        len(S[doc]),
        len([x for x in S[doc].values() if x[0] == 1]),
        len([x for x in S[doc].values() if x[0] == 1])/len(S[doc]),
        sum([cog[0] for cog in S[doc].values()])/len(S[doc])
        ]]
atable += [[
    'total',
    sum([row[1] for row in atable]),
    sum([row[2] for row in atable]),
    sum([row[3] for row in atable]),
    sum([row[3] for row in atable])/sum([row[2] for row in atable]),
    sum([row[5] for row in atable])/len(docs),
    ]]
print('\n### 2. Human Predictions\n')
print(tabulate(
    atable,
    headers=[
        'doculect',
        'words',
        'morphemes',
        'perfect',
        'proportion',
        'score'],
    tablefmt='pipe',
    floatfmt='.4f'
    ))

# count accuracy of 
btable = []
S = {d: {} for d in docs}
for doc in docs:
    docIdx = lex.cols.index(doc+' ATTESTED')
    for idx in AUTOMATED[doc]:
        cogids = lex[idx, 'cogids']
        words = lex[idx, 'alignment'].n
        if len(cogids) != len(words):
            print(idx, doc, lex[idx, 'concept'])
            raise ValueError
        for wordA, cogid in zip(words, cogids):
            attIdx = etd[cogid][docIdx]
            if attIdx:
                scores = []
                wordB = lex[attIdx[0], 'alignment'].n[lex[attIdx[0],
                    'cogids'].index(cogid)]
                if len(wordA) != len(wordB):
                    print(idx, doc, lex[idx, 'concept'], wordA, wordB)
                for charA, charB in zip(wordA, wordB):
                    if charA == charB:
                        scores += [1]
                    else:
                        scores += [0]
                score = sum(scores)/len(scores)
                S[doc][cogid] = [score, wordA, wordB, idxA, attIdx[0]]
    btable += [[
        doc,
        len(PREDICTED[doc]),
        len(S[doc]),
        len([x for x in S[doc].values() if x[0] == 1]),
        len([x for x in S[doc].values() if x[0] == 1])/len(S[doc]),
        sum([cog[0] for cog in S[doc].values()])/len(S[doc])
        ]]
btable += [[
    'total',
    sum([row[1] for row in btable]),
    sum([row[2] for row in btable]),
    sum([row[3] for row in btable]),
    sum([row[3] for row in btable])/sum([row[2] for row in btable]),
    sum([row[5] for row in btable])/len(S),
    ]]
print('\n### 3. Predictions (Automated, one candidate)\n')
print(tabulate(
    btable,
    headers=[
        'doculect',
        'words',
        'morphemes',
        'perfect',
        'proportion',
        'score'],
    tablefmt='pipe',
    floatfmt='.4f'
    ))

ctable = []
S = {d: {} for d in docs}
for doc in docs:
    docIdx = lex.cols.index(doc+' ATTESTED')
    for idx in SECOND[doc]:
        cogids = lex[idx, 'cogids']
        words = lex[idx, 'alignment'].n
        if len(cogids) != len(words):
            print(idx, doc, lex[idx, 'concept'])
            raise ValueError
        for wordA, cogid in zip(words, cogids):
            attIdx = etd[cogid][docIdx]
            if attIdx:
                scores = []
                wordB = lex[attIdx[0], 'alignment'].n[lex[attIdx[0],
                    'cogids'].index(cogid)]
                if len(wordA) != len(wordB):
                    print(idx, doc, lex[idx, 'concept'], wordA, wordB)
                for charA, charB in zip(wordA, wordB):
                    if charA == charB:
                        scores += [1]
                    else:
                        charsA = charA.split('|')
                        if charB in charsA:
                            scores += [1/(charsA.index(charB)+1)]
                        else:
                            scores += [0]
                score = sum(scores)/len(scores)
                S[doc][cogid] = [score, wordA, wordB, idxA, attIdx[0]]
    ctable += [[
        doc,
        len(PREDICTED[doc]),
        len(S[doc]),
        len([x for x in S[doc].values() if x[0] == 1]),
        len([x for x in S[doc].values() if x[0] == 1])/len(S[doc]),
        sum([cog[0] for cog in S[doc].values()])/len(S[doc])
        ]]

ctable += [[
    'total',
    sum([row[1] for row in ctable]),
    sum([row[2] for row in ctable]),
    sum([row[3] for row in ctable]),
    sum([row[3] for row in ctable])/sum([row[2] for row in ctable]),
    sum([row[5] for row in ctable])/len(S),
    ]]

print('\n### 4. Predictions (Automated, up to two candidates)\n')
print(tabulate(
    ctable,
    headers=[
        'doculect',
        'words',
        'morphemes',
        'perfect',
        'proportion',
        'score'],
    tablefmt='pipe',
    floatfmt='.4f'
    ))

dtable = []
S = {d: {} for d in docs}
for doc in docs:
    docIdx = lex.cols.index(doc+' ATTESTED')
    for idx in THIRD[doc]:
        cogids = lex[idx, 'cogids']
        words = lex[idx, 'alignment'].n
        if len(cogids) != len(words):
            print(idx, doc, lex[idx, 'concept'])
            raise ValueError
        for wordA, cogid in zip(words, cogids):
            attIdx = etd[cogid][docIdx]
            if attIdx:
                scores = []
                wordB = lex[attIdx[0], 'alignment'].n[lex[attIdx[0],
                    'cogids'].index(cogid)]
                if len(wordA) != len(wordB):
                    print(idx, doc, lex[idx, 'concept'], wordA, wordB)
                for charA, charB in zip(wordA, wordB):
                    if charA == charB:
                        scores += [1]
                    else:
                        charsA = charA.split('|')
                        if charB in charsA:
                            scores += [1/(charsA.index(charB)+1)]
                        else:
                            scores += [0]
                score = sum(scores)/len(scores)
                S[doc][cogid] = [score, wordA, wordB, idxA, attIdx[0]]
    dtable += [[
        doc,
        len(PREDICTED[doc]),
        len(S[doc]),
        len([x for x in S[doc].values() if x[0] == 1]),
        len([x for x in S[doc].values() if x[0] == 1])/len(S[doc]),
        sum([cog[0] for cog in S[doc].values()])/len(S[doc])
        ]]


dtable += [[
    'total',
    sum([row[1] for row in dtable]),
    sum([row[2] for row in dtable]),
    sum([row[3] for row in dtable]),
    sum([row[3] for row in dtable])/sum([row[2] for row in dtable]),
    sum([row[5] for row in dtable])/len(S),
    ]]

print('\n### 5. Predictions (Automated, up to three candidates)\n')
print(tabulate(
    dtable,
    headers=[
        'doculect',
        'words',
        'morphemes',
        'perfect',
        'proportion',
        'score'],
    tablefmt='pipe',
    floatfmt='.4f'
    ))


with open(Path('results', 'lexical-results.html').as_posix(), 'w') as f:
    f.write(tabulate(table,
        headers=[
            'doculect',
            'predictions',
            'elicited',
            'full',
            'part',
            'semi',
            'missing',
            'proportion'],
        tablefmt='html',
        floatfmt='.4f'))

with open(Path('results', 'human-predictions.html').as_posix(), 'w') as f:
    f.write(tabulate(
        atable,
        headers=[
            'doculect',
            'words',
            'morphemes',
            'perfect',
            'proportion',
            'score'],
        tablefmt='html',
        floatfmt='.4f'))

with open(Path('results', 'computer-predictions.html').as_posix(), 'w') as f:
    f.write(tabulate(
        btable,
        headers=[
            'doculect',
            'words',
            'morphemes',
            'perfect',
            'proportion',
            'score'],
        tablefmt='html',
        floatfmt='.4f'))

with open(Path('results', 'computer-predictions-2.html').as_posix(), 'w') as f:
    f.write(tabulate(
        ctable,
        headers=[
            'doculect',
            'words',
            'morphemes',
            'perfect',
            'proportion',
            'score'],
        tablefmt='html',
        floatfmt='.4f'))

with open(Path('results', 'computer-predictions-3.html').as_posix(), 'w') as f:
    f.write(tabulate(
        dtable,
        headers=[
            'doculect',
            'words',
            'morphemes',
            'perfect',
            'proportion',
            'score'],
        tablefmt='html',
        floatfmt='.4f'))



with open(Path('results', 'errors.tsv').as_posix(), 'w') as f:
    for (a, b, c), examples in errors.items():
        f.write(
                a + '\t'+b+'\t'+c+'\t'+str(len(examples))+'\t'+\
                        ' '.join(examples[0][0])+'\t'+\
                        ' '.join(examples[0][1])+'\n')
