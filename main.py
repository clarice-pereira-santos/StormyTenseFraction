import os
from flask import Flask
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv()

app = Flask(__name__)

supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

class tabela:
    def __init__(self, nome):
        self.nome = nome

    def listarconteudo(self):
        response = (
            supabase.table(self.nome)
            .select("*")
            .execute()
        )

        return response

    def criardataframe(self):
        return pd.DataFrame(self.listarconteudo().data)

    def mediaSegmento(self, segmento):
        df = self.criardataframe()
        return df[df["segmento"] == segmento]["total_venda"].mean()


@app.route('/')
def index():
    vendasinformatica = tabela("vendas_informatica")
    df = vendasinformatica.criardataframe()

    media_educacao = vendasinformatica.mediaSegmento("educacao")
    media_corporativo = vendasinformatica.mediaSegmento("corporativo")
    media_gamer = vendasinformatica.mediaSegmento("gamer")
    segmentos = ["Educação","corporativo","gamer"]
    medias = [media_educacao, media_corporativo,media_gamer]
    plt.figure(figsize=(8,5))
    plt.bar(segmentos,medias,color="red")
    plt.title("media de vendas por segmento")
    plt.xlabel("segmento")
    plt.ylabel("media")
    plt.savefig("static/medias_segmento.png")
    plt.close()
    return (
        df .to_html(index=False, border=1) 
        +f"<h3>Média do segmento Educação R$ {media_educacao:.2f}</h3>"
        +f"<h3>Média do segmento Corporativo R$ {media_corporativo:.2f}</h3>"
         +f"<h3>Média do segmento Gamer R$ {media_gamer:.2f}</h3>"
        + f"<img src='/static/medias_segmento.png'></img>"
    )

if __name__ == '__main__':
    app.run(debug=True)

