"""noticed that a lot of combo list or database leaks format their credentials in the following way username:pass This tools helps extract the passwords and save them to a text file """

with open("combo.txt", "r") as f:
	lines = f.readlines()

passwds = list(map(lambda x: x.split(":")[1],lines))

with open("wordlist.txt","w") as w:
	w.writelines(passwds)
