from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    clima = None
    erro = None
    if request.method == "POST":
        cidade = request.form.get("cidade")
        if cidade:
            api_key = "13e36c28ecc1f0ea053a1f1fa9c9ccf5"
            url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&units=metric&lang=pt_br"
            try:
                res = requests.get(url)
                if res.status_code == 200:
                    clima = res.json()
                else:
                    erro = "Cidade não encontrada. Verifique a ortografia."
            except requests.exceptions.RequestException:
                erro = "Erro de conexão com o servidor de meteorologia."
    return render_template("index.html", clima=clima, erro=erro)

if __name__ == "__main__":
    app.run(debug=True)