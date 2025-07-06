import sys
import png

def read_character():
	text = ""
	while len(text) != 1:
		while len(text) == 0:
			text = input("Enter a character: ");
		if len(text) > 1:
			sys.stderr.write("Please enter only one character.")
	return text

def translate_character(string):
	fontfile = open("font.h")
	bitmapfontfilecontent = fontfile.readlines()
	img = [()] * 8

	for ch in string:
		chnum = ord(ch)
		if chnum > 0x20:
			startline = 0
			while not '{' in bitmapfontfilecontent[startline]:
				startline += 1

			bitmapline = bitmapfontfilecontent[startline + chnum - 0x20]

			bitmapstr = ""

			for b in bitmapline:
				if b in "1234567890abcdefx":
					bitmapstr += b
			bitmap = int(bitmapstr, 16)
		else:
			bitmap = 0

		for x in range(8):
			for y in range(8):
				if (bitmap >> (x * 8 + y)) & 0x1 == 0x1:
					img[x] += (255, 255, 255)
				else:
					img[x] += (0,0,0)

	with open('output.png', 'wb') as fp:
		png.Writer(8 * len(string), 8, greyscale=False).write(fp, img)

if __name__ == '__main__':
	print(translate_character("abcdefghijklmnopqrstuvwxyz"))
