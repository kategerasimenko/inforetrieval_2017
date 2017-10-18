from flask import Flask, request, render_template
from search_function import search


app = Flask(__name__)

 
@app.route('/')
def index():
    if request.args:
        query = request.args['query']
        links = search(query)[:10]
        return render_template('index.html',links=links)
    return render_template('index.html',links=[])

if __name__ == '__main__':
    app.run()
            
