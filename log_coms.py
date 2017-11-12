from ciscosparkapi import CiscoSparkAPI

api = CiscoSparkAPI("MGRhZjcxMjktMTg0MS00NzU5LTg1MmQtMmE4ZGNjNWMxMDdkZjA2MzliMjMtNjYy") # My User code as Patient

log_feed_id = "Y2lzY29zcGFyazovL3VzL1JPT00vYjBjODQ0ZDAtYzc1Mi0xMWU3LWE5NjQtYTkwNzc5MjFhYmYx" # where I publish my triggers

DRINKING = 0
SMILING = 1
SLEEPING = 2
EATING = 3

#output = "DRINKING"
#output = "SMILING"
#output = "SLEEPING"
#output = "EATING"

# Post a message to the new room, and upload a file
last = []
def testStatus(output):
    global last
    '''
    if last == output: # and last[SLEEPING]:
        print(last)
        print(output)
        print('was speeping')
        return
    '''

    if output[DRINKING] == True:
        api.messages.create(log_feed_id, text="Grandpa is drinking.",
                            files=["imgs/drinking.png"])

    elif output[SMILING] == True:
        api.messages.create(log_feed_id, text="Grandpa is smiling.",
                            files=["imgs/smiling.png"])

    elif output[SLEEPING] == True:
        api.messages.create(log_feed_id, text="Grandpa is sleeping.",
                            files=["imgs/sleeping.png"])

    elif output[EATING] == True:
        api.messages.create(log_feed_id, text="Grandpa is eating.",
                            files=["imgs/eating.png"])
    else:
        pass

    last = output
