import sys
sys.path.append("../AccommodationRecommender-Airbnb/")


from icecream import ic
from text_similarity import get_embedings,get_similarity

text1 = "This is the demo text 1"
text2 = text1


emb1 = get_embedings(text1,len(text1))

emb2 = get_embedings(text2,len(text2))

ic(get_similarity(emb1,emb2))


