from sopel import module
from sopel.tools import SopelMemory
import random,json

def setup(bot):
   if not bot.memory.contains('postillon'):
      bot.memory['postillon'] = SopelMemory()
   bot.memory['postillon'] = dict()
   iniPost(bot)

@module.commands('postload')
def postload(bot,trigger):
   postload(bot)

def postload(bot):
   with open('posts.txt','r') as f:
      bot.memory['postillon'][1] = json.load(f)

@module.commands('postsafe')
def postsafe(bot,trigger):
   with open('posts.txt','w') as f:
      tosafe = bot.memory['postillon'][1]
      json.dump(tosafe,f)
   bot.say("Merk ich mir")

@module.commands('postadd')
def postadd(bot,trigger):
   if not trigger.group(2):
       return bot.reply("Na welchen Spruch soll ich mir denn merken?")
   if not trigger.group(2) in bot.memory['postillon'][1]:
       postload(bot)
       bot.memory['postillon'][1].append(trigger.group(2))
       postsafe(bot,trigger)
   else:
       return bot.reply("Den kenn ich schon")

def iniPost(bot):
  # posts = ["Wegen fehlender Quallenangaben: Meeresforscher verliert seinen Doktortitel",
  # 	"Er hält den Rand: Südafrikanischer Zeuge nahm Schweigegeld",
  #	"Wissenschaftler finden heraus: Labyrinth war zu einfach",]
   postload(bot)
   posts = bot.memory['postillon'][1]
   random.shuffle(posts)
   bot.memory['postillon'][1]=posts


@module.commands('post')
def post(bot, trigger):
   """Vom Postillon für'n Spass"""
   phrases = bot.memory['postillon'][1]
   if not phrases:
      iniPost(bot)
      phrases = bot.memory['postillon'][1]
   phrase = "+++ " + phrases.pop() + " +++"
   bot.say(phrase)
