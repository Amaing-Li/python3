import base64

left_align_png = "left_align_png.jpg"
binary = open(left_align_png, "rb").read()
ascii_text = ""
for i, c in enumerate(base64.b64decode(binary)):
    if i and i % 68 == 0:
        ascii_text += "\\\n"
    ascii_text += chr(c)
print(ascii_text)

LEFT_ALIGN_PNG = b"""\
iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABGdBTUEAALGPC/xhBQAA"""
binary = base64.b64decode(LEFT_ALIGN_PNG)
print(binary)