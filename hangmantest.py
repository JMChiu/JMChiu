import random
import string
# numpy for easy index search
import numpy as np
# request for api get lazy random word search
import requests
# os for console clear command
import os

'''
  Initialization
    @charsOfSelectedWord = characters of the selected mystery word
      used numpy array for easy grab of index of occurence
      refer to line 39 and 93
    @life = tries until game over
    -----(Optional)
    @selectedChars = container for already picked letters
    @remainingChars = container for letter still not picked
'''

# too lazy to think of a word, just gets a random word from an api
api = "https://random-word-api.herokuapp.com/word"
getResponse = requests.get(api)
apiRandomWord = getResponse.json()[0].lower()
#Feature - free api get word definition
defApi = "https://api.dictionaryapi.dev/api/v2/entries/en/"+apiRandomWord
defin = requests.get(defApi).json()

listofUserSpecifiedWords = ["paste","your","random","words","here"]

#### apiRandomWord for random from api or 
#### listofUserSpecifiedWords for User Specified Words and pick a random

# mysteryWord = random.choice(listofUserSpecifiedWords)
mysteryWord = apiRandomWord

life = 3

charsOfSelectedWord = np.array(list(mysteryWord))

# (Optional) loops to add whitespace between chars
remainingChars = ""
for chars in string.ascii_lowercase:
  remainingChars = remainingChars + chars + " "

# used same var to replace chars with '_ '
# '_ ' multiply by length of mystery word
# ('_ ' • 4) = _ _ _ _
mysteryWord = '_ '*len(mysteryWord)

'''
  (Optional) Checker func
    used function for abstraction but can be done without function

    @ins = selected letter
    global vars = outside vars need to be declared as global for the func to gain access to them
'''
def checker(ins):
  global mysteryWord,selectedChars,remainingChars,life
  
  #if its not in remainingChars then its already picked
  if ins not in remainingChars:
    return "Letter \'"+ins.upper()+"\' already picked. Pick another letter"
  
  # removes input letter from remainingChars Container
  remainingChars = remainingChars.replace(ins,'')

  '''
    if input is in charsOfSelectedWord it will get its index/indices 
    which uses numpy.where which easily gets the indices of the same letter in the list 

    @newList is used for converting mysteryWord into list and changing the _ into proper letter
      and using "".join(newList) to join it into a string again (e.g. M _ C E _ )

    i used index * 2 because mysteryWord has whitespaces between them
    if input letter is in index 3 then in mysteryWord it is index 6
    making them indexFromWord*2 = indexInMysteryWord
    refer to diag below

          M I C E S
    index 0 1 2 3 4
          _ _ _ _ _
    index 012345678

    else: if input letter is in charsOfSelectedWord then it will
      subtract life by 1 
    (life -= 1) is the same as (life = life - 1)
      googled it, its called Compound Assignment or Augmented Assignment
  '''
  if ins in charsOfSelectedWord:
    indices = np.where(charsOfSelectedWord == ins)[0]
    newList = list(mysteryWord)
    for index in indices:
      newList[index*2] = ins.upper()
    mysteryWord = "".join(newList)
    return ""
  else:
    life -= 1
    return "Letter \'"+ins.upper()+"\' not in word"

'''
  Just a function that shows word definition if it is available on the api
  created a funtion to prevent code redundancy since its called on more than one instance
'''
def defPrint():
  global defin
  try:
    if defin[0] != None:
      for arr in list(defin)[0]['meanings']:
        print(arr['partOfSpeech']+" - "+arr['definitions'][0]['definition'])
  except:
    print("No Definitions Found")

'''
  @userIn = the user input
  (userIn.isalpha) is used to check if it is a user input is an alphabet albeit uppercase or lower
  but i set it to lowercase so its uniform to prevent case error
  (len(userIn) > 1) checks if its more than 1 character then prints error

  @outp = its for Message
'''
outp = ""
while life > 0:
  os.system('cls')
  defPrint()
  print(outp+"\n")
  print("Life: "+str(life)+"\nGuess the Word:\n"+mysteryWord+"\n")
  userIn = input("Remaining Letter: "+remainingChars+" \n>>>")
  if userIn.isalpha() and len(userIn) == 1:
    outp = checker(userIn.lower())
    if '_' not in mysteryWord:
      break
  else:
    outp = "wrong input"

print("=================")
if life > 0:
  print("Congratulations\nYou Guessed the Word\n"+mysteryWord.replace(" ",""))
else:
  print("YOU LOSE\nThe word is "+("".join(charsOfSelectedWord)).upper())

defPrint()