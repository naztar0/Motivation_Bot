from aiogram import Bot, Dispatcher, executor, types, utils
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import mysql.connector
import constants as const

bot = Bot(const.token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    func_elem_role = State()
    data = State()


# функция для отправки вариантов для первого вопроса
async def select_answers(message):
    # список вопросов, использовано форматирование Markdown
    answers = "*1.* _Воспитываю детей дома_\n" \
              "*2.* _Работаю удаленно как фрилансер или сотрудник_\n" \
              "*3.* _Я пока без работы, хочу заняться собой!_\n" \
              "*4.* _Я предприниматель, работаю на себя_\n" \
              "*5.* _Работаю и удаленно управляю командой сотрудников_\n" \
              "*6.* _Студент, учусь и осваиваю новые знания_\n" \
              "*7.* _Ни один из вариантов указанных выше_\n" \
              "*8.* _Занят в другой профессии, хочу получать напоминания от Мотиватора_"
    # создание инлайн клавиатуры
    key = types.InlineKeyboardMarkup()
    # создание кнопок для инлайн клавиатуры, первый параметр отвечает за текст на кнопке, второй за данные, которые потом будем принимать
    but_1 = types.InlineKeyboardButton("1", callback_data="mom_with_children")
    but_2 = types.InlineKeyboardButton("2", callback_data="remote_admin")
    but_3 = types.InlineKeyboardButton("3", callback_data="unemployed")
    but_4 = types.InlineKeyboardButton("4", callback_data="self_employed")
    but_5 = types.InlineKeyboardButton("5", callback_data="remote_top")
    but_6 = types.InlineKeyboardButton("6", callback_data="remote_student")
    but_7 = types.InlineKeyboardButton("7", callback_data="other")
    but_8 = types.InlineKeyboardButton("8", callback_data="worker")
    # добавление кнопок в клавиатуру, порядок и размещение будет такое же, как и в коде
    key.add(but_1, but_2, but_3)
    key.add(but_4, but_5, but_6)
    key.add(but_7, but_8)
    # отправка сообщения с вариантами ответов, текстом и инлайн клавиатурой
    await message.answer("Выбери один из пунктов, который лучше всего описывает твою ежедневную деятельность.\n\n"
                         "Свой выбор всегда можно будет изменить.\n\n" + answers, reply_markup=key, parse_mode="Markdown")


# действия при команде /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    try:
        # отправка сообщения пользователю
        await message.answer("Привет!😉 \n\nМелкие полезные действия войдут в привычку и окажут плодотворное влияние "
                             "только после их многоразового повторения.\n\nЯ буду тебе напоминать и мотивировать "
                             "делать полезные активности в течение дня.")
        # функция выбора ответов
        await select_answers(message)
    except utils.exceptions.BotBlocked: pass


# распределение напоминаний в зависимости от роли
async def select_notifications(call, answer, message_id=None):
    n = const.notifications
    notes = []
    # запись в словарь notes значения глобального словаря notifications в зависимости от выбранной роли
    if answer == "mom_with_children":
        notes.append({3: n[3], 4: n[4], 5: n[5], 9: n[9], 11: n[11], 12: n[12]})
    elif answer == "remote_admin":
        notes.append({1: n[1], 3: n[3], 4: n[4], 5: n[5], 7: n[7], 8: n[8], 9: n[9], 10: n[10], 11: n[11], 12: n[12]})
    elif answer == "unemployed":
        notes.append({3: n[3], 4: n[4], 5: n[5], 8: n[8], 9: n[9], 11: n[11], 12: n[12]})
    elif answer == "self_employed":
        notes.append({3: n[3], 4: n[4], 5: n[5], 8: n[8], 9: n[9], 11: n[11], 12: n[12]})
    elif answer == "remote_top":
        notes.append({1: n[1], 3: n[3], 4: n[4], 5: n[5], 6: n[6], 7: n[7], 8: n[8], 9: n[9], 10: n[10], 11: n[11], 12: n[12]})
    elif answer == "remote_student":
        notes.append({1: n[1], 3: n[3], 4: n[4], 6: n[6], 8: n[8], 9: n[9], 10: n[10], 11: n[11], 12: n[12]})
    elif answer == "other":
        notes.append({1: n[1], 3: n[3], 4: n[4], 5: n[5], 6: n[6], 7: n[7], 8: n[8], 9: n[9], 10: n[10], 11: n[11], 12: n[12]})
    elif answer == "worker":
        notes.append({1: n[1], 3: n[3], 4: n[4], 5: n[5], 6: n[6], 7: n[7], 8: n[8], 9: n[9], 10: n[10], 11: n[11], 12: n[12]})
    key = types.InlineKeyboardMarkup()
    conn = mysql.connector.connect(host=const.host, user=const.db_user, passwd=const.password, database=const.db_name)
    cursor = conn.cursor(buffered=True)
    selectExistsQuery = "SELECT EXISTS (SELECT ID FROM notifications WHERE user_id=(%s))"
    selectQuery = "SELECT {} FROM notifications WHERE user_id=(%s)"
    insertUserQuery = "INSERT INTO notifications(user_id) VALUES(%s)"
    setDefaultQuery = "UPDATE notifications SET {}=0 WHERE user_id=(%s)"
    updateQuery = "UPDATE notifications SET {}=1 WHERE user_id=(%s)"

    if message_id is None:
        cursor.execute(selectExistsQuery, [call.message.chat.id])
        exist = cursor.fetchone()[0]
        if exist == 0:
            cursor.execute(insertUserQuery, [call.message.chat.id])
        for note in const.notifications:
            cursor.execute(setDefaultQuery.format('n' + str(note)), [call.message.chat.id])
        for note in notes[0]:
            cursor.execute(updateQuery.format('n' + str(note)), [call.message.chat.id])
        conn.commit()
    # заполнение кнопки вариантами сообщений-уведомлений
    for note in notes[0]:
        cursor.execute(selectQuery.format('n' + str(note)), [call.message.chat.id])
        getNote = cursor.fetchone()[0]
        if getNote == 1:
            key.add(types.InlineKeyboardButton(str("✅ ") + str(notes[0][note]), callback_data=str(note)))
        else:
            key.add(types.InlineKeyboardButton(str("❌ ") + str(notes[0][note]), callback_data=str(note)))
    conn.close()
    # добавление в конце двух служебных кнопок
    key.add(types.InlineKeyboardButton("🆗 Закончить выбор", callback_data="exit"))
    key.add(types.InlineKeyboardButton("⬅ Вернуться назад", callback_data="retry_answer"))
    if message_id:
        try:
            # изменение значения кнопок (вкл./выкл.)
            await bot.edit_message_reply_markup(call.message.chat.id, message_id, reply_markup=key)
        except Exception as e:
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Не кликай так быстро")
            await bot.send_message(call.message.chat.id, "Error: " + str(e))                                                            ###### УЗНАТЬ ЧТО ЗА ИСКЛЮЧЕНИЕ ПРИ БЫСТРОМ КЛИКАНЬИ
    else:
        # отправка сообщения вместе с кнопками пользователю
        await bot.send_message(call.message.chat.id, "Выбери сообщения которые ты бы хотел получать или определи заново чем ты занимаешься на удаленке дома", reply_markup=key)


# подтверждение выбора роли
async def confirm_answer(call, answer, callback):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton("Да, всё правильно", callback_data="insert_" + callback)
    but_2 = types.InlineKeyboardButton("Нет, ответить ещё раз", callback_data="retry_answer")
    key.add(but_1)
    key.add(but_2)
    await bot.send_message(call.message.chat.id, "Вы выбрали вариант:\n_" + answer + "_\nВы подтверждаете этот вариант?", reply_markup=key, parse_mode="Markdown")


# обработка данных с инлайн клавиатуры
@dp.callback_query_handler(func=lambda call: True)
async def callback_inline(call: types.CallbackQuery):
    # Повторно задаем вопрос
    if call.data == "retry_answer":
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await select_answers(call.message)

    # Подтверждения ответа на стартовый вопрос
    elif call.data == "mom_with_children":
        # answer - название роли, которую выбрал пользователь, callback - значение, соответствующее роли
        # в дальнейшем ключи answer и callback писать не нужно, в первом они для примера
        await confirm_answer(call, answer="Воспитываю детей дома", callback="mom_with_children")
    elif call.data == "remote_admin":
        await confirm_answer(call, "Работаю удаленно как фрилансер или сотрудник", "remote_admin")
    elif call.data == "unemployed":
        await confirm_answer(call, "Я пока без работы, хочу заняться собой!", "unemployed")
    elif call.data == "self_employed":
        await confirm_answer(call, "Я предприниматель, работаю на себя", "self_employed")
    elif call.data == "remote_top":
        await confirm_answer(call, "Работаю и удаленно управляю командой сотрудников", "remote_top")
    elif call.data == "remote_student":
        await confirm_answer(call, "Студент, учусь и осваиваю новые знания", "remote_student")
    elif call.data == "other":
        await confirm_answer(call, "Ни один из вариантов указанных выше", "other")
    elif call.data == "worker":
        await confirm_answer(call, "Занят в другой профессии, хочу получать напоминания от Мотиватора", "worker")

    # Если ответ правильный - заносим в БД
    elif str(call.data)[:7] == "insert_":
        answer = str(call.data)[7:]
        conn = mysql.connector.connect(host=const.host, user=const.db_user, passwd=const.password, database=const.db_name)
        cursor = conn.cursor(buffered=True)
        existQuery = "SELECT EXISTS (SELECT ID FROM users WHERE user_id=(%s))"
        insertQuery = "INSERT INTO users (user_id, username, role) VALUES (%s, %s, %s)"
        updateQuery = "UPDATE users SET username=(%s), role=(%s) WHERE user_id=(%s)"
        cursor.execute(existQuery, [call.message.chat.id])
        exist = cursor.fetchone()[0]
        if exist == 1: cursor.executemany(updateQuery, [(call.from_user.username, answer, call.message.chat.id)])
        else: cursor.executemany(insertQuery, [(call.message.chat.id, call.from_user.username, answer)])
        conn.commit()
        conn.close()
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await select_notifications(call, answer)

    # если кнопка с выбором уведомлений присылает боту одно из следующих значений (порядковый номер уведомления), бот заносит ответ в БД
    elif call.data in {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'}:
        note = 'n' + str(call.data)
        conn = mysql.connector.connect(host=const.host, user=const.db_user, passwd=const.password, database=const.db_name)
        cursor = conn.cursor(buffered=True)
        selectQuery = "SELECT {} FROM notifications WHERE user_id=(%s)"
        updateQuery = "UPDATE notifications SET {}=(%s) WHERE user_id=(%s)"
        selectRoleQuery = "SELECT role FROM users WHERE user_id=(%s)"
        cursor.execute(selectQuery.format(note), [call.message.chat.id])
        result = cursor.fetchone()[0]
        if result == 1: cursor.executemany(updateQuery.format(note), [(0, call.message.chat.id)])
        else: cursor.executemany(updateQuery.format(note), [(1, call.message.chat.id)])
        conn.commit()
        cursor.execute(selectRoleQuery, [call.message.chat.id])
        result = cursor.fetchone()[0]
        conn.close()
        await select_notifications(call, result, call.message.message_id)

    # если нажата кнопка "закончить выбор"
    elif call.data == "exit":
        await bot.delete_message(call.message.chat.id, call.message.message_id)
        await bot.send_message(call.message.chat.id, "Мы закончили! Теперь мне ясен твой профиль занятий и я буду высылать "
                                                     "тебе регулярные напоминания о разных ежедневных мелочах. Просто "
                                                     "следуй им и скоро заметишь позитивный результат💪\n\nТы всегда можешь "
                                                     "изменить мои напоминания. Для этого необходимо пройти опросник заново "
                                                     "при помощи команды /start")
        await bot.send_message(call.message.chat.id, "Если я буду сильно навязчивым со своими напоминаниями, отключи звук на мои уведомления. "
                                                     "Или пройди опросник заново и отключи ненужные напоминания.")


# ======== Дальше код для админки ========
@dp.message_handler(commands=['admin'])
async def message_handler(message: types.Message):
    if message.chat.id == const.admin:
        await message.answer("/text\n/sticker\n/photo\n/video\n/poll")


@dp.message_handler(commands=['text'])
async def message_handler(message: types.Message, state: FSMContext):
    if message.chat.id == const.admin:
        await admin_choose_role(message, "текст", state)


@dp.message_handler(commands=['sticker'])
async def message_handler(message: types.Message, state: FSMContext):
    if message.chat.id == const.admin:
        await admin_choose_role(message, "стикер", state)


@dp.message_handler(commands=['photo'])
async def message_handler(message: types.Message, state: FSMContext):
    if message.chat.id == const.admin:
        await admin_choose_role(message, "фото", state)


@dp.message_handler(commands=['video'])
async def message_handler(message: types.Message, state: FSMContext):
    if message.chat.id == const.admin:
        await admin_choose_role(message, "видео", state)


@dp.message_handler(commands=['poll'])
async def message_handler(message: types.Message, state: FSMContext):
    if message.chat.id == const.admin:
        await admin_choose_role(message, "опрос", state)


# выбор роли
async def admin_choose_role(message, elem, state):
    await Form.func_elem_role.set()                                                                                         ########## МОЖЕТ НЕ РАБОТАТЬ ЗАПИСЬ В ФОРМУ ТК ОНА НЕ ПРИНИМАЕТСЯ
    async with state.proxy() as data:
        data['elem_role'] = [elem, None]
    choices = "/mom_with_children\n/remote_admin\n/unemployed\n/self_employed\n/remote_top\n/remote_student\n/worker\n/ALL"
    await message.answer("Выбери группу, которой нужно отправить:\n\n" + choices)


@dp.message_handler(state=Form.func_elem_role)
async def admin_get_role(message: types.Message, state: FSMContext):
    role = str(message.text)[1:]
    async with state.proxy() as data:
        elem = data['func_elem_role'][0]
        data['func_elem_role'][1] = role
    if role not in {"mom_with_children", "remote_admin", "unemployed", "self_employed", "remote_top", "remote_student", "worker", "ALL"}:
        await message.answer("Ошибка ввода!")
        await state.finish()
        return
    await Form.next()
    await message.answer(f"Отправь {elem} для рассылки")


def get_users(role):
    conn = mysql.connector.connect(host=const.host, user=const.db_user, passwd=const.password, database=const.db_name)
    cursor = conn.cursor(buffered=True)
    if role == "ALL":
        selectQuery = "SELECT user_id FROM users"
        cursor.execute(selectQuery)
    else:
        selectQuery = "SELECT user_id FROM users WHERE role=(%s)"
        cursor.execute(selectQuery, [role])
    users = cursor.fetchall()
    conn.close()
    return users


@dp.message_handler(state=Form.data)
async def admin_choose_func(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        func = data['func_elem_role'][0]
        role = data['func_elem_role'][1]
    await state.finish()

    if func == "текст":
        await admin_send_text(message, role)
    elif func == "стикер":
        await admin_send_sticker(message, role)
    elif func == "фото":
        await admin_send_photo(message, role)
    elif func == "видео":
        await admin_send_video(message, role)
    elif func == "опрос":
        await admin_send_poll(message, role)


async def admin_send_text(message, role):
    try: text = message.text
    except AttributeError: return
    users = get_users(role)
    i = 0
    for user in users:
        try:
            await bot.send_message(user[0], text)
            i += 1
        except utils.exceptions.BotBlocked: pass
    await message.answer("Количество пользователей, получивших сообщение: " + str(i))


async def admin_send_sticker(message, role):
    try: fileID = message.sticker.file_id
    except AttributeError: return
    users = get_users(role)
    i = 0
    for user in users:
        try:
            await bot.send_sticker(user[0], fileID)
            i += 1
        except utils.exceptions.BotBlocked: pass
    await message.answer("Количество пользователей, получивших сообщение: " + str(i))


async def admin_send_photo(message, role):
    try: fileID = message.photo[-1].file_id
    except AttributeError: return
    except TypeError: return
    users = get_users(role)
    i = 0
    for user in users:
        try:
            await bot.send_photo(user[0], fileID)
            i += 1
        except utils.exceptions.BotBlocked: pass
    await message.answer("Количество пользователей, получивших сообщение: " + str(i))


async def admin_send_video(message, role):
    try: fileID = message.video.file_id
    except AttributeError: return
    users = get_users(role)
    i = 0
    for user in users:
        try:
            await bot.send_video(user[0], fileID)
            i += 1
        except utils.exceptions.BotBlocked: pass
    await message.answer("Количество пользователей, получивших сообщение: " + str(i))


async def admin_send_poll(message, role):
    users = get_users(role)
    i = 0
    for user in users:
        try:
            await bot.forward_message(user[0], message.chat.id, message.message_id)
            i += 1
        except utils.exceptions.BotBlocked: pass
    await message.answer("Количество пользователей, получивших сообщение: " + str(i))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
