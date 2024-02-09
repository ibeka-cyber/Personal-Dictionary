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
            print("How many words would you like add? ")
            num=int(input())
            for i in range(num):
                print("Write the word you want to add: ")
                word=input()
                print(f"The value of {word}: ")
                word_value=input()
                self.addWord(word.lower(),word_value.lower())
                
    def exerciseWithWord(self):
        sel_word=[]
        words= self.getWord()
        count=1
        while len(words)!=len(sel_word):
            selected_word = random.choice(words)
            if selected_word not in sel_word:
                while True:
                    print(selected_word ,"\nValue of word: ")
                    value=input()
                    if value.lower()==self.value_control(selected_word):
                        print(f"Doğru bilinen kelime sayısı:{count}")
                        print("Good!\n******************************\n")
                        break
                    else:
                        print("Try Again!\n******************************\n")
                
                count+=1
                sel_word.append(selected_word)
            
    def value_control(self,value):
        self.cursor.execute("SELECT WORD_Value FROM DICTIONARY WHERE WORD=?",(value,))
        row = self.cursor.fetchone()
        if row:
            word_value = row[0]
            return word_value
        else:
            print("Kelime bulunamadı.")
            return None
        
    #tüm kelimeleri getir
    def all_word(self):
        self.cursor.execute("SELECT * FROM DICTIONARY")
        rows = self.cursor.fetchall()
        pd.set_option("display.width",500)
        df=pd.DataFrame(rows,columns=["id","Word","Word Value"])
        
        print(df)
        
            
    
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
       
