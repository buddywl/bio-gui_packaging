"""
Runs on the RPi that is directly connected to the sensor.
This file is designed to run only on the RPi that is directly hooked up to the sensor. If it is run as main, it will just parse your arguments and print the sensor response. To get multiple sensor responses, create an SQM() instance from another program.
"""

import sys
import time
import struct
import argparse
import threading

# module import
import configs_ssh

# device info
device_type = configs_ssh.device_type.replace("_", "-")
device_addr = configs_ssh.device_addr

# debugging and retry settings
DEBUG = configs_ssh.debug
tries = configs_ssh.tries

# LU-specific
LU_BAUD = configs_ssh.LU_BAUD
lu_timeout = configs_ssh.LU_TIMEOUT

# LE-specific
LE_PORT = configs_ssh.LE_PORT
SOCK_BUF = configs_ssh.LE_SOCK_BUF
le_timeout = configs_ssh.LE_TIMEOUT

# text encoding
EOL = configs_ssh.EOL
utf8 = configs_ssh.utf8
hex = configs_ssh.hex

# timing
long_s = configs_ssh.long_s
mid_s = configs_ssh.mid_s
short_s = configs_ssh.short_s


if device_type == "SQM-LE":
    import socket
elif device_type == "SQM-LU":
    import serial


class SQM:
    """Shared methods for SQM devices"""

    def _reset_device(self) -> None:
        """Connection reset"""
        self._close_connection()
        time.sleep(short_s)
        self.start_connection()

    def _clear_buffer(self) -> None:
        """Clears buffer and prints to console"""
        print("Clearing buffer ... | ", end="", file=sys.stderr)
        print(self._read_buffer(), "| ... DONE", file=sys.stderr)

    def send_and_receive(self, s: str, tries: int = tries) -> str:
        """Sends and receives a single command. called from main

        Args:
            command (str): command to send
            tries (int, optional): how many attempts to make

        Returns:
            str: sensor response
        """
        m: str = ""
        self._send_command(s)
        time.sleep(long_s)
        byte_m = self._read_buffer()
        try:  # Sanity check
            assert byte_m != None
            m = byte_m.decode(utf8)
        except:
            if tries <= 0:
                print(
                    ("ERR. Reading the photometer!: %s" % str(byte_m)), file=sys.stderr
                )
                if DEBUG:
                    raise
                return ""
            time.sleep(mid_s)
            self._reset_device()
            time.sleep(mid_s)
            m = self.send_and_receive(s, tries - 1)
            print(("Sensor info: " + str(m)), end=" ", file=sys.stderr)
        return m

    def start_continuous_read(self) -> None:
        """Starts listener"""
        self.data: list[str] = []
        self.live = True
        self.t1 = threading.Thread(target=self._listen)  # listener in background
        self.t1.start()

    def stop_continuous_read(self) -> None:
        """Stops listener"""
        self.live = False
        self.t1.join()

    def _listen(self):
        """Listener. Runs in dedicated thread"""
        self.live
        while self.live:
            time.sleep(short_s)
            self._read_buffer()  # this stores the data

    def _return_collected(self) -> list[str]:
        """Clears data array, returns contents

        Returns:
            list[str]: data to return
        """
        d = self.data[:]  # pass by value, not reference
        self.data.clear()  # clear buffer
        return d

    def rpi_to_client(self, s: str) -> None:
        """Sends a command to the sensor

        Args:
            s (str): command to send
        """
        print(f"Sending to sensor: {s}", file=sys.stdout)
        self._send_command(s)

    def client_to_rpi(self) -> list[str]:
        """Returns responses from sensor

        Returns:
            list[str]: responses
        """
        m_arr = self._return_collected()
        return m_arr

    def start_connection(self) -> None: ...

    def _close_connection(self) -> None: ...

    def _read_buffer(self) -> bytes | None: ...

    def _send_command(self, s: str) -> None: ...


class SQMLE(SQM):
    """WARNING: this code hasn't been tested, because I don't have an SQM-LE to test with."""

    def __init__(self) -> None:
        """Search the photometer in the network and read its metadata"""
        self.data: list[str] = []
        try:
            self.addr = device_addr
            self.start_connection()
        except:
            print(
                f"Device not found on {device_addr}, searching for device address ...",
                file=sys.stderr,
            )
            self.addr = self._search()
            print(("Found address %s ... " % str(self.addr)), file=sys.stderr)
            self.start_connection()
        self._clear_buffer()

    def _search(self) -> list[None] | str:
        """Search SQM LE in the LAN. Return its address"""
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setblocking(False)

        if hasattr(socket, "SO_BROADCAST"):
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # used to be decode, idk why, it needs to be bytes anyways
        self.s.sendto(
            "000000f6".encode(hex), ("255.255.255.255", 30718)
        )  # no idea why this port is used
        buf = ""
        starttime = time.time()

        print("Looking for replies; press Ctrl-C to stop.", file=sys.stderr)
        addr = [None, None]
        while True:
            try:
                (buf, addr) = self.s.recvfrom(30)
                # BUG: the 3rd hex character probably doesn't correspond to the 3rd bytes character. However, I'm not working with an SQM-LE so I've made the command decision to ignore this.
                # was buf[3].decode("hex")
                if buf.decode(hex)[3] == "f7":
                    # was buf[24:30].encode("hex")
                    print(
                        "Received from %s: MAC: %s" % (addr, buf.decode(hex)[24:30]),
                        file=sys.stderr,
                        )
            except:
                # Timeout in seconds. Allow all devices time to respond
                if time.time() - starttime > 3:
                    break
                pass

        try:
            assert addr[0] != None
        except:
            print("ERR. Device not found!", file=sys.stderr)
            raise
        else:
            return str(addr[0])  # was addr[0]

    def start_connection(self) -> None:
        """Start photometer connection"""
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(le_timeout)
        self.s.connect((self.addr, int(LE_PORT)))
        # self.s.settimeout(1) # idk why this was commented, I didn't comment it out

    def _close_connection(self) -> None:
        """End photometer connection"""
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 1, 0))
        request = ""
        r = True
        while r:  # wait until device stops responding
            r = self._read_buffer()
            request += str(r)
        self.s.close()

    def _read_buffer(self) -> bytes | None:
        """Read the data"""
        m = None
        try:
            m = self.s.recv(SOCK_BUF)
            if m.decode(utf8) == "":
                return
            self.data.append(m.decode(utf8).strip())
        except:
            pass
        return m

    def _send_command(self, s: str) -> None:
        """SQM_LE sends a command to the sensor

        Args:
            s (str): the command to send
        """
        self.s.send(s.encode(utf8))


class SQMLU(SQM):
    def __init__(self) -> None:
        """Search for the photometer and read its metadata"""
        self.data: list[str] = []
        try:
            print(f"Trying fixed device address {device_addr}", file=sys.stderr)
            self.addr = device_addr
            # self.s = serial.Serial(self.addr, LU_BAUD, timeout=2)
            self.start_connection()
            print(f"Device found at address {device_addr}", file=sys.stderr)

        except:  # device not at that address
            print(
                f"Device not found on {device_addr}, searching for device address ...",
                file=sys.stderr,
            )
            self.addr = self._search()
            print(("Found address %s ... " % str(self.addr)), file=sys.stderr)
            self.start_connection()
        self._clear_buffer()

    def _search(self) -> str:
        """Photometer search. Name of the port depends on the platform."""
        ports_unix = ["/dev/ttyUSB" + str(num) for num in range(100)]
        ports_win = ["COM" + str(num) for num in range(100)]

        os_in_use = sys.platform
        ports: list[str] = []
        if os_in_use == "linux2":
            print("Detected Linux platform", file=sys.stderr)
            ports = ports_unix
        elif os_in_use == "win32":
            print("Detected Windows platform", file=sys.stderr)
            ports = ports_win

        used_port = None
        for port in ports:
            conn_test = serial.Serial(port, LU_BAUD, timeout=1)
            conn_test.write("ix".encode(utf8))
            if conn_test.readline().decode(utf8)[0] == "i":
                used_port = port
                break

        try:
            assert used_port != None
        except:
            print("ERR. Device not found!", file=sys.stderr)
            raise
        else:
            return used_port

    def start_connection(self) -> None:
        """Start photometer connection"""
        self.s = serial.Serial(self.addr, LU_BAUD, timeout=lu_timeout)

    def _close_connection(self) -> None:
        """End photometer connection"""
        request = ""
        r = True
        while r:  # wait until device stops responding
            r = self._read_buffer()
            request += str(r)
        self.s.close()

    def _read_buffer(self) -> bytes | None:
        """Read the data"""
        m = None
        try:
            m = self.s.readline()
            if m.decode(utf8) == "":
                return
            self.data.append(m.decode(utf8).strip())
        except:
            pass
        return m

    def _send_command(self, s: str) -> None:
        """SQM_LU sends a command to the sensor

        Args:
            s (str): the command to send
        """
        self.s.write(s.encode(utf8))

    def send_and_receive(self, s: str, tries: int = tries) -> str:
        """Deprecated way of sending a command and waiting for a response. However, there's no way to guarantee that the given response originated from the command that was sent.

        Args:
            s (str): command to send
            tries (int, optional): number of attempts to make. Defaults to tries.

        Returns:
            str: _description_
        """
        m: str = ""
        self._send_command(s)
        time.sleep(long_s)
        byte_m = self._read_buffer()
        try:  # Sanity check
            assert byte_m != None
            m = byte_m.decode(utf8)
        except:
            if tries <= 0:
                print(
                    ("ERR. Reading the photometer!: %s" % str(byte_m)), file=sys.stderr
                )
                if DEBUG:
                    raise
                return ""
            time.sleep(mid_s)
            self._reset_device()
            time.sleep(mid_s)
            m = self.send_and_receive(s, tries - 1)
            print(("Sensor info: " + str(m)), end=" ", file=sys.stderr)
        return m


if __name__ == "__main__":
    """For debugging purposes. Parses command line arguments."""
    parser = argparse.ArgumentParser(
        prog="rpi_to_sensor.py",
        description="Sends a command to the sensor. If run as main, prints result.",
        epilog=f"If no argument given, runs user interface",
    )

    parser.add_argument(
        "command",
        nargs="?",
        type=str,
        help="To send a command you've already made, just give it as an argument",
    )
    args = vars(parser.parse_args())
    command = args.get("command")
    if not isinstance(command, str):
        print(
            f"Command is not a string. command: {command}, type: {type(command)}",
            file=sys.stderr,
        )
        exit()

    if device_type == "SQM-LU":
        d = SQMLU()
    elif device_type == "SQM-LE":
        d = SQMLE()
    else:
        d = SQMLU()  # default

    time.sleep(long_s)
    resp = d.send_and_receive(command)
    print(f"Sensor response: {resp}", file=sys.stderr)