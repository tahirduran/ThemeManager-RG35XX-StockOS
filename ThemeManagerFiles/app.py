import sys
import ui
import input
import os
import func
import graphic as gr
import list
from pathlib import Path

AppDIR = os.path.dirname(os.path.abspath(__file__))

themeActive = 0

themeTypeActive = -1
themeData = {}

def start():
	theme_list_load()
	data_load()
	ui.load_menu()
	
def update():
	global themeActive, themeTypeActive

	input.check()

	if input.key("MENUF"):
		sys.exit()

	if ui.menuActive == "":
		if input.key("DY"):
			menu_change(input.value)
		if input.key("A") or (input.key("DX") and input.value == 1):
			ui.menuActive = "themeSelect"
			themeTypeActive = 0
	elif ui.menuActive == "themeSelect":
		if input.key("DY"):
			menu_type_change(input.value)
		if input.key("B") or (input.key("DX") and input.value == -1):
			ui.menuActive = ""
			themeTypeActive = -1
		if input.key("A"):
			theme_appy()
		
		# if input.key("A"):
		# 	ui.panelActive = "accept"

	# elif ui.panelActive == "accept":
	# 	if input.key("B"):
	# 		ui.panelActive = ""
	# 	if input.key("A"):
	# 		theme_appy()
	# elif ui.panelActive == "applyingOk":
	# 	if input.key("A"):
	# 		ui.panelActive = ""

	ui.load_menu()

	# if input.key("R2"):
	# 	gr.screen_shot()

def menu_change(value):
	global themeActive
	themeActive = menu_button_dy(value, themeActive, len(list.themeList))

def menu_type_change(value):
	global themeTypeActive
	themeTypeActive = menu_button_dy(value, themeTypeActive, len(list.themeTypes))

def menu_button_dy(value, i, count):
	if value == 1: i += 1
	if value == -1: i -= 1
	if i < 0: i = count - 1
	if i >= count: i = 0
	return i

def theme_appy():
	if theme_info_type(list.themeList[themeActive], list.themeTypes[themeTypeActive]) > 0:
		theme = themeActive
		if get_theme_type_apply(themeActive, themeTypeActive) == "yes":
			theme = 0
		
		ui.panelActive = "applying"
		ui.load_menu()

		theme_files_copy(list.themeList[theme], list.themeTypes[themeTypeActive])
		data_save("theme" + list.themeTypes[themeTypeActive], list.themeList[theme])

		ui.panelActive = ""
		ui.load_menu()

def theme_files_copy(theme, type):
	for folder in list.themeTypeFolders[type]:
		themePath = Path(AppDIR + "/themes/"+theme)
		folderPath = Path(str(themePath)+"/"+folder)
		paths = [
			str(p.relative_to(themePath)) for p in Path(folderPath).rglob('*') 
			if p.is_file() and p.suffix in {'.png', '.jpg'}
		]
		for p in paths:
			if(func.file_exists(get_path("app", theme)+"/"+p)):
				func.file_copy(get_path("app", theme) +"/"+ p, get_path("dev") +"/"+ os.path.dirname(p))

def get_theme_type_apply(theme, type):
	if themeData.get("theme"+list.themeTypes[type]) == list.themeList[theme]:
		return "yes"
	else:
		return "none"

def get_theme_any_apply(theme):
	used = 0
	for type in range(len(list.themeTypes)):
		if get_theme_type_apply(theme, type) == "yes":
			used += 1
	if used == len(list.themeTypes):
		return "yes"
	elif used > 0:
		return "part"
	else:
		return ""

def get_theme_img(theme):
	return get_path("app", list.themeList[theme]) + "/theme.png"

def get_path(type, theme=""):
	path = ""
	if type == "app":
		path = AppDIR + "/themes/"+theme
	if type == "dev":
		path = "/mnt/vendor"
	return path

def data_save(name, value):
	global themeData
	themeData[name] = value
	func.save_json(themeData, AppDIR + "/data/themes.json")

def data_load():
	global themeData
	themeData = func.load_json(AppDIR + "/data/themes.json")
	return themeData

def theme_list_load():
	dirs = os.listdir(AppDIR + "/themes")
	for theme in dirs:
		if not theme in list.themeList:
			list.themeList.append(theme)

def theme_info_load(theme):
	list.themeInfos[theme] = func.load_json(AppDIR + "/themes/"+theme+"/info.json")
	theme_info_types(theme)

def theme_info(theme, key):
	if list.themeInfos.get(theme) == None:
		theme_info_load(theme)
	if key == "name" and list.themeInfos[theme].get("name") == None:
		return theme
	return list.themeInfos[theme].get(key, "")

def theme_info_title(theme):
	t = theme_info(theme, "name")
	if theme_info(theme, "author") != "":
		t += " by " + theme_info(theme, "author")
	return t

def theme_info_types(theme):
	for type in list.themeTypeFolders:
		count = 0
		for folder in list.themeTypeFolders[type]:
			if func.file_exists(AppDIR + "/themes/"+theme+"/"+folder):
				count += 1
		list.themeInfos[theme][type+"Count"] = count

def theme_info_type(theme, type):
	return list.themeInfos[theme].get(type+"Count", 0)