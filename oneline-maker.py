#just an idea for now.

def Select_language():
  while True:
    try:
      user_input = int(input("What language do you need a one liner for 1- Powershell 2- Bash 3- Python 4- C# 5-C": ).strip())
      break
    except:
      print("Please enter a valid answer")
