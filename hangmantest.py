import random
import string
import numpy as np

'''
  Initialization
    @charsOfSelectedWord = characters of the selected mystery word
      used numpy array for easy grab of index of occurence
      refer to line 19 and 33
    @life = tries until game over
    -----(Optional)
    @selectedChars = container for already picked letters
    @remainingChars = container for letter still not picked

'''
listofWords = ["dogss","catsss","miceseses"]
mysteryWord = random.choice(listofWords)
life = 3

charsOfSelectedWord = np.array(list(mysteryWord))
selectedChars = []

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
  
  if ins in selectedChars:
    return "Letter already picked. Pick another letter"
  
  # puts input letter to selectedChars Container
  # removes input letter from remainingChars Container
  selectedChars.append(ins)
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
  else:
    life -= 1
    return "Letter not in word"



while life > 0:
  print("Life: "+str(life)+"\nGuess the Word:\n"+mysteryWord+"\n")
  userIn = input("Remaining Letter: "+remainingChars+" \n>>>")
  if userIn.isalpha():
    outp = checker(userIn.lower())
    if outp != None:
      print(outp)
  else:
    print("Letter Only plsz")

print("YOU LOSE\nThe word is "+("".join(charsOfSelectedWord)).upper())

