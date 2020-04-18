import time
import sys

done = False
def loading():
    chars = "/—\|"
    for char in chars:
        sys.stdout.write('\r'+'loading...'+char)
        time.sleep(.3)
        sys.stdout.flush()

#artwork from https://www.asciiart.eu/television/futurama
def welcome():
    print("""
      _________________________________
 |.--------_--_------------_--__--.|
 ||             HELLO             ||
 ;;        PRIMITIVE BEING        :|
((_(-,-----------.-.----------.-.)`)
 \__ )        ,'     `.        \ _/
 :  :        |_________|       :  :
 |-'|       ,'-.-.--.-.`.      |`-|
 |_.|      (( (*  )(*  )))     |._|
 |  |       `.-`-'--`-'.'      |  |
 |-'|        | ,-.-.-. |       |._|
 |  |        |(|-|-|-|)|       |  |
 :,':        |_`-'-'-'_|       ;`.;
  \  \     ,'           `.    /._/
   \/ `._ /_______________\_,'  /
    \  / :   ___________   : \,'
     `.| |  |  WELCOME  |  |,'
       `.|  |    TO     |  |
         |  | MY STORE! |  |
         """)
