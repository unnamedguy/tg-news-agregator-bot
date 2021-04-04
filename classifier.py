import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

def get_en_news_category(headline):
    category_list = ['sport', 'world', 'us', 'business', 'health', 'entertainment', 'sci_tech']

    docs_new = [headline]

    #LOAD MODEL
    loaded_vec = CountVectorizer(vocabulary=pickle.load(open('en_classifier/count_vector.pkl', 'rb')))
    loaded_tfidf = pickle.load(open('en_classifier/tfidf.pkl','rb'))
    loaded_model = pickle.load(open('en_classifier/softmax.pkl','rb'))

    X_new_counts = loaded_vec.transform(docs_new)
    X_new_tfidf = loaded_tfidf.transform(X_new_counts)
    predicted = loaded_model.predict(X_new_tfidf)
    return category_list[predicted[0]]

def get_ru_news_category(headline):
    category_list = ['business', 'internet', 'entertainment', 'world', 'sci_tech', 'ru', 'sport']

    docs_new = [headline]

    #LOAD MODEL
    loaded_vec = CountVectorizer(vocabulary=pickle.load(open('ru_classifier/count_vector_title.pkl', 'rb')))
    loaded_tfidf = pickle.load(open('ru_classifier/tfidf_title.pkl','rb'))
    loaded_model = pickle.load(open('ru_classifier/softmax_title.pkl','rb'))

    X_new_counts = loaded_vec.transform(docs_new)
    X_new_tfidf = loaded_tfidf.transform(X_new_counts)
    predicted = loaded_model.predict(X_new_tfidf)
    return category_list[predicted[0]]