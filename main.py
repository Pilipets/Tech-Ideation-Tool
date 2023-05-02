
import material_suggestions
import text_suggestions
#from ideation_tool import get_arxiv_articles, get_news, get_query_trends, get_related_phrases, get_patents

import logging
import PySimpleGUI as sg

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Define the layout of the window
layout = [
    [sg.Text("Enter your query:"), sg.Combo(key="-QUERY-", values=[], size=(30, 1), expand_x=True), sg.Button("Search", size=(10, 1), key="-SEARCH-")],
    [sg.Checkbox("Arxiv", key="-ARXIV-", size=(15, 1)), sg.Checkbox("News", key="-NEWS-", size=(10, 1)), sg.Checkbox("Trends", key="-GOOGLE-", size=(15, 1)), sg.Checkbox("OpenAI", key="-OpenAI-", size=(15, 1)), sg.Checkbox("Patents", key="-PATENTS-", size=(10, 1))],
    [sg.Text("Results:")],
    [sg.Output(size=(60, 20), key="-OUTPUT-", font=("Courier New", 12), expand_x=True, expand_y=True)],
]

for elem in layout[1]:
    elem.InitialState = True
    elem.expand_x = True

# Create the window
window = sg.Window("Ideation Tool", layout, size=(1600, 800), resizable=True)

# Event loop
while True:
    event, values = window.read()
    logging.debug("event={}, values={}".format(event, values))

    if event == sg.WINDOW_CLOSED:
        break

    if event == "-SEARCH-":
        # Get the selected sources
        query = values["-QUERY-"]
        sources = [source for source in ["-ARXIV-", "-NEWS-", "-GOOGLE-", "-OpenAI-", "-PATENTS-"] if values.get(source)]

        # Update text suggestions
        window["-QUERY-"].update(values=["suggestion1", "suggestion2", "suggestion3", "suggestion4", "suggestion5", "suggestion6"])

        # Perform the searches and update the output
        output = ""
        if "-ARXIV-" in sources:
            # Get Arxiv articles for the query
            articles = get_arxiv_articles(query)
            output += "Arxiv articles:\n" + "\n".join(articles) + "\n\n"

        if "-NEWS-" in sources:
            # Get news articles for the query
            articles = get_news_articles(query)
            output += "News articles:\n" + "\n".join(articles) + "\n\n"

        if "-GOOGLE-" in sources:
            # Get Google trends for the query
            trends = get_query_trends(query)
            output += "Google trends:\n" + str(trends) + "\n\n"

        if "-OpenAI-" in sources:
            # Get related phrases for the query
            phrases = get_related_phrases(query)
            output += "Related phrases:\n" + "\n".join(phrases) + "\n\n"

        if "-PATENTS-" in sources:
            # Get patents for the query
            patents = get_patents(query)
            output += "Patents:\n" + "\n".join(patents) + "\n\n"

        window["-OUTPUT-"].update(output)

# Close the window
window.close()