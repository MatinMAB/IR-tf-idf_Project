import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

data_file_path =  'irna-1400.csv'
data_file = pd.read_csv(data_file_path)
data_file = data_file['text']

vectorizer = TfidfVectorizer(lowercase=True)
vectorizer.fit(data_file)
print(vectorizer.vocabulary_)

data_file_tfidf = vectorizer.transform(data_file)
print(data_file_tfidf[0].A)


# tf-idf
vectorizer = TfidfVectorizer()
tfidf_data_file = vectorizer.fit_transform(data_file)

print(tfidf_data_file.shape)
print(len(vectorizer.vocabulary_))
print(list(vectorizer.vocabulary_.keys())[:20])

# query
query = 'نخبگان'

tfidf_query = vectorizer.transform([query])[0]
# similarities
cosines = []
for d in tqdm(tfidf_data_file):
  cosines.append(float(cosine_similarity(d, tfidf_query)))

# sorting
k = 10
sorted_ids = np.argsort(cosines)
for i in range(k):
  cur_id = sorted_ids[-i-1]
  print(cosines[cur_id])
  print(data_file[cur_id])
  print('_________________________________________________')