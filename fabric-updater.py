import os, glob, shutil, sys
if os.name == 'nt':
    osExt = 'bat'
else:
    osExt = 'sh'
def backup(bkup):
    if bkup == "Y":
        dst = input("Where would you like the files backed up too? ")
        try:
            shutil.copyfile(glob.glob('*'), dst)
            print("File copied successfully.")
        except shutil.SameFileError:
            print("Source and destination represents the same file.")
            c = input("Would you like to continue instillation? ").capitalize()
            if c != 'Y':
                sys.exit()
        except IsADirectoryError:
            print("Destination is a directory.")
            c = input("Would you like to continue instillation? ").capitalize()
            if c != 'Y':
                sys.exit()
        except PermissionError:
            print("Permission denied.")
            c = input("Would you like to continue instillation? ").capitalize()
            if c != 'Y':
                sys.exit()
        except:
            print("Unkown error occurred while copying file.")
            c = input("Would you like to continue instillation? ").capitalize()
            if c != 'Y':
                sys.exit()
def install(version, ram, eula, start):
    if version == "L":
        version = input("Enter the path to a local server Jar: ")
    else:
        os.system('curl -OJ https://meta.fabricmc.net/v2/versions/loader/' + version +'/0.14.4/0.10.2/server/jar')
    f = open("start." + osExt, "a")
    f.write("java -Xmx" + ram + " -jar fabric-server-mc." + version + "-loader.0.14.4-launcher.0.10.2.jar nogui")
    f.close()
    f = open("eula.txt", "a")
    f.write("eula=" + eula)
    f.close()
    if start == 'Y':
        os.system('sh start.' + osExt)
def upgrade(version, remV, ram, start):
    if remV == 'Y':
        files = glob.glob('*.jar')
        for f in files:
            os.remove(f)  
    if version == "L":
        version = input("Enter the path to a local server Jar: ")
        f = open("start." + osExt, "w")
        f.write("java -Xmx" + ram + " -jar " + version)
        f.close()
    else:
        os.system('curl -OJ https://meta.fabricmc.net/v2/versions/loader/' + version +'/0.14.4/0.10.2/server/jar')    
        f = open("start." + osExt, "w")
        f.write("java -Xmx" + ram + " -jar fabric-server-mc." + version + "-loader.0.14.4-launcher.0.10.2.jar nogui")
        f.close()
    if len(os.listdir('mods/')) > 0 and start == 'Y': 
        try:
            files = glob.glob('mods/*')
            for f in files:
                os.rename(f + '.jar', f + '.tmp')
        except FileNotFoundError:
            print()
    if start == 'Y':
        os.system('sh start.' + osExt)
upIn = input("(I)nstall or (U)pgrade a minecraft server ").capitalize()
if upIn == 'I':
    version = input("Enter a valid minecraft version (eg. 1.18.2, 1.17.1): ")
    ram = input("Ram usage (1G, 5G, etc): ")
    eula = input("Validate eula https://minecraft.net/eula (true/false): ")
    if eula == 'true':
        start = input("Start server? ").capitalize()
    else:
        start = ''
    install(version, ram, eula, start)
if upIn == 'U':
    version = input("Enter a valid minecraft version (eg. 1.18.2, 1.17.1): ")
    remV = input("Remove previous server jars? ").capitalize()
    ram = input("Ram usage (1G, 5G, etc.): ")
    bkup = input("Backup current files? ").capitalize()
    backup(bkup)
    start = input("Start server? ").capitalize()
    upgrade(version, remV, ram, start)
if upIn == 'H':
    print("H - shows this message")
