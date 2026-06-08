from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    clima = None
    erro = None
    if request.method == "POST":
        cidade = request.form.get("cidade", "").strip
        if cidade:
            api_key = "13e36c28ecc1f0ea053a1f1fa9c9ccf5"
            url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric&lang=pt_br"
            try:
                res = requests.get(url, timeout=10)
                if res.status_code == 200:
                    clima = res.json()
                elif res.status_code == 400:
                    erro = f"Cidade '{cidade}' não encontrada. Verifica a ortografia."
                elif res.status_code == 401:
                    erro = "Erro de autenticação: Chave de API inválida."
                else:    
                    erro = f"Erro no servidor OpenWeather (Status: {res.status_code}.)"
            except requests.exceptions.ConnectionError:
                erro = "Erro de conexão: Não foi possivel alcançar o servidor de meteorologia."
            except requests.exceptions.ConnectTimeout:
                erro = "A requisição demorou muito para responder."
            except Exception as e:
                erro = f"Ocorreu um erro inesperado: {str(e)}"
        else: "Por favor, digite o nome de uma cidade."
    return render_template("index.html", clima=clima, erro=erro)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)