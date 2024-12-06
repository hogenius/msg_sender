import telegram
from telegram.ext import (
    Application,
    CommandHandler
)
import asyncio
import datetime
from queue import Queue
from config import ConfigInfo
from simple_data.Logging import SimpleLogger
from singletone import SingletonInstane
from simple_data.simpledata import SimpleData
from simple_data.simpledata import TableType


class Messaging(SingletonInstane):

    def __init__(self):
        self.queue_msg = Queue()
        self.simple_data = SimpleData(ConfigInfo.Instance().db_path)
        self.bot = telegram.Bot(ConfigInfo.Instance().telegram_token)
        self.logging = SimpleLogger(name="msg_sender", log_file="msg.log")

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
                    self.logging.log(f"RoutineMsg error : {e}")
                    self.bot = telegram.Bot(ConfigInfo.Instance().telegram_token)

            await asyncio.sleep(ConfigInfo.Instance().polling_sec)

        
    def InitHandler(self):
        print(f"InitHandler!!!")
        self.logging.log("InitHandler!!!")
        self.app = Application.builder().token(ConfigInfo.Instance().telegram_token).build()
        self.app.add_handler(CommandHandler("refresh", self.handler_refresh))
        self.app.add_handler(CommandHandler("check", self.handler_check))
        self.app.add_handler(CommandHandler("reloadconfig", self.handler_reload_config))
        self.app.add_handler(CommandHandler("safemode", self.handler_safe_mode))
        self.app.add_handler(CommandHandler("normalmode", self.handler_normal_mode))
        self.app.add_handler(CommandHandler("attackmode", self.handler_attack_mode))
        self.app.add_handler(CommandHandler("pause", self.handler_pause))
        self.app.add_handler(CommandHandler("resume", self.handler_resume))
        self.app.add_handler(CommandHandler("showstatus", self.handler_show_status))
        self.app.add_handler(CommandHandler("cmd", self.handler_command))

        self.app.run_polling()

    async def handler_common(self, cmd, context):
        await asyncio.sleep(0)
        handle_msg = cmd
        if 0 < len(context.args):
            command_args = "/".join(context.args)
            handle_msg = f"{handle_msg}/{command_args}"
            
        self.Send(f"receive {handle_msg}")
        self.simple_data.add_string(TableType.Check, handle_msg)

    async def handler_command(self, update, context):
        await self.handler_common("cmd", context)

    async def handler_refresh(self, update, context):
        await self.handler_common("RefreshCoinList", context)

    async def handler_check(self, update, context):
        await self.handler_common("CheckCoinList", context)

    async def handler_reload_config(self, update, context):
        await self.handler_common("ReloadConfing", context)

    async def handler_safe_mode(self, update, context):
        await self.handler_common("SetSafeMode", context)

    async def handler_normal_mode(self, update, context):
        await self.handler_common("SetNormalMode", context)

    async def handler_attack_mode(self, update, context):
        await self.handler_common("SetAttackMode", context)

    async def handler_pause(self, update, context):
        await self.handler_common("SetPause", context)

    async def handler_resume(self, update, context):
        await self.handler_common("SetResume", context)

    async def handler_show_status(self, update, context):
        await self.handler_common("ShowStatus", context)

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

    