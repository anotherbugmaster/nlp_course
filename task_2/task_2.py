from gensim import summarization
import json

with open('dataset_43428_1.txt', 'r') as reader:
    texts = reader.read()

texts = json.loads(texts)

summaries = [summarization.summarize(text) for text in texts]

with open('result.json', 'w+') as writer:
    writer.writelines(json.dumps(summaries, ensure_ascii=False))

keywords = [summarization.keywords(text) for text in texts]

with open('result_keywords.json', 'w+') as writer:
    writer.writelines(json.dumps(keywords, ensure_ascii=False))
