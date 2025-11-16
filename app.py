#Importação
from flask import Flask  #importação da classe flask

app = Flask(__name__) #passando a váriavel é padrão, porém instancia o aplicativo do flask

#Definir uma rota raiz (página inicial) e a função que será executada, quando a aplicação ou usuário requisitar
@app.route('/teste')
def hello_world():
    return 'Hello World'
if __name__== "__main__":
    app.run(debug=True)
   

