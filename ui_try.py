import PySimpleGUI as sg
sg.theme('DarkAmber')


header_list = ['Function', 'Starting Address', 'Basic Blocks', 'Instructions', 'Cyclomatic Complexity', 'Jilb\'s Metric', 'ABC Metric', 'Halstead Estimated Length',
				'Halstead Volume', 'Halstead Difficulty', 'Halstead Effort', 'Halstead Time', 'Halstead Bugs', 'Harris Metric', 'Oviedo Metric', 'Chepin Metric',
                'Card & Glass Metric', 'Henry & Kafura Metric', 'Cocol Metric', 'Hybrid General Complexity']
table_data = []
import random
i = 0
while i < 2000:
	row = []
	j = 0
	while j < len(header_list):
		row.append(round(random.random(), 3))
		j += 1
	table_data.append(row)
	i += 1

window_col = [	[sg.Table(values=table_data, headings=header_list[1:], max_col_width=25, auto_size_columns=True, display_row_numbers=False, justification='center',
				vertical_scroll_only = False, alternating_row_color='#626366', num_rows=min(len(table_data), 20))]	]
layout = [	[sg.Col(window_col, vertical_alignment = 'top')],
			[sg.Button('Close')]	]

# Generated the gui window to display the table
window = sg.Window('Function Metrics', layout, size = (800, 600), font='AndaleMono 16')

# Event Loop to process "events" and get the "values" of the inputs
while True:
	event, values = window.read()
#	del values
	# End the function if the windows is closed via the "x" button or selecting the "Close" button
	if event == sg.WIN_CLOSED or event == 'Close':
		break

# Terminate the window, which will cause the function to return and the program to end
window.close()