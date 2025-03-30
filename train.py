import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque
from envs.eternal_quest import EternalQuestEnv

class DQN(nn.Module):
    def __init__(self, input_shape, n_actions):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(1, 32, 8, stride=4),  # Alterado para 1 canal
            nn.ReLU(),
            nn.Conv2d(32, 64, 4, stride=2),
            nn.ReLU()
        )
        self.fc = nn.Sequential(
            nn.Linear(64 * 9 * 9, 512),
            nn.ReLU(),
            nn.Linear(512, n_actions)
        )
        
    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.size(0), -1)
        return self.fc(x)

# Configurações
BATCH_SIZE = 32
MEMORY_SIZE = 10000

env = EternalQuestEnv()
model = DQN(input_shape=(1, 84, 84), n_actions=len(env.controller.key_binds))
optimizer = optim.Adam(model.parameters(), lr=0.0001)
memory = deque(maxlen=MEMORY_SIZE)

def train():
    for episode in range(50):
        state = env.reset()
        done = False
        total_reward = 0
        
        while not done:
            # 1. Escolhe ação (epsilon-greedy)
            if random.random() < 0.1:  # Exploração
                action = random.randint(0, len(env.controller.key_binds)-1)
            else:  # Exploitation
                with torch.no_grad():
                    q_values = model(state.unsqueeze(0))
                    action = torch.argmax(q_values).item()
            
            # 2. Executa ação
            next_state, reward, done, _ = env.step(action)
            total_reward += reward
            
            # 3. Armazena experiência
            memory.append((state, action, reward, next_state, done))
            
            # 4. Treina
            if len(memory) >= BATCH_SIZE:
                batch = random.sample(memory, BATCH_SIZE)
                # Implemente o treino aqui (loss e backprop)
            
            state = next_state
        
        print(f"Episódio {episode+1}, Recompensa: {total_reward}")

if __name__ == '__main__':
    train()