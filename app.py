from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)
CORS(app)

# modelagem
# usuario (username, senha)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(16), nullable=True)

# rota de login
@app.route('/login')


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
    return jsonify({'message': 'Product not found in database.'}), 404

# rota de detalhes do produto
@app.route('/api/products/<int:product_id>', methods=['GET'])
def getProduct(product_id):
    product = Product.query.get(product_id)
    if product != None:
        return jsonify({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description
        })
    return jsonify({'message': 'Product not found.'}), 404

# rota de atualização
@app.route('/api/products/update/<int:product_id>', methods=['PUT'])
def updProduct(product_id):
    product = Product.query.get(product_id)
    if product == None:
        return jsonify({'message': 'Product not found'}), 404
    
    data = request.json
    if 'name' in data:
        product.name = data['name']

    if 'price' in data:
        product.price = data['price']

    if 'description' in data:
        product.description = data['description']

    db.session.commit()  
    return jsonify({'message': 'Product updated successfully.'})

#rota de listagem de protutos
@app.route('/api/products', methods=['GET'])
def getProducts():
    products = Product.query.all()
    productList = []
    for product in products:
        productData = {
            'id': product.id,
            'name': product.name,
            'price': product.price
        }
        productList.append(productData)
    return jsonify(productList)



# rota raiz // funcao executada ao requisitar
@app.route('/')
def helloWorld():
    return 'Hello World!'

# rodar aplicaçao
if __name__ == '__main__':
    app.run(debug=True)