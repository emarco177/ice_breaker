# Task : Document Question Answering
# Takes a (document, question) pair as input and return an answer in natural language
# Used in text document in image format (png, jpg, etc.)

from transformers import pipeline
from PIL import Image
import pytesseract

# Image path in computer
image_path = "Declaracao.jpg"

''' 
    --- Python PIL ---
    PIL is an open-source library that provides python with external file support and efficiency to process images and their representations. 
    Basically, PIL is designed to access data in the form of images (pixels) to make the analysis faster. 
'''

# Load the image as a PIL object
image = Image.open(image_path)

'''
    --- Pytesseract ---
    Python-tesseract is an optical character recognition (OCR) tool for python. 
    That is, it will recognize and “read” the text embedded in images.
'''
# 1. The image_to_string() function takes an image object (image) as input.
# 2. It processes the image using optical character recognition techniques to extract any text that is present within the image.
# 3. The extracted text is then returned as a string, which is assigned to the variable text.
text = pytesseract.image_to_string(image)

nlp = pipeline(
    ##### Document Question Answering Task #####
    "document-question-answering",
    model="impira/layoutlm-document-qa",
    #model="madiltalay/layoutlmv2-base-uncased_finetuned_docvqa",

    ##### Question Answering Task #####
    #"question-answering",
    #model="PlanTL-GOB-ES/roberta-large-bne-sqac",
)


while True:
    # Question
    # question = "Qual é o tipo de declaração?"
    question = input('Question:' )

    # Answer
    # An example of an answer in document-question-answering tasks: [{'score': 0.8856253623962402, 'answer': '202106550', 'start': 162, 'end': 162}]
    answer = nlp(image, question)  #in document-question-answering tasks
    #answer = nlp(question, text) #in question-answering tasks
    #print(answer) 
    
    final_answer = answer[0]['answer']
    print(final_answer)

'''
    modelo madiltalay/layoutlmv2-base-uncased_finetuned_docvqa -> melhores respostas em português
    modelo impira/layoutlm-document-qa -> melhores respostas em inglês (num documento português e espanhol, se forem respostas pouco extensas)
    modelo PlanTL-GOB-ES/roberta-large-bne-sqac -> melhores respostas em espanhol (num documento em espanhol: doc-espanhol.png)
'''