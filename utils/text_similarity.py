import torch
import transformers
import numpy as np
from gensim.parsing.preprocessing import remove_stopwords 



model_name = 'bert-base-uncased'
tokenizer = transformers.BertTokenizer.from_pretrained(model_name)
model = transformers.BertModel.from_pretrained(model_name)



def get_embedings(text,max_lenght=512,remove_stop_words=False):

    if remove_stop_words:
        text = remove_stopwords(text)
        

    tokens = tokenizer.encode(text, add_special_tokens=True, max_length=max_lenght, truncation=True, return_tensors='pt')

    with torch.no_grad():
        embedings = model(tokens)[0][:,0,:].numpy()


    return embedings


def get_similarity(embedding1,embedding2):

    similarity = np.dot(embedding1, embedding2.T) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

    return similarity

