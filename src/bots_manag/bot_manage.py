import importlib

from src.orm.models.chatbot import ChatBot

class BotManager:
    def __init__(self, bot: ChatBot) -> None:
        self.botdef = bot
        self.botmodule = None
        self.botclass = None

    def load(self):
        # build module location
        module_path = f"botfirm.{self.botdef.module_filename}"

        # load bots dynamically
        try:
            # if already exists, reload definition
            if self.botmodule is not None:
                importlib.reload(module_path)

            self.botmodule = importlib.import_module(module_path)
            self.botclass = getattr(self.botmodule, self.botdef.classname)
        except ImportError as imex:
            print(f"failed to load from {module_path} class {self.botdef.classname}")

    async def send(self, message, history):
        bot = self.botclass()
        return await bot.bot_response(message, history)
