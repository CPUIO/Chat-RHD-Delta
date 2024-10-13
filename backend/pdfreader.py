from pypdf import PdfReader
import re

def extractText(file) -> list:
	# Читаем файл
	text = PdfReader(file)
	# Создаём буферную зону
	text_temp = []
	# Переираем страницы
	for i in text.pages:
		text_temp.append(" ".join(i.extract_text().split(" ")[1:]).replace("\n"," "))
	# Возвращаем список
	return text_temp	

# if __name__=="__main__":
# 	test = extractText("Коллективный договор.pdf")
# 	for i in test:
# 		print(i+"\n====\n\n")
