#Importação
from flask import Flask, request, jsonify  #importação da classe flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS #biblioteca que permite que outros sistemas de fora podem acessar o sistema, no caso o swagger, não consegui acessar, porque não criei usuário no swagger.
#classe UserMixin: utilizada para poder gravar os usuários, essa classe já vem com alguns recursos de validação;
#Pacote login_user: faz o processo de autenticação do usuário; não consegui entender se é uma classe ou só pacote
#Pacote LoginManager: Faz o gerenciamento dos usuáiros que estão ou não logados; não consegui entender se é uma classe ou só pacote
#Pacote login_required Faz a obrigação de usuário estar logado nas rotas que serão mexidas, ou seja só usuários validos;
#Método logout_user, para deslogar o usuário;
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

app = Flask(__name__) #passando a váriavel é padrão, porém instancia o aplicativo do flask
app.config['SECRET_KEY'] = "minha_chave_123" #O Login_Manger pede uma chave para autenticação, normalmente são chaves maiores e geradas, mas como é para estudo só colocamos uma padrão.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db=SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

#Modelagem
#Usuários (id, username, password)
class User(db.Model, UserMixin):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column(db.String(80), nullable=False, unique=True)
     password = db.Column(db.String(80), nullable=True)

#Produto (Id, name, price, description)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True) #opcional

#Autenticação - Antes de mexer nas rotas
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#logout
@app.route('/logout', methods=["POST"])
@login_required
def logout():
     logout_user()
     return jsonify({"message":"Logout successfully"})

#Rotas

#Rotas de usuários
@app.route('/login', methods=["POST"])
def login():
     data = request.json
  
     user = User.query.filter_by(username=data.get("username")).first()
     
     if user!= None:  # pode ser feito resumindo como if user, fiz no outro formato para lembrar bem
        if data.get("password") == user.password: #validando se a senha esta cadastrada no banco de dados;
          login_user(user) #Usando a classe de login_user
          return jsonify({"message":"Logged in successfully"})
     
     return jsonify({"message":"Unauthorized. Invalid credentials"}), 401
    
    #forma reduziada referente a parte acima. Porém ficou com erro
    #if user and data.get("password") == user.password: 
    # return jsonify({"message":"Logged in successfully"})

    #return jsonify({"message":"Unauthorized. Invalid credentials"}), 401
   
#Rotas de produtos
@app.route('/api/products/add', methods=["POST"])
@login_required
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
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:  
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message":"Product deleted successfully"}) 
    return jsonify({"message": "Product not found"}), 404 

@app.route('/api/products/<int:product_id>', methods=["GET"])
def get_product_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify ({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })
    return jsonify({"message":"Product not found"}), 404

@app.route('/api/products/update/<int:product_id>', methods=["PUT"])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
            return jsonify({"message": "Product not found"}), 404
    
    data = request.json
    if 'name' in data:
            product.name = data['name']

    if 'price' in data:
            product.price = data['price']
    
    if 'description' in data:
            product.description = data ['description']
    
    db.session.commit()
    return jsonify ({'message':'Product updated successully'})

#Nessa rota, como se trata de vários produtos, ele retorna uma lista que é um array, portanto
#terá de ser usado o for para tratar a lista de produtos
@app.route('/api/products', methods=['GET'])
def get_products():
     products = Product.query.all()
     product_list = []
     for product in products:
        product_data = {
            "id": product.id,
            "name": product.name,
            "price": product.price,
        }
        product_list.append(product_data)
        
     return jsonify(product_list) 

#Definir uma rota raiz (página inicial) e a função que será executada, quando a aplicação ou usuário requisitar
@app.route('/')
def hello_world():
    return 'Hello World'
if __name__== "__main__":
    app.run(debug=True)
   

