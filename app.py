from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dicionário para armazenar múltiplas listas de compras
shopping_lists = {}

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', shopping_lists=shopping_lists, enumerate=enumerate)

@app.route('/add_shopping_list', methods=['POST'])
def add_shopping_list():
    name = request.form['name']
    category = request.form['category']
    value = request.form['value']
    shopping_lists[name] = {'category': category, 'value': value, 'items': []}
    return redirect(url_for('index'))

@app.route('/delete_shopping_list', methods=['POST'])
def delete_shopping_list():
    name = request.form['name']
    if name in shopping_lists:
        del shopping_lists[name]
    return redirect(url_for('index'))

@app.route('/add_item/<list_name>', methods=['POST'])
def add_item(list_name):
    if list_name in shopping_lists:
        item = request.form['item']
        shopping_lists[list_name]['items'].append({'text': item, 'completed': False})
    return redirect(url_for('index'))

@app.route('/delete_item/<list_name>/<int:item_id>')
def delete_item(list_name, item_id):
    if list_name in shopping_lists and 0 <= item_id < len(shopping_lists[list_name]['items']):
        del shopping_lists[list_name]['items'][item_id]
    return redirect(url_for('index'))

@app.route('/toggle_item/<list_name>/<int:item_id>')
def toggle_item(list_name, item_id):
    if list_name in shopping_lists and 0 <= item_id < len(shopping_lists[list_name]['items']):
        shopping_lists[list_name]['items'][item_id]['completed'] = not shopping_lists[list_name]['items'][item_id]['completed']
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
