from pathlib import Path
import random
import json
from Utils.probability_utils import get_probabilistic_answer

def getDomesticPlayerName():
      current_dir = Path(__file__).resolve().parent
      json_file_path = current_dir / 'name_data.json'
      with open(json_file_path, "r") as f:
            data = json.load(f)
      
      data = data["domestic"]
      first = data["firstNames"]
      islamicLastNames = data["islamicLastNames"]
      hinduLastNames = data["hinduLastNames"]
      switchPossible = data["switchPossible"]
      additionalFirstNames = data["additionalFirstNames"]

      three_part_name_prob = get_probabilistic_answer(.15)

      if three_part_name_prob == 1:
            newFirstName = get_probabilistic_answer(.2)
            if newFirstName == 1:
                  firstName = random.choice(additionalFirstNames)
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
                  while(lastName == firstName):
                        lastName = random.choice(first)
                  return  firstName + " " + middleName + " " + lastName
      
      firstName = random.choice(first)
      last = random.choice([islamicLastNames, hinduLastNames])
      lastName = random.choice(last)

      switch = 0
      if lastName in switchPossible:
            switch = get_probabilistic_answer(.25)
      
      if switch == 1:
           return lastName + " " + firstName
      return firstName + " " + lastName


def getInternationalPlayerName(nationality):

      if nationality == "West Indies":
            current_dir = Path(__file__).resolve().parent
            json_file_path = current_dir / 'name_data.json'
            with open(json_file_path, "r") as f:
                  data = json.load(f)
            
            data = data["westIndies"]
            first = data["firstNames"]
            last = data["lastNames"]

            firstName = random.choice(first)
            lastName = random.choice(last)

            return firstName + " " + lastName
      
      if nationality == "South Africa" or nationality == "Netherlands":
            current_dir = Path(__file__).resolve().parent
            json_file_path = current_dir / 'name_data.json'
            with open(json_file_path, "r") as f:
                  data = json.load(f)
            
            # choice = random.choice(["van_de", "van_de", "commonWhite"])

            # if choice == "commonWhite":
            #       return generate_common_white_name()
            # elif choice == "african":
            #       data = data["african"]
            # elif choice == "van_de": 
                  
                  
            # data = data["van_de"]
                  
            first = data["van_de"]["firstNames"] + data["commonWhiteNames"]["firstNames"]
            last = data["van_de"]["lastNames"] + data["commonWhiteNames"]["lastNames"]

            firstName = random.choice(first)
            lastName = random.choice(last)
            return firstName + " " + lastName
      
      else:
            return generate_common_white_name()
      
def generate_common_white_name():
      current_dir = Path(__file__).resolve().parent
      json_file_path = current_dir / 'name_data.json'
      with open(json_file_path, "r") as f:
            data = json.load(f)
      
      data = data["commonWhiteNames"]
      first = data["firstNames"]
      last = data["lastNames"]

      firstName = random.choice(first)
      lastName = random.choice(last)

      return firstName + " " + lastName