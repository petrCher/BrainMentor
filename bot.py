import telebot, json, time
from random import *
from database import *

numbers=3
attempts=10
min=0
max=10
db = open("sqlite:///data.sqlite3")
API_TOKEN="7595557499:AAHW-sRZlWNfiVeIBagthfyQP-7bE2U5IqU"
bot = telebot.TeleBot(token=API_TOKEN)

def getnumbers(n):
   lst=[]
   r=randint(0, n-1)
   for i in range(n):
           lst.append(str(randint(min, max)))
   s1=' '.join(map(str, lst))
   d=str(lst[r])
   del lst[r]
   s2=' '.join(map(str, lst))
   return [s1, s2, d]

def play(user, nums, atts, count):
   lst=getnumbers(nums)
   set(db, user.user_id, 1, json.dumps([0, lst[0], lst[1], lst[2], nums, atts, count]), user.maximum)
   msg=bot.send_message(user.user_id, lst[0], protect_content=True)
   time.sleep(len(lst[0]))
   bot.edit_message_text(chat_id=user.user_id, message_id=msg.id, text=lst[1])
   bot.send_message(user.user_id, "Введите \"пропавшее\" число", protect_content=True)

def answer(user, text):
   lst=json.loads(user.game_data)
   if text==lst[3]:
      bot.send_message(user.user_id, "Правильно!", protect_content=True)
      play(user, lst[4]+1, lst[5], lst[6]+lst[4]*lst[5])
   else:
      if lst[5]>1:
         bot.send_message(user.user_id, f"Неправильно!\nОсталось попыток: {lst[5]-1}", protect_content=True)
         set(db, user.user_id, 1, json.dumps([lst[0], lst[1], lst[2], lst[3], lst[4], lst[5]-1, lst[6]]), user.maximum)
      else:
         bot.send_message(user.user_id, f"Неправильно!\nПопыток не осталось.\nТренировка завершена.\nВаш результат - {lst[6]}.", protect_content=True)
         if lst[6]>user.maximum:
            user.maximum=lst[6]
         set(db, user.user_id, 0, "", user.maximum)

@bot.message_handler(commands=["start"])  
def command_start(message, res=False):
   bot.send_message(message.from_user.id,"Вас приветствует бот для тренировки памяти BrainMentor, для получения справки - /help")
   try:
      user=get(db, message.from_user.id)
      maximum=user.maximum
   except:
      maximum=0
   remove(db, message.from_user.id)
   add(db, message.from_user.id, 0, "", maximum)

@bot.message_handler(commands=["help"])  
def command_help(message, res=False):
   bot.send_message(message.from_user.id,"Бот для тренировки памяти BrainMentor\n/help - справка\n/go - начать тренировку\n/stop - завершить тренировку\n/restart - начать тренировку заново\n/stat - статистика тренировок")

@bot.message_handler(commands=["go"])  
def command_go(message, res=False):
   try:
      user=get(db, message.from_user.id)
      if user.game_status:
         bot.send_message(message.from_user.id,"Тренировка уже идет")
      else:   
         bot.send_message(message.from_user.id,"Тренировка началась")
         play(user, numbers, attempts, 0)
   except:
      pass

@bot.message_handler(commands=["restart"])  
def command_go(message, res=False):
   try:
      user=get(db, message.from_user.id)
      if user.game_status:
         bot.send_message(message.from_user.id,"Тренировка началась заново")
         play(user, numbers, attempts, 0)
      else:   
         bot.send_message(message.from_user.id,"Для начала тренировки введите /go")
   except:
      pass

@bot.message_handler(commands=["stop"])  
def command_stop(message, res=False):
   try:
      user=get(db, message.from_user.id)
      if user.game_status:
         bot.send_message(message.from_user.id,"Тренировка завершена")
         lst=json.loads(user.game_data)
         if lst[6]>user.maximum:
            user.maximum=lst[6]
         set(db, message.from_user.id, 0, "", user.maximum)
      else:
         bot.send_message(message.from_user.id,"Тренировка уже завершена")
   except:
      pass

@bot.message_handler(commands=["stat"])  
def command_stop(message, res=False):
   try:
      user=get(db, message.from_user.id)
      if user.game_status:
         bot.send_message(message.from_user.id,f"Лучший результат - {getbest(db)}\nЛучший Ваш результат - {user.maximum}\nТекущий результат - {json.loads(user.game_data)[6]}")
      else:
         bot.send_message(message.from_user.id,f"Лучший результат - {getbest(db)}\nЛучший Ваш результат - {user.maximum}")
   except:
      pass

@bot.message_handler(content_types=["text"]) 
def command_text(message):
   try:
      user=get(db, message.from_user.id)
      if user.game_status:
         answer(user, message.text)
      else:
         bot.send_message(message.from_user.id,"Для начала тренировки введите /go")
   except:
      pass

def main():
   bot.polling(none_stop=True, interval=0)

if __name__ == '__main__':
   main()