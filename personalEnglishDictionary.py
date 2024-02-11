import sqlite3
import random
import pandas as pd
def main_menu():
    print("""
          ******************** WELCOME TO MENU ********************
          1)Add Word
          2)Exercise With Words
          3)All words
          ------------------------
          Make your choice 1 or 2 or 3?
          """)
class Words:
    def __init__(self, db_path='dictionary.db'):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_table()
    
    #veritabanı yoksa oluşturma
    def create_table(self):
        self.cursor.execute('''
          CREATE TABLE IF NOT EXISTS dictionary (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              word TEXT NOT NULL,
              word_value TEXT NOT NULL
                                                      );
        ''')
        self.connection.commit()
        
    def addWord(self,word,word_value):
        if word in self.getWord():
            print("Bu kelimeyi eklemiştin!")
        else:
            self.cursor.execute("""
                           INSERT INTO DICTIONARY (WORD,WORD_VALUE)
                           VALUES(?,?)
                           
                           """,(word,word_value))
            self.connection.commit()
            print("Word Add!")
            print("/////////////////////////////////////////////////\n")
    
    def getWord(self):
        self.cursor.execute("SELECT WORD FROM DICTIONARY")
        words = self.cursor.fetchall()
        return [word[0] for word in words] 
    
    def Addword_menu(self):
            print("--------------------\npress x if you want to exit\n-------------------- ")
            print("How many words would you like add? ")
            num=int(input())
            for i in range(num):
                print("Write the word you want to add: ")
                word=input()
                if word !="x":
                    print(f"The value of {word}: ")
                    word_value=input()
                    if word_value!="x":
                        self.addWord(word.lower(),word_value.lower())
                    else:
                        print(f"{word} did not add to the database")
                        cont()
                else:
                    cont()
                
    def exerciseWithWord(self):
        print("--------------------\npress x if you want to exit\n-------------------- ")
        sel_word=[]
        words= self.getWord()
        count=1
        incorrect_count=0
        numR=3
        space="\n******************************\n"
        while len(words)!=len(sel_word):
            selected_word = random.choice(words)
            exit_let="x"
            if selected_word not in sel_word:
                while True:
                    print(selected_word ,"\nValue of word: ")
                    value=input()
                    correct_value=self.value_control(selected_word)
                    if value ==exit_let:
                        cont()
                    elif value.lower()==correct_value:
                        print(f"Doğru bilinen kelime sayısı:{count}")
                        print("Good!"+space)
                        break
                    else:
                        incorrect_count+=1
                        if incorrect_count<numR:
                            print("Try Again!"+space)
                            print("Number of remaining rights:",numR-incorrect_count)
                        else:
                            print(f"The value of {selected_word}:",correct_value,space)
                            break
                
                count+=1
                sel_word.append(selected_word)
    
    def value_control(self,value):
        """
        

        Parameters
        ----------
        value : string
            client's response to the word

        Returns
        -------
        word_value : string
            return the correct value of the word

        """
        
        self.cursor.execute("SELECT WORD_Value FROM DICTIONARY WHERE WORD=?",(value,))
        row = self.cursor.fetchone()
        if row:
            word_value = row[0]
            return word_value
        else:
            print("Kelime bulunamadı.")
            return None
        
    #display every word in the database
    def all_word(self):
        self.cursor.execute("SELECT * FROM DICTIONARY")
        rows = self.cursor.fetchall()
        pd.set_option("display.width",500)
        df=pd.DataFrame(rows,columns=["id","Word","Word Value"])
        
        print(df)
        
            
def cont():   
    while True:
        main_menu()
        choice=input()
        w=Words()
        if choice not in ["1","2","3"]:
           print("Try again!")
        elif choice=="1":
            w.Addword_menu()
            
        elif choice=="2":
            w.exerciseWithWord()
        else:
           w.all_word()
       
cont()