import serial
from threading import Event, Thread
from time import sleep

# Serial configuration
serialPort = serial.Serial('/dev/ttyUSB0')
serialPort.baudrate = 9600

readMessagesEvent = Event()

def readMessages():
    while not readMessagesEvent.is_set():
        try:
            messages = serialPort.readline()
            print('Message received: ' + messages.decode("utf-8"))
        except:
            print('Serial port was closed!')

    print('Read messages thread closing, exiting program...')

def menu():
    while True:
        print('\n1 - Send a message to serial port')
        print('2 - Close connection with serial port\n')
        op = input().split() 
        if op[0] == '1':
            # Write a message
            print('Please write a message to be send:')
            message = input()
            print('\nMessage sent: ' + message)
            serialPort.write(str.encode(message))
        if op[0] == '2': 
            # Close serial connection
            serialPort.close()
            
            # Kill read messages thread
            readMessagesEvent.set()
            break

if __name__ == "__main__":
    # Try to connect to the serial port
    if (serialPort.is_open == False):
        serialPort.open()
        print(f'Connected to: {serialPort.name} {serialPort.is_open}')
        
        # Start read messages thread
        Thread(target=readMessages).start()
    elif (serialPort.is_open == True):
        print(f'Serial port {serialPort.name} already opened!')
        
        # Start read messages thread
        Thread(target=readMessages).start()
    else:
        print(f'Error connecting to: {serialPort.name}')
    
    # Loads the menu
    menu()

