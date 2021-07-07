# Este módulo serve para rodar a aplicação instanciada no modulo app.
from app import app
import views

if __name__ == "__main__":
    app.run(debug=True)