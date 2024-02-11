from fastapi import FastAPI, Form, Request
from starlette.templating import Jinja2Templates

from telegram_bot import TelegramBot
from facebook_auth import FacebookAuth

my_app_id = '323958937015510'
my_app_secret = '4017320d9d5dcc49869874e73904b872'
fs = FacebookAuth(my_app_id, my_app_secret, "http://localhost:5000/login/callback", "email")
bot = TelegramBot()
app = FastAPI()
templates = Jinja2Templates(directory="templates")
fs.run()
