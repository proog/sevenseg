# sevenseg

Display a string on a 4-digit 7-segment display connected to your Raspberry Pi.

Based on [this guide and kit by RasPi.TV](http://raspi.tv/2015/how-to-drive-a-7-segment-display-directly-on-raspberry-pi-in-python) for a common cathode, 4-digit 7-segment display, and uses the same wiring (as seen in `pinouts.png`).

The program in the guide is nice but doesn't handle strings longer than the display. This (fairly ugly) modification does, by moving the string left by one character every ~500 ms. It looks okay.

To get started, run `pipenv install`. It will install [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) to interface with the Pi's general purpose IO. Note that this will only work on the Raspberry Pi or similar.
