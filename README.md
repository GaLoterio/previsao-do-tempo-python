# Previsão do Tempo

App em Python com interface gráfica (Tkinter) que mostra o clima atual e a previsão dos próximos dias para qualquer cidade ou bairro, usando a API gratuita [Open-Meteo](https://open-meteo.com/).

## Funcionalidades

- Busca por nome de cidade ou bairro
- Temperatura, descrição do tempo, umidade e vento atuais
- Previsão diária com mínima, máxima e probabilidade de chuva

## Como rodar

```bash
git clone https://github.com/GaLoterio/previsao-do-tempo-python.git
cd previsao-do-tempo-python
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Tecnologias

Python 3, Tkinter, requests e Open-Meteo (geocoding e forecast).

## Observação

Os dados são previsões de modelos meteorológicos, não medições de um ponto exato, então podem divergir um pouco de outros apps.
