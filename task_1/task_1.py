import re


def analyze_word(word, forms_dict, pos_dict):
    word_lowered = word.lower()

    if word_lowered in forms_dict:
        word_lowered = forms_dict[word_lowered]

    if word_lowered in pos_dict:
        return word + '{' + word_lowered + '=' + pos_dict[word_lowered] + '}'
    else:
        return word + '{' + word_lowered + '=' + 'NI' + '}'


def analyze(sentence, forms_dict, pos_dict):
    return [
        analyze_word(word, forms_dict, pos_dict)
        for word
        in re.split(r'\W+', sentence)
        if re.match(r'\w+', word)
    ]


with open('dataset_37845_1.txt', 'r') as reader:
    sentences = reader.readlines()

forms_dict = {}
pos_dict = {}

pos_transform_dict = {
    'NOUN': 'S',
    'м': 'S',
    'ж': 'S',
    'мо': 'S',
    'жо': 'S',
    'мн.': 'S',
    'с': 'S',
    'INFN': 'V',
    'VERB': 'V',
    'PRTF': 'V',
    'PRTS': 'V',
    'GRND': 'V',
    'нсв': 'V',
    'св': 'V',
    'св-нсв': 'V',
    'ADJF': 'A',
    'ADJS': 'A',
    'п': 'A',
    'PREP': 'PR',
    'предл.': 'PR',
    'CONJ': 'CONJ',
    'союз': 'CONJ',
    'ADVB': 'ADV',
    'PRCL': 'ADV',
    'INTJ': 'ADV',
    'н': 'ADV',
    'част.': 'ADV'
}

with open('odict.csv', 'r', encoding='cp1251') as reader:
    for line in reader:
        words = line.split(',')

        if words[1] in pos_transform_dict:
            pos_dict[words[0]] = pos_transform_dict[words[1]]
        else:
            pos_dict[words[0]] = 'NI'

        for word in words[2:]:
            forms_dict[word] = words[0]

with open('data', 'r') as reader:
    for line in reader:
        if re.match(r'(\w+)\t(\w+),?.*', line):
            word, pos = re.match(r'(\w+)\t(\w+),?.*', line).groups()

            if pos in pos_transform_dict:
                pos = pos_transform_dict[pos]
            else:
                pos = 'NI'

            if not word.lower() in pos_dict or pos_dict[word.lower()] == 'NI':
                pos_dict[word.lower()] = pos

result = [
    analyze(line, forms_dict, pos_dict)
    for line
    in sentences
]

with open('result.txt', 'w+') as writer:
    writer.writelines([' '.join(words) + '\n' for words in result])
