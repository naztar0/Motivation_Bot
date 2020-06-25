import mysql.connector
import constants as c
import schedule
import asyncio
import schedule_settings as ss
from aiogram import Bot, Dispatcher, utils

bot = Bot(c.token)
dp = Dispatcher(bot)


#  УТОЧНИТЬ
async def send_message(num):
    conn = mysql.connector.connect(host=c.host, user=c.db_user, passwd=c.password, database=c.db_name)
    cursor = conn.cursor(buffered=True)
    get_user_ids = "SELECT user_id FROM notifications WHERE {}=1"
    cursor.execute(get_user_ids.format('n' + str(num)))
    result = cursor.fetchall()
    conn.close()
    for user in result:
        try:
            await bot.send_message(user[0], c.notifications[num])
        except utils.exceptions.BotBlocked: pass
        except utils.exceptions.UserDeactivated: pass
        except utils.exceptions.ChatNotFound: pass


#  УТОЧНИТЬ
async def daily_message(num=None, minutes=None, stop=False):
    if not stop:
        schedule.every(minutes).minutes.do(send_message, num=num).tag(num)
        await send_message(num)
    else:
        await schedule.clear(num)


# Message_1
schedule.every().monday.at(ss.start_time_m_1).do(daily_message, 1, ss.period_m_1)
schedule.every().monday.at(ss.stop_time_m_1).do(daily_message, num=1, stop=True)
schedule.every().tuesday.at(ss.start_time_m_1).do(daily_message, 1, ss.period_m_1)
schedule.every().tuesday.at(ss.stop_time_m_1).do(daily_message, num=1, stop=True)
schedule.every().wednesday.at(ss.start_time_m_1).do(daily_message, 1, ss.period_m_1)
schedule.every().wednesday.at(ss.stop_time_m_1).do(daily_message, num=1, stop=True)
schedule.every().thursday.at(ss.start_time_m_1).do(daily_message, 1, ss.period_m_1)
schedule.every().thursday.at(ss.stop_time_m_1).do(daily_message, num=1, stop=True)
schedule.every().friday.at(ss.start_time_m_1).do(daily_message, 1, ss.period_m_1)
schedule.every().friday.at(ss.stop_time_m_1).do(daily_message, num=1, stop=True)

# Message_3
schedule.every().monday.at(ss.start_time_m_3).do(daily_message, 3, ss.period_m_3)
schedule.every().monday.at(ss.stop_time_m_3).do(daily_message, num=3, stop=True)
schedule.every().tuesday.at(ss.start_time_m_3).do(daily_message, 3, ss.period_m_3)
schedule.every().tuesday.at(ss.stop_time_m_3).do(daily_message, num=3, stop=True)
schedule.every().wednesday.at(ss.start_time_m_3).do(daily_message, 3, ss.period_m_3)
schedule.every().wednesday.at(ss.stop_time_m_3).do(daily_message, num=3, stop=True)
schedule.every().thursday.at(ss.start_time_m_3).do(daily_message, 3, ss.period_m_3)
schedule.every().thursday.at(ss.stop_time_m_3).do(daily_message, num=3, stop=True)
schedule.every().friday.at(ss.start_time_m_3).do(daily_message, 3, ss.period_m_3)
schedule.every().friday.at(ss.stop_time_m_3).do(daily_message, num=3, stop=True)

# Message_4
schedule.every().day.at(ss.start_time_m_4).do(daily_message, 4, ss.period_m_4)
schedule.every().day.at(ss.stop_time_m_4).do(daily_message, num=4, stop=True)

# Message_5
schedule.every().day.at(ss.at_time_m_5).do(send_message, 5)

# Message_6
schedule.every().monday.at(ss.at_time_m_6).do(send_message, 6)
schedule.every().tuesday.at(ss.at_time_m_6).do(send_message, 6)
schedule.every().wednesday.at(ss.at_time_m_6).do(send_message, 6)
schedule.every().thursday.at(ss.at_time_m_6).do(send_message, 6)
schedule.every().friday.at(ss.at_time_m_6).do(send_message, 6)

# Message_7
schedule.every().monday.at(ss.at_time_m_7).do(send_message, 7)
schedule.every().tuesday.at(ss.at_time_m_7).do(send_message, 7)
schedule.every().wednesday.at(ss.at_time_m_7).do(send_message, 7)
schedule.every().thursday.at(ss.at_time_m_7).do(send_message, 7)
schedule.every().friday.at(ss.at_time_m_7).do(send_message, 7)

# Message_8
schedule.every().monday.at(ss.at_time_m_8).do(send_message, 8)
schedule.every().tuesday.at(ss.at_time_m_8).do(send_message, 8)
schedule.every().wednesday.at(ss.at_time_m_8).do(send_message, 8)
schedule.every().thursday.at(ss.at_time_m_8).do(send_message, 8)
schedule.every().friday.at(ss.at_time_m_8).do(send_message, 8)

# Message_9
schedule.every().monday.at(ss.at_time_m_9).do(send_message, 9)
schedule.every().tuesday.at(ss.at_time_m_9).do(send_message, 9)
schedule.every().wednesday.at(ss.at_time_m_9).do(send_message, 9)
schedule.every().thursday.at(ss.at_time_m_9).do(send_message, 9)
schedule.every().friday.at(ss.at_time_m_9).do(send_message, 9)

# Message_10
schedule.every().monday.at(ss.start_time_m_10).do(daily_message, 10, ss.period_m_10)
schedule.every().monday.at(ss.stop_time_m_10).do(daily_message, num=10, stop=True)
schedule.every().tuesday.at(ss.start_time_m_10).do(daily_message, 10, ss.period_m_10)
schedule.every().tuesday.at(ss.stop_time_m_10).do(daily_message, num=10, stop=True)
schedule.every().wednesday.at(ss.start_time_m_10).do(daily_message, 10, ss.period_m_10)
schedule.every().wednesday.at(ss.stop_time_m_10).do(daily_message, num=10, stop=True)
schedule.every().thursday.at(ss.start_time_m_10).do(daily_message, 10, ss.period_m_10)
schedule.every().thursday.at(ss.stop_time_m_10).do(daily_message, num=10, stop=True)
schedule.every().friday.at(ss.start_time_m_10).do(daily_message, 10, ss.period_m_10)
schedule.every().friday.at(ss.stop_time_m_10).do(daily_message, num=10, stop=True)

# Message_11
schedule.every().monday.at(ss.at_time_m_11_1).do(send_message, 11)
schedule.every().monday.at(ss.at_time_m_11_2).do(send_message, 11)
schedule.every().tuesday.at(ss.at_time_m_11_1).do(send_message, 11)
schedule.every().tuesday.at(ss.at_time_m_11_2).do(send_message, 11)
schedule.every().wednesday.at(ss.at_time_m_11_1).do(send_message, 11)
schedule.every().wednesday.at(ss.at_time_m_11_2).do(send_message, 11)
schedule.every().thursday.at(ss.at_time_m_11_1).do(send_message, 11)
schedule.every().thursday.at(ss.at_time_m_11_2).do(send_message, 11)
schedule.every().friday.at(ss.at_time_m_11_1).do(send_message, 11)
schedule.every().friday.at(ss.at_time_m_11_2).do(send_message, 11)

# Message_12
schedule.every().day.at(ss.at_time_m_12_1).do(send_message, 12)
schedule.every().day.at(ss.at_time_m_12_2).do(send_message, 12)
schedule.every().day.at(ss.at_time_m_12_3).do(send_message, 12)
schedule.every().day.at(ss.at_time_m_12_4).do(send_message, 12)
schedule.every().day.at(ss.at_time_m_12_5).do(send_message, 12)

# Message_13
schedule.every().monday.at(ss.at_time_m_13).do(send_message, 13)

# Message_14
schedule.every().tuesday.at(ss.at_time_m_14).do(send_message, 14)

# Message_15
schedule.every().wednesday.at(ss.at_time_m_15).do(send_message, 15)

# Message_16
schedule.every().thursday.at(ss.at_time_m_16).do(send_message, 16)

# Message_17
schedule.every().friday.at(ss.at_time_m_17).do(send_message, 17)

# Message_18
schedule.every().saturday.at(ss.at_time_m_18).do(send_message, 18)


# Это бесконечный цикл в котором функция schedule каждую секунду проверяет текущее время и если оно совпадает с нужным то выполняет нужные действия
async def loop_schedule():
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)
