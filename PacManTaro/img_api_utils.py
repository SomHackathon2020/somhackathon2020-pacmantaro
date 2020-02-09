import numpy as np
from translate import Translator
from sklearn.feature_extraction.text import TfidfVectorizer

translator = Translator(from_lang="Catalan", to_lang="English")


def getStops():
    with open("stopwords.txt") as f:
        words = [x.replace("\n", "") for x in f.readlines()]
    return words


def remove_topos(text, stops=["mataró", "mataro", "maresme", "catalunya"]):
    """ Delete toponyms. """
    text = text.lower().split(" ")
    for i, word in enumerate(text):
        if word in stops:
            del text[i]

    return " ".join(text)


def remove_words(text, stops=getStops(), hard_stops=",.-_!?¡''*+^/|"):
    """ Delete stopwords. """
    for char in hard_stops:
        text = text.replace(char, "")

    text = text.lower().split(" ")

    for i, word in enumerate(text):
        if word in stops:
            del text[i]

    return " ".join(text)


def analyze(text, corpus, max_k=3):
    if corpus is None:
        #return corpus.split(" ")
        return ""


    vectorizer = TfidfVectorizer()

    total_data = corpus + [text]
    rankings = vectorizer.fit_transform(total_data)
    i2word = vectorizer.get_feature_names()
    keys = np.argsort(np.array(rankings.todense())[-1])[::-1]
    keywords = [i2word[x] for x in keys[:min(max_k, len(text.split(" ")))]]
    return keywords


def getKeywords(title, corpus_keys=None):
    # remove toponyms - bad translated
    doc_ = remove_topos(title)
    # translate
    doc_t = translator.translate(doc_)
    # remove stopwords
    doc_1 = remove_words(doc_t)

    # get TfIdf
    keywords = analyze(doc_1, corpus_keys, max_k=100)
    return " ".join(keywords)


def getImageURL(title, corpus_keys=None, location="mataró", max_k=3):
    """ Get the url for an image based on the experience title. """
    # remove toponyms - bad translated
    doc_ = remove_topos(title)
    # translate
    doc_t = translator.translate(doc_)
    # remove stopwords
    doc_1 = remove_words(doc_t)

    # get TfIdf
    keywords = analyze(doc_1, corpus_keys, max_k=max_k)
    # generate img url
    print("HERE")
    print(keywords)
    img_url = "https://source.unsplash.com/1600x900/?" + location + "," + ",".join(keywords)
    return img_url