import random


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
     "Omio", "Tawsif", "Sadik", "Jahirul", "Tasnim", "Ashraf", "Saif",
     "Radi", "Sadi", "Ataur", "Atik", "Apurbo", "Arnab"]

last = ['Chowdhury', 'Ahmed', 'Khan', 'Hossain',
 'Uddin', 'Hasan', 'Haque', "Haq", "Hoq", 'Mahmud', 'Islam', "Mohammad", "Mohammed", 
  'Ali', 'Alam', 'Rahman', 'Ahmad', 'Khondokar'
  , 'Ahsan', 'Zaman', 'Sarker', 'Habib', 'Majumder', 
  "Sen", "Datta", "Sarkar", "Biswas", "Ghosh", "Roy", "Pal",
  "Mia", "Siddique", "Karim", "Malik", "Iqbal", "Barman", "Karmakar", "Abdullah"
  ]


def getPlayerName():
      return random.choice(first) + " " + random.choice(last)

for i in range(1000):
   print(getPlayerName())