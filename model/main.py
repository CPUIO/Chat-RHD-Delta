from navec import Navec
# from sklearn.metrics.pairwise import cosine_similarity
import pymupdf  # PyMuPDF
import numpy as np
from annoy import AnnoyIndex

path = 'navec_hudlit_v1_12B_500K_300d_100q.tar'
navec = Navec.load(path)

# Допустим, размерность вектора эмбеддинга 300
embedding_dim = 300
index = AnnoyIndex(embedding_dim, 'angular')  # Мера угла

paragraphs = [
    '''
    Коллективный договор ОАО «РЖД» на 2023 - 2025 годы - правовой акт,
    регулирующий социально-трудовые отношения в открытом акционерном
    обществе «Российские железные дороги» между сторонами социального
    партнерства - Работниками и Работодателем в лице их представителей.
    ''',
    '''
    Настоящий Договор является единым для ОАО «РЖД», включая
    филиалы, структурные подразделения и представительства, за исключением
    Петропавловского отделения Южно-Уральской железной дороги - филиала
    ОАО «РЖД», расположенного на территории Республики Казахстан, в котором,
    на основе настоящего Договора и с учетом особенностей законодательства
    Республики Казахстан, заключается отдельный коллективный договор на 2023 -
    2025 годы.
    ''',
    '''
    Нормы раздела 9 настоящего Договора не применяются в отношении
    указанного филиала. При этом, нормы, регулирующие вопросы социального
    партнерства, включаются в коллективный договор данного филиала в редакции,
    согласованной с Комиссией по подготовке коллективного договора ОАО
    «РЖД» и контролю за его выполнением в установленном порядке; указанные
    нормы не могут снижать уровень гарантий, установленных для
    уполномоченного представителя работников указанного филиала, по
    сравнению с уровнем гарантий, установленных для Профсоюза.
    '''
]

# Функция для вычисления эмбеддинга предложения (абзаца)
def get_sentence_embedding(text):
  words = text.split()  # Разбиваем текст на слова
  # Получаем эмбединги для слов
  words_embeddings = [navec[word] for word in words if word in navec]
  if words_embeddings:
    # Усредняем эмбеддинги для получения эмбеддинга текста
    return np.mean(words_embeddings, axis=0)
  else:
    # Возвращаем нулевой вектор, если нет известных слов
    return np.zeros(embedding_dim)

# query_text = "Ваш текст"

# print(sentence_embedding)

# Построение дерева для поиска
index.build(10)  # 10 деревьев

# Сохранение индекса на диск (опционально)
# index.save('sentence_embeddings.ann')

#
# doc = pymupdf.open("a.pdf")  # open a document
# output_doc = open("output.txt", "wb")  # create a text output
# for page in doc:  # iterate the document pages
#   text = page.get_text().encode("utf8")  # get plain text (is in UTF-8)
#   out.write(text)  # write text of page
#   out.write(bytes((12,)))  # write page delimiter (form feed 0x0C)
# out.close()

# similarity = cosine_similarity([query_embedding], document_embeddings)


# def extract_paragraphs_from_pdf(pdf_path):
#   doc = pymupdf.open(pdf_path)  # Открываем документ
#   paragraphs = []

#   for page in doc:  # Итерируем страницы
#     text = page.get_text()  # Получаем текст
#     # Разделяем текст на абзацы по переносу строки
#     paragraphs.extend(text.split('\n'))

#   return paragraphs


# text = extract_paragraphs_from_pdf(
#     '/home/denis/Документы/dev/ЦифровойПрорыв2024/dataset/Коллективный договор.pdf')
# print(text)
