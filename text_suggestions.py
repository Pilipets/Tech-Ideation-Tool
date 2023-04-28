from pytrends.request import TrendReq
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import nltk


nltk.download('wordnet')
nltk.download('punkt')
pytrend = TrendReq()


def get_google_trends_related():
	# Create pytrends object

	# Define the phrase you want to generate related phrases for
	query = "coffee"

	# Get related queries
	pytrend.build_payload(kw_list=[query])
	
	related_queries = pytrend.related_queries()[query]
	# Print the top 10 rising related queries
	print(list(related_queries["rising"]["query"]))

	# Print the top 10 top related queries
	print(list(related_queries["top"]["query"]))

	related_topics = pytrend.related_topics()[query]
	# Print the top 10 rising related topics
	df = related_topics["rising"]
	#print(df)

	result = ['{}-{}'.format(x, y) for x, y in zip(df['topic_title'], df['topic_type'])]
	print(result)

	# Print the top 10 top related topics
	df = related_topics["top"]
	#print(df)

	result = ['{}-{}'.format(x, y) for x, y in zip(df['topic_title'], df['topic_type'])]
	print(result)


def get_google_trends_suggestions():
	keywords = pytrend.suggestions(keyword='apple headphones')

	results = ['{}-{}'.format(q['title'], q['type']) for q in keywords]
	print(results)
	

def get_synsets_word_related_phrases(word = 'whatever'):
    # Get synsets for the given word
    synsets = wordnet.synsets(word)

    # Collect related words and phrases
    related = set()
    for synset in synsets:
        for lemma in synset.lemmas():
            # Add synonyms
            if lemma.name() != word:
                related.add(lemma.name().replace("_", " "))

            # Add antonyms
            for antonym in lemma.antonyms():
                related.add(antonym.name().replace("_", " "))

    return list(related)


def get_synsets_phrase_related_phrases(phrase = 'whatever'):
	# Tokenize input phrase into words
    words = word_tokenize(phrase.lower())

    related = set()
    for word in words:
        related.update(get_synsets_word_related_phrases(word))

    print(list(related))


def main():
    get_google_trends_related()
    get_google_trends_suggestions()
    print(get_synsets_word_related_phrases('coffee'))
    get_synsets_phrase_related_phrases('I want this cup of coffee for the morning')


if __name__ == '__main__':
    main()