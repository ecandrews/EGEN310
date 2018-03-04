import Tkinter as tk
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART, DeviceInformation

ble = Adafruit_BluefruitLE.get_provider()

def launchGUI():
    root = tk.Tk()
    format_win(root)
    buttonFrame = tk.Frame(root)
    buttonFrame.pack(side=tk.TOP)
    infoFrame = tk.Frame(root)
    infoFrame.pack(side=tk.BOTTOM)

    clickedLabel = tk.Label(infoFrame, text="nothing clicked yet")
    clickedLabel.grid(row=0, column=0)
    timerLabel = tk.Label(infoFrame, text="timer")
    timerLabel.grid(row=1, column=0)

    forwardButton = tk.Button(buttonFrame, text="FORWARD", command=lambda: clickedLabel.config(text="forward clicked"))
    forwardButton.grid(row=0, column=1)
    rightButton = tk.Button(buttonFrame, text="RIGHT", command=lambda: clickedLabel.config(text="right button clicked"))
    rightButton.grid(row=1, column=2)
    backwardButton = tk.Button(buttonFrame, text="BACKWARD",
                               command=lambda: clickedLabel.config(text="backwards clicked"))
    backwardButton.grid(row=2, column=1)
    leftButton = tk.Button(buttonFrame, text="LEFT", command=lambda: clickedLabel.config(text="left button clicked"))
    leftButton.grid(row=1, column=0)
    root.mainloop()

def format_win(toplevel):
    toplevel.minsize(width=300, height=100)
    toplevel.update_idletasks()
    width = toplevel.winfo_screenwidth()
    height = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = width/2 - size[0]/2
    y = height/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))


def main():
    ble.clear_cached_data()
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))

    print('Disconnecting any connected UART devices...')
    UART.disconnect_devices()

    print('Searching for UART device...')
    try:
        adapter.start_scan()
        device = UART.find_device()
        if device is None:
            raise RuntimeError('Failed to find UART device!')
    finally:
        adapter.stop_scan()

    print("Connecting to a UART device...")
    device.connect()
    print("Connected to " + device.name + "!")

    # call method to launch gui, implement later
    # getch library for sending stuff
    # launchGUI()

    try:
        print('Discovering services...')
        DeviceInformation.discover(device)
        dis = DeviceInformation(device)

        # Print out the DIS characteristics.
        print('Manufacturer: {0}'.format(dis.manufacturer))
        print('Model: {0}'.format(dis.model))
        print('Serial: {0}'.format(dis.serial))
        print('Hardware Revision: {0}'.format(dis.hw_revision))
        print('Software Revision: {0}'.format(dis.sw_revision))
        print('Firmware Revision: {0}'.format(dis.fw_revision))
        print('System ID: {0}'.format(dis.system_id))
        print('Regulatory Cert: {0}'.format(dis.regulatory_cert))
        print('PnP ID: {0}'.format(dis.pnp_id))
    finally:
        device.disconnect()


ble.initialize()
ble.run_mainloop_with(main)
