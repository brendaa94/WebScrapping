import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

def extrair_dados_e_processar(url, chrome_driver_path, nome_arquivo_saida):
    # Inicializa o driver do Chrome
    chrome_options = Options()
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Acessa a página da web
        driver.get(url)
        time.sleep(3)  # Espera para o carregamento da página

        # Extrai o HTML do elemento desejado
        dados_0 = driver.find_element(By.CLASS_NAME, "view-content")
        html_0 = dados_0.get_attribute("innerHTML")

        # Analisa o HTML para obter os dados
        soup = BeautifulSoup(html_0, 'html.parser')
        resultado = soup.get_text()

        # Escreve os dados em um arquivo CSV
        with open(nome_arquivo_saida, "w", encoding="utf-8") as f:
            f.write(resultado)

        # Lê os dados do arquivo CSV e os processa
        df = pd.read_csv(nome_arquivo_saida, header=None)
        df_saida = pd.DataFrame()
        ii = 0
        while ii < df.shape[0]:
            df_aux = pd.DataFrame([[df.values[ii][0].strip(), df.values[ii+1][0].strip()]])
            df_saida = pd.concat([df_aux, df_saida])
            ii += 2
        
        # Renomeia as colunas e salva o resultado em um novo arquivo CSV
        df_saida = df_saida.rename(columns={0:'Partido',1:'Vereador'})
        df_saida.to_csv(nome_arquivo_saida, index=False, sep=';', encoding='cp1252')

    finally:
        # Fecha o driver
        driver.quit()

def main():
    url = "https://www.cmbh.mg.gov.br/vereadores"
    chrome_driver_path = r'C:\Users\brend\chromedriver.exe'
    nome_arquivo_saida = "Partido_Vereador.csv"
    
    extrair_dados_e_processar(url, chrome_driver_path, nome_arquivo_saida)

if __name__ == "__main__":
    main()
