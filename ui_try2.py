import PySimpleGUI as sg

# Define the table
table_data = [['1', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'], 
              ['2', 'Nulla dictum turpis vel purus molestie consequat.'], 
              ['3', 'Nunc elementum dolor id vestibulum commodo.']]
table_headings = ['ID', 'Description']
table = sg.Table(values=table_data, headings=table_headings, 
                 max_col_width=50, background_color='white',
                 auto_size_columns=False, justification='left',
                 num_rows=10, alternating_row_color='lightblue',
                 key='-TABLE-')

# Define the layout
layout = [[sg.Col(table, size=(500, 300), scrollable=True, expand_x=True, 
                  vertical_scroll_only=True)]]

# Create the window
window = sg.Window('Table Example', layout, size=(600, 400))

# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

window.close()
