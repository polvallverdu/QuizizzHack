import json
import urllib.request

# Inputs the quizizz ID, found on the URL (or debugging the network tab)
quizizz_id = str(input("Enter quizizz ID: "))

# Request to quizizz server to obtain all information of the quiz
response = urllib.request.urlopen(f"https://quizizz.com/quiz/{quizizz_id}")
data = json.loads(response.read())

# If the id is invalid, exit the program
if (str(data["success"]) == "false"):
  print("Invalid ID")
  exit()

# Gets the questions dictionary
questions = data["data"]["quiz"]["info"]["questions"]

# Loops through every question and prints the question and the correct answer
for x in range(0, len(questions)):
  title = questions[x]["structure"]["query"]["text"].replace("<p>", "").replace("</p>", "")
  answer = data["options"][data["answer"]]["text"].replace("<p>", "").replace("</p>", "")
  
  print("\n{}- {}\nAnswer: {}\n".format(str(x), title, answer))
