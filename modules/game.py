from sopel import module
from sopel.tools import SopelMemory
import sys
import random
import json, jsonpickle

class Question(object):
   def __init__(self, question, answers=None):
      self.question = question #single string
      if answers:
         self.answers = answers #list of strings
      else:
         self.answers=[]
      #dict.__init__(self,question=question, answers = answers)

   #def default(o):
   #   return o.__dict__

   def addanswer(self,ans):
      self.answers.append(ans)

   def safe(self,file):
     outp=jsonpickle.encode([self.question,self.answers])
     file.write(outp)

   def ask(self,bot):
      bot.say(self.question)

   def answer(self,bot):
      for answer in self.answers:
         bot.say(answer)

def setup(bot):
   if not bot.memory.contains('ada_game'):
      bot.memory['ada_game'] = SopelMemory()
   bot.memory['ada_game'] = dict()
   if not bot.memory.contains('ada_game_add'):
      bot.memory['ada_game_add'] = SopelMemory()
   bot.memory['ada_game_add'] = dict()
   iniQuestions(bot)

def iniQuestions(bot):
   adal(bot)
   random.shuffle(bot.memory['ada_game'][1])    # randomizes the order of the questions
   

def getQuestion(bot):
   questions = bot.memory['ada_game'][1]
   if questions:
      question = questions.pop()
      return question
   else:
      iniQuestions(bot)
      return Question("Ende.",["Shuffle...Restart"])


@module.commands('ada')
def ada(bot, trigger):
   """Kleines Q&A Spiel für die AdA Meisterprüfung"""
   nick = trigger.nick
   if nick in bot.memory['ada_game'].keys():
      question = bot.memory['ada_game'].pop(nick,None)
      question.answer(bot)
   else:
       question = getQuestion(bot)
       bot.memory['ada_game'][nick] = question
       question.ask(bot)

@module.commands('adasafe')
def adasafe(bot, trigger):
   """Speichern der Fragen und Antworten"""
   tosafe = bot.memory['ada_game'][1]
   with open('adaquestions.txt','w') as f:
      for question in tosafe:
         question.safe(f)
         f.write('\n')
         #f.write(jsonpickle.encode([question.q(),question.a()]))
         #json.dump(question,f)
   bot.reply("Fragenkatalog gespeichert...")

@module.commands('adaload')
def adaload(bot, trigger):
   """Laden der Fragen und Antworten"""
   adal(bot)
   bot.say("Fragenkatalog geladen")

def adal(bot):
   inpu=[]
   with open('adaquestions.txt','r') as f:
      for line in f.readlines():
        #bot.reply(line)
         li= jsonpickle.decode(line)
         inpu.append(Question(li[0],li[1]))
   bot.memory['ada_game'][1]=inpu

@module.commands('ad')
def ad(bot,trigger):
   """Eine Frage zum Pool hinzufügen (.adaadd 1,Frage .adaadd 2,Antwort1 .adaadd 2,Antwort2... .adadd 3,ende"""
   if not trigger.group(2):
      bot.reply("Was soll ich denn aufnehmen?")
   state = trigger.group(2)[0]
   inpu = trigger.group(2)[2:]
   nick = trigger.nick
   #bot.reply(state)
   #bot.reply(inpu)
   if nick in bot.memory['ada_game_add'].keys():
      question = bot.memory['ada_game_add'].pop(nick,None)
      if state == "3":
         adal(bot)
         bot.memory['ada_game'][1].append(question)
         bot.reply("Frage/Antworten in Fragenkatalog aufgenommen")
         adasafe(bot,trigger)
         return
      question.addanswer(inpu)
      bot.memory['ada_game_add'][nick] = question
      bot.reply("Antwort eingefügt")
   else:
       if state == "1":
          question = Question(inpu)
          bot.memory['ada_game_add'][nick] = question
          bot.reply("Frage aufgenommen")
        
