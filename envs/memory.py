class MapMemory:
    def __init__(self):
        self.explored = {}  # Formato: {(x,y): "inimigo/seguro"}
        self.current_pos = (0, 0)  # Posição relativa inicial

    def update_position(self, movement):
        """Atualiza posição baseada no movimento (W/A/S/D)"""
        x, y = self.current_pos
        if movement == 'w': y += 1
        elif movement == 's': y -= 1
        elif movement == 'a': x -= 1
        elif movement == 'd': x += 1
        self.current_pos = (x, y)

    def log_encounter(self, enemy_type):
        """Registra inimigos encontrados"""
        self.explored[self.current_pos] = enemy_type