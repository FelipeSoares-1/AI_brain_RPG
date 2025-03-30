from envs.memory import MapMemory
import random

class DecisionMaker:
    def __init__(self):
        self.memory = MapMemory()
        
    def _low_health(self, game_state):
        """Verifica se a vida está abaixo de 30%"""
        return game_state.get("health", 100) < 30
        
    def choose_action(self, game_state):
        # 30% de chance de ação aleatória para explorar
        if random.random() < 0.3:
            return random.choice(["engage_right", "engage_left", "retreat_left"])
        
        # Lógica original (70% do tempo)
        if self._low_health(game_state):
            return "retreat_left"
        return "engage_right" if game_state["enemies"] > 2 else "engage_left"

if __name__ == '__main__':
    tester = DecisionMaker()
    print(tester.choose_action({"health": 10, "enemies": 1}))  # retreat_left
    print(tester.choose_action({"health": 50, "enemies": 3}))  # engage_right
    print(tester.choose_action({"health": 80, "enemies": 1}))  # engage_left