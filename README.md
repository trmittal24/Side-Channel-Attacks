# Side Channel Attacks

This repo contains all the codes uploaded on Arduino for power analysis and all the python codes used to process the power traces.
You can watch the video of live demo [here].

  - ### Basic_Operations.ino
    This contains the arduino code performing different operations in loop so that the varied power consumption is visible.

  - ### Transmit
    Contains code for the transmitting Arduino.

  - ### Receive
    Contains code for the receiving Arduino.
 
  - ### mod_expo
    This contains all the captured traces (.mat files) from the Oscilloscope using KeySight BenchVue software. The file name corresponds to the key used for the particular power trace. 

    **generate_cheats**
    It generates the features from all the traces and saves it in *dpa.mat*.
    
    **processing**
    It uses the features extracted to determine the key of the power trace. Pass the required *.mat* file as an argument to the command. 

  - ### UART_trace
    Contains the encrypted UART data snooped from the secure communication channel saved in *.mat* files.

    **decrypt**
    Will decode the acquired UART data to give the cipher text. Pass the required *.mat* file as an argument to the command.
    
Use the key obtained from processing.py along with ciphertext to get back the message.


[here]: https://youtu.be/rZ0nI8NSrhM