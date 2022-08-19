from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

#Database
class RSA_ALG:

    def Key_generate():

        global keyPair, pubKey

        keyPair = RSA.generate(1024)
        pubKey = keyPair.publickey()
        FileControl.store_pubkey(pubKey)
        FileControl.store_privkey(keyPair)

        #print(keyPair.export_key().decode('utf-8'))

    def encrypt(plaintext):
        #size = len(plaintext)
        pubKey = FileControl.read_pubkey()
        #for x in range (0, size):
        encryptor = PKCS1_OAEP.new(pubKey)
        encrypt_user = encryptor.encrypt(str.encode(plaintext.user))
        encrypt_passwd = encryptor.encrypt(str.encode(plaintext.passwd))
        All_encrypted = (Student(encrypt_user.hex(), encrypt_passwd.hex()))
        #print("Encrypted", All_encrypted.user)
        #print(type(encrypt_user.hex()))
        #print("Encrypted:", binascii.hexlify(encrypted))
        return All_encrypted
    
    def decrypt(ciphertext):
        size = len(ciphertext)
        All_decrypted = []
        keyPair = FileControl.read_privkey()
        #print(keyPair.export_key().decode('utf-8'))
        for x in range (0, size):
            decryptor = PKCS1_OAEP.new(keyPair)
            decrypted_user = decryptor.decrypt(bytes.fromhex(ciphertext[x].user))
            #print(decrypted_user)
            decrypted_passwd = decryptor.decrypt(bytes.fromhex(ciphertext[x].passwd))
            #print(decrypted_passwd)
            All_decrypted.append(Student((decrypted_user.decode('utf-8')).strip(), (decrypted_passwd.decode('utf-8')).strip()))
            #print('Decrypted:', decrypted)
        return All_decrypted

class Build:
    
    def data(mode):

        if (mode != "getall" and mode != "getlists"):
            print("You have no correct right\n")
            return

        All = []
        userlists = []
        All.clear()
        userlists.clear()

        global Login_information

        '''
        ## ADD Yourself using this code
        All.append(Student("108xxxxx", "12345678"))
        '''
        print("There are users: ")
        for i in range (0, len(All)):
            print(All[i].user)
            userlists.append(All[i].user)

        
        if (mode == "getall"): return All
        elif (mode == "getlists"): return userlists
        else: return

class Student:

    def __init__(self, user = None, passwd = None):
        self.user = user
        self.passwd = passwd

class FileControl:

    def read_file():
        All = []
        All.clear()
        f1 = open('pythondatabase.txt', 'r')
        n = 0
        while True:
            line1 = f1.readline()
            line2 = f1.readline()
            if not line2: break 
            n += 1
            line1 = line1.strip() 
            line2 = line2.strip() 
            All.append(Student(line1, line2))
        f1.close
        if (n != 0): return All
        else: return n

    def write_file(All):
        try:
            f2 = open('pythondatabase.txt', 'a')
        except:
            f2 = open('pythondatabase.txt', 'w')
        f2.write(All.user)
        f2.write('\n')
        f2.write(All.passwd)
        f2.write('\n')
        f2.close()
    
    def change_file(i, person):

        file = open("pythondatabase.txt", 'r')
        All_Lines = file.readlines()
        passwd = RSA_ALG.encrypt(person).passwd
        All_Lines[2 * i + 1] = passwd + '\n'
        file = open("pythondatabase.txt", 'w')
        file.writelines(All_Lines)
        file.close()


    def store_privkey(pubKey):
        keyword = "jacky"
        f3 = open('privkey.pem', 'wb')
        privKeyPEM = keyPair.export_key(passphrase=keyword, pkcs=8,
                              protection="scryptAndAES128-CBC")
        f3.write(privKeyPEM)
        f3.close()

    def store_pubkey(pubKey):
        keyword = "jacky"
        f4 = open('pubkey.pem', 'wb')
        pubKeyPEM = pubKey.export_key(passphrase=keyword, pkcs=1,
                              protection="scryptAndAES128-CBC")
        f4.write(pubKeyPEM)
        f4.close()

    def read_privkey():
        keyword = "jacky"
        encodedKey = open("privkey.pem", "rb").read()
        key = RSA.import_key(encodedKey, passphrase=keyword)

        return key

    def read_pubkey():
        keyword = "jacky"
        encodedKey = open("pubkey.pem", "rb").read()
        key = RSA.import_key(encodedKey, passphrase=keyword)

        return key

class Write_and_Export:

    def __init__(self) -> None:
        pass

    def store(self, person):
        #print("Building")
        #FileControl.write_file(Build.data("getall"))

        print("Key Generating...")

        try:
            FileControl.read_pubkey()
            print("Keys do exist")
        except:
            print("Keys dont exist, create one")
            RSA_ALG.Key_generate()

        print("Encrypting...")
        status = FileControl.read_file()
        
        if (status == 0): print("no data in database")

        flag = self.check_exist(person.user)

        if (type(flag) == type(1)):
            print("account is already exist, replacing with new passwd...")
            FileControl.change_file(flag, person)

        elif (flag == False):

            All_encrypted = RSA_ALG.encrypt(person)
            FileControl.write_file(All_encrypted)

    def export(self):
        print("Decrypting...")
        status = FileControl.read_file()
        if (status == 0):
            return None
        else:
            All_decrypted = RSA_ALG.decrypt(status)

        return All_decrypted

    def check_exist(self, ID):
        
        Datas = self.export()

        for i in range(0, len(Datas)):

            if (Datas[i].user == ID):
                print("Is locate at ", i)
                return i

        return False

def run0():
        #print("Building")
        #FileControl.write_file(Build.data("getall"))

        print("Key Generating...")

        try:
            FileControl.read_pubkey()
            print("Keys do exist")
        except:
            print("Keys dont exist, create one")
            RSA_ALG.Key_generate()

        print("Encrypting...")
        status = FileControl.read_file()
        
        if (status == 0): print("no data in database")

        person = Student("10828152", "Psptim53")

        flag = Write_and_Export().check_exist(person.user)

        if (type(flag) == type(1)):
            print("account is already exist, replacing with new passwd...")
            FileControl.change_file(flag, person)

        else:

            All_encrypted = RSA_ALG.encrypt(person)
            FileControl.write_file(All_encrypted)

def run1():
    print("Decrypting...")
    status = FileControl.read_file()
    if (status == 0):
        return None
    else:
        All_decrypted = RSA_ALG.decrypt(status)
    
    #FileControl.write_file(All_decrypted[0])
    return All_decrypted

#run0()
#run1()