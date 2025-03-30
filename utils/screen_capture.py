import cv2
import numpy as np
from mss import mss
import time
import pyautogui

def countdown(seconds=3):
    """Contagem regressiva para preparar o full screen"""
    for i in range(seconds, 0, -1):
        print(f"Iniciando em {i}... (Deixe o jogo em tela cheia)")
        time.sleep(1)
    print("Capturando tela!")
    time.sleep(0.5)  # Tempo extra para garantir foco

def capture_game_window():
    """Captura a tela inteira (full screen)"""
    with mss() as sct:
        monitor = sct.monitors[1]  # Monitor principal
        img = np.array(sct.grab(monitor))
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

# TESTE: Execute este arquivo para ver se a captura funciona
if __name__ == '__main__':
    countdown()
    img = capture_game_window()
    cv2.imwrite('C:\\EternalQuestAI\\data\\test_screenshot.png', img)
    print("Captura salva em 'data/test_screenshot.png'")