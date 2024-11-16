import telegram
from telegram.ext import (
    Application,
    CommandHandler
)
import asyncio
import datetime
from queue import Queue
from config import ConfigInfo
from singletone import SingletonInstane
from simple_data.simpledata import SimpleData
from simple_data.simpledata import TableType


class Messaging(SingletonInstane):

    def __init__(self):
        self.queue_msg = Queue()
        self.simple_data = SimpleData(ConfigInfo.Instance().db_path)
        self.bot = telegram.Bot(ConfigInfo.Instance().telegram_token)

    def SetTest(self, isTest):
        self.is_test = isTest

    def Send(self, msg):
        now = datetime.datetime.now()
        if self.is_test:
            message = f"TestMode\n[{now.strftime('%Y-%m-%d %H:%M:%S')}]\n{str(msg)}"
        else:
            message = f"[{now.strftime('%Y-%m-%d %H:%M:%S')}]\n{str(msg)}"
        #print(message)
        self.queue_msg.put(message)

    async def RoutinePolling(self):
        while True:
            list_msg = self.simple_data.load_strings(TableType.Msg)
            #print(f"InitPollingRoutine list_msg: {list_msg}")
            for msg in list_msg:
                #print(f"InitPollingRoutine : {msg}")
                self.queue_msg.put(msg)

            #print("InitPollingRoutine")
            await asyncio.sleep(ConfigInfo.Instance().polling_sec)

    async def RoutineMsg(self):
        while True:
            if 0 < self.queue_msg.qsize():
                msg = self.queue_msg.get()
                try:
                    await self.bot.send_message(chat_id=ConfigInfo.Instance().telegram_chat_id, text=msg)
                except Exception as e:
                    print(f"RoutineMsg error : {e}")
                    self.bot = telegram.Bot(ConfigInfo.Instance().telegram_token)

            await asyncio.sleep(ConfigInfo.Instance().polling_sec)

        
    def InitHandler(self):
        print(f"InitHandler!!!")
        self.app = Application.builder().token(ConfigInfo.Instance().telegram_token).build()
        self.app.add_handler(CommandHandler("help", self.handler_help))
        self.app.add_handler(CommandHandler("refresh", self.handler_refresh))
        self.app.add_handler(CommandHandler("check", self.handler_check))
        self.app.add_handler(CommandHandler("reload_config", self.handler_reload_config))
        self.app.add_handler(CommandHandler("safemode", self.handler_safe_mode))
        self.app.add_handler(CommandHandler("normalmode", self.handler_normal_mode))
        self.app.add_handler(CommandHandler("attackmode", self.handler_attack_mode))
        self.app.add_handler(CommandHandler("pause", self.handler_pause))
        self.app.add_handler(CommandHandler("resume", self.handler_resume))
        self.app.add_handler(CommandHandler("show_status", self.handler_show_status))
        
        self.app.run_polling()

    async def handler_help(self, update, context):
        await asyncio.sleep(0)
        print(f"handler_help!!!")
        self.Send("good day! what kind do you want?")
        self.simple_data.add_string(TableType.Check, "good day! what kind do you want?")

    async def handler_refresh(self, update, context):
        await asyncio.sleep(0)
        print(f"handler_refresh!!!")
        self.Send("refresh coin list start")
        self.simple_data.add_string(TableType.Check, "RefreshCoinList")

    async def handler_check(self, update, context):
        await asyncio.sleep(0)
        print(f"handler_check!!!")
        self.Send("check coin list start")
        self.simple_data.add_string(TableType.Check, "CheckCoinList")

    async def handler_reload_config(self, update, context):
        await asyncio.sleep(0)
        print(f"handler_reload_config!!!")
        self.Send("reload config start")
        self.simple_data.add_string(TableType.Check, "ReloadConfing")

    async def handler_safe_mode(self, update, context):
        await asyncio.sleep(0)
        print(f"handler_safe_mode!!!")
        self.Send("safe mode start")
        self.simple_data.add_string(TableType.Check, "SetSafeMode")

    async def handler_normal_mode(self, update, context):
        await asyncio.sleep(0)
        print(f"handler_normal_mode!!!")
        self.Send("normal mode start")
        self.simple_data.add_string(TableType.Check, "SetNormalMode")

    async def handler_attack_mode(self, update, context):
        await asyncio.sleep(0)
        print(f"handler_attack_mode!!!")
        self.Send("attack mode start")
        self.simple_data.add_string(TableType.Check, "SetAttackMode")

    async def handler_pause(self, update, context):
        await asyncio.sleep(0)
        print(f"handler_pause!!!")
        self.Send("pause mode start")
        self.simple_data.add_string(TableType.Check, "SetPause")

    async def handler_resume(self, update, context):
        await asyncio.sleep(0)
        print(f"handler_resume!!!")
        self.Send("resume mode start")
        self.simple_data.add_string(TableType.Check, "SetResume")

    async def handler_show_status(self, update, context):
        await asyncio.sleep(0)
        print(f"handler_show_status!!!")
        self.Send("show status")
        self.simple_data.add_string(TableType.Check, "ShowStatus")

'''
async def help_handler(update, context):
    print(f"help_handler!!!")
    await asyncio.sleep(0);

if __name__ == '__main__':
    print(f"__main__!!!")
    app = Application.builder().token(ConfigInfo.Instance().telegram_token).build()
    app.add_handler(CommandHandler("help", help_handler))
    app.run_polling()
'''

    