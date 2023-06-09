import arxiv
import requests
from dateutil.parser import parse
from gnews import GNews


MAX_RESULTS = 10


def arxiv_sample(query):
	print('arxiv_sample')
	search = arxiv.Search(
		query = query,
		max_results = MAX_RESULTS,
		sort_by = arxiv.SortCriterion.SubmittedDate
	)

	ret = []
	for result in search.results():
		ret.append({'title':result.title, 'published':result.published, 'link':result.entry_id, 'summary':result.summary})
	return ret


def patents_view_sample(query):
	print('patents_view_sample')
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

		ret = []
		for patent in results:
			ret.append({
				'title':patent.get('patent_title', 'Not Found'),
				'date':patent.get('patent_date', 'Not Found'),
				'number':patent.get('patent_number', 'Not Found'),
				'summary':patent.get('patent_abstract', 'Not Found')
			})
		return ret
	else:
		raise f"Error fetching data from PatentsView API: {response.status_code}"


def arxiv_explorer_sample(query):
	print('arxiv_explorer_sample')
	url = 'https://us-west1-semanticxplorer.cloudfunctions.net/semantic-xplorer-db'

	resp = requests.get(url, params={'query': query})

	elems = []
	for el in resp.json():
		url = 'https://arxiv.org/abs/' + el['id']
		el = el['metadata']
		elems.append({'title': el['title'], 'date': parse(el['date']), 'url': url, 'abstract': el['abstract']})

	elems.sort(key=lambda el: el['date'], reverse=True)

	elems = elems[:MAX_RESULTS]
	return elems


def google_news_sample(query):
	print('google_news_sample')
	google_news = GNews()

	google_news.max_results = MAX_RESULTS

	news = google_news.get_news(query)
	ret = []

	for new in news:
		ret.append({
			'title':new['title'], 'date':new['published date'],
			'description':new['description'], 'url':new['url']}
		)
	return ret


def main():
	print(arxiv_sample('quantum'))
	print(arxiv_explorer_sample('trying something unusual'))
	print(patents_view_sample('electric car'))
	print(google_news_sample('distributed databases'))


if __name__ == '__main__':
	main()