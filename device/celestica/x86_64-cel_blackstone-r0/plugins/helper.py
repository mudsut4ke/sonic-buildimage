#!/usr/bin/env python

import os
import struct
import subprocess
from sonic_daemon_base.daemon_base import DaemonBase
from mmap import *

HOST_CHK_CMD = "docker > /dev/null 2>&1"
EMPTY_STRING = ""


class APIHelper():

    def __init__(self):
        (self.platform, self.hwsku) = DaemonBase().get_platform_and_hwsku()

    def is_host(self):
        return os.system(HOST_CHK_CMD) == 0

    def pci_get_value(self, resource, offset):
        status = True
        result = ""
        try:
            fd = os.open(resource, os.O_RDWR)
            mm = mmap(fd, 0)
            mm.seek(int(offset))
            read_data_stream = mm.read(4)
            result = struct.unpack('I', read_data_stream)
        except:
            status = False
        return status, result

    def run_command(self, cmd):
        status = True
        result = ""
        try:
            p = subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            raw_data, err = p.communicate()
            if err == '':
                result = raw_data.strip()
        except:
            status = False
        return status, result

    def run_interactive_command(self, cmd):
        try:
            os.system(cmd)
        except:
            return False
        return True

    def read_txt_file(self, file_path):
        try:
            with open(file_path, 'r') as fd:
                data = fd.read()
                return data.strip()
        except IOError:
            pass
        return None

    def read_one_line_file(self, file_path):
        try:
            with open(file_path, 'r') as fd:
                data = fd.readline()
                return data.strip()
        except IOError:
            pass
        return None
