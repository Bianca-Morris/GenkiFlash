# -*- coding: utf-8 -*-
# sys.setdefaultencoding() does not exist, here!
import sys
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox
import random
import genkiWords
import datetime
import tkSimpleDialog
    
now = datetime.datetime.now()
    
class GenkiFLASH(Frame):
    """Starts the program"""
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        
        #scoring variables
        self.highscore = 0
        self.highscoredate = "n/a"
        
        self.secondbest = 0
        self.secondbestdate = "n/a"
        
        self.thirdbest = 0
        self.thirdbestdate = "n/a"
        
        #toggles between answer checking/guessing states
        self.gameState = 0
       
        self.initIntroUI()
    
    def initIntroUI(self):
        """Loads the Intro Screen UI"""
        self.parent.title("GenkiFLASH")
        self.pack(fill = BOTH, expand=1)
        
        self.startWindow = Frame(self, background="red")
        self.startWindow.pack()
        
        #Places Picture for Intro
        introPic = PhotoImage(file="Pics\introPic.gif")
        introPicLabel = Label(self.startWindow,image=introPic, borderwidth=0)
        introPicLabel.introPic = introPic
        introPicLabel.grid()
        
        #Creates button
        button = Button(self.startWindow, text="Start a practice session", command=self.initNewGameOptionsUI)
        button.grid()
    
    def initNewGameOptionsUI(self):
        """Loads the New Game Options UI"""
        #Gets rid of old window(s)
        try:
            self.gameWindow.destroy()
        except:
            pass
        try:
            self.scoresWindow.destroy()
        except:
            pass
        try:
            self.startWindow.destroy()
        except:
            pass
        
        #Creates a new window with new game options.
        self.optionsWindow = Frame(self, width=400, height=350)
        self.optionsWindow.pack()
        self.optionsWindow.pack_propagate(0)
        
        #Places Picture for Intro
        introPic = PhotoImage(file="Pics\deckOptions.gif")
        introPicLabel = Label(self.optionsWindow,image=introPic, borderwidth=0)
        introPicLabel.introPic = introPic
        introPicLabel.pack()
        
        #Creates frame for Options
        self.optionsFrame = Frame(self.optionsWindow)
        self.optionsFrame.pack()
        
        #'Choose a Vocab List' Pulldown Menu
        Text1 = "Vocabulary list"
        TextLabel = Label(self.optionsFrame, text=Text1)
        TextLabel.grid(row=1, column=1)
        
        self.VL = StringVar(self.optionsFrame)
        self.VL.set("...")
        
        vocabList = OptionMenu(self.optionsFrame, self.VL, "Verbs - ALL", "Verbs - RU","Verbs - U","Verbs - IRREGULAR","Adj - ALL", "Adj - II", "Adj - NA")
        vocabList.config(width = 20)
        vocabList.grid(row=2, column=1)
        
        #'Practice' Pulldown Menu
        Text2 = "Game mode"
        TextLabel2 = Label(self.optionsFrame, text=Text2)
        TextLabel2.grid(row=3, column=1)
        
        self.VL2 = StringVar(self.optionsFrame)
        self.VL2.set("...")
        
        vocabList2 = OptionMenu(self.optionsFrame, self.VL2, "Translation", "Conjugation")
        vocabList2.config(width = 20)
        vocabList2.grid(row=4, column=1)
    
        #'Card Order' Pulldown Menu
        Text3 = "Card Order"
        TextLabel3 = Label(self.optionsFrame, text=Text3)
        TextLabel3.grid(row=1, column=2)
        
        self.VL3 = StringVar(self.optionsFrame)
        self.VL3.set("...")
        
        cardOrder = OptionMenu(self.optionsFrame, self.VL3, "Kanji -> ENG", "Romaji -> ENG", "ENG -> Kanji","ENG -> Romaji")
        cardOrder.config(width = 20)
        cardOrder.grid(row=2, column=2)
        
        self.VL.trace("w", self.conjugationSettings)
        self.VL2.trace("w", self.conjugationSettings)
        
        #GO! Button
        Go = Button(self.optionsWindow, text="GO!", command=self.onGo, bg="red", fg="white")
        Go.pack()
        
        #Status bar at the bottom
        tipoftheday = genkiWords.tips[random.randint(0,len(genkiWords.tips)-1)]
        self.statusLabel = Label(self.optionsWindow, text=tipoftheday, fg="red",font=("Tahoma", 8))
        self.statusLabel.pack()
        
    def onGo(self):
        """Starts the New Game with Player-Selected Settings"""
        self.statusLabel.config(text="Loading your chosen deck...")

        #Sets up Card deck
        self.setUpDeck(self.VL.get())
        if self.VL2.get() == "Translation":
            self.translationGameInit(self.VL3.get())
        elif self.VL2.get() == "Conjugation":
            self.conjugationGameInit(self.VL3.get(), self.VL4.get())
        else: 
            self.statusLabel.config(text="Error loading chosen deck; reselect settings")    

    def setUpDeck(self, Var1):
        """Creates a deck of possible cards from the appropriate wordList"""
        self.deck = []
        if Var1 == "Verbs - ALL":
            for word in genkiWords.verbs:
                self.deck.append(word)
            return self.deck
        elif Var1 == "Verbs - RU":
            for index in range(0, len(genkiWords.verbs)-1):
                if genkiWords.verbs[index]['type'] == "ru":
                    self.deck.append(genkiWords.verbs[index])
            return self.deck
        elif Var1 == "Verbs - U":
            for index in range(0, len(genkiWords.verbs)-1):
                if genkiWords.verbs[index]['type'] == "u":
                    self.deck.append(genkiWords.verbs[index])
            return self.deck
        elif Var1 == "Verbs - IRREGULAR":
            for index in range(0, len(genkiWords.verbs)-1):
                if (genkiWords.verbs[index]['type'] == 
                    "kaeru") or (genkiWords.verbs[index]['type'] ==
                    "suru") or (genkiWords.verbs[index]['type'] ==
                    "kuru"):
                    self.deck.append(genkiWords.verbs[index])
            return self.deck
        elif Var1 == "Adj - ALL":
            for word in genkiWords.adj:
                self.deck.append(word)
            return self.deck 
        elif Var1 == "Adj - II":
            for index in range(0, len(genkiWords.adj)-1):
                if (genkiWords.adj[index]['type'] 
                == "ii") or (genkiWords.adj[index]['type'] 
                == "ii-ir"):
                    self.deck.append(genkiWords.adj[index])
            return self.deck 
        elif Var1 == "Adj - NA":
            for index in range(0, len(genkiWords.adj)-1):
                if genkiWords.adj[index]['type'] == "na":
                    self.deck.append(genkiWords.adj[index])
            return self.deck

#Conjugatuion Game
    def conjugationSettings(self, name, index, mode):
        """Interprets"""
        Text4 = "Practice..." 
        self.VL4 = StringVar(self.optionsFrame)
        self.VL4.set("...")
        
        if self.VL2.get() == "Conjugation":
            if (self.VL.get() == "Verbs - ALL") or (self.VL.get() == 
        "Verbs - RU") or (self.VL.get() == "Verbs - U") or (self.VL.get() ==
        "Verbs - IRREGULAR"):
                self.TextLabel4 = Label(self.optionsFrame, text=Text4)
                self.TextLabel4.grid(row=3, column=2)
    
                self.practice = OptionMenu(self.optionsFrame, self.VL4, "Dictionary form", "Long form", "Te-form", "Short past form")
                self.practice.config(width = 20)
                self.practice.grid(row=4, column=2)
            elif (self.VL.get() == "Adj - ALL") or (self.VL.get() == "Adj - II") or (self.VL.get() == "Adj - NA"):
                TextLabel4 = Label(self.optionsFrame, text=Text4)
                TextLabel4.grid(row=3, column=2)
    
                self.practice = OptionMenu(self.optionsFrame, self.VL4, "Present", "Past")
                self.practice.config(width = 20)
                self.practice.grid(row=4, column=2)
        elif self.VL2.get() == "Translation":
            try: 
                self.practice.grid_remove()
                self.TextLabel4.grid_remove()
            except AttributeError:
                pass
                #Currently, there is an error being passed here... not sure what's up with it
        
    def conjugationGameInit(self, cardOrder, conjType):
        self.statusLabel.config(text="Conjugation mode is still in development! Please select 'Translation' mode!")

#Translation Game  
    def translationGameInit(self, cardOrder):      
        self.playerScore = 0
       
        #Creates Card order variables:
        if cardOrder == "Kanji -> ENG":
            self.transTo = "kanji"
            self.transFrom = "english"
        elif cardOrder == "Romaji -> ENG":
            self.transTo = "romaji"
            self.transFrom = "english"
        elif cardOrder == "ENG -> Kanji":
            self.transTo = "english"
            self.transFrom = "kanji"
        elif cardOrder == "ENG -> Romaji":
            self.transTo = "english"
            self.transFrom = "romaji"
        else: 
            self.statusLabel.config(text="ERROR: Please select cardOrder")
            
        self.optionsWindow.destroy()
        self.dealCard()

    def dealCard(self):     
        #Prepares the first Card
        self.card = self.newCard()
        self.front = self.card[0]
        self.back = self.card[1]
        
        self.updateGUIforNewCard()
        
    
    def updateGUIforNewCard(self):
        #Creates GUI
        self.gameWindow = Frame(self)
        self.gameWindow.pack()
        
        #Card Window
        self.cardWindow = Frame(self.gameWindow)
        self.cardWindow.pack()
        
        self.frontCard = Canvas(self.cardWindow, width=400, height = 100)
        self.frontCard.config(background="firebrick2")
        self.frontCard.pack()
        
        self.frontLabel = self.frontCard.create_text(200, 50, text=self.front, font="NSimSun 22", width = 380)
        
        self.backCard = Canvas(self.cardWindow, width=400, height = 100)
        self.backCard.config(background="white")
        self.backCard.pack()
        
        self.backLabel = self.backCard.create_text(200, 50, text=" ", font="NSimSun 22", width = 380)
        
        self.instructions = Label(self.cardWindow, text=("Translate the term into " + str(self.transTo) + " in the space below"), width=380)
        self.instructions.pack()
        
        #Guess Window
        guessWindow = Frame(self.gameWindow)
        guessWindow.pack()
        
        self.guess = StringVar()
        
        playerGuess = Entry(guessWindow, textvariable=self.guess)
        playerGuess.grid(row=1, column=2)
        
        checkButton = Button(guessWindow, text="Check",command=self.checkEntry)
        checkButton.grid(row=2, column=2)
        
        skipButton = Button(guessWindow, text="Next",command=self.onNextButton)
        skipButton.grid(row=3, column =2)
       
        self.updateHiScore = StringVar()
        self.updateHiScore.set("High Score: " + str(self.highscore))
        
        hiScore = Label(guessWindow, textvariable=self.updateHiScore)
        hiScore.grid(row=4, column=1)
        
        self.updatePlayerScore = StringVar()
        self.updatePlayerScore.set("Score: " + str(self.playerScore))
        
        score = Label(guessWindow, textvariable=self.updatePlayerScore)
        score.grid(row=4, column=3)
        
        #Card currently being guessed
        if self.gameState == 0:
            #updates the graphics/canvas
            self.backCard.itemconfig(self.backLabel, text=" ")
            self.backCard.config(background="white")
            self.frontCard.itemconfig(self.backLabel, text=self.front)
            self.instructions.config(text="Translate the term into " + 
            str(self.transFrom) + " in the space below")
        #Needs new card
        else:
            self.instructions.config(text = "Click 'next' to deal another card.")        

    def onNextButton(self):
        if len(self.deck) > 0:
            self.gameWindow.destroy()
            self.dealCard()
        else:
            self.endOfDeck()
        
    def checkEntry(self):
        #If answer is correct:
        if (((self.guess.get()).lower() in self.back) or 
        ((self.guess.get()).lower() == self.back)) and (len(self.guess.get()) != 0):
            self.backCard.itemconfig(self.backLabel, text="Correct!")
            self.backCard.config(background="green")
            self.instructions.config(text = "Awesome! Click next to draw a new card")
            self.playerScore += 1
            
            self.updateScores()
            self.gameState = 1
            
        #Temporary fix for the bug where if you enter nothing, you still get points
        elif len(self.guess.get()) == 0:
            self.backCard.itemconfig(self.backLabel, text="Incorrect!")
            self.backCard.config(background="red")
            self.instructions.config(text = "Too bad... the correct answer was: "+
            str(self.back) + ". Click next to draw a new card.")
            self.playerScore = 0
            self.gameState = 1
            
        #If answer is wrong:
        else:
            self.backCard.itemconfig(self.backLabel, text="Incorrect!")
            self.backCard.config(background="red")
            self.instructions.config(text = "Too bad... the correct answer was: "+
            str(self.back) + ". Click next to draw a new card.")
            self.playerScore = 0
            self.gameState = 1
            
        self.updatePlayerScore.set("Score: " + str(self.playerScore))
        self.updateHiScore.set("High Score: " + str(self.highscore))
        
    def updateScores(self):
        """Updates the scores according to the curent playerScore"""
        #NOT FINAL - I know there's got to be a better way to do this...
        if (self.playerScore > self.highscore):
            self.thirdbest = self.secondbest
            self.thirdbestdate = self.secondbestdate
            
            self.secondbest = self.highscore
            self.secondbestdate = self.highscoredate
            
            self.highscore = self.playerScore
            self.highscoredate = now.strftime("%m/%d/%Y %I:%M")
            
        elif (self.playerScore > self.secondbest) and (self.playerScore <= 
        self.highscore):
            self.thirdbest = self.secondbest
            self.thirdbestdate = self.secondbestdate
            
            self.secondbestdate = now.strftime("%m/%d/%Y %I:%M")
            self.secondbest = self.playerScore
            
        elif (self.playerScore > self.thirdbest) and (self.playerScore <=
        self.secondbest):
            self.thirdbest = self.playerScore
            self.thirdbestdate = now.strftime("%m/%d/%Y %I:%M")
             
        else:
            pass
            
    def newCard(self):
        """Selects a new card and updates the canvas; returns a tuple with the 
        front and back of the card."""
        #If the deck is still full, takes cards from the thing
        if len(self.deck) > 0:
            card = random.choice(self.deck)#picks a random card from the deck
            front = card[self.transTo] #finds the front
            back = card[self.transFrom] #finds the back
            index = int(self.deck.index(card)) 
            self.deck.pop(index)
            #updates the details of the new card
            return (front, back)
        #If the deck runs out, it asks you to restart
        elif len(self.deck) == 0:
            print "ERROR ERROR"
            
            
            
    def endOfDeck(self):
        """Spawns a pop-up notifying the player that they have reached the end of
        their deck. Asks player if they want to add their score to the 'Hall of
        Fame'."""
        if self.playerScore >= self.highscore:
            if tkMessageBox.askyesno(
                "New High Score!", 
                ("Your score is "+str(self.playerScore)+ ". Would you like to see the Hall of Fame?")
                ):
                self.seeHighScores()
            if tkMessageBox.askyesno(
                "End of deck.", 
                ("Your final score is " + str(self.playerScore)+ ". Would you like to start a new game?")
                ):
                self.initNewGameOptionsUI()
            else:
                pass             
                                
    def seeHighScores(self):
        """Initializes 'High Score' GUI"""
        #Checks for open windows, closes them
        try:
            self.gameWindow.destroy()
        except:
            pass
        try:
            self.optionsWindow.destroy()
        except:
            pass
        try:
            self.startWindow.destroy()
        except:
            pass
        #If they are not there, ignores it, and moves on
        
        #Starts up new gui window
        self.scoresWindow = Frame(self, width=400, height=350)
        self.scoresWindow.pack()
        self.scoresWindow.pack_propagate(0)
        
        #High Score Header Image
        hiScorePic = PhotoImage(file="Pics\highScores.gif")
        hiScorePicLabel = Label(self.scoresWindow,image=hiScorePic, borderwidth=0)
        hiScorePicLabel.hiScorePic = hiScorePic
        hiScorePicLabel.pack()
        
        #Creates frame for High Scores
        self.scoresFrame = Frame(self.scoresWindow)
        self.scoresFrame.pack()
        
        #Scores
        #Topmost Labels
        PlaceLabel1 = "Place"
        PL1 = Label(self.scoresFrame, text=PlaceLabel1)
        PL1.grid(row=1, column=1)
        
        ScoreLabel1 = "Score"
        SL1 = Label(self.scoresFrame, text=ScoreLabel1)
        SL1.grid(row=1, column=2)
        
        DateLabel1 = "Date"
        DL1 = Label(self.scoresFrame, text=DateLabel1)
        DL1.grid(row=1, column=3)
        
        #First Place Labels
        PlaceLabel2 = "1st"
        PL2 = Label(self.scoresFrame, text=PlaceLabel2)
        PL2.grid(row=2, column=1)
        
        SL2 = Label(self.scoresFrame, text=str(self.highscore))
        SL2.grid(row=2, column=2)
        
        DL2 = Label(self.scoresFrame, text=str(self.highscoredate))
        DL2.grid(row=2, column=3)
        
        #Second Place Labels
        PlaceLabel3 = "2nd"
        PL3 = Label(self.scoresFrame, text=PlaceLabel3)
        PL3.grid(row=3, column=1)
        
        SL3 = Label(self.scoresFrame, text=str(self.secondbest))
        SL3.grid(row=3, column=2)
        
        DL3 = Label(self.scoresFrame, text=str(self.secondbestdate))
        DL3.grid(row=3, column=3)
        
        #Third Place Labels
        PlaceLabel4 = "3rd"
        PL4 = Label(self.scoresFrame, text=PlaceLabel4)
        PL4.grid(row=4, column=1)
        
        SL4 = Label(self.scoresFrame, text=str(self.thirdbest))
        SL4.grid(row=4, column=2)
        
        DL4 = Label(self.scoresFrame, text=str(self.thirdbestdate))
        DL4.grid(row=4, column=3)
        
    def aboutGF(self):
        """Spawns a pop-up window with information about GenkiFlash"""
        tkMessageBox.showinfo(
            "About GenkiFlash",
            ("Thank you for using GenkiFlash!" +
            "\n GenkiFlash was created in 2015 by Bianca Allyn Morris." +
            "\n Learn more about this software at biancaallynm.wordpress.com/programming/." +
            "\n Please note that GenkiFlash is not an affiliate of the textbooks by Eri Banno."
            )
        )
                                
def main():
    """Sets up the window; keeps it running"""
    root = Tk()
    
    # Creates the Menu Bar
    menu = Menu(root)
    root.config(menu=menu)
    
    root.geometry("400x325+300+300")
    app = GenkiFLASH(root)
    root.iconbitmap('genkiFLASH.ico')
    
    # Options Bar
    optsmenu = Menu(menu)
    menu.add_cascade(label = "Options", menu = optsmenu)
    optsmenu.add_command(label = "Choose New Deck...", command = app.initNewGameOptionsUI)
    optsmenu.add_command(label = "See High Scores...", command = app.seeHighScores)
    optsmenu.add_separator()
    helpmenu = Menu(menu)
    menu.add_cascade(label="Help", menu = helpmenu)
    helpmenu.add_command(label="About...", command=app.aboutGF)

    
    root.mainloop()

if __name__=='__main__':
    main()
          
    #def startCardGame(self, Tuple):
    #    deck = Tuple[0]
    #    mode = Tuple[1]
    #    
    #    #Gets rid of old window
    #    self.optionsWindow.destroy()
    #    
    #    #Creates a new window with new game options.
    #    self.gameWindow = Frame(self, width=400, height=350)
    #    self.gameWindow.pack()
    #    self.gameWindow.pack_propagate(0)
    #    
    #    if mode == "ENG -> JPN Translation":
    #        #popup for detailed settings
    #        
    #        
    #        self.optionsWindow.destroy()
    #        
    #        
    #        
    #        self.translation(deck, 'english', '')
    #    elif mode == "Kanji Recognition":
    #        
    #    
    #    elif mode == "Conjugation":
    #        #Create popup window 
    #
    #def translation(self, deck, frontCard, backCard):
    #def recognition(self, deck, frontCard, backCard):
    #def conjugation(self, deck, frontCard, backCard):
    #    """Starts conjugation"""