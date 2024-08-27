import time
import os
import graphic as graphic
import input
import ui
import app


AppDIR = os.path.dirname(os.path.abspath(__file__))


app.start()

while True:
	
	app.update()
	

	# if code == "X":
	# 	for i in range(7):
	# 		func.copy_file(AppDIR + "/themes/BasicGray/res2/theme/0/lcd/"+str(i)+".png", "/mnt/vendor/res2/theme/0/lcd")
	# 		func.copy_file(AppDIR + "/themes/BasicGray/res2/theme/0/lcd/"+str(i)+"A.png", "/mnt/vendor/res2/theme/0/lcd")
	# if code == "Y":
	# 	for i in range(7):
	# 		func.copy_file(AppDIR + "/themes/default/res2/theme/0/lcd/"+str(i)+".png", "/mnt/vendor/res2/theme/0/lcd")
	# 		func.copy_file(AppDIR + "/themes/default/res2/theme/0/lcd/"+str(i)+"A.png", "/mnt/vendor/res2/theme/0/lcd")
		# for i in range(7):
		# 	func.copy_file("/mnt/vendor/res2/theme/0/lcd/"+str(i)+".png", AppDIR + "/themes/default/res2/theme/0/lcd")
		# 	func.copy_file("/mnt/vendor/res2/theme/0/lcd/"+str(i)+"A.png", AppDIR + "/themes/default/res2/theme/0/lcd")

	# if time.time() - timeStart > 60:
	# 	break


# time.sleep(5)