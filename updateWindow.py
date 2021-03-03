import PySimpleGUI
def updateTextWindow(window, text):
	window["-UPDATE-"].Update(text)
	window.read(timeout=0.0001)