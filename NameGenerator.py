import random
from ProbabilisticFunctionsModule import getProbabilisticAnswer

first = ['Asif', 'Sakib', 'Fahim', 'Sajib',
 'Farhan', 'Tahmid', 'Nayeem', 'Jawad',
  'Mridul', 'Imran', 'Zahid', 'Masud', 'Abir',
  'Jahir', 'Shadman', 'Shadman', 'Digonto', 'Junayet', 'Rahat',
   'Alif', 'Anik', 'Sowad', 'Umaar', 'Tawhid', 'Maruf',
   'Ahnaf', 'Rafi', 'Jubaer', 'Tanvir', 'Foysal', 
   'Siam', 'Koushik', 'Tanjim', 'Shihab', 'Fuad',
   'Sami', 'Samin', 'Mahfuz', 'Sourav', 'Sayem',
    'Shovon', 'Azad', 'Abdul', 'Shakil', 'Punno',
    'Mominul', 'Rakib', 'Zarif', 'Sakif', 'Akash',
     'Ananta', 'Anondo', 'Anan', 'Zadid', 'Tareq', 
     'Aziz' ,'Nahid', 'Mehedi', 'Noyon', 'Ayon', 
     'Golam', 'Ishtiaq', 'Rafid', 'Tausif', 'Kabir',
     'Fuad', 'Fida', 'Srizon', 'Rashid', 'Saad',
     'Ayman', 'Arian', 'Dewan', 'Adib', 'Ratul', 
     'Ashfaq', 'Salman', 'Nafees', 'Nazeef', 'Faiyaz', 
     'Parvez', 'Mahin', 'Samir', 'Arafat', 'Syed', 'Sifat',
     'Muzahid', 'Joy', 'Adnan', "Sameer", "Afsan", "Towkir"
     , "Aziz", "Afif", "Alfy", "Soumya", "Rizwan", 
     "Rizvi", "Saklain", "Shajib", "Dipto", "Rasel",
     "Naeem", "Naim", "Shubho", "Taaz", "Nabil", "Tahrim",
     "Takrim", "Zarzis", "Shahid", "Imtiaz", "Shourobh", "Abul", "Abu",
     "Nazim", "Nazmul", "Naz", "Taaz", "Fatik", "Farhad", "Bappa", "Bappi", 
     "Nasir", "Yasir", "Araf", "Anas", "Ariful", "Miraz", "Pritom", "Mahfuz",
     "Topu", "Rimon", "Shumon", "Jayed", "Kabbo", "Toimur", "Fardin", 
     "Jamal", "Tushar", "Fazle", "Tonmoy", "Haidar", "Moinul", "Shadab",
     "Irtiza", "Shoummo", "Nibir", "Shafin", "Safin", "Ninad", "Raiyan",
     "Alvi", "Himel", "Shahriar", "Ramim", "Sadman", "Mahee", "Mugdho",
     "Omio", "Tawsif", "Sadik", "Jahirul", "Tasnim", "Ashraf", "Saif", "Motaher",
     "Radi", "Sadi", "Ataur", "Atik", "Apurbo", "Arnab", "Ankon", "Ongkon",
     "Mahid", "Tauhid", "Zakir", "Iftikhar", "Noor", "Naseem", "Rishad", "Imrul",
     "Mushfik", "Amir", "Kamrul", "Pranto", "Mosaddek", "Sarwar", "Mustahid", "Fazal"
     ]

islamicLastNames = ['Chowdhury', 'Ahmed', 'Khan', 'Hossain', "Choudhuri",
 'Uddin', 'Hasan', 'Haque', "Haq", "Hoq", 'Mahmud', 'Islam', "Mohammad", "Mohammed", 
  'Ali', 'Alam', 'Rahman', 'Ahmad', 'Khondokar', "Ur-Rahman", "Sheikh", "Amin",
  'Ahsan', 'Zaman', 'Habib', "Al-Ahsan", "Uzzaman", "Al-Amin", "Bhuiyan",
  "Mia", "Siddique", "Karim", "Malik", "Iqbal", "Abdullah", "Skider",
  ]

# islamicLastNames = []
hinduLastNames = [ "Barman", 'Sarker', "Sarkar", "Biswas", "Ghosh", "Roy", "Pal", "Kumar", "Sen", "Datta", "Karmakar", 'Chowdhury', "Choudhuri", 'Majumder', "Paul"]

switchPossible = ["Mahmud", "Ahsan", "Hasan", "Abdullah", "Mohammad", "Mohammed", "Sheikh", "Kumar"]

def getPlayerName():

      three_part_name_prob = getProbabilisticAnswer(.15)

      if three_part_name_prob == 1:
            newFirstName = getProbabilisticAnswer(.2)
            if newFirstName == 1:
                  NewFirst = ["Kazi", "Syed", "Md.", "Mohammed", "K.M."]
                  firstName = random.choice(NewFirst)
                  middleName = random.choice(first)
                  lastName = random.choice(islamicLastNames)
                  if firstName in ["Md.", "Mohammed"]:
                        while lastName in  ["Mohammad", "Mohammed"]:
                              lastName = random.choice(islamicLastNames)
                  return firstName + " " + middleName + " " + lastName
            else:
                  last = random.choice([islamicLastNames, hinduLastNames])
                  firstName = random.choice(first)
                  middleName = random.choice(last)
                  lastName = random.choice(first)
                  return  firstName + " " + middleName + " " + lastName
      
      firstName = random.choice(first)
      last = random.choice([islamicLastNames, hinduLastNames])
      lastName = random.choice(last)

      switch = 0
      if lastName in switchPossible:
            switch = getProbabilisticAnswer(.25)
      
      if switch == 1:
           return lastName + " " + firstName
      return firstName + " " + lastName

# for i in range(1000):
#    print(getPlayerName())