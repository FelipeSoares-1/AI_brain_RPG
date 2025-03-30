import cv2
import numpy as np
import torch
from utils.screen_capture import capture_game_window, countdown
from utils.input_simulator import GameController


class EternalQuestEnv:
    def __init__(self):
        self.controller = GameController()
        self.actions = list(self.controller.key_binds.keys())
        self.frame_stack = []  # Histórico de 4 frames
        self.current_xp = 0
        
    @property
    def current_health(self):
        img = capture_game_window()
        life_roi = img[30:50, 100:300]  # Ajuste as coordenadas
        
        # Detecta pixels da cor da vida CHEIA (ex: verde)
        life_color = cv2.inRange(life_roi, (0, 200, 0), (50, 255, 50))
        total_pixels = life_roi.size
        health_pixels = cv2.countNonZero(life_color)
        
        # Debug: salva imagem da barra de vida para ajuste
        cv2.imwrite('life_debug.png', life_roi)
        
        return int((health_pixels / total_pixels) * 100) if total_pixels > 0 else 100 # % de vida
    
    def detect_enemies(self):
        img = capture_game_window()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Ajuste esses valores para a cor dos inimigos no seu jogo
        lower_enemy = np.array([0, 100, 100])  
        upper_enemy = np.array([10, 255, 255])
        
        mask = cv2.inRange(hsv, lower_enemy, upper_enemy)
        cv2.imwrite('enemies_debug.png', mask)  # Para ajuste visual
        
        # Filtra contornos pequenos (ruído)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return len([c for c in contours if cv2.contourArea(c) > 50])  # Ignora contornos pequenos
    
    def _check_death(self, img):
        # Verifica tanto tela de morte quanto vida zerada
        death_screen = np.mean(img[100:150, 100:300]) > 200
        zero_health = self.current_health <= 0
        return death_screen or zero_health
    
    def reset(self):
        """Versão mais robusta do reset"""
        try:
            # Tenta focar no jogo (opcional)
            if hasattr(self.controller, 'focus_game'):
                self.controller.focus_game()
                
            img = capture_game_window()
            processed_img = self._preprocess(img)
            self.frame_stack = [processed_img] * 4
            return torch.stack(self.frame_stack)
        except Exception as e:
            print(f"[ERRO] Reset falhou: {e}")
            raise

    def step(self, action_name):
        """Versão completa e testada do step"""
        try:
            # 1. Executa ação
            self.controller.execute_sequence(action_name)
            
            # 2. Captura novo estado
            new_img = capture_game_window()
            processed_img = self._preprocess(new_img)
            
            # 3. Atualiza frame stack
            self.frame_stack.pop(0)
            self.frame_stack.append(processed_img)
            
            # 4. Calcula recompensa
            new_xp = self._detect_xp(new_img)
            xp_gained = new_xp - self.current_xp
            self.current_xp = new_xp
            reward = float(xp_gained * 10)  # Definindo reward aqui
            movement_bonus = 0.1 if action_name in ['move_right', 'move_left', 'explore'] else 0
            reward = (xp_gained * 10) + movement_bonus

            # 5. Verifica término
            done = self._check_death(new_img)
            
            # 6. Info adicional
            info = {
                "action": action_name,
                "xp_gained": xp_gained,
                "health": self.current_health
                
            }
            
            return torch.stack(self.frame_stack), reward, done, info
            
        except Exception as e:
            print(f"[ERRO] Step falhou: {e}")
            raise
    def _preprocess(self, img):
        """Prepara a imagem para a rede neural"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (84, 84)) / 255.0  # Normaliza para [0, 1]
        return torch.FloatTensor(resized)

    def _detect_xp(self, img):
        """Detecta XP na tela (simplificado - implemente sua lógica)"""
        # Exemplo: contar pixels dourados (ajuste os valores HSV)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_gold = np.array([20, 100, 100])
        upper_gold = np.array([30, 255, 255])
        mask = cv2.inRange(hsv, lower_gold, upper_gold)
        return cv2.countNonZero(mask)

    def _check_death(self, img):
        """Verifica se o personagem morreu (ex: tela vermelha)"""
        # Analisa região específica da tela
        roi = img[100:150, 100:300]  # Ajuste as coordenadas
        return np.mean(roi) > 200  # Se muito branco (game over)

# Teste manual
if __name__ == '__main__':
    env = EternalQuestEnv()
    state = env.reset()
    print("Estado inicial shape:", state.shape)
    
    next_state, reward, done, info = env.step(0)  # Testa primeira ação
    print(f"Recompensa: {reward} | Ação: {info['action']} | Terminou? {done}")

    