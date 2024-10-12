from navec import Navec
# from sklearn.metrics.pairwise import cosine_similarity
import pymupdf  # PyMuPDF
import numpy as np

path = 'navec_hudlit_v1_12B_500K_300d_100q.tar'
navec = Navec.load(path)

# Допустим, размерность вектора эмбеддинга 300
embedding_dim = 300
index = AnnoyIndex(embedding_dim, 'angular')  # Мера угла

query_text = "Ваш текст"
query_words = query_text.split()  # Разбиваем предложение на слова
words_embeddings = [navec[word] for word in query_words if word in navec]
if words_embeddings:
  # Усредняем эмбеддинги слов для предложения
  sentence_embedding = np.mean(words_embeddings, axis=0)
else:
  sentence_embedding = np.zeros(300)  # Если ни одного слова нет в словаре

print(sentence_embedding)

#
# doc = pymupdf.open("a.pdf")  # open a document
# output_doc = open("output.txt", "wb")  # create a text output
# for page in doc:  # iterate the document pages
#   text = page.get_text().encode("utf8")  # get plain text (is in UTF-8)
#   out.write(text)  # write text of page
#   out.write(bytes((12,)))  # write page delimiter (form feed 0x0C)
# out.close()

# similarity = cosine_similarity([query_embedding], document_embeddings)
