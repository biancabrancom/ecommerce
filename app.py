from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

# modelagem
# produto (id, nome, preco, descricao)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

# rota de adição de produto
@app.route('/api/products/add', methods=['POST'])
def addProduct():
    data = request.json
    if 'name' and 'price' in data:
        product = Product(name=data['name'], price=data['price'], description=data.get('description', ''))
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully.'})
    return jsonify({'message': 'Invalid product data.'}), 400

# rota de remoção
@app.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
def delProduct(product_id):
#recuperar, verificar, se existe -> apagar, se nao -> 404
    product = Product.query.get(product_id)
    if product != None:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully.'})
    return jsonify({'message': 'Product not found in database.'}), 400

#    data = request.json
#    if 'product' and 'price' in data:
        
        

# rota raiz // funcao executada ao requisitar
@app.route('/')
def helloWord():
    return 'Hello World!'

# rodar aplicaçao
if __name__ == '__main__':
    app.run(debug=True)