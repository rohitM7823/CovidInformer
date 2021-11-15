import re

import requests as req
from bs4 import BeautifulSoup as bs


class Main:

    def __init__(self):
        print("Welcome to Chat... I can give you some information about COVID19\n"
              "....To exit from chat just type 'quit'....Happy Chatting...")

        source1 = req.get("https://www.worldometers.info/coronavirus/")
        url = "https://corona.lmao.ninja/v2/countries?yesterday&sort"
        payload = {}
        headers = {}
        response = req.request("GET", url, headers=headers, data=payload)
        self.json_obj = response.json()

        source1.encoding = 'utf-8'
        page = source1.text

        self.parse_html1 = bs(page, "html.parser")
        self.get_information()

        self.replies = {'hi': 'Hi..',
                        'can you tell me about covid19?': 'Yes OF Course.',
                        'how are you?': "I'm Fine..How are You?",
                        'who created you': 'Rohit Manna created me. How can i help you?',
                        "can you tell me current state of covid19?": 'I\'ll show you the stat.'}

    def get_information(self):
        self.total_cases = self.parse_html1.find("div", class_="maincounter-number").text
        self.total_deaths = self.parse_html1.find("div", class_="maincounter-number"). \
            find_next("div", class_="maincounter-number").text
        self.total_recovered = self.parse_html1.find("div", class_="maincounter-number"). \
            find_next("div", class_="maincounter-number"). \
            find_next("div", class_="maincounter-number").text
        self.total_active = self.parse_html1.find("div", class_="number-table-main").text
        self.id_dict = {j: c for j, c in enumerate(self.json_obj)}
        self.id_country = {c["country"]: j for j, c in enumerate(self.json_obj)}

    def get_replies(self):
        print()
        while True:
            print()
            usr_input = input("Type Here: \t")

            world_obj = re.search('[wW]orldwide', usr_input.title())
            death_obj = re.search('[dD]eath|[dD]ied', usr_input.title())
            cured_obj = re.search('[cC]ured|[rR]ecovered', usr_input.title())
            active_obj = re.search('[aA]ctive', usr_input.title())

            if usr_input in self.replies.keys():
                print(self.replies[usr_input])

            elif re.search("[Hh]ey|[Hh]i\.*|[hH]el\.*", usr_input):
                print(self.replies['hi'])

            elif re.search("[aA]bout ([Cc]ovid19|[Cc]coronavirus)", usr_input):
                print(self.replies['can you tell me about covid19?'])

            elif re.findall("([hH]o\.*)([aA]r\.*)", usr_input):
                print(self.replies['how are you?'])

            elif re.search("(creat\.*|made) you", usr_input):
                print(self.replies['who created you'])

            # Worldwide death, cured, active cases
            elif (death_obj and world_obj) or (active_obj and world_obj) or (cured_obj and world_obj) is not None:

                if ("Death" or "Died" and world_obj.group()) \
                        or ("Cured" or "Recovered" and world_obj.group()) \
                        or ("Active" and world_obj.group()) in re.split("[\W]", usr_input.title()):

                    if re.search('[dD]eath|[dD]ied', usr_input.title()):
                        print(f"Worldwide Currently Died Patients: {self.total_deaths}")
                    elif re.search('[cC]ured|[rR]ecovered', usr_input.title()):
                        print(f"Worldwide Currently Recovered Patients: {self.total_recovered}")
                    elif re.search('[aA]ctive', usr_input.title()):
                        print(f"Worldwide Currently Active Patients: {self.total_active}")

            # Worldwide Total Statistics...
            elif re.findall("[cC]urrent [sS]tate|[wW]orldwide|([sS]tatistic|[sS]tats)", usr_input):
                print(self.replies["can you tell me current state of covid19?"],
                      f"{self.total_cases}THIS IS REALTIME CASES..")

            # Countrywise Death, Cured, Total Cases....
            elif input_country := [s.title() for s in re.split("[\W]", usr_input)
                                   if any(c for c in self.id_country.keys()
                                          if s.title() in c)]:
                for x in input_country:
                    if x in self.id_country.keys():
                        if re.search("([dD]ie|[dD]eat*)", usr_input):
                            if re.search("[cC]ur|[rR]ecov*", usr_input):
                                print(f'Death Cases: {self.id_dict[self.id_country.get(x)]["deaths"]}\n'
                                      f'Cured Cases: {self.id_dict[self.id_country.get(x)]["recovered"]}')
                            else:
                                print(f'Death Cases: {self.id_dict[self.id_country.get(x)]["deaths"]}')
                            break
                        elif re.search("[tT]ot.", usr_input):
                            print(f'Total Cases: {self.id_dict[self.id_country.get(x)]["cases"]}')

                        elif re.search("[aA]cti.", usr_input):
                            print(f"Active Cases: {self.id_dict[self.id_country.get(x)]['active']}")
                        else:
                            print(f'Recovered Cases: {self.id_dict[self.id_country.get(x)]["recovered"]}')


            # For Existing from the Chat..
            elif usr_input == 'quit':
                print("Thank You using me, Good Bye.")
                break

            else:
                print("I'm still learning...so go slow!")


if __name__ == "__main__":
    obj = Main()
    obj.get_replies()
