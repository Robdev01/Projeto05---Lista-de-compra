from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista de espera com itens
lista_de_espera = []

# Função enumerate
def enumerate_context(iterable):
    return enumerate(iterable)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/waiting_list', methods=['GET'])
def waiting_list_page():
    total_value = sum(item['value'] * item.get('quantity', 1) for item in lista_de_espera)
    total_items = len(lista_de_espera)
    return render_template('lista_de_espera.html', lista_de_espera=lista_de_espera, total_value=total_value, total_items=total_items, enumerate=enumerate_context)

@app.route('/add_to_waiting_list', methods=['POST'])
def add_to_waiting_list():
    item = request.form['item']
    try:
        value = float(request.form.get('value', 0.0))
    except ValueError:
        value = 0.0
    try:
        quantity = int(request.form.get('quantity', 1))
    except ValueError:
        quantity = 1
    lista_de_espera.append({'text': item, 'value': value, 'quantity': quantity, 'completed': False})
    return redirect(url_for('waiting_list_page'))

@app.route('/remove_from_waiting_list/<int:item_id>', methods=['POST'])
def remove_from_waiting_list(item_id):
    if 0 <= item_id < len(lista_de_espera):
        del lista_de_espera[item_id]
    return redirect(url_for('waiting_list_page'))

@app.route('/toggle_item/<int:item_id>', methods=['POST'])
def toggle_item(item_id):
    if 0 <= item_id < len(lista_de_espera):
        lista_de_espera[item_id]['completed'] = not lista_de_espera[item_id]['completed']
    return redirect(url_for('waiting_list_page'))

@app.route('/edit_value/<int:item_id>', methods=['POST'])
def edit_value(item_id):
    if 0 <= item_id < len(lista_de_espera):
        try:
            new_value = float(request.form['value'])
        except ValueError:
            new_value = lista_de_espera[item_id]['value']  # Retain old value if conversion fails
        lista_de_espera[item_id]['value'] = new_value
    return redirect(url_for('waiting_list_page'))

if __name__ == '__main__':
    app.run(debug=True)
