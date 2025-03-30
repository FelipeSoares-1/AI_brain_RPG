import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from envs.eternal_quest import EternalQuestEnv
from envs.memory import MapMemory
from envs.decision_maker import DecisionMaker
from utils.input_simulator import GameController
import time

def start_session():
    # Inicialização
    env = EternalQuestEnv()
    controller = GameController()
    memory = MapMemory()
    ai = DecisionMaker()

    print("=== Eternal Quest AI ===")
    print("1. Deixe o jogo em full screen")
    print("2. Não mova o mouse durante a execução")

    # Contagem regressiva
    for i in range(3, 0, -1):
        print(f"Iniciando em {i}...")
        time.sleep(1)

    # Estado inicial
    state = env.reset()
    
    try:
        while True:
            # 1. Obtém estado do jogo
            game_state = {
                "health": env.current_health,
                "enemies": env.detect_enemies(),
                "position": memory.current_pos
            }

            # 2. Escolhe ação (retorna nome da ação)
            action_name = ai.choose_action(game_state)
            
            # 3. Executa e atualiza ambiente
            next_state, reward, done, info = env.step(action_name)  # Passa o nome da ação
            
            # 4. Atualiza memória
            direction = action_name.split('_')[-1]  # 'left' ou 'right'
            memory.update_position(direction)
            
            print(f"Ação: {action_name} | Recompensa: {reward:.2f} | Vida: {game_state['health']}%")

            if done:
                print("Episódio concluído!")
                break

    except KeyboardInterrupt:
        print("Execução interrompida pelo usuário.")

if __name__ == '__main__':
    start_session()