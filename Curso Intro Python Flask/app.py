#Importação
from flask import Flask, request, jsonify  #importação da classe flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__) #passando a váriavel é padrão, porém instancia o aplicativo do flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db=SQLAlchemy(app)


#Modelagem
#Produto (Id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True) #opcional

@app.route('/api/products/add', methods=["POST"])
def add_product():
    data = request.json
    if 'name' in data and 'price' in data: 
        #dois formatos de chamar o campo do json que está sendo recebido abaixo, nos dois primeiros campos, se não achar vai dar erro, no segundo formato se ele não encontrar ele vai chamar o valor padrão "" em branco
        product = Product(name=data["name"],price=data["price"], description=data.get("description", ""))     
        db.session.add(product) #adicionando as informações de produto
        db.session.commit() #comitando as informações no banco. 
        return jsonify({"message":"Product added successfully"}) #não precisa do 200, porque já é padrão.
    #precisa retornar a mensagem em json, 
    return jsonify({"message": "Invalid product data"}), 400 #400 é para devolver o código de erro 


@app.route('/api/products/delete/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:  
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message":"Product deleted successfully"}) 
    return jsonify({"message": "Product not found"}), 404 


#Definir uma rota raiz (página inicial) e a função que será executada, quando a aplicação ou usuário requisitar
@app.route('/')
def hello_world():
    return 'Hello World'
if __name__== "__main__":
    app.run(debug=True)
   

