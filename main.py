
import material_suggestions
import text_suggestions
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTextBrowser
#from ideation_tool import get_arxiv_articles, get_news, get_query_trends, get_related_phrases, get_patents

import PySimpleGUI as sg

# Define the layout of the window
layout = [
    [sg.Text("Enter your query:"), sg.Input(key="-QUERY-"), sg.Button("Search")],
    [sg.Checkbox("Arxiv articles", key="-ARXIV-"), sg.Checkbox("News", key="-NEWS-"), sg.Checkbox("Google trends", key="-GOOGLE-"), sg.Checkbox("Related phrases", key="-RELATED-"), sg.Checkbox("Patents", key="-PATENTS-")],
    [sg.Text("Results:")],
    [sg.Output(size=(120, 40), key="-OUTPUT-")],
]

# Create the window
window = sg.Window("Ideation Tool", layout, size=(800, 600))

# Event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    if event == "Search":
        # Get the selected sources
        sources = [source for source in ["Arxiv articles", "News", "Google trends", "Related phrases", "Patents"] if values.get(source)]

        # Perform the searches and update the output
        output = ""
        if "Arxiv articles" in sources:
            # Get Arxiv articles for the query
            articles = get_arxiv_articles(values["-QUERY-"])
            output += "Arxiv articles:\n" + "\n".join(articles) + "\n\n"

        if "News" in sources:
            # Get news articles for the query
            articles = get_news_articles(values["-QUERY-"])
            output += "News articles:\n" + "\n".join(articles) + "\n\n"

        if "Google trends" in sources:
            # Get Google trends for the query
            trends = get_query_trends(values["-QUERY-"])
            output += "Google trends:\n" + str(trends) + "\n\n"

        if "Related phrases" in sources:
            # Get related phrases for the query
            phrases = get_related_phrases(values["-QUERY-"])
            output += "Related phrases:\n" + "\n".join(phrases) + "\n\n"

        if "Patents" in sources:
            # Get patents for the query
            patents = get_patents(values["-QUERY-"])
            output += "Patents:\n" + "\n".join(patents) + "\n\n"

        window["-OUTPUT-"].update(output)

# Close the window
window.close()