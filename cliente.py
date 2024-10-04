import tkinter as tk
from tkinter import filedialog, messagebox
import requests

def upload_file():
    # Abre uma janela de seleção de arquivo
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    
    if not file_path:
        return  # Se nenhum arquivo foi selecionado, retorna

    # Define a URL do endpoint de upload
    url = 'http://192.168.1.2:5000/print'
    
    # Cria um dicionário com o arquivo para o envio
    files = {'file': open(file_path, 'rb')}
    
    try:
        # Envia o arquivo usando uma solicitação POST
        response = requests.post(url, files=files)
        
        # Verifica se a solicitação foi bem-sucedida
        if response.status_code == 200:
            messagebox.showinfo("Sucesso", "Arquivo enviado com sucesso!")
        else:
            messagebox.showerror("Erro", f"Falha ao enviar o arquivo: {response.text}")
    except Exception as e:
        messagebox.showerror("Erro", str(e))
    finally:
        files['file'].close()  # Certifique-se de fechar o arquivo

# Cria a janela principal
root = tk.Tk()
root.title("Cliente de Upload de PDF")

# Cria um botão para fazer o upload
upload_button = tk.Button(root, text="Selecionar PDF e Enviar", command=upload_file)
upload_button.pack(pady=20)

# Inicia o loop da interface gráfica
root.mainloop()
