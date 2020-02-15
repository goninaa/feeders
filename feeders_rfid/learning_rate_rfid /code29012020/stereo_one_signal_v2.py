import pygame as pg
import time

class stereo:

    def __init__(self, left_signal, right_signal, frequency=22050, size=-16,channels=2, buffer=4096): # 2 channels means stereo
        self.frequency = frequency
        self.size = size
        self.channels = channels
        self.buffer = buffer
        pg.mixer.init(self.frequency, self.size, self.channels, self.buffer) 
        self.left_signal = pg.mixer.Sound(left_signal)
        self.right_signal = pg.mixer.Sound(right_signal)

    def play_left (self): 
        channel1 = pg.mixer.Channel(0) 
        channel1.play(self.left_signal) # plays sound
        channel1.set_volume(1.0, 0.0) # The first argument is the volume of the left speaker and the second is the volume of the right speaker.

    def play_right (self):
        channel2 = pg.mixer.Channel(1)
        channel2.play(self.right_signal) # plays sound
        channel2.set_volume(0.0, 1.0)

    def play_stereo (self):
        channel1 = pg.mixer.Channel(0) 
        channel2 = pg.mixer.Channel(1)
        channel1.play(self.left_signal)
        channel2.play(self.left_signal) # plays sound

    def run (self):
        print ("playing signal")
        # self.play_left()
        # time.sleep (3)
        # self.play_right()
        # time.sleep (3)
        self.play_stereo()


if __name__ == "__main__":

    # st = stereo('left_sig.wav', 'right_sig.wav')
    # st = stereo('learning_rate_rfid /right_sig.wav', 'learning_rate_rfid /left_sig.wav')
    st = stereo('learning_rate_rfid /right_sig.wav', 'learning_rate_rfid /right_sig.wav')
    while True:
        # st = stereo('learning_rate_rfid /right_sig.wav', 'learning_rate_rfid /right_sig.wav')
        st.run()
        
    