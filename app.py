from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)

# modelagem
# produto (id, nome, preco, descricao)
class product(db.Model);
    


# rota raiz // funcao executada ao requisitar
@app.route('/')
def helloWord():
    return 'Hello World!'

# rodar aplicaçao
if __name__ == '__main__':
    app.run(debug=True)