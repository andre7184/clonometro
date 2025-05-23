import tkinter as tk
from tkinter import ttk
import time
import pygame
import threading

class Cronometro:
    def __init__(self, root, column):
        self.rodando = False
        self.tempo_inicial = 0
        self.tempo_decorrido = 0

        self.frame = tk.Frame(root, bg="black")
        self.frame.grid(row=1, column=column, sticky="nsew", padx=10, pady=10)

        self.label = tk.Label(self.frame, text="00:00:00", font=("Helvetica", 60), fg="yellow", bg="black")
        self.label.pack(fill="both", expand=True)

        self.botoes_frame = tk.Frame(self.frame, bg="black")
        self.botoes_frame.pack(pady=10)

        self.botao_iniciar = tk.Button(self.botoes_frame, text="Iniciar", command=self.iniciar,
                                       bg="black", fg="yellow", font=("Helvetica", 12))
        self.botao_iniciar.pack(side="left", padx=5)

        self.botao_parar = tk.Button(self.botoes_frame, text="Parar", command=self.parar,
                                     bg="red", fg="black", font=("Arial black", 15))
        self.botao_parar.pack(side="left", padx=5)

        self.botao_resetar = tk.Button(self.botoes_frame, text="Resetar", command=self.resetar,
                                       bg="black", fg="yellow", font=("Helvetica", 12))
        self.botao_resetar.pack(side="left", padx=5)

        self.atualizar_tela()

    def iniciar(self):
        if not self.rodando:
            self.rodando = True
            self.tempo_inicial = time.time() - self.tempo_decorrido
            self.atualizar_tela()

    def parar(self):
        if self.rodando:
            self.rodando = False
            self.tempo_decorrido = time.time() - self.tempo_inicial
            
            threading.Thread(target=self.tocar_som).start()

    def resetar(self):
        self.rodando = False
        self.tempo_inicial = 0
        self.tempo_decorrido = 0
        self.label.config(text="00:00:00")

    def atualizar_tela(self):
        if self.rodando:
            self.tempo_decorrido = time.time() - self.tempo_inicial
        tempo_formatado = self.formatar_tempo(self.tempo_decorrido)
        self.label.config(text=tempo_formatado)
        self.label.after(100, self.atualizar_tela)

    def formatar_tempo(self, segundos):
        minutos, segundos = divmod(int(segundos), 60)
        horas, minutos = divmod(minutos, 60)
        return f"{horas:02}:{minutos:02}:{segundos:02}"

    
    def tocar_som(self):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("galo.mp3")
            pygame.mixer.music.play()
            print("🎵 Som tocado com sucesso! 🎵")
        except Exception as e:
            print(f"⚠️ Erro ao tocar o som: {e}")



def iniciar_todos():
    for c in cronometros:
        c.iniciar()


root = tk.Tk()
root.title("Cronômetros")
root.configure(bg="black")
root.state('zoomed')

root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=1)
for i in range(4):
    root.grid_columnconfigure(i, weight=1)

btn_iniciar_todos = tk.Button(
    root, text="▶ Iniciar Todos", command=iniciar_todos,
    bg="black", fg="yellow", font=("Helvetica", 30)
)
btn_iniciar_todos.grid(row=0, column=0, columnspan=4, pady=20)

cronometros = [Cronometro(root, i) for i in range(4)]

root.mainloop() 
