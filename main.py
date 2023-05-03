
import material_suggestions
import text_suggestions
import json
#from ideation_tool import get_arxiv_articles, get_news, get_query_trends, get_related_phrases, get_patents

import logging
import PySimpleGUI as sg

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

sg.theme('DefaultNoMoreNagging')
sg.set_options(background_color='#F0F0F0', text_color='#333333', element_background_color='#FFFFFF', element_text_color='#000000', scrollbar_color=None)

results = []
window_col = [ [sg.Table(key='-RESULTS-', values=[], headings=['Type', 'Main info'], auto_size_columns=False,
                display_row_numbers=False, justification='left',
                vertical_scroll_only = False,
				alternating_row_color='#D6EAF8', col_widths=[1, 70], expand_x=True, expand_y=True)] ]

# Define the layout of the window
layout = [
    [sg.Text("Enter your query:"), sg.Combo(key="-QUERY-", values=[], size=(30, 1), expand_x=True, default_value='quantum'), sg.Button("Search", size=(10, 1), key="-SEARCH-")],
    [sg.Checkbox("Arxiv", key="-ARXIV-", size=(15, 1)), sg.Checkbox("News", key="-NEWS-", size=(10, 1)), sg.Checkbox("Trends", key="-GOOGLE-", size=(15, 1)), sg.Checkbox("OpenAI", key="-OpenAI-", size=(15, 1)), sg.Checkbox("Patents", key="-PATENTS-", size=(10, 1))],
    [sg.Text("Results:")],
    [sg.Col(window_col, vertical_alignment = 'top', expand_x=True, expand_y=True)],
]

for elem in layout[1]:
    elem.InitialState = False
    elem.expand_x = True

# Create the window
window = sg.Window("Ideation Tool", layout, size=(1800, 800), resizable=False, font=("Helvetica", 20))

# Event loop
while True:
    event, values = window.read()
    logging.debug("event={}, values={}".format(event, values))

    if event == sg.WINDOW_CLOSED:
        break

    elif event == "-SEARCH-":
        # Get the selected sources
        query = values["-QUERY-"]
        sources = [source for source in ["-ARXIV-", "-NEWS-", "-GOOGLE-", "-OpenAI-", "-PATENTS-"] if values.get(source)]

        # Update text suggestions
        window["-QUERY-"].update(values=["suggestion1", "suggestion2", "suggestion3", "suggestion4", "suggestion5", "suggestion6"])

        # Perform the searches and update the output
        output = []
        results.clear()
        if "-ARXIV-" in sources:
            # Get Arxiv articles for the query
            articles = material_suggestions.arxiv_sample(query)

            results.extend([elem for elem in articles])
            output.extend(['ARXIV', elem['title'], elem] for elem in articles)

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

        window["-RESULTS-"].update(values=output)
    
    elif event == '-RESULTS-':
        selected_row = values['-TABLE-'][0]
        if selected_row is not None:
            elem = results[selected_row]

            json_layout = [[sg.Multiline(json.dumps(elem))]]
            popup = sg.Window('Row %d JSON' % selected_row, json_layout, finalize=True, non_blocking=True)


# Close the window
window.close()