import random
import pickle
import os
import json
import requests
import pytz

import matplotlib.colors as mcolors

from datetime import datetime

from tkinter import *
from tkinter import messagebox as mb
from tkinter import simpledialog as sd

# Define your classes before loading the data
class stack:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

class plr:
    rolls = 0
    rollcd = 1000
    pickaxe = 'None'
    fortune = 0
    username = 'Anonymous'

    @classmethod
    def reevaluate(cls):
        if cls.pickaxe in tool_data:
            cls.fortune = tool_data[cls.pickaxe]['fortune']
            cls.rollcd = tool_data[cls.pickaxe]['rollcd']

            print(f'Fortune has been set to {cls.fortune}, roll cooldown has been set to {cls.rollcd}')
        else:
            cls.fortune = 0
            cls.rollcd = 1000

    @classmethod
    def getattr(cls):
        return {
            'pickaxe': cls.pickaxe,
            'rollcd': cls.rollcd,
            'fortune': cls.fortune,
            'rolls': cls.rolls,
        }

# fixed vars
tool_data = {
    'Wooden Pickaxe': {
        'requirements': {'Wood': 400},
        'fortune': 1,
        'rollcd': 950,
        'description': 'Why do I need 400 logs to craft a pickaxe half the size of a log?'
    },
    'Stone Pickaxe': {
        'requirements': {'Wood': 256, 'Stone': 512, 'Iron': 6},
        'fortune': 3,
        'rollcd': 1250,
        'description': 'Think about it, why doesn\'t your pickaxe crumble when you go mining?'
    },
    'Iron Pickaxe': {
        'requirements': {'Wood': 512, 'Iron': 256},
        'fortune': 3,
        'rollcd': 850,
        'description': 'Your typical trusty pickaxe'
    },
    'Gilded Pickaxe': {
        'requirements': {'Wood': 1024, 'Copper': 512, 'Iron': 256, 'Gold': 256},
        'fortune': 6,
        'rollcd': 900,
        'description': 'Iron Pickaxe plated and enchanted with Rose Gold alloy'
    },
    'Steel Pickaxe': {
        'requirements': {'Wood': 1024, 'Coal': 2048, 'Iron': 1024},
        'fortune' : 5,
        'rollcd' : 650,
        'description': 'A sturdy pickaxe made with steel'
    },
    'Quartztone Pickaxe': {
        'requirements': {'Wood': 12000, 'Coal': 10000, 'Iron': 3500, 'Gold': 1024, 'Quartz': 512, 'Diamond': 256},
        'fortune': 10,
        'rollcd': 850,
        'description': 'A pickaxe enchanted with the energy of quartz'
    },
    'Diamond-Plated Pickaxe': {
        'requirements': {'Wood': 20480, 'Coal': 20480, 'Iron': 5126, 'Gold': 2148, 'Diamond': 512},
        'fortune': 9,
        'rollcd': 650,
        'description': 'A majestic pickaxe plated with Diamonds and adorned in gold'
    },
    'Darksteel Pickaxe': {
        'requirements': {'Wood': 64960, 'Coal': 40960, 'Iron': 20480, 'Diamond': 1024, 'Obsidian': 256},
        'fortune': 9,
        'rollcd': 500,
        'description': 'A strong pickaxe forged with Obsidian alloys'
    },
    'Tree Pickaxe': {
        'requirements': {'Wood': 350000},
        'fortune': 1,
        'rollcd': 250,
        'description': 'Why is there wood underground?'
    },
    'Mountain Pickaxe': {
        'requirements': {'Stone': 500000, 'Copper': 300000, 'Iron': 200000, 'Gold': 75000, 'Quartz' : 50000, 'Diamond': 7500, 'Obsidian': 1250, 'Bedrock': 100},
        'fortune': 75,
        'rollcd': 7500,
        'description': 'How did you manage to pick this up?'
    },
    'Deepdriller': {
        'requirements': {'Coal': 500000, 'Copper': 250000, 'Iron': 125000, 'Gold': 100000, 'Quartz': 35000, 'Diamond': 7500, 'Obsidian': 2500, 'Bedrock': 500},
        'fortune': 20,
        'rollcd': 350,
        'description': 'High-tech drill built with bedrock alloys and enchanted with precious materials.'
    }
}

resources = {
    'inventory': {
        'Wood': 1000,
        'Stone': 0,
        'Coal' : 0,
        'Copper': 0,
        'Iron': 0,
        'Gold': 0,
        'Quartz': 0,
        'Diamond': 0,
        'Obsidian': 0,
        'Bedrock': 0
    },
    'oreabundance': {
        'Wood': (7, 12),
        'Stone': (5, 8),
        'Coal' : (5, 10),
        'Copper': (2, 5),
        'Iron': (3, 8),
        'Gold': (1, 4),
        'Quartz': (1, 3),
        'Diamond': (1, 2),
        'Obsidian': (1, 1),
        'Bedrock': (1, 1)
    },
    'index': {
        'Wood': 75,
        'Stone': 50,
        'Coal': 35,
        'Copper': 25,
        'Iron': 17,
        'Gold': 8,
        'Quartz': 2.5,
        'Diamond': 1,
        'Obsidian': 0.5,
        'Bedrock': 0.05
    }
}

# colors for formatting
colors = {
    'Wood' : 'brown',
    'Stone' : 'gray',
    'Coal' : 'black',
    'Copper' : 'orange',
    'Iron' : 'pink',
    'Gold' : 'yellow',
    'Diamond' : 'cyan',
    'Quartz': 'pink',
    'Obsidian' : 'purple',
    'Bedrock': 'black'
}

# Percentage rarity
total_weight = sum(resources['index'].values())

percentage_rarity = {
    item: round((weight / total_weight) * 100, 4)  # Rounded to 4 decimal places
    for item, weight in resources['index'].items()
}

# Load data
pathtodata = 'rnggamedata.txt'

#webhook
webhook = 'https://discord.com/api/webhooks/1362220157463826565/QW-7LjsgHQuG_6n5iamRwC3zLpvRbCmbnTYGZ5WTXQkxUrA_aN6SJrjdlp2MkOzNHGqJ'

# template
def getTemplate():
    return {
        'pickaxe': 'None',
        'fortune': 0,
        'rolls': 0,
        'rollcd': 1000,
        'tools': [],
        'username': '',
        'inventory': resources['inventory']
    }

try:
    with open(pathtodata, 'rb') as file:
        data = pickle.load(file)
except FileNotFoundError:
    data = getTemplate()
    
if 'username' not in data or not data['username']:
    data['username'] = input('Please input username here: ')

tempinv = resources['inventory']
tempinv.update(data['inventory'])
data['inventory'] = tempinv

# Load player data
plr.rolls = data['rolls']
plr.pickaxe = data['pickaxe']
plr.username = data['username']
plr.reevaluate()

# functions
def enablebuttons():
    for button in buttonstodisable:
        button.config(state=NORMAL)

def disablebuttons():
    global autorolling

    autorolling = False
    autoroll.config(fg='red')

    for button in buttonstodisable:
        button.config(state=DISABLED)
        
def getitem(ls, name):
    for item in ls:
        if item.name == name:
            return item

def updatebox():
    global displayinv

    displayinv.delete(0, END)
    for item in inventory:
        displayinv.insert(END, f'{item.name}: {item.amount}')

def populate():
    global counter

    counter.config(text=f'Total rolls: {plr.rolls}')
    updatebox()

def saveprogram():
    global inventory

    datatosave = {
        'pickaxe' : plr.pickaxe,
        'fortune' : plr.fortune,
        'rollcd' : plr.rollcd,
        'rolls' : plr.rolls,
        'username': plr.username,
        'tools' : tools,
        'inventory' : {item.name: item.amount for item in inventory}
    }


    with open(pathtodata, 'wb') as file:
        pickle.dump(datatosave, file)
        
def onCraft(pickname):
    tool = tool_data[pickname]
    requirements_str = '\n'.join([f'{key}: {value}' for key, value in tool['requirements'].items()])
    
    payload = {
        'username': 'Mining RNG: Pickaxe Crafts',
        'embeds': [{
            'title': f'{plr.username} has crafted {pickname}! Congratulations!',
            'description': f'{pickname} Stats:',
            "fields": [
                {"name": "🍀 Fortune", "value": tool['fortune'], "inline": True},
                {'name': '💨 Roll Cooldown', 'value': str(tool['rollcd']) + 'ms', 'inline': True},
                {"name": "💰 Cost", "value": requirements_str, "inline": False},
            ],
            'color': 0x7dda58
        }],
    }
    
    requests.post(webhook, json=payload)

def rareFound(ore, amt):
    currenttime = datetime.now(pytz.timezone('Singapore')).strftime('Rolled at %d/%m/%Y %H:%M.%S')

    color_decimal = int(mcolors.to_hex(colors[ore]).lstrip("#"), 16)

    payload = {
        'username': 'Mining RNG: Rare Rolls',
        'embeds': [{
            'title': f'{ore} ({percentage_rarity[ore]}%) has been rolled!',
            'description': f'{plr.username} has rolled {amt} {ore} at {plr.rolls} rolls.',
            'footer': {
                'text': currenttime
            },
            'color': color_decimal,
        }],
    }

    requests.post(webhook, json=payload)
    
def statsCheck():
    payload = {
        "username": "Mining RNG: Stats",
        "embeds": [
            {
                "title": f"📊 {plr.username}\'s Stats",
                "color": 0x00ff99,
                "fields": [
                    {"name": "🔁 Rolls", "value": plr.rolls, "inline": True},
                    {"name": "🍀 Fortune", "value": plr.fortune, "inline": True},
                    {'name': '💨 Roll Cooldown', 'value': f'{plr.rollcd}ms', 'inline': True},
                    {"name": "⛏️ Equipped Pickaxe", "value": plr.pickaxe, "inline": False},
                ]
            },
            {
                'title': f'🎒 {plr.username}\'s Ore Inventory 🪨💎',
                'color': 0x00ff99,
                'fields': [{'name': f'{item.name} ({percentage_rarity[item.name]}%)', 'value': item.amount, 'inline': False} for item in inventory]
            },
            {
                'title': f'🎒 {plr.username}\'s Pickaxe Inventory ⛏️',
                'color': 0x00ff99,
                'fields': [
                    {
                        'name': f"⛏️ {tool_name}",
                        'value': (
                            f"{'✅ Owned' if tool_name in tools else '❌ Locked'}\n"
                        ),
                        'inline': False
                    }
                    for tool_name, data in tool_data.items()
                ]
            }
        ]
    }


    requests.post(webhook, json=payload)
    

def additem():
    global inventory
    global items
    global weights
    global autorolling

    blocks = ['Wood', 'Stone', 'Obsidian', 'Bedrock']

    roll.config(state=DISABLED)
    roll.after(plr.rollcd, lambda: (roll.config(state=NORMAL)) or (additem() if autorolling else None))

    check = False
    name = random.choices(items, weights, k=1)[0]
    
    amtgained = 0

    for stax in inventory:
        if stax.name == name:
            amtgained = random.randint(resources['oreabundance'][name][0], resources['oreabundance'][name][1])

            if not name in blocks:
                amtgained += plr.fortune

            notif.config(text=f'You got {amtgained} {name}!', fg=colors.get(name, 'black'))
            notif.after(plr.rollcd - 5, lambda: notif.config(text=''))
            stax.amount += amtgained
            check = True
            break

    plr.rolls += 1
    
    if percentage_rarity[name] < 1:
        rareFound(name, amtgained)

    populate()

def craftitem(name):
    temproot.destroy()

    # Retrieve the tool data for the selected tool
    tool_info = tool_data[name]

    # Get the required materials for crafting
    costs = tool_info['requirements']
    requirements = ', '.join([f'{item}: {costs[item]}' for item in costs])

    query = mb.askyesno('', f'Would you like to craft {name}?\nThe requirements for {name} are:\n{requirements}\n')

    matslog = {}

    if query:
        print('\n\n*DEBUG*')
        print('-' * 50)

        for key, value in costs.items():
            print(f'\nName of item: {key}')
            print(f'Value of item needed: {value}')

            print(f'\nFinding {key} in inventory...')
            invamt = getitem(inventory, key).amount

            print(f'Amount of {key} in inventory: {invamt}')

            if invamt >= value:
                print(f'You have enough {key}.')
                matslog[key] = True
            else:
                print(f'You do not have enough {key}. You need {value - invamt} more.')
                matslog[key] = False

            print('-' * 50)

        if name in [x for x in tools]:
            mb.showwarning('', f'You already own {name}.')

        elif False in matslog.values():
            mb.showwarning('', f'{name} not crafted, you do not have enough of {[key for key, val in matslog.items() if val == False]}.')

        else:
            mb.showinfo('', f'{name} has been crafted! The materials will be deducted from your inventory.')

            for k, v in matslog.items():  # Deduct cost of {k} off of getitem(inventory, k).amount
                print(f'{getitem(inventory, k).amount} {k} --> {getitem(inventory, k).amount - costs[k]} {k}')
                getitem(inventory, k).amount -= costs[k]
            
            onCraft(name)
            tools.append(name)

    try:
        enablebuttons()
    except:
        print('No temproot, ignore')

    populate()

def craftmenu():
    disablebuttons()

    global temproot
    temproot = Toplevel()
    temproot.title('Crafting Menu')
    temproot.protocol('WM_DELETE_WINDOW', lambda: (enablebuttons(), temproot.destroy()))

    craftables = Listbox(temproot, selectmode=BROWSE, width=50, height=25)
    for tool_name in tool_data:
        craftables.insert(END, tool_name)

    craftables.grid(row=0, column=1)

    def craft_with_check():
        selected_index = craftables.curselection()
        if selected_index:  # Check if something is selected
            selected_tool = craftables.get(selected_index)  # Get the selected tool name
            craftitem(selected_tool)
        else:
            mb.showwarning("No selection", "Please select a tool to craft.")

    # buttons for each tool
    craftbutton = Button(temproot, text='Craft selected item', command=craft_with_check)
    craftbutton.grid(row=0, column=0, sticky='nsew')

def getfortune(toolname):
    # Retrieve the fortune value from the tool data
    tool_info = tool_data.get(toolname)
    if tool_info:
        return tool_info['fortune']
    return 0  # Default to 0 if the tool doesn't exist

def getrollcd(toolname):
    tool_info = tool_data.get(toolname)
    if tool_info:
        return tool_info['rollcd']
    return 1000

def equiptool(name):
    if not name:  # If no tool is selected, do nothing
        mb.showwarning("No selection", "Please select a tool to equip.")
        return

    temproot.destroy()
    disablebuttons()

    print('\n*DEBUG*')
    print(f'Equipping {name}...')

    plr.pickaxe = name
    plr.reevaluate()  # This updates the fortune and rollcd based on the equipped pickaxe

    mb.showinfo('', f'{name} has been equipped.')

    enablebuttons()

def toolmenu():
    disablebuttons()

    global temproot
    temproot = Toplevel()
    temproot.title('Tools')
    temproot.protocol('WM_DELETE_WINDOW', lambda: (enablebuttons(), temproot.destroy()))

    # list
    toolslist = Listbox(temproot, selectmode=BROWSE, width=50, height=25)
    toolslist.grid(row=0, column=1)

    for item in tools:
        toolslist.insert(END, item)

    # buttons
    equipbuttn = Button(temproot, text='Equip selected tool', command=lambda: equiptool(toolslist.get(toolslist.curselection()) if toolslist.curselection() else None))
    equipbuttn.grid(row=0, column=0, sticky='nsew')


def showstats():
    disablebuttons()

    temproot = Toplevel()
    temproot.title('Player Statistics')
    temproot.protocol('WM_DELETE_WINDOW', lambda: (enablebuttons(), temproot.destroy()))

    row = 0
    for attribute in plr.getattr():
        attribute_value = getattr(plr, attribute, "Unknown")
        thing = Label(temproot, text=f'{attribute.capitalize()}: {attribute_value}', font=('Sans', 25, 'bold'), pady=20)
        thing.grid(row=row, column=0)
        row += 1
    
    sendStats = Button(temproot, text='Send player stats to server...', command=statsCheck)
    sendStats.grid(row=row, column=0)

def descviewable(name, desc):
    if name in tools:
        return f'\nDescription: {desc}'
    return ''

def displaystats(name):
    if not name:  # If no tool is selected, do nothing
        mb.showwarning("No selection", "Please select a tool first.")
        return

    temproot.destroy()

    target = tool_data[name]
    costs = tool_data[name]['requirements']
    requir = ', '.join([f'{item}: {costs[item]}' for item in costs])
    fortun = target['fortune']
    sped = target['rollcd']
    desc = target['description']

    mb.showinfo(name, f'Cost to craft: {requir}\nFortune: {fortun}\nRoll Cooldown: {sped}{descviewable(name, desc)}')
    enablebuttons()

def showpickstats():
    disablebuttons()

    global temproot
    temproot = Toplevel()
    temproot.title('Crafting Menu')
    temproot.protocol('WM_DELETE_WINDOW', lambda: (enablebuttons(), temproot.destroy()))

    picks = Listbox(temproot, selectmode=BROWSE, width=50, height=25)
    for tool_name in tool_data:
        picks.insert(END, tool_name)

    picks.grid(row=0, column=1)

    # Check if an item is selected before passing to displaystats
    showinfobutton = Button(temproot, text='Show pickaxe info', command=lambda: displaystats(picks.get(picks.curselection()) if picks.curselection() else None))
    showinfobutton.grid(row=0, column=0, sticky='nsew')

def autorollswitch():
    global autoroll
    global autorolling

    if plr.rolls < 500:
        mb.showwarning('Requirement not met', f'You need {500 - plr.rolls} more rolls to use auto roll')
    else:
        if not autorolling:
            autoroll.config(fg='green')
            additem()
        else:
            autoroll.config(fg='red')

        autorolling = not autorolling

# data
autorolling = False
buttonstodisable = []

items = [key for key in resources['index'].keys()]
weights = [val for val in resources['index'].values()]

inventory = [stack(item, value) for item, value in data['inventory'].items()]
tools = data['tools']

# main program
root = Tk()
root.title('Mining RNG')

displayinv = Listbox(root, selectmode=BROWSE, width=30, height=15, font=('Sans', 12))
displayinv.grid(row=1, column=1, rowspan=6)

updatebox()

# buttons
roll = Button(root, text='Roll', font=('Sans', 17), command=additem)
roll.grid(row=6, column=0, columnspan=2, sticky='nsew')
buttonstodisable.append(roll)

autoroll = Button(root, text='Auto Roll', font=('Sans', 17), fg='red', command=autorollswitch)
autoroll.grid(row=7, column=0, columnspan=2, sticky='nsew')
buttonstodisable.append(autoroll)

craft = Button(root, text='Craft', command=craftmenu)
craft.grid(row=1, column=0, sticky='nsew')
buttonstodisable.append(craft)

equip = Button(root, text='Equip', command=toolmenu)
equip.grid(row=2, column=0, sticky='nsew')
buttonstodisable.append(equip)

stats = Button(root, text='Stats', command=showstats)
stats.grid(row=3, column=0, sticky='nsew')
buttonstodisable.append(stats)

pickinfo = Button(root, text='Pickaxe Info', command=showpickstats)
pickinfo.grid(row=4, column=0, sticky='nsew')
buttonstodisable.append(pickinfo)

counter = Label(root, text=f'Total Rolls: {plr.rolls}')
counter.grid(row=5, column=0)

notif = Label(root, font=('Sans', 25))
notif.grid(row=0, column=0, columnspan=2, sticky='nsew')

try:
    root.mainloop()
except Exception as e:
    print(f'Ending program, exception {e} detected')
    
saveprogram()
