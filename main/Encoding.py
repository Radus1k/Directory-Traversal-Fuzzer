import binascii
import urllib.parse
import base64
import html

# values = ["URL", "HTML", "Base64", "Text", "Hex", "Binary"]
from tkinter import END


class Encoder:
    def __init__(self, given_str):
        self.str = given_str

    def toUrl(self):
        return urllib.parse.quote(self.str)

    def fromUrl(self):
        return urllib.parse.unquote(self.str)

    def toBase64(self):
        encodedBytes = base64.b64encode(self.str.encode("utf-8"))
        return str(encodedBytes, "utf-8")

    def fromBase64(self):
        return base64.b64decode(self.str)

    def fromHtml(self):
        print('ere')
        return html.unescape(self.str)

    def toHex(self):
        return binascii.hexlify(bytearray(self.str, 'utf8'))

    def fromHex(self):
        print("from hex to text")
        return binascii.unhexlify(bytearray(self.str, 'utf8'))


    def toBinary(self):
        return ' '.join(format(ord(x), 'b') for x in self.str)

    def fromBinary(self):
        return self.str.encode('ascii')

    @staticmethod
    def write_to_TextWidget(string, widget):
        # First delete everything in there67to90987
        widget.delete('1.0', END)
        widget.insert('1.0', string)

    def set_Results_encoded(self, arg, text_widget):
        if len(self.str) > 1:
            if arg == "Base64":
                self.write_to_TextWidget(self.toBase64(), text_widget)
            elif arg == "URL":
                self.write_to_TextWidget(self.toUrl(), text_widget)
            elif arg == "Hex":
                self.write_to_TextWidget(self.toHex(), text_widget)
            elif arg == "Binary":
                self.write_to_TextWidget(self.toBinary(), text_widget)
            else:
                return "error at getting decoding results"

    #values_to_decode = ["URL", "HTML", "Base64", "Text", "Hex", "Binary"]
    def set_Results_decoded(self, arg, text_widget):
        if len(self.str) > 1:
            if arg == "Base64":
                self.write_to_TextWidget(self.fromBase64(), text_widget)
            elif arg == "URL":
                self.write_to_TextWidget(self.fromUrl(), text_widget)
            elif arg == "HTML":
                self.write_to_TextWidget(self.fromHtml(), text_widget)
            elif arg == "Hex":
                self.write_to_TextWidget(self.fromHex(), text_widget)
            elif arg == "Binary":
                self.write_to_TextWidget(self.fromBinary(), text_widget)
            else:
                return "error at getting decoding results"
