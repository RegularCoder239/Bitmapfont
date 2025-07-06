import sys
import png
import math

def translate_string(string):
	string += "\n"
	fontfile = open("font.h")
	bitmapfontfilecontent = fontfile.readlines()
	longestline = 0
	for l in string.split("\n"):
		if len(l) > longestline:
			longestline = len(l)
	img = []
	for i in range(9 * string.count("\n")):
		img.append([0,0,0] * 8 * longestline)
	lineno = 0

	for line in string.split("\n"):
		chidx = 0
		for ch in line:
			chnum = ord(ch)
			if chnum > 0x20:
				startline = 0
				while not '{' in bitmapfontfilecontent[startline]:
					startline += 1

				bitmapline = bitmapfontfilecontent[startline + chnum - 0x1f]

				bitmapstr = ""
				prevb = ""
				for b in bitmapline:
					if b == "/" and prevb == "/":
						break;
					if b in "1234567890abcdefx":
						bitmapstr += b
					prevb = b
				bitmap = int(bitmapstr, 16)
			else:
				bitmap = 0

			for x in range(8):
				for y in range(8):
					if (bitmap >> (y * 8 + x)) & 0x1 == 0x1:
						img[y + lineno * 9][(x + chidx * 8) * 3 + 0] = 255
						img[y + lineno * 9][(x + chidx * 8) * 3 + 1] = 255
						img[y + lineno * 9][(x + chidx * 8) * 3 + 2] = 255
			chidx += 1
		lineno += 1
	imgtuple = []
	for idx in range(len(img)):
		imgtuple.append(tuple(img[idx]))

	with open('output.png', 'wb') as fp:
		png.Writer(8 * longestline, 9 * string.count("\n"), greyscale=False).write(fp, imgtuple)

if __name__ == '__main__':
	if len(sys.argv) != 1:
		text = open(sys.argv[1]).read(-1)
	else:
		text = input("Enter text: ")
	print(translate_string(text))
