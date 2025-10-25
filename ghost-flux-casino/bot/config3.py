import os

BOT_TOKEN = "7877247730:AAEz52OmuzAX940LEjnS6mNrGBmXIEZ5hSw"
ADMIN_ID = 5450857649
ADMIN_USERNAME = "@KXKXKXKXKXKXKXKXKXKXK"
CHANNEL = "@Ghost_FluX"

# Настройки игры
ROULETTE_COST = 50
MIN_DEPOSIT = 50
MAX_DEPOSIT = 200

# Призы и их вероятности
PRIZES = [
    {"name": "Мишка", "value": 15, "probability": 0.35, "emoji": "🧸"},
    {"name": "Сердечко", "value": 15, "probability": 0.35, "emoji": "💖"},
    {"name": "Ракета", "value": 50, "probability": 0.10, "emoji": "🚀"},
    {"name": "Торт", "value": 50, "probability": 0.10, "emoji": "🎂"},
    {"name": "Кубок", "value": 100, "probability": 0.05, "emoji": "🏆"},
    {"name": "Кольцо", "value": 100, "probability": 0.05, "emoji": "💍"}
]

# База данных (временная, для демо)
users_db = {}
withdraw_requests = []