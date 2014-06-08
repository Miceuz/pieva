from argparse import ArgumentParser
from pieva import *
import fastopc as opc
import time

leds = opc.FastOPC()

def testPattern(pattern):
    global testDotIndex
    pixels = []
    for i in range(len(pattern)):
        if i == testDotIndex:
            pixels.append(testDot)
        else:
            pixels.append(testBlank)
    testDotIndex = testDotIndex + 1
    if(testDotIndex >= len(pattern)):
        testDotIndex = 0
    return pixels
    
def blank(pattern):
    pixels = []
    for led in pattern:
        pixels.append(testBlank)
    return pixels

def test(testSectionIdx):
    for t in range(len(sections[testSectionIdx]['pattern'])):
        s = 0
        pixels = []
        for section in sections:
            if s == testSectionIdx:
                pixels.append(testPattern(section['pattern']))
            else:
                pixels.append(blank(section['pattern']))
            s = s +1
        leds.putPixels(0, pixels)
        if None != screen:
            screen.putPixels(0, pixels)
        time.sleep(0.02)

parser = ArgumentParser(description = "Play test sequences")
parser.add_argument("testSection", type=int, action="store", default=None, nargs="?", help=" - which section to test. All sections will be tested if omitted")
parser.add_argument("--server", action="store", default=None, help="additional OPC server for debug purposes")
cliargs = parser.parse_args()

testDotIndex = 0
testBlank = [0, 0, 0]
testDot = [255, 255, 255]

if None != cliargs.server:
    screen = opc.FastOPC(cliargs.server)
else:
    screen = None


if None != cliargs.testSection:
    currSection = cliargs.testSection
    print "Testing section", currSection 
else:
    currSection = 0
    print "Testing all sections"
print "Control-C to interrupt"
while True:
    test(currSection)
    if None == cliargs.testSection:
        currSection += 1
        if currSection >= len(sections):
            currSection = 0
