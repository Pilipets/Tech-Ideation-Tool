
import material_suggestions
import text_suggestions
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QTextBrowser
#from ideation_tool import get_arxiv_articles, get_news, get_query_trends, get_related_phrases, get_patents

import PySimpleGUI as sg
# from get_arxiv_articles import get_arxiv_articles
# from get_news import get_news
# from get_google_trends import get_google_trends
# from get_related_phrases import get_related_phrases
# from get_patents import get_patents

sg.theme("DefaultNoMoreNagging")

# Define the layout
layout = [
    [sg.Text("Enter a keyword or phrase: "), sg.InputText()],
    [sg.Checkbox("Arxiv articles"), sg.Checkbox("News"), sg.Checkbox("Google trends"), sg.Checkbox("Related phrases"), sg.Checkbox("Patents")],
    [sg.Button("Search"), sg.Button("Exit")],
    [sg.Text("Search results: ")],
    [sg.Multiline(size=(100, 20), key="-OUTPUT-")],
]

# Create the window
window = sg.Window("Ideation Tool", layout)

# Start the event loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "Search":
        search_term = values[0]
        sources = [source for source in ["Arxiv articles", "News", "Google trends", "Related phrases", "Patents"] if values[source]]
        results = []
        # for source in sources:
        #     if source == "Arxiv articles":
        #         articles = get_arxiv_articles(search_term)
        #         results.extend(articles)
        #     elif source == "News":
        #         news = get_news(search_term)
        #         results.extend(news)
        #     elif source == "Google trends":
        #         trends = get_google_trends(search_term)
        #         results.extend(trends)
        #     elif source == "Related phrases":
        #         related_phrases = get_related_phrases(search_term)
        #         results.extend(related_phrases)
        #     elif source == "Patents":
        #         patents = get_patents(search_term)
        #         results.extend(patents)

        results = [{'key':'value', 'key2':'value2'}, {'KEY1':'VALUE1 OR VALUE2', 'KEY2':'VALUE2', 'KEY3':'VALUE3'}]

        # Display the results
        output = ""
        for i, result in enumerate(results):
            output += f"{i+1}. {result}\n"
        window["-OUTPUT-"].update(output)

# Close the window
window.close()
