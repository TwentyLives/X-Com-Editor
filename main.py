#allows for easier UX
import os

# grabs next 2 bytes of given location
def u16le(b, off):
    return b[off] | (b[off+1] << 8)

# making sure user had the correct file location
def fileTest(path):
    print(f"Trying to open: {path}")
    try:
        with open(path, "rb") as f:
            data = f.read()
            print(f"Succesfully opened: {path}")
            return True
    except FileNotFoundError:
        print(f"Error: {path} not found.")
        return False
    except PermissionError:
        print("Error: Permission denied.")
        return False
    except Exception as e:
        print(f"Error opening file: {e}")
        return False

def braveryDecode(code):
    return 110 - (code*10)

# list every soldier that has a name
def listSoldiers():
    if not fileTest(mainFile):
        return
    with open(mainFile, "rb") as f:
        while True:
            soldier = f.read(structLen)
            if len(soldier) < structLen:
                break
            
            if chosenGame == "X-COM: TFTD":
                rank = soldier[0x0A] | (soldier[0x0B] << 8)
            else:
                rank = soldier[0x00] | (soldier[0x01] << 8)
            
            if rank != 0xFFFF:
                if chosenGame == "X-COM: TFTD":
                    name = soldier[0x23:0x23+27].split(b'\x00')[0].decode("ascii", errors="ignore").strip()
                    rank = u16le(soldier, 0x0A)
                    
                    if rank == 0x0000:
                        rank = "Seaman"
                    elif rank == 0x0001:
                        rank = "Able Seaman"
                    elif rank == 0x0002:
                        rank = "Ensign"
                    elif rank == 0x0003:
                        rank = "Lieutenant"
                    elif rank == 0x0004:
                        rank = "Commander"
                    elif rank == 0x0005:
                        rank = "Captain"
                    code = soldier[0x40]
                    bravery = braveryDecode(code)
                    print("---- Soldier ----")
                    print(f"Name: {name}")
                    print(f"Rank: {rank}")
                    print(f"Missions: {u16le(soldier, 0x12)}")
                    print(f"Kills: {u16le(soldier, 0x0E)}")

                    print()

                    print("Initial stats:")
                    print(f"  Time Units: {soldier[0x1A]}")
                    print(f"  Stamina: {soldier[0x1C]}")
                    print(f"  Health: {soldier[0x1B]}")
                    print(f"  Bravery: {soldier[0x40]}")
                    print(f"  Displayed Bravery: {bravery}")
                    print(f"  Reactions: {soldier[0x45]}")
                    print(f"  Firing Accuracy: {soldier[0x21]}")
                    print(f"  Throwing Accuracy: {soldier[0x1D]}")
                    print(f"  Strength: {soldier[0x22]}")

                    print()
                    print("Psionics:")
                    print(f"  {psiTerm} skill: {soldier[0x41]}")
                    print(f"  {psiTerm} strength: {soldier[0x43]}")

                    print("-----------------\n")
                else:
                    name = soldier[0x10:0x10+25].split(b'\x00')[0].decode("ascii", errors="ignore").strip()
                    rank = u16le(soldier, 0x00)
                    if rank == 0x0000:
                        rank = "Rookie"
                    elif rank == 0x0001:
                        rank = "Squaddie"
                    elif rank == 0x0002:
                        rank = "Sergeant"
                    elif rank == 0x0003:
                        rank = "Captain"
                    elif rank == 0x0004:
                        rank = "Colonel "
                    elif rank == 0x0005:
                        rank = "Commander"
                    code = soldier[0x34]
                    bravery = braveryDecode(code)
                    print("---- Soldier ----")
                    print(f"Name: {name}")
                    print(f"Rank: {rank}")
                    print(f"Missions: {u16le(soldier, 0x08)}")
                    print(f"Kills: {u16le(soldier, 0x0A)}")

                    print()

                    print("Initial stats:")
                    print(f"  Time Units: {soldier[0x2A]}")
                    print(f"  Stamina: {soldier[0x2C]}")
                    print(f"  Health: {soldier[0x2B]}")
                    print(f"  Bravery: {soldier[0x34]}")
                    print(f"  Displayed Bravery: {bravery}")
                    print(f"  Reactions: {soldier[0x2D]}")
                    print(f"  Firing Accuracy: {soldier[0x2F]}")
                    print(f"  Throwing Accuracy: {soldier[0x30]}")
                    print(f"  Strength: {soldier[0x2E]}")

                    print()
                    print("Psionics:")
                    print(f"  {psiTerm} skill: {soldier[0x33]}")
                    print(f"  {psiTerm} strength: {soldier[0x32]}")

                    print("-----------------\n")

                



#stat locaiton list for TFTD
STAT_OFFSETS = {
    1: (0x1A, "Time Units"),
    2: (0x1C, "Stamina"),
    3: (0x1B, "Health"),
    4: (0x40, "Bravery (CODE 0-11)"), 
    5: (0x45, "Reactions"),
    6: (0x21, "Firing Accuracy"),
    7: (0x1D, "Throwing Accuracy"),
    8: (0x22, "Strength"),
    9: (0x41, "MC skill"),
    10: (0x43, "MC strength")
}

#stat locaiton list for Enemy Unknown
STAT_OFFSETS_EU = {
    1:  (0x2A, "Time Units"),
    2:  (0x2C, "Stamina/Energy"),
    3:  (0x2B, "Health"),
    4:  (0x34, "Bravery (CODE 0-11)"), 
    5:  (0x2D, "Reactions"),
    6:  (0x2F, "Firing Accuracy"),
    7:  (0x30, "Throwing Accuracy"),
    8:  (0x2E, "Strength"),
    9:  (0x33, "Psi Skill"),  
    10: (0x32, "Psi Strength "), 
}

#function to write to the soldier file
def writeSoldier(record_start, offset, new_val):
    try:
        with open(mainFile, "r+b") as f:
            f.seek(record_start + offset)
            f.write(bytes([new_val]))
            f.flush()
        return True
    except Exception as e:
        print(f"Failed to write: {e}")
        return False

#edit a single soldier
def editSoldier():
    if not fileTest(mainFile):
        return

    targetName = input("Input the name of the Soldier (Case Sensitive): ").strip()
    print(f"Looking for {targetName}")

    found = False
    recordStart = None
    soldier = None

    with open(mainFile, "rb") as f:
        while True:
            recStart = f.tell()
            soldier = f.read(structLen)
            if len(soldier) < structLen:
                break

            if chosenGame == "X-COM: TFTD":
                rank = soldier[0x0A] | (soldier[0x0B] << 8)
            else:
                rank = soldier[0x00] | (soldier[0x01] << 8)
            
            if rank == 0xFFFF:
                continue
            
            if chosenGame == "X-COM: TFTD":
                name = soldier[0x23:0x23+27].split(b'\x00')[0].decode("ascii", errors="ignore").strip()
            else:
                name = soldier[0x10:0x10+25].split(b'\x00')[0].decode("ascii", errors="ignore").strip()
            
            if name == targetName:
                found = True
                recordStart = recStart
                break

    if not found:
        print("Soldier not found (must match exactly)")
        input("Press Enter to continue")
        return

    while True:
        print("\n--Character Editor--")
        print(f"Currently editing: {targetName}")
        print("1. Time Units")
        print("2. Stamina")
        print("3. Health")
        print("4. Bravery")
        print("5. Reactions")
        print("6. Firing Accuracy")
        print("7. Throwing Accuracy")
        print("8. Strength")
        print (f"9. {psiTerm} skill")
        print (f"10. {psiTerm} strength")
        print("0. Exit editor")

        usersInput = input("--type a number and press enter to choose a command-- ").strip()

        try:
            usersInput = int(usersInput)
        except ValueError:
            print("Invalid input (must be a number)")
            input("Press Enter to continue")
            continue

        if usersInput == 0:
            print("Exiting")
            input("Press Enter to continue")
            return

        if usersInput not in statsActive:
            print("Invalid input")
            input("Press Enter to continue")
            continue

        offset, label = statsActive[usersInput]
        with open(mainFile, "rb") as f:
            f.seek(recordStart + offset)
            current = f.read(1)[0]

        print(f"\n{label}")
        print(f"Current value: {current}")

        try:
            new_val = int(input("Enter new value (0-255): ").strip())
            if not (0 <= new_val <= 255):
                raise ValueError
        except ValueError:
            print("Invalid value")
            input("Press Enter to continue")
            continue

        confirm = input(f"Confirm change {label}: {current} -> {new_val}? (y/n): ").strip().lower()
        if confirm != "y":
            print("Canceled.")
            input("Press Enter to continue")
            continue

        if writeSoldier(recordStart, offset, new_val):
            print("Saved")
        else:
            print("Save failed")

        input("Press Enter to continue")

#have user select where SOLDIER.DAT is
def chooseFile():
    global mainFile

    print("Input the directory containing SOLDIER.DAT")
    print(r"Example - if 'C:\Users\<username>\Downloads\SOLDIER.DAT' then input 'C:\Users\<username>\Downloads\'")

    userInput = input("Directory: ").strip().strip('"')
    mainFile = findFile(userInput, "SOLDIER.DAT")

    if mainFile == None:
        print(f"SOLDIER.DAT was not found in {userInput}")
        input("Press Enter to continue")
        return
    
    print(f"Saved as: {mainFile}")
    input("Press Enter to continue")

#makes a stat to every single soldier possible for the given user input
def allStatChange():
    try:
        newVal = int(input("Enter new value (0-255): ").strip())
        if not (0 <= newVal <= 255):
            raise ValueError
    except ValueError:
        print("Invalid value")
        input("Press Enter to continue")
        return False
    
    confirm = input(f"Confirm change all stats to: {newVal}? (y/n): ").strip().lower()
    if confirm != "y":
        print("Canceled.")
        input("Press Enter to continue")
        return False
    
    with open(mainFile, "rb") as f:
            while True:
                recStart = f.tell()
                soldier = f.read(structLen)
                if len(soldier) < structLen:
                    break
                if chosenGame == "X-COM: TFTD":
                    rank = soldier[0x0A] | (soldier[0x0B] << 8)
                else:
                    rank = soldier[0x00] | (soldier[0x01] << 8)
                
                if rank == 0xFFFF:
                    continue
                else:
                    for offset, label in statsActive.values():
                        if "Bravery" in label:
                            continue
                        if chosenGame == "X-COM: TFTD":
                            name = soldier[0x23:0x23+27].split(b'\x00')[0].decode("ascii", errors="ignore").strip()
                        else:
                            name = soldier[0x10:0x10+25].split(b'\x00')[0].decode("ascii", errors="ignore").strip()
                        recordStart = recStart
                        if writeSoldier(recordStart, offset, newVal):
                            print(f"Saved to {newVal} to {name} for {label}")
                        else:
                            print(f"Save failed to {name} for {label}")
                
            return True

                



#Change all alive soldiers
def batchChange():
    if not fileTest(mainFile):
        return
    
    while True:
        print("\n--Character Editor--")
        print("Currently editing all soldiers")
        print("1. Time Units")
        print("2. Stamina")
        print("3. Health")
        print("4. Bravery")
        print("5. Reactions")
        print("6. Firing Accuracy")
        print("7. Throwing Accuracy")
        print("8. Strength")
        print(f"9. {psiTerm} skill")
        print(f"10. {psiTerm} strength")
        print("11. Change all stats (except Bravery) to a value")
        print("0. Exit editor")

        usersInput = input("--type a number and press enter to choose a command-- ").strip()

        try:
            usersInput = int(usersInput)
        except ValueError:
            print("Invalid input (must be a number)")
            input("Press Enter to continue")
            continue

        if usersInput == 0:
            print("Exiting")
            input("Press Enter to continue")
            return
        
        if usersInput == 11:
            if allStatChange():
                print("Saved changest to all soldiers")
                input("Press Enter to continue")
                return
            else:
                print("Save failed")
                input("Press Enter to continue")
                return

        if usersInput not in statsActive:
            print("Invalid input")
            input("Press Enter to continue")
            continue

        offset, label = statsActive[usersInput]

        try:
            newVal = int(input("Enter new value (0-255): ").strip())
            if not (0 <= newVal <= 255):
                raise ValueError
        except ValueError:
            print("Invalid value")
            input("Press Enter to continue")
            continue

        confirm = input(f"Confirm change {label}: {newVal}? (y/n): ").strip().lower()
        if confirm != "y":
            print("Canceled.")
            input("Press Enter to continue")
            continue

        with open(mainFile, "rb") as f:
            while True:
                recStart = f.tell()
                soldier = f.read(structLen)
                if len(soldier) < structLen:
                    break
                if chosenGame == "X-COM: TFTD":
                    rank = soldier[0x0A] | (soldier[0x0B] << 8)
                else:
                    rank = soldier[0x00] | (soldier[0x01] << 8)
                
                if rank == 0xFFFF:
                    continue
                else:
                    if chosenGame == "X-COM: TFTD":
                        name = soldier[0x23:0x23+27].split(b'\x00')[0].decode("ascii", errors="ignore").strip()
                    else:
                        name = soldier[0x10:0x10+25].split(b'\x00')[0].decode("ascii", errors="ignore").strip()
                    recordStart = recStart
                    if writeSoldier(recordStart, offset, newVal):
                        print(f"Saved to {name}")
                    else:
                        print("Save failed")

        input("Press Enter to continue")


#Choose between modifying TFTD and Enemy Unknown
def chooseGame():
    global chosenGame 
    global psiTerm
    global structLen
    global statsActive
    global structLenRef

    print("\n--Game Chooser--")
    print(f"Current choice: {chosenGame}")
    print("1. X-COM: TFTD")
    print("2. X-COM: Enemy Unknown")
    choice = input("Choose a game: ").strip()
    try:
        choice = int(choice)
    except ValueError:
        print("Invalid input (must be a number).")
        input("Press Enter to continue")
        return
    
    if choice == 1:
        chosenGame = "X-COM: TFTD"
        psiTerm = "MC"
        structLen = 70
        statsActive =  STAT_OFFSETS
        structLenRef = 132
    elif choice == 2:
        chosenGame = "X-COM: Enemy Unknown"
        psiTerm = "Psi"
        structLen = 68
        statsActive =  STAT_OFFSETS_EU
        structLenRef = 124
    else:
        print("Invalid input") 
        input("Press Enter to continue")  
    
    print(f"Chosen: {chosenGame}")
    input("Press Enter to continue")

#have user select where UNITPOS.DAT is
def definePosFile():
    global posFile

    print("Input the directory containing UNITPOS.DAT")
    print(r"Example - if 'C:\Users\<username>\Downloads\UNITPOS.DAT' then input 'C:\Users\<username>\Downloads\'")

    userInput = input("Directory: ").strip().strip('"')
    posFile = findFile(userInput, "UNITPOS.DAT")

    if posFile == None:
        print(f"UNITPOS.DAT was not found in {userInput}")
        input("Press Enter to continue")
        return
    
    print(f"Saved as: {posFile}")
    input("Press Enter to continue")

#have user select where UNITREF.DAT is
def defineRefFile():
    global refFile

    print("Input the directory containing UNITREF.DAT")
    print(r"Example - if 'C:\Users\<username>\Downloads\UNITREF.DAT' then input 'C:\Users\<username>\Downloads\'")

    userInput = input("Directory: ").strip().strip('"')
    refFile = findFile(userInput, "UNITREF.DAT")

    if refFile == None:
        print(f"UNITREF.DAT was not found in {userInput}")
        input("Press Enter to continue")
        return
    
    print(f"Saved as: {refFile}")
    input("Press Enter to continue")

#finds target file in a given directory path - dfs
def findFile(folder, targ):
    folder = os.path.normpath(folder)
    if not os.path.isdir(folder):
        return None

    for root, dirs, files in os.walk(folder):
        if targ in files:
            return os.path.join(root, targ)
    return None

#function to write to the given file
def writeUnit(path, record_start, offset, new_val):
    try:
        with open(path, "r+b") as f:
            f.seek(record_start + offset)
            f.write(bytes([new_val]))
            f.flush()
        return True
    except Exception as e:
        print(f"Failed to write: {e}")
        return False

#Opens up both files and kills the enemies
def killEnemies():
    if not fileTest(posFile) or not fileTest(refFile):
        return

    with open(posFile, "rb") as f:
        while True:
            recStart = f.tell()
            unit = f.read(14)
            if len(unit) < 14:
                break

            if unit[0x09] != 1:
                continue
            else:
                deadFlag = unit[0x0A] & 0xFD
                writeUnit(posFile, recStart, 0x0A, deadFlag)

    with open(refFile, "rb") as f:
        while True:
            recStart = f.tell()
            unit = f.read(structLenRef)

            if len(unit) < structLenRef:
                break
            
            if unit[0x00] < 4 or unit[0x00] > 14:
                continue
            else:
                writeUnit(refFile, recStart, 0x0D, 0)

    print("Done killing all soldiers")
    input("Press Enter to continue")
    return



#Menu to kill enemies
def killEnemiesMenu():
    while True:
        print("--Enemy Killer--")
        print("   PLEASE DEFINE FILE AND GAME BEFORE USE")
        print("   to define the game please use the main menu")
        print("1.   Kill all enemies in selected mission")
        print("2.   Define UNITPOS.DAT location")
        print("3.   Define UNITREF.DAT location")
        print("0.   Exit enemy killer")
        userInput = input("--type a number and press enter to choose a command-- ").strip()

        try:
            userInput = int(userInput)
        except ValueError:
            print("Invalid input (must be a number).")
            input("Press Enter to continue")
            return
        
        if userInput == 1:
            killEnemies()
        elif userInput == 2:
            definePosFile()
        elif userInput == 3:
            defineRefFile()
        elif userInput == 0:
            print("Exiting")
            input("Press Enter to continue")
            return
        else:
            print("Invalid input") 
            input("Press Enter to continue")  
    

# variables
run = 1
userInput = 0
chosenGame = "X-COM: TFTD"
psiTerm = "MC"
structLen = 70
statsActive =  STAT_OFFSETS
structLenRef = 132
try:
    # main
    while run == 1:
        print("--X-COM Editor--")
        print("   PLEASE DEFINE FILE AND GAME BEFORE USE")
        print("1. list all current soldiers")
        print("2. edit a specific soldier")
        print("3. edit all soldiers")
        print("4. kill all enemies in a mission")
        print("5. choose between TFTD or EU to edit")
        print("6. define SOLDIER.DAT location")
        print("0. exit program")
        userInput = input("--type a number and press enter to chooose a command--")

        try:
            userInput = int(userInput)
        except ValueError:
            print("Invalid input (must be a number).")
            input("Press Enter to continue")
            continue



        if userInput == 1:
            listSoldiers()
        elif userInput == 2:
            editSoldier()
        elif userInput == 3:
            batchChange()
        elif userInput == 4:
            killEnemiesMenu()
        elif userInput == 5:
            chooseGame()
        elif userInput == 6:
            chooseFile()
        elif userInput == 0:
            print("Exiting") 
            input("Press Enter to continue")  
            run = 0
        else:
            print("Invalid input") 
            input("Press Enter to continue")   

except Exception as e:
    print("Fatal error:")
    print(e)
    input("Press Enter to exit")
