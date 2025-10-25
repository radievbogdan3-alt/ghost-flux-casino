import logging
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import config

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CasinoBot:
    def __init__(self):
        self.application = Application.builder().token(config.BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("admin", self.admin_panel))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = user.id
        
        # Инициализация пользователя
        if user_id not in config.users_db:
            config.users_db[user_id] = {
                "balance": 0,
                "inventory": [],
                "username": user.username
            }
        
        # Клавиатура с Web App
        keyboard = [
            [InlineKeyboardButton("🎰 Открыть казино", web_app=WebAppInfo(url=f"{config.BOT_WEBAPP_URL}/index.html?user_id={user_id}"))],  # ← ЗАПЯТАЯ ДОБАВЛЕНА
            [InlineKeyboardButton("💰 Мой баланс", callback_data="balance"),
             InlineKeyboardButton("🎒 Инвентарь", callback_data="inventory")],
            [InlineKeyboardButton("📢 Наш канал", url=f"https://t.me/{config.CHANNEL[1:]}")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"👻 Добро пожаловать в Ghost FluX Casino, {user.first_name}!\n\n"
            "🎮 Испытай удачу в нашей рулетке!\n"
            "💫 Выигрывай ценные призы!\n\n"
            "Нажми кнопку ниже чтобы начать играть!",
            reply_markup=reply_markup
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        user_id = query.from_user.id
        
        await query.answer()
        
        if query.data == "balance":
            balance = config.users_db[user_id]["balance"]
            await query.edit_message_text(
                f"💰 Ваш баланс: {balance} звезд\n\n"
                f"Чтобы пополнить баланс, свяжитесь с администратором: {config.ADMIN_USERNAME}"
            )
        
        elif query.data == "inventory":
            inventory = config.users_db[user_id]["inventory"]
            if not inventory:
                await query.edit_message_text("🎒 Ваш инвентарь пуст")
            else:
                items_text = "\n".join([f"{item['emoji']} {item['name']} - {item['value']} звезд" for item in inventory])
                await query.edit_message_text(
                    f"🎒 Ваш инвентарь:\n\n{items_text}\n\n"
                    f"Для вывода свяжитесь с {config.ADMIN_USERNAME}"
                )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        # Админ команды
        if user_id == config.ADMIN_ID:
            text = update.message.text
            if text.startswith("/add"):
                try:
                    _, target_user_id, amount = text.split()
                    target_user_id = int(target_user_id)
                    amount = int(amount)
                    
                    if target_user_id not in config.users_db:
                        config.users_db[target_user_id] = {
                            "balance": 0,
                            "inventory": [],
                            "username": "unknown"
                        }
                    
                    config.users_db[target_user_id]["balance"] += amount
                    await update.message.reply_text(f"✅ Добавлено {amount} звезд пользователю {target_user_id}")
                    
                except Exception as e:
                    await update.message.reply_text("❌ Ошибка формата: /add user_id amount")
    
    async def admin_panel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        
        if user_id != config.ADMIN_ID:
            await update.message.reply_text("❌ У вас нет доступа к админ панели")
            return
        
        total_users = len(config.users_db)
        total_balance = sum(user["balance"] for user in config.users_db.values())
        
        keyboard = [
            [InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")],
            [InlineKeyboardButton("⏰ Ожидают вывода", callback_data="admin_withdrawals")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            f"👑 Админ панель Ghost FluX\n\n"
            f"👥 Пользователей: {total_users}\n"
            f"💰 Общий баланс: {total_balance} звезд\n"
            f"⏰ Запросов на вывод: {len(config.withdraw_requests)}",
            reply_markup=reply_markup
        )
    
    def run(self):
        self.application.run_polling()

if __name__ == "__main__":
    bot = CasinoBot()
    bot.run()