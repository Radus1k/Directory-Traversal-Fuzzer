from flask import Flask
import markdown
import os

app = Flask(__name__)

@app.route("/")
def index():
    with open(os.path.dirname(app.root_path) + 'README/md', 'r') as markdown_file:
        #Read the content of file:
        content = markdown_file.read()

        #convert to HTML
        return markdown.markdown(content)
