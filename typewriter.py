import sys, time

text = "It's kind of hard bein' Snoop D-O-double-G... But I, somehow, some way... Keep comin' up with funky ass shit like every single day... May I, kick a little something for the Gs (yeah)... And, make a few ends as I breeze, through... Two in the mornin' and the partys still jumpin'... 'Cause my momma ain't home"

def typewriter(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()

        if char != "\n":
            time.sleep(0.05)
        else:
            time.sleep(0.05)

typewriter(text)