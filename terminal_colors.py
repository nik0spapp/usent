####################################################################
# Licence:    Creative Commons (see COPYRIGHT)                     #
# Authors:    Nikolaos Pappas, Georgios Katsimpras                 #
#             {nik0spapp, gkatsimpras}@gmail.com                   # 
# Supervisor: Efstathios stamatatos                                #
#             stamatatos@aegean.gr                                 #
# University of the Aegean                                         #
# Department of Information and Communication Systems Engineering  #
# Information Management Track (MSc)                               #
# Karlovasi, Samos                                                 #
# Greece                                                           #
####################################################################

class Tcolors:
    HEADER = '\033[1;95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[1;92m'
    WARNING = '\033[1;93m'
    W = '\033[1;37m'
    GRAY = W
    BGGRAY = '\033[1;37;40m'
    BG = '\033[1;30;47m' 
    BGH = '\033[1;40;41m' 
    FAIL = '\033[91m'
    RED = '\033[1;91m'
    ENDC = '\033[0m'
    CYAN = '\033[1;36m'
    INF = '\033[1;90m'
    C = ENDC 
    
    ACT = W + "["+RED+"*"+ENDC+W+"]" + C
    PROC = W + "["+OKBLUE+"*"+ENDC+W+"]" + C
    ADD = W + "["+WARNING+"+"+ENDC+W+"]" + C
    RES = W + "["+OKGREEN+"x"+ENDC+W+"]" + C
    INFO = W + "["+OKBLUE+"INFO:"+ENDC+W+"]" + C
    OK = W + "[ "+ OKGREEN + "OK" + ENDC+W+ " ]" + C
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
