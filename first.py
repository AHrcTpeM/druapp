import os
from dotenv import load_dotenv

# Загрузите переменные окружения из файла .env
load_dotenv()
# db connection URL (In order to submit your project do NOT change this value!!!)
DB_URL = os.environ['DB_URL']

print('Hello world!')
print(DB_URL)
