from flask import Flask
import markdown
import os

app = Flask(__name__)

@app.route("/")
def index():
	print("\n\n\n\n    CALLED     \n\n\n\n")
        with open(os.path.dirname(app.root_path) + 'intro.txt', 'r') as markdown_file:
        	#Read the content of file:
        	content = markdown_file.read()

        #convert to HTML
        return markdown.markdown(content)
