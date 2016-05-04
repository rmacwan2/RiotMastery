from RiotAPI import RiotAPI
from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import time
import collections

# Globals
champ_name_ids = {}
mastery_list = {}
summoner_id = ' '
menu = {}
summoner_name = ''
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Mastery_Table.db'
db = SQLAlchemy(app)
db.create_all()
api = RiotAPI('your-api-key')
# connection = engine.connect()

class Champ(db.Model):
    name = db.Column(db.String(15))
    champ_id = db.Column(db.Integer, primary_key=True)
    summoner_id = db.Column(db.Integer, primary_key=True)
    champ_level = db.Column(db.Integer)
    champ_points = db.Column(db.Integer)
    time_since = db.Column(db.BigInteger)
    chests_granted = db.Column(db.Boolean)

    def __init__(self, name, champ_id, summoner_id, champ_level, champ_points, time_since, chests_granted):
        self.name = name
        self.champ_id = champ_id
        self.summoner_id = summoner_id
        self.champ_level = champ_level
        self.champ_points = champ_points
        self.time_since = time_since
        self.chests_granted = chests_granted

'''
def summoner_query(summoner_id, {})
    for id_1, level in mastery_dict.items():
        for name, id_2 in champ_name_ids.items():
            if id_1 == id_2:
                print('Champion: {:15} Mastery Level: {:2}\n').format(name, level)
'''
def main2():
    db.create_all()
    db.session.flush()
    db.session.commit()
    # for i in range(0, 480):
    #    Champ.query.filter_by(champ_id=i).delete()
    # user_query = input('Enter a champion name: ')

    # my_query = Champ.query.filter_by(name='{}'.format(user_query)).all()
    # print('The Summoner ID\'s who play {} are '.format(user_query))
    ### test if a specific summoner is in the table
    # my_query = Champ.query.filter_by(summoner_id=23452661).all()
    # for i in range(0, len(my_query)):
    #    print(my_query[i].name)

    # Print the whole database

    super_query = Champ.query.filter_by().all()
    filler = '--------------------------------------------------------------------------------'
    print(filler + '\n' + filler)
    print('|' + 'Champion Name{:2}'.format(' ') + '|' +
          'C ID{}'.format(' ') + '|' +
          'Summoner ID' + '|' +
          'Level' + '|'
          'Champion Points' + '|'
          'Time Since Played' + '|' +
          'Chest' + '|')
    print(filler)
    for i in super_query:
        print('|' + '{:15}'.format(i.name) + '|' +
              '{:5}'.format(str(i.champ_id)) + '|' +
              '{:11}'.format(str(i.summoner_id)) + '|' +
              '{:5}'.format(str(i.champ_level)) + '|' +
              '{:15}'.format(str(i.champ_points)) + '|' +
              '{:17}'.format(i.time_since) + '|' +
              '{:5}'.format(str(i.chests_granted)) + '|')
        print(filler)


def main():
    # summoner inputs summoner name
    # summoner_name = input('Enter your summoner name: ')
    # summoner_name = summoner_name.lower()
    # summoner_name = summoner_name.replace(' ', '')
    # print('Hello {}\n'.format(summoner_name))

    # get summoner info
    # r = api.get_summoner_by_name(summoner_name)

    # get summoner id
    # current_id = r[summoner_name]['id']

    # get champ id's
    r = api.get_champion_ids()

    for i in r['data'].keys():
        champ_name_ids[i] = r['data'][i]['id']

    # send champ and ids to file
    with open('champ_data.txt', 'w') as outfile:
        for key, value in champ_name_ids.items():
            outfile.write('Champion: {:15} ID: {}\n'.format(key, value))

    # count of valid id's grabbed
    summoners_grabbed = 0
    for summoner in range(7783, 1000000):
        r = api.get_mastery_list(summoner)
        # check to see if summoner id exists
        if len(r) == 0:
            print('The mastery for summoner id {} does not exist.'.format(summoner))
            time.sleep(2)
        else:
            for i in range(0, len(r)):
                mastery_list[r[i]['championId']] = r[i]['championLevel']
                for name, id_2 in champ_name_ids.items():
                    if r[i]['championId'] == id_2:
                        # print(id_2, r[i]['championLevel'])
                        mastery = Champ(name, r[i]['championId'], summoner, r[i]['championLevel'], r[i]['championPoints'], r[i]['lastPlayTime'], chests_granted=r[i]['chestGranted'])
                        db.session.add(mastery)
                        db.session.commit()
            time.sleep(2)
            summoners_grabbed += 1
            print(summoners_grabbed)
        if summoners_grabbed == 10000:
            break

    # sorted(mastery_list)

    superLevel = 0
    with open('mastery_list_{}.txt'.format(summoner_name), 'w') as outfile1:
        for id_1, level in mastery_list.items():
            for name, id_2 in champ_name_ids.items():
                if id_1 == id_2:
                    outfile1.write('Champion: {:15} Mastery Level: {:2}\n'.format(name, level))
                    superLevel += level

    print("Your average mastery level is: {:.3}".format(superLevel/len(mastery_list)))


def main3():
    summoner_name = input('Enter your summoner name: ')
    summoner_name = summoner_name.lower()
    summoner_name = summoner_name.replace(' ', '')

    # get summoner info
    r = api.get_summoner_by_name(summoner_name)

    # get summoner id
    current_id = r[summoner_name]['id']

    stmt = text("SELECT champ_id, COUNT(summoner_id) FROM MasteryTable.db GROUP BY champ_id")
    result = db.execute(stmt)
    names = []
    for row in result:
        names.append(row[0])
    print(names)
    r = api.get_mastery_list(current_id)
    menu['1']="View Summoner Data"
    menu['2']="View Champion Data"
    menu['3']="Find Student"
    menu['4']="Exit"
    while True:
        options = collections.OrderedDict(sorted(menu))
        for k, v in options.items():
            print(k, v)

        for entry in options:
            print(entry, '. ', menu[entry])

            selection=input("Please Select: ")
            if selection == '1':
                print(summoner_name)
            elif selection == '2':
                print('nothing')
            elif selection == '3':
                print('nothing')
            elif selection == '4':
                break
            else:
                print("Unknown Option Selected!")
if __name__ == "__main__":
    # main2()
    main()
    # main3()



