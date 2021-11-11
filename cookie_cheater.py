from tkinter import *

class cookies_info():
    def __init__(self):
        self.initial_price = [15,100,1100,12000,130000,1400000,20000000,330000000,5100000000,75000000000,1000000000000,14000000000000,170000000000000,2100000000000000]
        self.initial_cps = [0.1,1,8,47,260,1400,7800,44000,260000,1600000,10000000,65000000,430000000,2900000000]
        self.multiplier = 4.71
        self.upgrades = [1,2**18,64,64,32,32,16,16,16,8,8,4,4,1]
        self.grandma_upgrades = 10
        self.actual_price = []

        self.retrieve("test.cki")
        self.cps = []
        self.names = ["Cursor", "Grandma", "Farm", "Mine", "Factory", "Bank", "Temple", "Wizard tower", "Shipment", "Alchemy", "Portal", "Time machine", "Antimatter condenser", "Prism"]
        for loop in range(len(self.initial_price)):
            self.actual_price.append(self.initial_price[loop] * (1.15 ** self.owned[loop]))
        for loop in range(len(self.initial_cps)):
            self.cps.append(self.initial_cps[loop] * self.multiplier * self.upgrades[loop])
            if (loop >= 2 and loop <= self.grandma_upgrades + 1):
                self.cps[loop] *= (self.owned[1] / (loop - 1)) / 100 + 1
            print(self.names[loop], self.cps[loop])

    def get_next_buy(self):
        best = self.actual_price[0] / self.cps[0]
        best_one = 0
        for loop in range(len(self.cps)):
            if (self.actual_price[loop] / self.cps[loop] < best):
                best = self.actual_price[loop] / self.cps[loop]
                best_one = loop
        return best_one

    def buy_next_one(self):
        next_one = self.get_next_buy()
        self.owned[next_one] += 1
        self.actual_price[next_one] *= 1.15
        return self.names[next_one]

    def save(self, filename):
        strs = []
        for number in self.owned:
            strs.append(str(number))
        f = open(filename, "w")
        f.write(",".join(strs))
        f.close()
        print("The cookie infos has been saved properly")

    def retrieve(self, filename):
        f = open(filename, "r")
        readable = f.read()
        strs = readable.split("\n")[0].split(",")
        self.owned = []
        for number in strs:
            self.owned.append(int(number))

    def create_hud(self, window, buildings):
        for number, name in zip(self.owned, self.names):
            buildings.append((Label(window, text=name + " " + str(number), bg = "black", fg= "white"), number, name))
        for loop in range(len(buildings)):
            buildings[loop][0].place(x=800, y=80 + 20 * loop)

def temp(cookie, actual_cookie, text_list, buildings):
    text_list.append(text_list.pop(0))
    found_name = text_list[9]["text"]
    text_list[9].configure(text=cookie.buy_next_one())
    text_list[9].place(x=10, y=410)
    for loop in range(9):
        text_list[loop].place(x=10, y=50+40*loop)
    for loop in range(len(buildings)):
        if (buildings[loop][2] == found_name):
            temp_nb = buildings[loop][1] + 1
            buildings[loop][0].configure(text=buildings[loop][2] + " " + str(temp_nb))
            buildings[loop] = (buildings[loop][0], temp_nb, buildings[loop][2])
            break
    actual_cookie.buy_next_one()


window = Tk()
window.title('Cookie Cheater')
window.configure(bg='#000000', width=1000, height=500)

cookie = cookies_info()
actual_cookie = cookies_info()

button_get_next = Button(window, text="Bought", command= lambda: temp(cookie, actual_cookie, text_list, buildings))
button_get_next.place(x=800, y=50)

text_list= []
for loop in range(10):
    text_list.append(Label(window, text=cookie.buy_next_one(),font=("Courier", 30), bg="black", fg="white"))
    text_list[loop].place(x=10, y=50 + 40 * loop)

buildings = []
actual_cookie.create_hud(window, buildings)

window.mainloop()
actual_cookie.save("test.cki")
