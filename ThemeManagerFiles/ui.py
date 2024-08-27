import graphic as gr
import app
import func
import input
import list

menuActive = ""
panelActive = ""

# def menu_box(text, i, active=False):
# 	y = 50 + (i * 35)
# 	if active:	
# 		gr.draw_rectangle_r([20, y, 300, y+35], 5, fill=gr.colorBlue, outline=gr.colorBlueD1)
# 	if app.themeApply == i:
# 		check = "yes" if i == 0 else "part" if i == 1 else "none"
# 		gr.draw_image("/img/check_"+check+".png", position=(270, y + 4))
# 	gr.draw_text((25, y + 5), text)

def line_checkbox(text, pos, width, active=False, hover=False, check="", readonly=False):
	if active or hover:
		gr.draw_rectangle_r([pos[0], pos[1], pos[0]+width, pos[1]+32], 5, fill=(gr.colorBlue if active else gr.colorGrayL1))
	if not readonly and check != "":
		gr.draw_image("/img/check_"+check+".png", position=(pos[0]+width-30, pos[1] + 4))
	color = 'white'
	if readonly:
		color = gr.colorGrayL1
	gr.draw_text((pos[0]+5, pos[1] + 5), text, color=color)

def load_menu():
	gr.draw_clear()

	# gr.draw_log(str(input.code) + " " + input.codeName + " " + str(input.value))
	
	gr.draw_rectangle_r([10, 40, 630, 440], 15, fill=gr.colorGrayD2, outline=None)

	gr.draw_text((320, 20), "Theme Manager", anchor="mm")
	for i in range(len(list.themeList)):
		line_checkbox(list.themeList[i], (20, 50 + (i * 35)), 290, 
				active = app.themeActive==i and menuActive == "", 
				hover = app.themeActive==i, 
				check = app.get_theme_any_apply(i)
		)
	
	gr.draw_text((470, 295), app.theme_info_title(list.themeList[app.themeActive]), font=11, anchor="mm")

	for i in range(len(list.themeTypes)):
		line_checkbox(list.themeTypeNames[list.themeTypes[i]], (320, 310 + (i * 35)), 300, 
			active = app.themeTypeActive==i,
			hover = False, 
			check = app.get_theme_type_apply(app.themeActive, i),
			readonly=app.theme_info_type(list.themeList[app.themeActive], list.themeTypes[i]) == 0
		)

	abuttontext = "Select"
	if app.themeTypeActive == -1:
		button_circle((30, 460), "A", abuttontext)
	else:
		if app.themeActive == 0 and app.get_theme_type_apply(0, app.themeTypeActive) == "yes":
			abuttontext = "Apply"
		elif app.get_theme_type_apply(app.themeActive, app.themeTypeActive) == "yes":
			abuttontext = "Undo"
		else:
			abuttontext = "Apply"
		button_circle((30, 460), "A", abuttontext)
		button_circle((133, 460), "B", "Back")
		# button_circle((225, 460), "Y", "Preview " + list.themeTypeNames[list.themeTypes[app.themeTypeActive]])


	# if panelActive == "accept":
	# 	panel_dialog("Cancel", "Apply", "Will the selected theme be applied?")
	if panelActive == "applying":
		panel_info("Applying theme...")
	# if panelActive == "applyingOk":
	# 	panel_ok("Theme applied")
	
	gr.draw_paint()

	if panelActive == "":
		if func.file_exists(app.get_theme_img(app.themeActive)):
			gr.draw_image_path(app.get_theme_img(app.themeActive), position=(320,50), screenWrite=True)

def panel_dialog(b1, b2, text):
	gr.draw_rectangle_r([90, 160, 550, 350], 15, fill=gr.colorGray, outline=gr.colorGrayL1)
	gr.draw_text((320, 200), text, anchor="mm")
	button_circle((190, 300), "B", b1)
	button_circle((390, 300), "A", b2)
	gr.draw_paint()

def panel_info(text):
	gr.draw_rectangle_r([90, 180, 550, 260], 15, fill=gr.colorGray, outline=gr.colorGrayL1)
	gr.draw_text((320, 220), text, anchor="mm")
	gr.draw_paint()

def panel_ok(text):
	gr.draw_rectangle_r([90, 180, 550, 300], 15, fill=gr.colorGray, outline=gr.colorGrayL1)
	gr.draw_text((320, 220), text, anchor="mm")
	button_circle((300, 260), "A", "OK")

def button_circle(pos, button, text):
	gr.draw_circle(pos, 15, fill=gr.colorBlueD1, outline=None)
	gr.draw_text(pos, button, anchor="mm")
	gr.draw_text((pos[0] + 20, pos[1]), text, font=13, anchor="lm")

