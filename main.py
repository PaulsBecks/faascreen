#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import re
import time
import argparse
import requests
import json
import socket

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


def demo(n, block_orientation, rotate, inreverse):
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90, width=32, height=8,
                     rotate=0, blocks_arranged_in_reverse_order=inreverse, contrast=122)
    print("Created device")

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    print("IP:" + str(ip))
    s.close()

    while True:
      # get list of service active
      try:
        r = requests.get("http://localhost:8080/list")
        list = r.json()
        if len(list) == 0:
          show_message(device, "No functions deployed. Please configure for host: "+str(ip), fill="white", font=SINCLAIR_FONT)
        else:
          for function in list:
            r = requests.get("http://localhost"+function["resource"])
            data = r.json()
            print(data)
            with canvas(device) as draw:
              for i in range(0, len(data["symbol"])):
                 if data["symbol"][i] == "1":
                   draw.point((i%8, int(i/8)), fill="white")
              text(draw, (8,0), data["text"], fill="white", font=proportional(TINY_FONT))
            time.sleep(5)
            #show_message(device, "Connected to: "+function["name"], fill="white", font=SINCLAIR_FONT)

      except Exception as e:
        print(e)
        show_message(device, "Could not connect to tinyFaas. Please restart.", fill="white", font=SINCLAIR_FONT)
        pass
#        text(draw, str(msg), fill="white", font=proportional(TINY_FONT))
#      r = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
      # display content
#      msg = r.json()["bpi"]["USD"]["rate"].split(".")[0]
#      print(msg)
#      with canvas(device) as draw:
#        draw.point((2,0), fill="white")
#        draw.point((2,7), fill="white")
#        draw.point((3,0), fill="white")
#        draw.point((3,7), fill="white")
#        draw.point((1,1), fill="white")
#        draw.point((2,1), fill="white")
#       draw.point((3,1), fill="white")
#        draw.point((4,1), fill="white")
#        #draw.point((5,1), fill="white")
#        draw.point((1,2), fill="white")
#        draw.point((5,2), fill="white")
#        draw.point((1,3), fill="white")
#        draw.point((4,3), fill="white")
#        #draw.point((6,3), fill="white")
#        draw.point((1,4), fill="white")
#        draw.point((5,4), fill="white")
#        draw.point((1,5), fill="white")
#        draw.point((5,5), fill="white")
#        draw.point((1,6), fill="white")
#        #draw.point((5,6), fill="white")
#        draw.point((2,6), fill="white")
#        draw.point((3,6), fill="white")
#        draw.point((4,6), fill="white")
#     time.sleep(5)

#      r = requests.get("https://api1.binance.com/api/v3/ticker/price?symbol=ETHUSDT")
#      msg = r.json()["price"][:6]
#      points = [(3,0), 
#                (2,1), (3, 1), (4, 1), 
#                (1, 2), (2, 2), (3, 2), (4, 2), (5, 2),
#                (1, 3), (2, 3), (3, 3), (4, 3), (5,3), 
#                (2,4), (3, 4), (4, 4), 
#                (1, 5), (3, 5), (5, 5), 
#                (2, 6), (4,6),
#                (3,7)]
#      with canvas(device) as draw:
#        for point in points:
#          draw.point(point, fill="white")
#        text(draw, (8, 0), str(msg), fill="white", font=proportional(TINY_FONT))
#      time.sleep(5)
    # start demo#
#    msg = "B 27,132"
#    print(msg)
    #show_message(device, msg, fill="white", font=proportional(TINY_FONT), scroll_delay=0.1)
    #time.sleep(1)
#    with canvas(device) as draw:
#        text(draw, (8, 0), msg, fill="white", font=proportional(TINY_FONT))
#    time.sleep(1)
    #device.hide()
    #max7219.cleanup(device)
    
    """
    msg = "Fast scrolling: Lorem ipsum dolor sit amet, consectetur adipiscing\
    elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut\
    enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut\
    aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in\
    voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint\
    occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit\
    anim id est laborum."
    msg = re.sub(" +", " ", msg)
    print(msg)
    show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0)

    msg = "Slow scrolling: The quick brown fox jumps over the lazy dog"
    print(msg)
    show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.1)
    
    print("Vertical scrolling")
    words = [
        "Victor", "Echo", "Romeo", "Tango", "India", "Charlie", "Alpha",
        "Lima", " ", "Sierra", "Charlie", "Romeo", "Oscar", "Lima", "Lima",
        "India", "November", "Golf", " "
    ]

    virtual = viewport(device, width=device.width, height=len(words) * 8)
    with canvas(virtual) as draw:
        for i, word in enumerate(words):
            text(draw, (0, i * 8), word, fill="white", font=proportional(CP437_FONT))

    for i in range(virtual.height - device.height):
        virtual.set_position((0, i))
        time.sleep(0.05)

    msg = "Brightness"
    print(msg)
    show_message(device, msg, fill="white")

    time.sleep(1)
    with canvas(device) as draw:
        text(draw, (0, 0), "A", fill="white")

    time.sleep(1)
    for _ in range(5):
        for intensity in range(16):
            device.contrast(intensity * 16)
            time.sleep(0.1)

    device.contrast(0x80)
    time.sleep(1)

    msg = "Alternative font!"
    print(msg)

    time.sleep(1)
    msg = "Proportional font - characters are squeezed together!"
    print(msg)
    show_message(device, msg, fill="white", font=proportional(SINCLAIR_FONT))

    # http://www.squaregear.net/fonts/tiny.shtml
    time.sleep(1)
    msg = "Tiny is, I believe, the smallest possible font \
    (in pixel size). It stands at a lofty four pixels \
    tall (five if you count descenders), yet it still \
    contains all the printable ASCII characters."
    msg = re.sub(" +", " ", msg)
    print(msg)
    show_message(device, msg, fill="white", font=proportional(TINY_FONT))

    time.sleep(1)
    msg = "CP437 Characters"
    print(msg)
    show_message(device, msg)

    time.sleep(1)
    for x in range(256):
        with canvas(device) as draw:
            text(draw, (0, 0), chr(x), fill="white")
            time.sleep(0.1)

    """
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
    parser.add_argument('--reverse-order', type=bool, default=False, help='Set to true if blocks are in reverse order')

    args = parser.parse_args()

    try:
        demo(args.cascaded, args.block_orientation, args.rotate, args.reverse_order)
    except KeyboardInterrupt:
        pass
