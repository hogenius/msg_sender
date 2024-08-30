import asyncio
from config import ConfigInfo
from msg_telegram import Messaging
is_test = False

if __name__ == '__main__':
    
    Messaging.Instance().SetTest(is_test)
    #Messaging.Instance().Send("msg start")
    
    loop = asyncio.get_event_loop()
    loop.create_task(Messaging.Instance().RoutinePolling())
    loop.create_task(Messaging.Instance().RoutineMsg())
    
    Messaging.Instance().InitHandler()
    loop.run_forever()

    

    