import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

def getEnNewsCategory(headline):
    category_list = ["sport", "world", "us", "business", "health", "entertainment", "sci_tech"]

    docs_new = [headline]

    #LOAD MODEL
    loaded_vec = CountVectorizer(vocabulary=pickle.load(open("count_vector.pkl", "rb")))
    loaded_tfidf = pickle.load(open("tfidf.pkl","rb"))
    loaded_model = pickle.load(open("softmax.pkl","rb"))

    X_new_counts = loaded_vec.transform(docs_new)
    X_new_tfidf = loaded_tfidf.transform(X_new_counts)
    predicted = loaded_model.predict(X_new_tfidf)

    return category_list[predicted[0]]