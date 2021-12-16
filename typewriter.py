import sys, time

text = "I wanna be adopted my michael jordan"

def typewriter(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()

        if char != "\n":
            time.sleep(0.05)
        else:
            time.sleep(0.05)

typewriter(text)