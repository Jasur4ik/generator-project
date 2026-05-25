import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# --- Конфигурация ---
TOKEN = "8813494935:AAEf82gOc2pUsR-O-fn2JjAyTPWKW_RJy-Q"  # Замените на реальный токен от BotFather

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Клавиатуры ---
main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔬 О проекте", callback_data="about")],
    [InlineKeyboardButton(text="👥 Команда", callback_data="team")],
    [InlineKeyboardButton(text="📊 Текущие результаты", callback_data="results")],
    [InlineKeyboardButton(text="📐 Рассчитать снижение шума", callback_data="calc")]
])

# --- Команда /start ---
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "⚡ Привет! Я бот проекта «Генератор 2.0».\n"
        "Помогу узнать о проекте, команде и результатах.\n"
        "А также рассчитать ожидаемое снижение шума.\n\n"
        "Выбери нужный раздел:",
        reply_markup=main_keyboard
    )

# --- Обработчики кнопок ---
@dp.callback_query(F.data == "about")
async def about(callback):
    await callback.message.edit_text(
        "🔬 *О проекте*\n\n"
        "🎯 *Цель:* Снизить шум генератора на ≥15 дБ(А) и вибрацию на ≥40%.\n"
        "🔧 *Решение:* Кит-набор (кожух, глушитель, виброопоры, пространственная рама).\n"
        "🏭 *Аудитория:* Промышленность, строительство, больницы, военные, частные дома.\n\n"
        "📊 *Статистика:* 350 000+ генераторов продаётся ежегодно.",
        parse_mode="Markdown",
        reply_markup=main_keyboard
    )

@dp.callback_query(F.data == "team")
async def team(callback):
    await callback.message.edit_text(
        "👥 *Команда проекта*\n\n"
        "👨‍🏫 *Руководитель:* Ефремов Андрей Евгеньевич\n\n"
        "Участники:\n"
        "• Алексеев Кирилл — конструктор кожуха\n"
        "• Бизюкин Матвей — акустические измерения\n"
        "• Коваленко Максим — система выпуска\n"
        "• Никитин Дмитрий — виброопоры\n"
        "• Солдаткин Михаил — 3D-моделирование\n"
        "• Соловьёв Александр — испытания\n"
        "• Тарусин Дмитрий — материаловедение\n"
        "• Чудаков Никита — проектирование рамы\n"
        "• Шепель Семён — система охлаждения\n"
        "• Джураев Джасур — сборка\n"
        "• Майнагашев Сергей — сертификация\n"
        "• Ашаков Артём — экономика проекта\n\n"
        "Всего 12 участников + руководитель. Проект реализуется на базе Московского Политеха.",
        parse_mode="Markdown",
        reply_markup=main_keyboard
    )

@dp.callback_query(F.data == "results")
async def results(callback):
    await callback.message.edit_text(
        "📊 *Текущие результаты*\n\n"
        "✅ Снижение шума: до *16 дБ(А)* на отдельных моделях (цель 15 дБ).\n"
        "✅ Снижение вибрации: *42%*.\n"
        "✅ Этап: внедрение опытной серии (10 комплектов передано партнёрам).\n"
        "✅ Сертификация по ГОСТ Р 12.2.017-2012 начата.\n\n"
        "Планируем завершить проект к февралю 2027 года.",
        parse_mode="Markdown",
        reply_markup=main_keyboard
    )

@dp.callback_query(F.data == "calc")
async def calc(callback):
    await callback.message.edit_text(
        "📐 *Рассчитать снижение шума*\n\n"
        "Введите текущий уровень шума генератора в децибелах (например, 95).\n"
        "Я рассчитаю, какой будет шум после установки кит-набора.\n\n"
        "❗️ Отправьте число в следующем сообщении.",
        parse_mode="Markdown",
        reply_markup=main_keyboard
    )

# --- Обработчик ввода числа (расчёт) ---
@dp.message(F.text.regexp(r"^\d+$"))
async def calc_noise(message: Message):
    try:
        current_noise = int(message.text)
        if current_noise < 30 or current_noise > 120:
            await message.answer("⚠️ Пожалуйста, введите реалистичный уровень шума (30–120 дБ).")
            return
        reduction = 16  # среднее снижение по проекту
        new_noise = current_noise - reduction
        if new_noise < 0:
            new_noise = 0
        await message.answer(
            f"🔊 Исходный шум: *{current_noise} дБ(А)*\n"
            f"🔇 После установки кит-набора: *{new_noise} дБ(А)*\n"
            f"📉 Снижение: *{reduction} дБ(А)*\n\n"
            f"Это соответствует целевым показателям проекта (≥15 дБ).",
            parse_mode="Markdown"
        )
    except:
        await message.answer("❌ Ошибка. Отправьте число.")

# --- Запуск ---
async def main():
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())