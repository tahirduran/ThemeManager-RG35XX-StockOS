from fcntl import ioctl
from PIL import Image, ImageDraw, ImageFont
import mmap
import os
import func

fb: any
mm: any
screen_width=640
screen_height=480
bytes_per_pixel = 4
screen_size = screen_width * screen_height * bytes_per_pixel
AppDIR = os.path.dirname(os.path.abspath(__file__))

fontFile = {}
fontFile[15] = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 15)
fontFile[13] = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 13)
fontFile[11] = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 11)
colorBlue = "#bb7200"
colorBlueD1 = "#7f4f00"
colorGray = "#292929"
colorGrayL1 = "#383838"
# colorGrayD1 = "#222222"
colorGrayD2 = "#141414"

activeImage: Image.Image
activeDraw: ImageDraw.ImageDraw

def screen_reset():
	ioctl(fb, 0x4601, b'\x80\x02\x00\x00\xe0\x01\x00\x00\x80\x02\x00\x00\xc0\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x18\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00^\x00\x00\x00\x96\x00\x00\x00\x00\x00\x00\x00\xc2\xa2\x00\x00\x1a\x00\x00\x00T\x00\x00\x00\x0c\x00\x00\x00\x1e\x00\x00\x00\x14\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
	ioctl(fb, 0x4611, 0)

def screen_write(b, pos=(0,0)):
	mm.seek((pos[0]+pos[1]*screen_width)*4)
	mm.write(b)

def draw_start():
	global fb, mm
	fb = os.open('/dev/fb0', os.O_RDWR)
	mm = mmap.mmap(fb, screen_size)

def draw_end():
	mm.close()
	os.close(fb)

def draw_paste(base_image, overlay_image, position):
	base_image = base_image.convert('RGBA')
	overlay_image = overlay_image.convert('RGBA')    
	overlay_width, overlay_height = overlay_image.size
	base_data = base_image.load()
	overlay_data = overlay_image.load()
	for x in range(overlay_width):
		for y in range(overlay_height):
			if x + position[0] < base_image.width and y + position[1] < base_image.height:
				overlay_pixel = overlay_data[x, y]
				if overlay_pixel[3] > 126:  # Şeffaf olmayan pikselleri kontrol et
					base_data[x + position[0], y + position[1]] = overlay_pixel
	return base_image

def draw_image(image_path, **kwargs):
	draw_image_path(AppDIR + image_path, **kwargs)

def draw_image_path(image_path, position=(0, 0), resize=None, screenWrite=False):
	imgOverlay = Image.open(image_path)
	if resize:
		imgOverlay = imgOverlay.resize(resize, box=(0,0,resize[0],resize[1]))
	if screenWrite:
		draw_image_screenwrite(imgOverlay, position)
	else:
		global activeImage, activeDraw
		activeImage = draw_paste(activeImage, imgOverlay, position)
		activeDraw = ImageDraw.Draw(activeImage)

def draw_image_screenwrite(img, pos):
	img = img.convert('RGBA')
	r, g, b, a = img.split()
	img = Image.merge('RGBA', (b, g, r, a))
	width, height = img.size
	image_data = img.tobytes()
	for row in range(height):
		screen_offset = ((pos[1] + row) * screen_width + pos[0]) * 4
		mm.seek(screen_offset)
		row_start = row * width * 4
		row_end = row_start + (width * 4)
		mm.write(image_data[row_start:row_end])

def crate_image():
	image = Image.new('RGBA', (screen_width, screen_height), color='black')
	return image

def draw_active(image):
	global activeImage, activeDraw
	activeImage = image
	activeDraw = ImageDraw.Draw(activeImage)

def draw_paint():
	global activeImage
	mm.seek(0)
	mm.write(activeImage.tobytes())

def draw_clear():
	global activeDraw
	activeDraw.rectangle([0, 0, screen_width, screen_height], fill='black')

def draw_text(position, text, font=15, color='white', **kwargs):
	global activeDraw
	activeDraw.text(position, text, font=fontFile[font], fill=color, **kwargs)

def draw_rectangle(position, fill=None, outline=None, width=1):
	global activeDraw
	activeDraw.rectangle(position, fill=fill, outline=outline, width=width)

def draw_rectangle_r(position, radius, fill=None, outline=None):
	global activeDraw
	activeDraw.rounded_rectangle(position, radius, fill=fill, outline=outline)

def draw_circle(position, radius, fill=None, outline='white'):
	global activeDraw
	activeDraw.ellipse([position[0]-radius, position[1]-radius, position[0]+radius, position[1]+radius], fill=fill, outline=outline)

def draw_log(text):
	draw_rectangle([0, 0, 300, 85], fill="Black", outline='black')
	draw_text((0, 5), text)

def screen_shot():
	global fb
	# framebuffer_data = os.read(fb, screen_size)
	# os.lseek(fb, 0, os.SEEK_SET)
	pixels = []
	for i in range(0, len(mm), 4):
		b = mm[i]
		g = mm[i + 1]
		r = mm[i + 2]
		a = 255
		pixels.append((r, g, b, a))
	image = Image.new("RGBA", (screen_width, screen_height))
	image.putdata(pixels)
	imgid = 1
	os.makedirs(AppDIR + "/ss", exist_ok=True)
	while func.file_exists(AppDIR + "/ss/img"+str(imgid)+".png"):
		imgid += 1
	image.save(AppDIR + "/ss/img"+str(imgid)+".png")


draw_start()
screen_reset()

imgMain = crate_image()
draw_active(imgMain)
# draw_image(AppDIR + "/img.png", position=(100, 50))

# draw_rectangle([10, 50, 300, 85], fill=None, outline='gray')
# draw_text("Hello World!", position=(15, 55))
# draw_paint()

# draw_end()