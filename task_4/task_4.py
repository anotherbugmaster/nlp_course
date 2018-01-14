from natasha import NamesExtractor, OrganisationExtractor
import re

docs = []

with open('dataset_40163_1.txt', 'r') as reader:
    for line in reader:
        docs.append(line)

names_extractor = NamesExtractor()
orgs_extractor = OrganisationExtractor()

with open('result.txt', 'w+') as writer:
    for doc in docs:
        for match in names_extractor(doc):
            ner_len = 0
            ner_start = match.span[0]
            for idx in range(*match.span):
                if re.match(r'\w', doc[idx]):
                    if ner_len == 0:
                        ner_start = idx
                    ner_len += 1
                elif ner_len > 0:
                    writer.write(f"{ner_start} {ner_len} PERSON ")
                    ner_len = 0

            if ner_len > 0:
                writer.write(f"{ner_start} {ner_len} PERSON ")
                ner_len = 0

        for match in orgs_extractor(doc):
            ner_len = 0
            ner_start = match.span[0]
            for idx in range(*match.span):
                if re.match(r'\w', doc[idx]):
                    if ner_len == 0:
                        ner_start = idx
                    ner_len += 1
                elif ner_len > 0:
                    writer.write(f"{ner_start} {ner_len} ORG ")
                    ner_len = 0

            if ner_len > 0:
                writer.write(f"{ner_start} {ner_len} ORG ")
                ner_len = 0

        writer.write('EOL\n')
