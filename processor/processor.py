from flask import Flask, redirect, url_for, request, render_template, jsonify
import tfidf_loader

app = Flask(__name__)

@app.route('/search/<query_result>', methods=['GET'])
def searchResult(query_result):
    results = tfidf_loader.search_query(query_result)

    print(results)

    data = {}

    for index, each in enumerate(results):
        if each[0] != 0: data[index+1] = each[1]

    link_component = ''

    for ele in data.values():
        link_component += f'<div><a href={ele}>{ele.split("/")[-1]}</a></div>'
    
    return link_component

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == "POST":
        query = request.form['search_query']
        return redirect(url_for('searchResult', query_result=query))
    
    return render_template("search.html")

if __name__ == '__main__':
	app.run(debug=True)