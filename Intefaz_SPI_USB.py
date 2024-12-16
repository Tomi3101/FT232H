from pyftdi.spi import SpiController
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

spi = SpiController(cs_count=2)
spi.configure('ftdi://ftdi:232h/1')
slave = spi.get_port(cs=1, freq=1E6, mode=2)

# Initialize arrays
x = np.arange(0, 1000)  # x initially contains values from 0 to 100
y = np.random.randint(0, 2, 1000)  # Random initial y values

# Create a figure and axis for plotting
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

# Set plot limits
ax.set_xlim(0, 1000)
ax.set_ylim(0, 4500)

def uDelay():
    j=0
    while j<=5000:
        j+=1

def combine_to_32bit(a, b, c, d):
    if not all(0 <= x < 256 for x in [a, b, c, d]):
        raise ValueError("All inputs must be 8-bit integers (0-255).")
    
    # Combine the integers using bitwise shifts and OR
    result = (a << 24) | (b << 16) | (c << 8) | d
    return result

# Function to initialize the plot
def init():
    line.set_data(x, y)  # Start with the initial data
    return line,

# Function to update the plot
def update(frame):
    global x, y  # Declare x and y as global variables
    global read_buf_0,read_buf_1 #,read_buf_2,read_buf_3
    # Shift x and y axis to the left
    x = np.roll(x, 1)
    
    # Update the last element with new values and shif arrays to the left
    i=0
    while i<=998: 
        x[i] = x[i+1]
        y[i] = y[i+1]
        i += 1
    
    x[999]=x[999]+1

    #Comunicacion SPI 8bit
    '''
    read_buf=slave.read(2)
    y[999]=ord(read_buf)
    #'''
    
    #Comunicacion SPI 16bit (f=1MHz anda muy bien)
    #'''
    read_buf=slave.read(2)
    y[999]=combine_to_32bit(0, 0, read_buf[1], read_buf[0])
    #'''


    #Comunicacion SPI 32bit (No probado)
    '''
    global y_ff
    read_buf_3 = ord(slave.read(1))
    read_buf_2 = ord(slave.read(1))
    read_buf_1 = ord(slave.read(1))
    read_buf_0 = ord(slave.read(1))
    
    y_ff=combine_to_32bit(read_buf_3, read_buf_2, read_buf_1, read_buf_0)

    if(y_ff<4500):
        y[999]=y_ff
    else:
        y[999]=y_ff
        #y[999]=y[998]
    #'''
    
    # Update the line data
    line.set_data(x, y)
    return line,

# Create an animation that updates the plot
ani = FuncAnimation(fig, update, frames=100, init_func=init, blit=True, interval=0.1)

# Display the plot
plt.show()


