#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
syst = sys.argv[1]
cpu = CPU()

cpu.load(syst)
cpu.run()