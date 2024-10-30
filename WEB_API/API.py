from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Inicializa o WebDriver
driver = webdriver.Chrome()
driver.get('https://web.whatsapp.com')

# Tempo para escanear o QR Code
input("Escaneie o QR Code e pressione Enter para continuar...")

# Lista para armazenar as mensagens coletadas
messages_data = []

# Aguardar e coletar mensagens
try:
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, 'message-in')))
    
    # Loop para coletar e processar mensagens
    while True:
        chat_elements = driver.find_elements(By.CLASS_NAME, 'message-in')
        
        for element in chat_elements:
            try:
                # Obter remetente, conteúdo da mensagem e horário
                sender = element.find_element(By.CLASS_NAME, 'copyable-text').get_attribute('data-pre-plain-text')
                content = element.find_element(By.CLASS_NAME, 'selectable-text').text
                time_sent = element.find_element(By.CLASS_NAME, 'x1rg5ohu').text
                
                # Armazenar as informações coletadas
                message = {
                    'Sender': sender,
                    'Content': content,
                    'Time': time_sent
                }
                
                # Adiciona à lista se não for duplicado
                if message not in messages_data:
                    messages_data.append(message)
                    print("Mensagem coletada:", message)  # Exibir a mensagem coletada
                    
                    # Salvar em Excel após adicionar uma nova mensagem
                    df = pd.DataFrame(messages_data)
                    df.to_excel(r'c:\Users\user\Desktop\Projeto-api-production-day\mensagens_whatsapp.xlsx', index=False)
                    print("Dados salvos no Excel:", message)  # Mensagem de confirmação
                
            except Exception as e:
                print("Erro ao processar mensagem:", e)
                    
        # Pausa para atualização
        time.sleep(5)

except Exception as e:
    print("Erro geral:", e)

finally:
    driver.quit()
