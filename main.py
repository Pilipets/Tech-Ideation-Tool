
import spacy
import numpy as np
from gensim.models import KeyedVectors


# load spaCy model and Word2Vec model
# nlp = spacy.load('en_core_web_sm')
# w2v = KeyedVectors.load_word2vec_format('path/to/word2vec/model', binary=True)


def get_local_similar_phrase_phrases():
	given_phrase = "i like coffee"
	num_phrases = 15

    # tokenize given phrase and convert each word into a vector representation
	given_doc = nlp(given_phrase)
	given_vecs = [word.vector for word in given_doc if word.has_vector]

    # calculate the average vector of the given phrase
	given_avg_vec = np.mean(given_vecs, axis=0)

    # generate similar vectors by adding the difference between each word vector and the average vector
	similar_vecs = [given_avg_vec + (word.vector - given_avg_vec) * 0.5 for word in given_doc if word.has_vector]

    # convert similar vectors back into phrases
	similar_phrases = [w2v.similar_by_vector(vec, topn=1)[0][0] for vec in similar_vecs]
	
	return similar_phrases[:num_phrases]


def main():
    pass


if __name__ == '__main__':
	main()