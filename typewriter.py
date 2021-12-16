import sys, time

message = "please enter your name: "


def typewriter(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()

        if char != "\n":
            time.sleep(0.05)
        else:
            time.sleep(1)


def type_input(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)
    return input()


name = type_input(message)

typewriter("nice to meet you " + name)