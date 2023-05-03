import PySimpleGUI as sg
import json

# Define the layout of the main window
layout = [
    [sg.Table(values=[['1', '2', '3'], ['a', 'b', 'c'], ['A', 'B', 'C']],
              headings=['Col1', 'Col2', 'Col3'],
              bind_return_key=True,  # Enable row selection on Enter key
              key='-TABLE-')]
]

# Create the main window
window = sg.Window('Main Window', layout)

# Event loop to handle events
while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED:
		break
	elif event == '-TABLE-':
		selected_row = values['-TABLE-'][0]
		if selected_row is not None:
			# Create a new window to display the JSON data
			elem = {'a':'b', 'dsfsdfdsfggfhytjhjhgjgjgjhgjhgjhg':'sdfsdfdsfsdfsdfsdfsdfsdfsdfsdd', 'esdfsfdsd':'sdfsdfsdf'}
			json_layout = [
				[sg.Multiline(json.dumps(elem), size=(50, 10), key='-JSON-')]
			]
			json_window = sg.Window('JSON Data', json_layout)

			# Event loop to handle events in the JSON window
			while True:
				json_event, json_values = json_window.read()
				if json_event == sg.WIN_CLOSED or json_event == 'Close':
					json_window.close()
					break

# Close the main window when the event loop is exited
window.close()