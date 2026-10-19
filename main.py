import tkinter as tk
import requests

DESCRICOES = {
    0: "Céu limpo",
    1: "Predominantemente limpo",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Neblina",
    61: "Chuva fraca",
    63: "Chuva moderada",
    65: "Chuva forte",
    80: "Pancadas de chuva",
    95: "Tempestade",
}


def buscar_cidade(nome):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    parametros = {"name": nome, "count": 1, "language": "pt"}
    resposta = requests.get(url, params=parametros, timeout=10)
    resposta.raise_for_status()
    resultados = resposta.json().get("results")

    if not resultados:
        return None
    return resultados[0]


def buscar_clima(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"
    parametros = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto",
    }
    resposta = requests.get(url, params=parametros, timeout=10)
    resposta.raise_for_status()
    return resposta.json()


def consultar():
    nome = entrada.get().strip()

    if not nome:
        lbl_local.config(text="Digite um local.")
        return

    try:
        local = buscar_cidade(nome)
        if not local:
            lbl_local.config(text="Local não encontrado.")
            lbl_temp.config(text="")
            lbl_desc.config(text="")
            lbl_extra.config(text="")
            lbl_previsao.config(text="")
            return

        dados = buscar_clima(local["latitude"], local["longitude"])
    except requests.exceptions.RequestException:
        lbl_local.config(text="Erro de conexão. Tente novamente.")
        return

    atual = dados["current"]
    descricao = DESCRICOES.get(atual["weather_code"], "Condição desconhecida")

    lbl_local.config(text=f"{local['name']} - {local.get('admin2', '')}")
    lbl_temp.config(text=f"{atual['temperature_2m']}°C")
    lbl_desc.config(text=descricao)
    lbl_extra.config(
        text=f"Umidade: {atual['relative_humidity_2m']}%   "
             f"Vento: {atual['wind_speed_10m']} km/h"
    )

    diario = dados["daily"]
    linhas = []
    for data, minima, maxima, chuva in zip(
        diario["time"],
        diario["temperature_2m_min"],
        diario["temperature_2m_max"],
        diario["precipitation_probability_max"],
    ):
        linhas.append(f"{data}:  {minima}° a {maxima}°  |  chuva {chuva}%")
    lbl_previsao.config(text="\n".join(linhas))


# --- Interface ---
janela = tk.Tk()
janela.title("Previsão do Tempo")
janela.geometry("380x480")

entrada = tk.Entry(janela, font=("Arial", 14))
entrada.pack(pady=(20, 5), padx=20, fill="x")
entrada.insert(0, "Vila Madalena")
entrada.bind("<Return>", lambda evento: consultar())  # Enter também consulta

botao = tk.Button(janela, text="Consultar", command=consultar)
botao.pack(pady=5)

lbl_local = tk.Label(janela, text="", font=("Arial", 16, "bold"))
lbl_local.pack(pady=(20, 0))

lbl_temp = tk.Label(janela, text="", font=("Arial", 48))
lbl_temp.pack()

lbl_desc = tk.Label(janela, text="", font=("Arial", 14))
lbl_desc.pack()

lbl_extra = tk.Label(janela, text="", font=("Arial", 11))
lbl_extra.pack(pady=5)

lbl_previsao = tk.Label(janela, text="", font=("Arial", 11), justify="left")
lbl_previsao.pack(pady=15)

janela.mainloop()