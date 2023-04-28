import arxiv
import requests
from dateutil.parser import parse
import openai
from transformers import pipeline
from gnews import GNews
import os


openai.api_key = open(os.path.join('keys', 'open_ai.key')).read()
MAX_RESULTS = 5


def arxiv_sample():
	print('arxiv_sample')
	search = arxiv.Search(
		query = "quantum",
		max_results = MAX_RESULTS,
		sort_by = arxiv.SortCriterion.SubmittedDate
	)

	for result in search.results():
		print("Title:", result.title)
		print("Published:", result.published)
		print("Link:", result)
		print("Summary:", result.summary)
		print()
	print()


def patents_view_sample():
	print('patents_view_sample')
	query = "electric car"
	url = "https://api.patentsview.org/patents/query"

	# Set the parameters for the API request
	params = {
		"q": '{"_text_any":{"patent_abstract":"%s"}}' % query,
		"f": '["patent_title", "patent_date", "patent_abstract", "patent_number"]',
		"o": '{"per_page": %d}' % MAX_RESULTS,
		"s": '[{"patent_date":"desc"}]', 
	}

	response = requests.get(url, params=params)

	if response.status_code == 200:
		data = response.json()
		results = data.get('patents', [])

		for patent in results:
			print('Title:', patent.get('patent_title', 'Not Found'))
			print('Date:', patent.get('patent_date', 'Not Found'))
			print('Number:', patent.get('patent_number', 'Not Found'))
			print('Summary:', patent.get('patent_abstract', 'Not Found'))
			print()
	else:
		print(f"Error fetching data from PatentsView API: {response.status_code}")
	print()


def arxiv_explorer_sample():
	print('arxiv_explorer_sample')
	query = 'trying something unusual'
	url = 'https://us-west1-semanticxplorer.cloudfunctions.net/semantic-xplorer-db'

	resp = requests.get(url, params={'query': query})

	elems = []
	for el in resp.json():
		url = 'https://arxiv.org/abs/' + el['id']
		el = el['metadata']
		elems.append({'title': el['title'], 'date': parse(el['date']), 'url': url, 'abstract': el['abstract']})

	elems.sort(key=lambda el: el['date'], reverse=True)

	elems = elems[:MAX_RESULTS]
	for el in elems:
		print(el)
	print()


def chatgpt_sample():
	print('chatgpt_sample')
	query = 'trying something unusual'
	def generate_ideas(prompt):
		response = openai.Completion.create(
		engine="text-davinci-003",
		prompt=prompt,
		max_tokens=200 * MAX_RESULTS,
		stop=None,
		temperature=0.5,
		)

		ideas = [choice.text.strip() for choice in response.choices]
		return ideas

	prompt = "Generate %d ideas or facts or insights related to '%s'" % (MAX_RESULTS, query)
	ideas = generate_ideas(prompt)

	assert len(ideas) == 1, ideas
	ideas = ideas[0].split('\n\n')
	print(ideas)
	print()


def hugging_face_sample():
	print('hugging_face_sample')
	query = 'climate change'

	generator = pipeline('text-generation', model = 'gpt2')
	results = generator("New idea/fact/insight related to the %s is" % query, max_length = 200, num_return_sequences=MAX_RESULTS)

	ideas = [r['generated_text'].replace('\n\n', '\n') for r in results]
	for idea in ideas:
		print('Idea:', idea)
		print()
	print()


def google_news_sample():
	query = 'distributed databases'
	google_news = GNews()

	google_news.max_results = MAX_RESULTS

	news = google_news.get_news(query)
	for new in news:
		print('Title:', new['title'])
		print('Date:', new['published date'])
		print('Description:', new['description'])
		print('Url:', new['url'])
		print()


def main():
	arxiv_sample()
	arxiv_explorer_sample()
	patents_view_sample()
	chatgpt_sample()
	hugging_face_sample()
	google_news_sample()


if __name__ == '__main__':
	main()