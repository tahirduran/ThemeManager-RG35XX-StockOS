import shutil
import os
import app
import json

def file_copy(source, destination):
	if file_exists(source):
		os.makedirs(destination, exist_ok=True)
		shutil.copy2(source, destination)

def file_delete(file):
	os.remove(file)

def file_exists(file):
	return os.path.exists(file)

def save_json(array, file_name):
	with open(file_name, 'w') as file:
		json.dump(array, file, indent=4)

def load_json(file_name):
	array = {}
	if file_exists(file_name):
		with open(file_name, 'r') as file:
			array = json.load(file)
	return array

def save_txt(text, file_name):
	with open(file_name, 'w') as file:
		file.write(str(text))

def load_txt(file_name):
	text = ""
	if file_exists(file_name):
		with open(file_name, 'r') as file:
			text = file.read()
	return text