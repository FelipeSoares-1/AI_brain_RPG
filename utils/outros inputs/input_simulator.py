import pyautogui
import time
from typing import List

class GameController:
    def __init__(self):
        self.key_binds = {
            # Movimento
            'move_up': 'w',
            'move_left': 'a',
            'move_down': 's',
            'move_right': 'd',
            'move_pattern_1': ['w', 'a', 'w', 'd'],  # Zigue-zague
            'move_pattern_2': ['w', 'w', 'd', 'd', 's', 's', 'a', 'a'],  # Quadrado
            
            # Combate
            'skill_combo_1': ['1', '2', '3'],  # AOE básico
            'skill_combo_2': ['4', '5', '2'],  # Single-target
            'burst_combo': ['9', '0', 'space'],  # Ultimate + coleta
            
            # Utilidades
            'collect_items': 'space',
            'switch_target': 'tab',
            'open_map': 'm'
        }
        self.cooldowns = {'skill_1': 0, 'skill_2': 0}  # Track cooldowns
    def focus_game(self):
        """Garante que o jogo está em foco"""
        pyautogui.click(x=100, y=100)  # Clique em posição segura do jogo
        time.sleep(0.5)
    def press_key(self, key: str, duration: float = 0.1):
        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)
        print(f"[ACTION] {key}")

    def execute_sequence(self, action_name: str):
        """Executa sequências complexas"""
        for key in self.key_binds[action_name]:
            self.press_key(key)
            time.sleep(0.15)  # Intervalo entre ações

# Teste
if __name__ == '__main__':
    gc = GameController()
    gc.execute_sequence('move_pattern_1')