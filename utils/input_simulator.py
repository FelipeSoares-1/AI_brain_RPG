import pyautogui
import time
from typing import List

class GameController:
    def __init__(self):
        self.key_binds = {
            'retreat_left': ['a', 's', 'space'],
            'engage_right': ['d', 'w', '2'],
            'engage_left': ['a', 'w', '1'],
            'move_right': ['d'],
            'move_left': ['a'],
            'explore': ['w', 'a', 'w', 'd']  # Padrão de exploração
        }
    
    def execute_sequence(self, action_name):
        """Executa uma sequência de teclas"""
        if action_name not in self.key_binds:
            raise ValueError(f"Ação desconhecida: {action_name}")
            
        for key in self.key_binds[action_name]:
            self.press_key(key)
    
    def press_key(self, key, duration=0.1):
        """Pressiona uma tecla individual"""
        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)
        print(f"[AÇÃO] {key}")

    def focus_game(self):
        """Garante que o jogo está em foco clicando em uma posição segura"""
        try:
            pyautogui.click(x=100, y=100)  # Ajuste as coordenadas conforme necessário
            time.sleep(0.5)  # Tempo para o jogo receber foco
            print("[FOCUS] Jogo em foco")
        except Exception as e:
            print(f"[ERRO] Falha ao focar no jogo: {e}")
            raise