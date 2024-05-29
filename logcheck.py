logs=[]
suborder={
    "Start subscriber":0,
    "Got ID from fastapi app":1,
    "Connection to fastapi app failed":1,
    "Created client":2,
    "Cannot create client":2,
    "Connecting to broker:":3,
    "Connected to broker":4,
    "Cannot connect to broker":4,
    "Subcribing":5,
    "Received message":6,
    "User stopped script":6,
    "Disconnected":7}
puborder={
    "Start publisher":0,
    "Got ID from fastapi app":1,
    "Connection to fastapi app failed":1,
    "Created client":2,
    "Cannot create client":2,
    "Connecting to broker:":3,
    "Connected to broker":4,
    "Cannot connect to broker":4,
    "Publishing":5,
    "Published: ":6,
    "Script stopped by user":6,
    "Client disconnected":7,
    "Publisher stopped":8}
fstorder={
    "Start FastApi App":0,
    "Someone connected":1,
    "Id created":2}
def getWeight(logdict,string):
    weight=-1
    for i in logdict:
        if i in string:
            weight=logdict[i]
    return weight
with open ("my_app.log",'r') as file:
    logs=file.readlines()
def Checklogs(logdict,logs,typelog):
    count=-1
    for i in logs:
        divstr=i.split(" - ")
        if divstr[2]==typelog:
            if count>getWeight(logdict, divstr[4]):
                print("Incorrect order of "+typelog+": "+i)
            count=getWeight(logdict, divstr[4])
Checklogs(suborder,logs,"subscriber_logger")
Checklogs(puborder,logs,"publisher_logger")
Checklogs(fstorder,logs,"fastapiapp_logger")
