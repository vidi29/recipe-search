from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RecipeSearch:
    def __init__(self):
        self.tfidf = None
        self.docs = []  # list of combined text
        self.ids = []

    def fit(self, recipes):
        # recipes: list of dict {id, title, ingredients, steps}
        self.ids = [r['id'] for r in recipes]
        self.docs = [ (r.get('title','') + ' ' + r.get('ingredients','') + ' ' + r.get('steps','')) for r in recipes ]
        self.tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
        self.mat = self.tfidf.fit_transform(self.docs)

    def query(self, q, topk=10):
        if self.tfidf is None:
            return []
        v = self.tfidf.transform([q])
        sim = cosine_similarity(v, self.mat).flatten()
        idx = np.argsort(-sim)[:topk]
        return [(self.ids[i], float(sim[i])) for i in idx if sim[i] > 0]
