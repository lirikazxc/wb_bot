import json

from aiogram import *
from aiogram.filters import *
from aiogram.types import *
from utils.wildberries_api import WildberriesAPI
from utils.config_manager import add_shop, delete_shop, list_shops
from utils.report_formatter import *
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from aiogram import types, Bot


router = Router()


HELP_TEXT = """
Добро пожаловать в Telegram-бот для аналитики продаж на Wildberries! 📊

Вот доступные команды для удобной работы с ботом:

➕  /addshop - Добавить магазин 🏪
❌  /delshop - Удалить магазин 🗑️
📋  /shops - Список магазинов 📈
📊  /report - Получить отчет о продажах 🤑
❓  /help - Помощь, если возникнут вопросы 💬

Начните использовать и получайте точные данные о ваших продажах на Wildberries! 🚀
"""

#/start#
@router.message(Command("start"))
async def send_welcome(message: Message):
    help_text = HELP_TEXT
    await message.answer(help_text)



#/help#
@router.message(Command("help"))
async def send_help(message: Message):
    help_text = HELP_TEXT
    await message.answer(help_text)



#/report#
@router.message(Command("report"))
async def report_command(message: Message, state: FSMContext):
    shops = list_shops()
    if not shops:
        await message.answer("У вас нет доступных магазинов.")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=shop["name"], callback_data=f"select_shop:{shop['name']}")]
        for shop in shops
    ])

    await message.answer("Выберите магазин для отчета:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("select_shop:"))
async def select_shop(call: CallbackQuery, state: FSMContext):
    shop_name = call.data.split(":")[1]
    await state.update_data(shop_name=shop_name)
    await call.answer()

    period_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сегодня", callback_data="period_today")],
        [InlineKeyboardButton(text="Вчера", callback_data="period_yesterday")],
        [InlineKeyboardButton(text="Последние 7 дней", callback_data="period_last_7_days")],
        [InlineKeyboardButton(text="Кастомный период", callback_data="period_custom")]
    ])

    await call.message.answer(f"Вы выбрали магазин {shop_name}. Теперь выберите период для отчета:", reply_markup=period_keyboard)



@router.callback_query(F.data.startswith("report_sales"))
async def report_sales(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await fetch_and_send_report(call, state, report_type="sales")

@router.callback_query(F.data.startswith("report_stocks"))
async def report_stocks(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await fetch_and_send_report(call, state, report_type="stocks")

@router.callback_query(F.data.startswith("report_incomes"))
async def report_incomes(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await fetch_and_send_report(call, state, report_type="incomes")

@router.callback_query(F.data.startswith("report_orders"))
async def report_orders(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await fetch_and_send_report(call, state, report_type="orders")

@router.callback_query(F.data.startswith("report_reportDetailByPeriod"))
async def report_reportDetailByPeriod(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await fetch_and_send_report(call, state, report_type="reportDetailByPeriod")

# @router.callback_query(F.data.startsWith("report_all"))
# async def report_all(call: CallbackQuery, state: FSMContext):
#     await call.answer()
#     await fetch_and_send_report(call, state, report_type="all")


@router.callback_query(F.data == "period_today")
async def period_today(call: CallbackQuery, state: FSMContext):
    current_time = datetime.now()

    start_date = current_time.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
    end_date = (current_time - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")

    await state.update_data(start_date=start_date, end_date=end_date)

    await call.message.answer(f"Вы выбрали период: Сегодня ({start_date} - {end_date})")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отчет по продажам", callback_data="report_sales")],
        [InlineKeyboardButton(text="Отчет по остаткам", callback_data="report_stocks")],
        [InlineKeyboardButton(text="Отчет по поставкам", callback_data="report_incomes")],
        [InlineKeyboardButton(text="Отчет по заказам", callback_data="report_orders")],
        [InlineKeyboardButton(text="Детальный отчет по периодам", callback_data="report_reportDetailByPeriod")],
        # [InlineKeyboardButton(text="Получить все отчеты", callback_data="report_all")]
    ])

    await call.message.answer("Теперь выберите тип отчета:", reply_markup=keyboard)


@router.callback_query(F.data == "period_yesterday")
async def period_yesterday(call: CallbackQuery, state: FSMContext):
    current_time = datetime.now() - timedelta(days=1)

    start_date = current_time.replace(hour=0, minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
    end_date = current_time.replace(hour=23, minute=59, second=59, microsecond=999999).strftime("%Y-%m-%d %H:%M:%S")

    await state.update_data(start_date=start_date, end_date=end_date)

    await call.message.answer(f"Вы выбрали период: Вчера ({start_date} - {end_date})")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отчет по продажам", callback_data="report_sales")],
        [InlineKeyboardButton(text="Отчет по остаткам", callback_data="report_stocks")],
        [InlineKeyboardButton(text="Отчет по поставкам", callback_data="report_incomes")],
        [InlineKeyboardButton(text="Отчет по заказам", callback_data="report_orders")],
        [InlineKeyboardButton(text="Детальный отчет по периодам", callback_data="report_reportDetailByPeriod")],
        # [InlineKeyboardButton(text="Получить все отчеты", callback_data="report_all")]
    ])

    await call.message.answer("Теперь выберите тип отчета:", reply_markup=keyboard)


@router.callback_query(F.data == "period_last_7_days")
async def period_last_7_days(call: CallbackQuery, state: FSMContext):
    current_time = datetime.now()

    start_date = (current_time - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
    end_date = (current_time - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")

    await state.update_data(start_date=start_date, end_date=end_date)

    await call.message.answer(f"Вы выбрали период: Последние 7 дней ({start_date} - {end_date})")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отчет по продажам", callback_data="report_sales")],
        [InlineKeyboardButton(text="Отчет по остаткам", callback_data="report_stocks")],
        [InlineKeyboardButton(text="Отчет по поставкам", callback_data="report_incomes")],
        [InlineKeyboardButton(text="Отчет по заказам", callback_data="report_orders")],
        [InlineKeyboardButton(text="Детальный отчет по периодам", callback_data="report_reportDetailByPeriod")],
        # [InlineKeyboardButton(text="Получить все отчеты", callback_data="report_all")]
    ])

    await call.message.answer("Теперь выберите тип отчета:", reply_markup=keyboard)

@router.callback_query(F.data == "period_custom")
async def period_custom(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Введите дату начала периода (в формате YYYY-MM-DD HH:MM:SS):")
    await state.set_state("waiting_for_start_date")

@router.message(StateFilter("waiting_for_start_date"))
async def set_start_date(message: types.Message, state: FSMContext):
    start_date = message.text.strip()
    await state.update_data(start_date=start_date)
    await message.answer(f"Дата начала установлена на {start_date}. Теперь введите дату окончания периода:")
    await state.set_state("waiting_for_end_date")

@router.message(StateFilter("waiting_for_end_date"))
async def set_end_date(message: Message, state: FSMContext):
    end_date = message.text.strip()
    await state.update_data(end_date=end_date)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отчет по продажам", callback_data="report_sales")],
        [InlineKeyboardButton(text="Отчет по остаткам", callback_data="report_stocks")],
        [InlineKeyboardButton(text="Отчет по поставкам", callback_data="report_incomes")],
        [InlineKeyboardButton(text="Отчет по заказам", callback_data="report_orders")],
        [InlineKeyboardButton(text="Детальный отчет по периодам", callback_data="report_reportDetailByPeriod")],
        # [InlineKeyboardButton(text="Получить все отчеты", callback_data="report_all")]
    ])

    await message.answer("Теперь выберите тип отчета:", reply_markup=keyboard)
    await state.set_state("waiting_for_report_type")



async def fetch_and_send_report(call, state: FSMContext, report_type: str = None):
    user_data = await state.get_data()
    shop_name = user_data.get("shop_name")
    start_date = user_data.get("start_date")
    end_date = user_data.get("end_date")

    if not start_date or not end_date:
        await call.message.answer("Ошибка: Период не задан. Пожалуйста, выберите или введите период.")
        return

    api_key = load_api_key_by_shop(shop_name)
    if not api_key:
        await call.message.answer(f"Ошибка: не найден API ключ для магазина '{shop_name}'.")
        return

    endpoint_map = {
        "sales": "https://statistics-api.wildberries.ru/api/v1/supplier",
        "stocks": "https://statistics-api.wildberries.ru/api/v1/supplier",
        "incomes": "https://statistics-api.wildberries.ru/api/v1/supplier",
        "orders": "https://statistics-api.wildberries.ru/api/v1/supplier",
        "reportDetailByPeriod": "https://statistics-api.wildberries.ru/api/v5/supplier",
    }

    endpoint = endpoint_map.get(report_type, endpoint_map["sales"])

    wb_api = WildberriesAPI(api_url=endpoint, api_key=api_key)

    report_data = wb_api.get_sales_data(start_date, end_date) if report_type == "sales" else None
    if report_type == "stocks":
        report_data = wb_api.get_stocks_data(start_date, end_date)
    elif report_type == "incomes":
        report_data = wb_api.get_incomes_data(start_date, end_date)
    elif report_type == "orders":
        report_data = wb_api.get_orders_data(start_date, end_date)
    elif report_type == "reportDetailByPeriod":
        report_data = wb_api.get_reportDetailByPeriod_data(start_date, end_date)

    if report_data:
        if report_type == "sales":
            report = await handle_sales_report(report_data)
        elif report_type == "stocks":
            report = await handle_stocks_report(report_data)
        elif report_type == "incomes":
            report = await handle_incomes_report(report_data)
        elif report_type == "orders":
            report = await handle_orders_report(report_data)
        elif report_type == "reportDetailByPeriod":
            report = await handle_reportDetailByPeriod(report_data)

        await send_report_as_text(call, report)
    else:
        await call.message.answer("Не удалось получить данные.")

async def send_report_as_text(call, report):
    max_length = 4096
    if isinstance(call, CallbackQuery):
        for i in range(0, len(report), max_length):
            await call.message.answer(report[i:i + max_length])
    elif isinstance(call, Message):
        for i in range(0, len(report), max_length):
            await call.answer(report[i:i + max_length])


#/addshop
@router.message(Command("addshop"))
async def add_shop_command(message: Message, state: FSMContext):
    await message.answer("Введите API-ключ вашего магазина:")
    await state.set_state("waiting_for_api_key")

@router.message(StateFilter("waiting_for_api_key"))
async def save_shop_api_key(message: Message, state: FSMContext):
    api_key = message.text.strip()


    wb_api = WildberriesAPI(api_url="https://common-api.wildberries.ru", api_key=api_key)

    response = wb_api.ping()
    if not response:
        await message.answer("Неверный API-ключ. Попробуйте снова.")
        return

    await message.answer("Введите имя магазина:")
    await state.update_data(api_key=api_key)
    await state.set_state("waiting_for_shop_name")

def is_duplicate_shop(shop_name: str, api_key: str) -> str:
    with open('config.json', 'r') as f:
        config = json.load(f)

    for shop in config['shops']:
        if shop['name'] == shop_name:
            return f"Магазин с именем '{shop_name}' уже существует."
        if shop['api_key'] == api_key:
            return f"API-ключ уже используется другим магазином."
    return None



@router.message(StateFilter("waiting_for_shop_name"))
async def save_shop_name(message: Message, state: FSMContext):
    shop_name = message.text.strip()
    user_data = await state.get_data()
    api_key = user_data.get("api_key")
    duplicate_message = is_duplicate_shop(shop_name, api_key)
    if duplicate_message:
        await message.answer(duplicate_message)
        await state.clear()
        return
    add_shop(api_key, shop_name)
    await message.answer(f"Магазин '{shop_name}' успешно добавлен!")
    await state.clear()

# Команда /shops
@router.message(Command("shops"))
async def list_shops_command(message: Message):
    shops = list_shops()
    if not shops:
        await message.answer("Нет сохранённых магазинов.")
        return

    shop_list = "\n".join([f"- {shop['name']}" for shop in shops])
    await message.answer(f"Сохранённые магазины:\n{shop_list}")


# Команда /delshop
@router.message(Command("delshop"))
async def delete_shop_command(message: Message, state: FSMContext):
    shops = list_shops()
    if not shops:
        await message.answer("Нет доступных магазинов для удаления.")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Удалить магазин", callback_data="delete_shop")],
    ])
    inline_buttons = [
        [InlineKeyboardButton(text=shop["name"], callback_data=f"delshop:{shop['name']}")]
        for shop in shops
    ]

    keyboard.inline_keyboard = inline_buttons

    await message.answer("Выберите магазин для удаления:", reply_markup=keyboard)


@router.callback_query(F.data.startswith("delshop:"))
async def confirm_delete_shop(call: CallbackQuery, state: FSMContext):
    if call.data.startswith("delshop:"):
        shop_name = call.data.split(":")[1]
        delete_shop(shop_name)
        await call.message.answer(f"Магазин '{shop_name}' успешно удалён.")
        await call.answer()



async def setup_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="help", description="Справка по командам"),
        BotCommand(command="addshop", description="Добавить магазин"),
        BotCommand(command="delshop", description="Удалить магазин"),
        BotCommand(command="shops", description="Список магазинов"),
        BotCommand(command="report", description="Получить отчет"),
    ]
    await bot.set_my_commands(commands)


def load_api_key_by_shop(shop_name: str) -> str:
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)

        for shop in config['shops']:
            if shop['name'] == shop_name:
                return shop['api_key']

        return None

    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None