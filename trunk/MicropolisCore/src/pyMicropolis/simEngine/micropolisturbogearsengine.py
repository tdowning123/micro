# micropolisturbogearsengine.py
#
# Micropolis, Unix Version.  This game was released for the Unix platform
# in or about 1990 and has been modified for inclusion in the One Laptop
# Per Child program.  Copyright (C) 1989 - 2007 Electronic Arts Inc.  If
# you need assistance with this program, you may contact:
#   http://wiki.laptop.org/go/Micropolis  or email  micropolis@laptop.org.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.  You should have received a
# copy of the GNU General Public License along with this program.  If
# not, see <http://www.gnu.org/licenses/>.
#
#             ADDITIONAL TERMS per GNU GPL Section 7
#
# No trademark or publicity rights are granted.  This license does NOT
# give you any right, title or interest in the trademark SimCity or any
# other Electronic Arts trademark.  You may not distribute any
# modification of this program using the trademark SimCity or claim any
# affliation or association with Electronic Arts Inc. or its employees.
#
# Any propagation or conveyance of this program must include this
# copyright notice and these terms.
#
# If you convey this program (or any modifications of it) and assume
# contractual liability for the program to recipients of it, you agree
# to indemnify Electronic Arts for any liability that those contractual
# assumptions impose on Electronic Arts.
#
# You may not misrepresent the origins of this program; modified
# versions of the program must be marked as such and not identified as
# the original program.
#
# This disclaimer supplements the one included in the General Public
# License.  TO THE FULLEST EXTENT PERMISSIBLE UNDER APPLICABLE LAW, THIS
# PROGRAM IS PROVIDED TO YOU "AS IS," WITH ALL FAULTS, WITHOUT WARRANTY
# OF ANY KIND, AND YOUR USE IS AT YOUR SOLE RISK.  THE ENTIRE RISK OF
# SATISFACTORY QUALITY AND PERFORMANCE RESIDES WITH YOU.  ELECTRONIC ARTS
# DISCLAIMS ANY AND ALL EXPRESS, IMPLIED OR STATUTORY WARRANTIES,
# INCLUDING IMPLIED WARRANTIES OF MERCHANTABILITY, SATISFACTORY QUALITY,
# FITNESS FOR A PARTICULAR PURPOSE, NONINFRINGEMENT OF THIRD PARTY
# RIGHTS, AND WARRANTIES (IF ANY) ARISING FROM A COURSE OF DEALING,
# USAGE, OR TRADE PRACTICE.  ELECTRONIC ARTS DOES NOT WARRANT AGAINST
# INTERFERENCE WITH YOUR ENJOYMENT OF THE PROGRAM; THAT THE PROGRAM WILL
# MEET YOUR REQUIREMENTS; THAT OPERATION OF THE PROGRAM WILL BE
# UNINTERRUPTED OR ERROR-FREE, OR THAT THE PROGRAM WILL BE COMPATIBLE
# WITH THIRD PARTY SOFTWARE OR THAT ANY ERRORS IN THE PROGRAM WILL BE
# CORRECTED.  NO ORAL OR WRITTEN ADVICE PROVIDED BY ELECTRONIC ARTS OR
# ANY AUTHORIZED REPRESENTATIVE SHALL CREATE A WARRANTY.  SOME
# JURISDICTIONS DO NOT ALLOW THE EXCLUSION OF OR LIMITATIONS ON IMPLIED
# WARRANTIES OR THE LIMITATIONS ON THE APPLICABLE STATUTORY RIGHTS OF A
# CONSUMER, SO SOME OR ALL OF THE ABOVE EXCLUSIONS AND LIMITATIONS MAY
# NOT APPLY TO YOU.


########################################################################
# Micropolis TurboGears Engine
# Don Hopkins


########################################################################
# Import stuff


import micropolisgenericengine
import random
import math
import array
import time
from datetime import datetime
import traceback
import re
import cairo
from pyMicropolis.tileEngine import tileengine
import micropolisengine
from turbogears import identity
import cherrypy
import eliza
from micropolis import model


########################################################################
# Globals


UserNameExp = re.compile('^[a-zA-Z0-9_-]+$')

MicropolisCorePath = 'micropolis/MicropolisCore/src'

MicropolisTilesPath = 'micropolis/htdocs/static/images/micropolis_tiles.png'

LoopsPerYear = micropolisengine.PASSES_PER_CITYTIME * micropolisengine.CITYTIMES_PER_YEAR

SpeedConfigurations = [
    { # 0: Ultra Slow
        'speed': 3,
        'pollDelay': 5000,
        'animateDelay': 1000,
        'loopsPerSecond': round(LoopsPerYear / 60.0), # One year per minute.
        'maxLoopsPerPoll': 100,
    },
    { # 1: Super Slow
        'speed': 3, 
        'pollDelay': 1000,
        'animateDelay': 500,
        'loopsPerSecond': round(LoopsPerYear / 30.0), # One year per 30 seconds, 2 years per minute.

        'maxLoopsPerPoll': 200,
    },
    { # 2: Very Slow
        'speed': 3, 
        'pollDelay': 500,
        'animateDelay': 250,
        'loopsPerSecond': round(LoopsPerYear / 20.0), # One year per 20 seconds, 3 years per minute.
        'maxLoopsPerPoll': 400,
    },
    { # 3: Slow
        'speed': 3, 
        'pollDelay': 500,
        'animateDelay': 250,
        'loopsPerSecond': round(LoopsPerYear / 15.0), # One year per 15 seconds, 4 years per minute.
        'maxLoopsPerPoll': 600,
    },
    { # 4: Medium
        'speed': 3, 
        'pollDelay': 500,
        'animateDelay': 250,
        'loopsPerSecond': round(LoopsPerYear / 10.0), # One year per 10 seconds, 6 years per minute.
        'maxLoopsPerPoll': 800,
    },
    { # 5: Fast
        'speed': 3, 
        'pollDelay': 500,
        'animateDelay': 250,
        'loopsPerSecond': round(LoopsPerYear / 5.0), # One year per 5 seconds, 12 years per minute.
        'maxLoopsPerPoll': 1000,
    },
    { # 6: Very Fast
        'speed': 3, 
        'pollDelay': 300,
        'animateDelay': 250,
        'loopsPerSecond': round(LoopsPerYear / 3.0), # One year per 3 seconds, 20 years per minute.
        'maxLoopsPerPoll': 2000,
    },
    { # 7: Super Fast
        'speed': 3, 
        'pollDelay': 250,
        'animateDelay': 250,
        'loopsPerSecond': round(LoopsPerYear / 2.0), # One year per 2 seconds, 30 years per minute.
        'maxLoopsPerPoll': 5000,
    },
    { # 8: Ultra Fast
        'speed': 3, 
        'pollDelay': 500,
        'animateDelay': 250,
        'loopsPerSecond': round(LoopsPerYear / 1.0), # One year per 1 second, 60 years per minute.
        'maxLoopsPerPoll': 10000,
    },
    { # 9: Astronomically Fast
        'speed': 3, 
        'pollDelay': 500,
        'animateDelay': 250,
        'loopsPerSecond': round(4 * LoopsPerYear / 1.0), # Four years per second, 240 years per minute.
        'loopsPerSecond': 1000,
        'maxLoopsPerPoll': 40000,
    },
]

CityNames = {
    'about': MicropolisCorePath + '/cities/about.xml',
    'badnews': MicropolisCorePath + '/cities/badnews.xml',
    'bluebird': MicropolisCorePath + '/cities/bluebird.xml',
    'bruce': MicropolisCorePath + '/cities/bruce.xml',
    'deadwood': MicropolisCorePath + '/cities/deadwood.xml',
    'finnigan': MicropolisCorePath + '/cities/finnigan.xml',
    'freds': MicropolisCorePath + '/cities/freds.xml',
    'haight': MicropolisCorePath + '/cities/haight.xml',
    'happisle': MicropolisCorePath + '/cities/happisle.xml',
    'joffburg': MicropolisCorePath + '/cities/joffburg.xml',
    'kamakura': MicropolisCorePath + '/cities/kamakura.xml',
    'kobe': MicropolisCorePath + '/cities/kobe.xml',
    'kowloon': MicropolisCorePath + '/cities/kowloon.xml',
    'kyoto': MicropolisCorePath + '/cities/kyoto.xml',
    'linecity': MicropolisCorePath + '/cities/linecity.xml',
    'med_isle': MicropolisCorePath + '/cities/med_isle.xml',
    'ndulls': MicropolisCorePath + '/cities/ndulls.xml',
    'neatmap': MicropolisCorePath + '/cities/neatmap.xml',
    'radial': MicropolisCorePath + '/cities/radial.xml',
    'senri': MicropolisCorePath + '/cities/senri.xml',
    'southpac': MicropolisCorePath + '/cities/southpac.xml',
    'splats': MicropolisCorePath + '/cities/splats.xml',
    'wetcity': MicropolisCorePath + '/cities/wetcity.xml',
    'yokohama': MicropolisCorePath + '/cities/yokohama.xml',
}

ToolNameToIndex = {
    'residential': 0,
    'commercial': 1,
    'industrial': 2,
    'firestation': 3,
    'policestation': 4,
    'query': 5,
    'wire': 6,
    'bulldozer': 7,
    'railroad': 8,
    'road': 9,
    'stadium': 10,
    'park': 11,
    'seaport': 12,
    'coalpower': 13,
    'nuclearpower': 14,
    'airport': 15,
    'network': 16,
    'water': 17,
    'land': 18,
    'forest': 19,
}

AniTiles = (
    0,   1,   2,   3,   4,   5,   6,   7,   8,   9,   10,  11,  12,  13,  14,  15,
    16,  17,  18,  19,  20,  21,  22,  23,  24,  25,  26,  27,  28,  29,  30,  31, 
    32,  33,  34,  35,  36,  37,  38,  39,  40,  41,  42,  43,  44,  45,  46,  47,
    48,  49,  50,  51,  52,  53,  54,  55,
    # Fire
                                            57,  58,  59,  60,  61,  62,  63,  56,
    # No Traffic
    64,  65,  66,  67,  68,  69,  70,  71,  72,  73,  74,  75,  76,  77,  78,  79,
    # Light Traffic
    128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143,
    80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94,  95,
    96,  97,  98,  99,  100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
    112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127,
    # Heavy Traffic
    192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207,
    144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159,
    160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175,
    176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191,
    # Wires & Rails
    208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223,
    224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239,
    # Residential
    240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255,
    256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271,
    272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287,
    288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303,
    304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319,
    320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335,
    336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351,
    352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367,
    368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383,
    384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399,
    400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415,
    416, 417, 418, 419, 420, 421, 422,
    # Commercial
                                       423, 424, 425, 426, 427, 428, 429, 430, 431,
    432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447,
    448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463,
    464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479,
    480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495,
    496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511,
    512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527,
    528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 543,
    544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 554, 555, 556, 557, 558, 559,
    560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575,
    576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591,
    592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607,
    608, 609, 610, 611,
    # Industrial
                        612, 613, 614, 615, 616, 617, 618, 619, 852, 621, 622, 623,
    624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639,
    640, 884, 642, 643, 888, 645, 646, 647, 648, 892, 896, 651, 652, 653, 654, 655,
    656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671,
    672, 673, 674, 675, 900, 904, 678, 679, 680, 681, 682, 683, 684, 685, 908, 687,
    688, 912, 690, 691, 692,
    # SeaPort
                             693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703,
    704, 705, 706, 707, 708,
    # AirPort
                             709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719,
    720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735,
    736, 737, 738, 739, 740, 741, 742, 743, 744,
    # Coal power
                                                 745, 746, 916, 920, 749, 750, 924,
    928, 753, 754, 755, 756, 757, 758, 759, 760,
    # Fire Dept
                                                 761, 762, 763, 764, 765, 766, 767,
    768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778,
    # Stadium
                                                           779, 780, 781, 782, 783,
    784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794,
    # Stadium Anims
                                                           795, 796, 797, 798, 799,
    800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810,
    # Nuclear Power
                                                           811, 812, 813, 814, 815,
    816, 817, 818, 819, 952, 821, 822, 823, 824, 825, 826,
    # Power out + Bridges
                                                           827, 828, 829, 830, 831,
    # Radar dish
    833, 834, 835, 836, 837, 838, 839, 832,
    # Fountain / Flag
                                            841, 842, 843, 840, 845, 846, 847, 848,
    849, 850, 851, 844, 853, 854, 855, 856, 857, 858, 859, 852,
    # zone destruct & rubblize
                                                                861, 862, 863, 864,
    865, 866, 867, 867,
    # totally unsure
                        868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879,
    880, 881, 882, 883,
    # Smoke stacks
                        885, 886, 887, 884, 889, 890, 891, 888, 893, 894, 895, 892,
    897, 898, 899, 896, 901, 902, 903, 900, 905, 906, 907, 904, 909, 910, 911, 908,
    913, 914, 915, 912, 917, 918, 919, 916, 921, 922, 923, 920, 925, 926, 927, 924,
    929, 930, 931, 928,
    # Stadium Playfield
                        933, 934, 935, 936, 937, 938, 939, 932, 941, 942, 943, 944,
    945, 946, 947, 940,
    # Bridge up chars
                        948, 949, 950, 951,
    # Nuclear swirl
                                            953, 954, 955, 952,
)


# Compute the animation groups (loops and sequences).
# Then make a tile map that maps any tile in the group
# to the tile in the group with the lowest number.
# 
# Note: How should we handle the bulldozer explosion sequences? They
# should be animated on the client, but they end up in a non-animated
# end state, instead of looping. The server could call animateTiles,
# and use the tile map to map all but the end state to the first
# state, so we don't send a tile each time and let the animation
# happend on the client. So we need to map the last state of a
# sequence to itself instead of to the first state. TODO: Take last
# state of sequence out of the set of tiles mapped to first state.

AniTileGroupMap = {}
for tileIndex in range(0, len(AniTiles)):

    #print "tileindex", tileIndex, (tileIndex in AniTileGroupMap)
    if tileIndex in AniTileGroupMap:
        continue

    nextTileIndex = AniTiles[tileIndex]

    if nextTileIndex == tileIndex:
        continue

    curGroup = [tileIndex]
    AniTileGroupMap[tileIndex] = curGroup
    #print "start", curGroup

    while True:
        if nextTileIndex in AniTileGroupMap:
            # If we are at the end of a linear sequence, do not include the last tile in the group.
            # TODO: Test this out and think it through some more.
            if nextTileIndex == tileIndex:
                break

            group = AniTileGroupMap[nextTileIndex]
            if group == curGroup:
                #print "looped"
                break
            #print "merge", curGroup, group
            # Merge curGroup into group.
            group.extend(curGroup)
            for i in curGroup:
                AniTileGroupMap[i] = group
            break

        tileIndex = nextTileIndex
        curGroup.append(tileIndex)
        #print "accumulate", tileIndex, curGroup
        AniTileGroupMap[nextTileIndex] = curGroup
        nextTileIndex = AniTiles[tileIndex]
        #print "... tileIndex", tileIndex, "nextTileindex", nextTileIndex


AniTileGroups = []
for group in AniTileGroupMap.values():
    if group not in AniTileGroups:
        AniTileGroups.append(group)

for group in AniTileGroups:
    group.sort()

AniTileGroups.sort()

#print len(AniTileGroups), "AniTileGroups"

AniTileMap = array.array('i')
for i in range(0, len(AniTiles)):
    AniTileMap.append(i)

for group in AniTileGroups:
    baseTile = group[0]
    for tile in group:
        AniTileMap[tile] = baseTile

#print AniTileMap


########################################################################
# Utilities


def PRINT(*args):
    print args


def Now():
    return time.time()


def UniqueID(prefix="ID_"):
    id = prefix
    for i in range(0, 4):
        id += "_%06d" % (random.randint(0, 1000000),)
    return id


########################################################################
# Session class.


class Session(object):


    def __init__(self, controller, sessionID):
        self.sessionID = sessionID
        self.engine = None
        self.views = []
        self.messages = []
        self.messagesSeen = {}
        self.createTime = time.time()
        self.lastPollTime = 0
        self.lastTouchTime = 0
        self.expireDelay = 60 * 10 # ten minutes
        self.controller = controller
        self.user = None

        self.touch()

        tileViewCache = array.array('i')
        self.tileViewCache = tileViewCache
        row = (-1,) * micropolisengine.WORLD_W
        for i in range(0, micropolisengine.WORLD_H):
            tileViewCache.extend(row)


    def __del__(self):
        self.setEngine(None)


    def touch(self):
        self.lastTouchTime = Now()


    def handlePoll(self, pollDict):
        self.lastPollTime = Now()

        self.engine.handlePoll(
            pollDict,
            self)

        result = self.receiveMessages()
        #print "session.handlePoll receiveMessages", result

        return result


    def touchAge(self):
        return Now() - self.lastTouchTime


    def pollAge(self):
        return Now() - self.lastPollTime


    def isExpired(self):
        return self.pollAge < self.expireDelay


    def expire(self):
        print "Expiring session", self
        self.setEngine(None)


    def sendMessage(self, msg):
        #print "SENDMESSAGE", msg
        collapse = msg.get('collapse', False)
        #print "COLLAPSE", collapse
        if collapse:
            id = msg.get('id', None)
            message = msg.get('message', '')
            variable = msg.get('variable', '')
            key = (message, variable, id)
            messagesSeen = self.messagesSeen
            if key in messagesSeen:
                messagesSeen[key].update(msg)
            else:
                messagesSeen[key] = msg
                self.messages.append(msg)
        else:
             self.messages.append(msg)
        self.touch()


    def receiveMessages(self):
        messages = self.messages

        self.messages = []
        self.messagesSeen = {}

        if False and messages:
            print "=" * 72
            for message in messages:
                print message['message'], message.get('variable', ''), message
        
        if False:
            print [
                (message['message'], message.get('variable', None))
                for message in messages
            ]

        return messages


    def setEngine(self, engine):
        #print "setEngine", self, engine
        if self.engine:
            self.engine.removeSession(self)
        self.engine = engine
        if engine:
            engine.addSession(self)


    def createEngine(self):
        if self.engine:
            return

        engine = CreateTurboGearsEngine(
            controller=self.controller)

        self.setEngine(engine)


########################################################################
# MicropolisTurboGearsEngine Class


class MicropolisTurboGearsEngine(micropolisgenericengine.MicropolisGenericEngine):


    sessions = [] # Back stop.


    def __init__(
        self, 
        controller=None, 
        *args, 
        **kw):
        micropolisgenericengine.MicropolisGenericEngine.__init__(self, *args, **kw)
        self.controller = controller
        self.eliza = eliza.eliza()


    def initGamePython(self):

        self.sessions = []

        self.resourceDir = MicropolisCorePath + '/res'

        tengine = tileengine.TileEngine()
        self.tengine = tengine

        tengine.setBuffer(self.getMapBuffer())
        tengine.width = micropolisengine.WORLD_W
        tengine.height = micropolisengine.WORLD_H

        # Unsigned short tile values, in column major order.
        tengine.tileFormat = tileengine.TILE_FORMAT_SHORT_UNSIGNED
        tengine.colBytes = micropolisengine.BYTES_PER_TILE * micropolisengine.WORLD_H
        tengine.rowBytes = micropolisengine.BYTES_PER_TILE
        tengine.tileMask = micropolisengine.LOMASK

        self.tileCount = micropolisengine.TILE_COUNT
        self.tileSize = micropolisengine.EDITOR_TILE_SIZE

        self.tilesSurface = cairo.ImageSurface.create_from_png(MicropolisTilesPath)
        self.tilesWidth = self.tilesSurface.get_width()
        self.tilesHeight = self.tilesSurface.get_height()
        self.tilesCols = self.tilesWidth / micropolisengine.EDITOR_TILE_SIZE

        self.tileSurface = self.tilesSurface.create_similar(cairo.CONTENT_COLOR, self.tileSize, self.tileSize)
        self.tileCtx = cairo.Context(self.tileSurface)
        self.tileCtx.set_antialias(cairo.ANTIALIAS_NONE)

        self.tileMap = AniTileMap

        self.tileSizeCache = {}

        self.startVirtualSpeed = 2
        self.virtualSpeed = self.startVirtualSpeed
        self.loopsPerSecond = 100
        self.maxLoopsPerPoll = 10000 # Tune this

        self.resetRealTime()

        self.loadInitialCity()


    def loadInitialCity(self):

        #print "LOADINITIALCITY"

        # Load a city file.
        cityFileName = MicropolisCorePath + '/cities/haight.xml'
        #print "Game loading city file:", cityFileName
        self.loadMetaCity(cityFileName)

        # Initialize the simulator engine.

        self.setSpeed(2)
        self.pause()
        self.setFunds(1000000000)
        self.setCityTax(10)
        self.setAutoGoto(False)
        self.setEnableDisasters(False)


    def startTimer(self):

        pass


    def stopTimer(self):

        pass


    def resetRealTime(self):
        self.lastLoopTime = time.time()


    def addSession(self, session):
        sessions = self.sessions
        if session not in sessions:
            sessions.append(session)


    def removeSession(self, session):
        sessions = self.sessions
        if session in sessions:
            sessions.remove(session)


    def sendAllControllerSessions(self, message, exceptSession=None):
        print "sendAllControllerSessions", self.controller.getSessions()
        for session in self.controller.getSessions():
            if session != exceptSession:
                try:
                    session.sendMessage(message)                
                except Exception, e:
                    print "======== XXX sendSessions exception:", e
                    traceback.print_exc(10)

        # Clean up the collapse flag so none of the sessions send it
        # to the client.
        if 'collapse' in message:
            del message['collapse']


    def sendSessions(self, message):
        try:
            for session in self.sessions:
                session.sendMessage(message)
        except Exception, e:
            print "======== XXX sendSessions exception:", e
            traceback.print_exc(10)

        # Clean up the collapse flag so none of the sessions send it
        # to the client.
        if 'collapse' in message:
            del message['collapse']


    def handleMessage(self, session, messageDict):
        message = messageDict.get('message', None)
        user = session.user
        #print "HANDLEMESSAGE", message, messageDict

        if message == 'disaster':

            disaster = messageDict.get('disaster', None)
            #print "disaster", disaster

            if disaster == 'monster':
                self.makeMonster()
            elif disaster == 'fire':
                self.setFire()
            elif disaster == 'flood':
                self.makeFlood()
            elif disaster == 'meltdown':
                self.makeMeltdown()
            elif disaster == 'tornado':
                self.makeTornado()
            elif disaster == 'earthquake':
                self.makeEarthquake()
            elif disaster == 'eco':
                self.heatSteps = 1
                self.heatRule = 1
            elif disaster == 'melt':
                self.heatSteps = 1
                self.heatRule = 0
            else:
                print "Invalid disaster name:", disaster

        elif message == 'setTaxRate':

            taxRateStr = messageDict.get('taxRate', self.cityTax)
            taxRate = self.cityTax
            try:
                taxRate = int(taxRateStr)
            except: pass
            taxRate = max(0, min(taxRate, 20))
            self.cityTax = taxRate
            #print "==== TAXRATE", taxRate

        elif message == 'setRoadPercent':

            roadPercent = int(self.roadPercent * 100.0)
            roadPercentStr = messageDict.get('roadPercent', roadPercent)
            try:
                roadPercent = int(roadPercentStr)
            except: pass
            roadPercent = max(0, min(roadPercent, 100))
            self.roadPercent = float(roadPercent) / 100.0
            self.roadSpend = int(self.roadPercent * self.roadFund)
            self.updateFundEffects()
            #print "==== ROADPERCENT", self.roadPercent

        elif message == 'setFirePercent':

            firePercent = int(self.firePercent * 100.0)
            firePercentStr = messageDict.get('firePercent', firePercent)
            try:
                firePercent = int(firePercentStr)
            except: pass
            firePercent = max(0, min(firePercent, 100))
            self.firePercent = float(firePercent) / 100.0
            self.fireSpend = int(self.firePercent * self.fireFund)
            self.updateFundEffects()
            #print "==== FIREPERCENT", self.firePercent

        elif message == 'setPolicePercent':

            policePercent = int(self.policePercent * 100.0)
            policePercentStr = messageDict.get('policePercent', policePercent)
            try:
                policePercent = int(policePercentStr)
            except: pass
            policePercent = max(0, min(policePercent, 100))
            self.policePercent = float(policePercent) / 100.0
            self.policeSpend = int(self.policePercent * self.policeFund)
            self.updateFundEffects()
            #print "==== POLICEPERCENT", self.policePercent

        elif message == 'loadCity':

            cityName = messageDict.get('city', None)
            print "loadCity", cityName
            if cityName in CityNames:
                cityFileName = CityNames[cityName]
                print "cityFileName", cityFileName
                self.loadMetaCity(cityFileName)

        elif message == 'loadScenario':

            scenarioStr = messageDict.get('scenario', None)
            #print "loadScenario", scenarioStr
            scenario = 0
            try:
                scenario = int(scenarioStr)
            except: pass
            if scenario:
                self.loadScenario(scenario)

        elif message == 'generateCity':

            print "generateCity"
            self.generateNewCity()

        elif message == 'setGameMode':

            gameMode = messageDict.get('gameMode')

            print "setGameMode", gameMode, self.startVirtualSpeed
            if gameMode == "start":
                self.setVirtualSpeed(0)
                self.pause()
            elif gameMode == "play":
                self.setVirtualSpeed(self.startVirtualSpeed)
                self.resetRealTime()
                self.updateFundEffects()
                self.resume()

        elif message == 'setPaused':

            paused = messageDict.get('paused')

            #print "setPaused", paused
            if paused == True:
                self.pause()
            elif paused == False:
                self.resume()
            else:
                print "Bad paused value, should be true or false, not", paused

        elif message == 'setVirtualSpeed':

            virtualSpeed = int(messageDict.get('virtualSpeed'))
            speed = max(0, min(virtualSpeed, len(SpeedConfigurations) - 1))

            print "setVirtualSpeed", virtualSpeed
            self.setVirtualSpeed(virtualSpeed)

        elif message == 'abandonCity':

            print "ABANDON CITY"

        elif message == 'saveCity':

            print "SAVE CITY"

        elif message == 'drawToolStart':

            #print "DRAWTOOLSTART", messageDict
            tool = messageDict.get('tool')
            x = int(messageDict.get('x'))
            y = int(messageDict.get('y'))

            if ((tool not in ToolNameToIndex) or
                (not self.testBounds(x, y))):

                print "INVALID ARGUMENT TO DRAWTOOLSTART", tool, x, y

            else:

                toolIndex = ToolNameToIndex[tool]
                self.toolDown(toolIndex, x, y)

        elif message == 'drawToolMove':

            #print "DRAWTOOLMOVE", messageDict
            tool = messageDict.get('tool')
            x0 = int(messageDict.get('x0'))
            y0 = int(messageDict.get('y0'))
            x1 = int(messageDict.get('x1'))
            y1 = int(messageDict.get('y1'))

            #print "DRAWTOOLMOVE", tool, x0, y0, x1, x1
            if ((tool not in ToolNameToIndex) or
                (not self.testBounds(x0, y0)) or
                (not self.testBounds(x1, y1))):

                print "INVALID ARGUMENT TO DRAWTOOLMOVE", tool, x0, y0, x1, y1

            else:

                toolIndex = ToolNameToIndex[tool]
                self.toolDrag(toolIndex, x0, y0, x1, y1)

        elif message == 'drawToolStop':

            #print "DRAWTOOLSTOP", messageDict
            tool = messageDict.get('tool')
            x = int(messageDict.get('x'))
            y = int(messageDict.get('y'))

            #print "DRAWTOOLSTOP", tool, x, y
            if ((tool not in ToolNameToIndex) or
                (not self.testBounds(x, y))):

                print "INVALID ARGUMENT TO DRAWTOOLSTOP", tool, x, y

            else:

                # Nothing to do, since the user interface is
                # responsible for sending us a move to the endpoint.
                pass

        elif message == 'sendChatMessage':

            text = messageDict['text']
            channel = messageDict['channel']
            language = messageDict['language']

            userName = 'anonymous'
            user = session.user
            if user:
                userName = user.user_name

            print "CHAT", userName, language, text

            if text and text[0] == '!':

                command = text[1:]
                print "CHEAT COMMAND", command

                if command == 'million':
                    session.engine.spend(-1000000)

            elif channel == 'eliza':

                elizaResponse = self.eliza.respond(text)
                print "RESPONSE", elizaResponse

                session.sendMessage({
                    'message': 'chatMessage',
                    'from': 'Me',
                    'channel': channel,
                    'text': text,
                    'collapse': False,
                })

                session.sendMessage({
                    'message': 'chatMessage',
                    'from': 'Eliza',
                    'channel': channel,
                    'text': elizaResponse,
                    'collapse': False,
                })

            elif channel == 'all':

                session.sendMessage({
                    'message': 'chatMessage',
                    'from': 'You',
                    'channel': channel,
                    'text': text,
                    'collapse': False,
                })

                self.sendAllControllerSessions(
                    {
                        'message': 'chatMessage',
                        'from': userName,
                        'channel': channel,
                        'text': text,
                        'collapse': False,
                    },
                    exceptSession=session)


            else:

                print "Unknown chat channel:", channel

        elif message == 'tileview':

            #print "MESSAGE TILEVIEW", messageDict
            try:
                id = messageDict['id']
                col = messageDict['col']
                row = messageDict['row']
                cols = messageDict['cols']
                rows = messageDict['rows']
                viewX = messageDict['viewX']
                viewY = messageDict['viewY']
                viewWidth = messageDict['viewWidth']
                viewHeight = messageDict['viewHeight']
                code = messageDict['code']
            except Exception, e:
                self.expectationFailed("Invalid parameters: " + str(e))

            #print "ID", id
            #print "TILE", col, row, cols, rows
            #print "VIEW", viewX, viewY, viewWidth, viewHeight

            if ((col < 0) or
                (row < 0) or
                (cols <= 0) or
                (rows <= 0) or
                ((col + cols) > micropolisengine.WORLD_W) or
                ((row + rows) > micropolisengine.WORLD_H)):
                self.expectationFailed("Invalid parameters.")

            #print "Calling getTileData", "col", col, "row", row, "cols", cols, "rows", rows, "code", code
            tiles = self.tengine.getTileData(
                None,
                self.tileMap,
                col, row,
                cols, rows,
                code,
                session.tileViewCache)
            #print "TILES", "code", code, "tiles", type(tiles), len(tiles), tiles
            #t = tiles
            #tiles = ByteArray()
            #tiles.write(t)
            #print "TILES NOW", type(tiles)
            #print "TILES", tiles

            session.sendMessage({
                'message': 'update',
                'variable': 'tileview',
                'id': id,
                'col': col,
                'row': row,
                'cols': cols,
                'rows': rows,
                'viewX': viewX,
                'viewY': viewY,
                'viewWidth': viewWidth,
                'viewHeight': viewHeight,
                'tiles': tiles,
                'code': code,
                'collapse': True,
            })

        elif message == 'historyview':

            #print "HISTORYVIEW", messageDict

            try:
                id = messageDict['id']
                historyScale = messageDict['scale']
                historyCount = messageDict['count']
                historyOffset = messageDict['offset']
                historyTypes = messageDict['types']
                historyWidth = messageDict['width']
                historyHeight = messageDict['height']
            except Exception, e:
                self.expectationFailed("Invalid parameters: " + str(e))

            #print "HISTORYVIEW", id, historyScale, historyCount, historyOffset, historyTypes, historyWidth, historyHeight

            # Scale the residential, commercial and industrial histories
            # together relative to the max of all three.  Up to 128 they
            # are not scaled. Starting at 128 they are scaled down so the
            # maximum is always at the top of the history.

            def calcScale(maxVal):
                if maxVal < 128:
                    maxVal = 0
                if maxVal > 0:
                    return 128.0 / float(maxVal)
                else:
                    return 1.0

            cityTime = self.cityTime
            startingYear = self.startingYear
            year = int(cityTime / 48) + startingYear
            month = int(cityTime % 48) >> 2

            getHistoryRange = self.getHistoryRange
            getHistory = self.getHistory

            resHistoryMin, resHistoryMax = getHistoryRange(
                micropolisengine.HISTORY_TYPE_RES,
                historyScale)
            comHistoryMin, comHistoryMax = getHistoryRange(
                micropolisengine.HISTORY_TYPE_COM,
                historyScale)
            indHistoryMin, indHistoryMax = getHistoryRange(
                micropolisengine.HISTORY_TYPE_IND,
                historyScale)
            allMax = max(resHistoryMax,
                         max(comHistoryMax,
                             indHistoryMax))
            rciScale = calcScale(allMax)

            # Scale the money, crime and pollution histories
            # independently of each other.

            moneyHistoryMin, moneyHistoryMax = getHistoryRange(
                micropolisengine.HISTORY_TYPE_MONEY,
                historyScale)
            crimeHistoryMin, crimeHistoryMax = getHistoryRange(
                micropolisengine.HISTORY_TYPE_CRIME,
                historyScale)
            pollutionHistoryMin, pollutionHistoryMax = getHistoryRange(
                micropolisengine.HISTORY_TYPE_POLLUTION,
                historyScale)
            moneyScale = calcScale(moneyHistoryMax)
            crimeScale = calcScale(crimeHistoryMax)
            pollutionScale = calcScale(pollutionHistoryMax)

            historyRange = 128.0

            valueScales = (
                rciScale, rciScale, rciScale, # res, com, ind
                moneyScale, crimeScale, pollutionScale, # money, crime, pollution
            )

            valueRanges = (
                (resHistoryMin, resHistoryMax,),
                (comHistoryMin, comHistoryMax,),
                (indHistoryMin, indHistoryMax,),
                (moneyHistoryMin, moneyHistoryMax,),
                (crimeHistoryMin, crimeHistoryMax,),
                (pollutionHistoryMin, pollutionHistoryMax,),
            )

            histories = []

            for historyType in range(0, micropolisengine.HISTORY_TYPE_COUNT):

                if historyType not in historyTypes:
                    histories.append(None)
                    continue

                valueScale = valueScales[historyType]
                valueRange = valueRanges[historyType]

                values = [
                        getHistory(
                            historyType,
                            historyScale,
                            historyIndex)
                        for historyIndex in range(micropolisengine.HISTORY_COUNT - 1, -1, -1)
                ]

                histories.append({
                    'historyType': historyType,
                    'valueScale': valueScale,
                    'valueRange': valueRange,
                    'values': values,
                })

            session.sendMessage({
                'message': 'update',
                'variable': 'historyview',
                'id': id,
                'scale': historyScale,
                'count': historyCount,
                'offset': historyOffset,
                'types': historyTypes,
                'width': historyWidth,
                'height': historyHeight,
                'year': year,
                'month': month,
                'histories': histories,
                'range': historyRange,
                'collapse': True,
            })

        elif message == 'login':

            print "login", messageDict

            success = True
            feedback = ''

            userName = messageDict['userName']
            password = messageDict['password']
            passwordEncrypted = identity.encrypt_password(password)
            fullName = ''
            emailAddress = ''

            user = model.User.by_user_name(unicode(userName))
            if user and user.password == passwordEncrypted:
                success = True
                feedback = 'You are logged in.*' # TRANSLATE
                fullName = user.display_name
                emailAddress = user.email_address
                session.user = user
            else:
                success = False
                feedback = 'Incorrect user name or password.' # TRANSLATE
                session.user = None

            session.sendMessage({
                'message': 'loginResponse',
                'success': success,
                'feedback': feedback,
                'fullName': fullName,
                'emailAddress': emailAddress,
            })

        elif message == 'logout':

            print "logout", messageDict

            loggedIn = user != None
            if not loggedIn:
                success = False
                feedback = 'You are already logged out,*' # TRANSLATE
            else:
                session.user = None
                success = True
                feedback = 'You are logged out.*' # TRANSLATE

            session.sendMessage({
                'message': 'logoutResponse',
                'success': success,
                'feedback': feedback,
            })

        elif message == 'newAccount':

            print "newAccount", messageDict

            success = False
            feedback = ''

            userName = messageDict['userName']
            password1 = messageDict['password1']
            password2 = messageDict['password2']
            fullName = messageDict['fullName']
            emailAddress = messageDict['emailAddress']

            if userName == '':
                feedback = 'Please enter a user name.' # TRANSLATE
            elif not self.checkUserName(userName):
                feedback = 'The user name contains invalid characters.*' # TRANSLATE
            elif password1 == '':
                feedback = 'Please enter a password.' # TRANSLATE
            elif model.User.by_user_name(unicode(userName)):
                feedback = 'A user of that name already exists.*' # TRANSLATE
            elif password1 != password2:
                feedback = 'Please repeat the same password in the next field.' # TRANSLATE
            else:
                user = model.User()
                user.user_name = unicode(userName)
                user.email_address = unicode(emailAddress)
                user.display_name = unicode(fullName)
                registeredGroup = model.Group.by_name(u'registered')
                user.groups.append(registeredGroup)
                user.password = unicode(password1)
                user.created = datetime.now()
                user.activity = datetime.now()
                success = True
                feedback = 'A new account has been created*' # TRANSLATE
                session.user = user

            session.sendMessage({
                'message': 'newAccountResponse',
                'success': success,
                'feedback': feedback,
            })

        elif message == 'changePassword':

            passwordOld = messageDict['passwordOld']
            passwordOldEncrypted = identity.encrypt_password(passwordOld)
            password1 = messageDict['password1']
            password2 = messageDict['password2']
            feedback = ''
            success = False

            if not user:
                feedback = 'You are not logged in.'
            elif passwordOldEncrypted != user.password:
                feedback = 'Incorrect old password.'
            elif (not password1) or (not password2):
                feedback = 'You must enter your new password twice.'
            elif password1 != password2:
                feedback = 'The new passwords do not match.'
            else:
                user.password = unicode(password1)
                feedback = 'Your password has been changed.'
                success = True

            session.sendMessage({
                'message': 'changePasswordResponse',
                'success': success,
                'feedback': feedback,
            })

        elif message == 'setUserFullName':
            if user:
                fullName = messageDict['fullName']
                user.display_name = unicode(fullName)

        elif message == 'setUserEmailAddress':
            if user:
                emailAddress = messageDict['emailAddress']
                user.email_address = emailAddress

        else:

            print "UNKNOWN MESSAGE", message


    def checkUserName(self, userName):
        match = UserNameExp.match(userName)
        #print "CHECKUSERNAME", userName, match
        return match


    def setVirtualSpeed(self, virtualSpeed):
        print "setVirtualSpeed", virtualSpeed
        self.virtualSpeed = virtualSpeed
        speedConfiguration = SpeedConfigurations[virtualSpeed]
        #print "==== setVirtualSpeed", virtualSpeed, speedConfiguration
        self.loopsPerSecond = speedConfiguration['loopsPerSecond']
        self.maxLoopsPerPoll = speedConfiguration['maxLoopsPerPoll']
        simSpeed = speedConfiguration['speed']
        if self.simSpeed != simSpeed:
            #self.setSpeed(simSpeed)
            self.simSpeed = simSpeed
        #self.handle_update('delay')
        self.handle_update('virtualSpeed')


    def tickEngine(self):

        #print "TICKENGINE 1", "PAUSED", self.simPaused, "CITYTIME", self.cityTime

        now = time.time()
        fracTime = now - math.floor(now)

        self.blinkFlag = fracTime < 0.5

        if not self.simPaused:

            #print "NOW", now, "lastLoopTime", self.lastLoopTime
            elapsed = now - self.lastLoopTime
            self.lastLoopTime = now
            ticks = int(max(1, math.ceil(elapsed * self.loopsPerSecond)))
            #print "******** Loops per second", self.loopsPerSecond, "elapsed", elapsed, "ticks", ticks, "maxLoopsPerPoll", self.maxLoopsPerPoll
            ticks = min(ticks, self.maxLoopsPerPoll)

            #print "********", "TICKS", ticks, "ELAPSED", elapsed

            if self.simPasses != ticks:
                self.setPasses(ticks)

            #print "****", "PASSES", self.simPasses, "PAUSED", self.simPaused, "SPEED", self.simSpeed
            #print "CityTime", self.cityTime, "CityMonth", self.cityMonth, "CityYear", self.cityYear
            #print "simPaused", self.simPaused, "simPasses", self.simPasses, "simPass", self.simPass

            try:
                self.simTick()
            except Exception, e:
                print "SIMTICK EXCEPTION:", e

            self.animateTiles()

            #self.simUpdate()

            if not self.simPaused:
                self.updateMapView()

        #self.handle_update('tick')

        #print "TICKENGINE 2", "PAUSED", self.simPaused, "CITYTIME", self.cityTime

    ########################################################################
    # expectationFailed
    #
    # Report an unexpected error, given a message.
    #
    def expectationFailed(
        self,
        message):
        
        self.fatalError(
            417,
            message)

        
    ########################################################################
    # fatalError
    #
    # Report a fatal error, given a status code and a message.
    #
    def fatalError(
        self,
        status,
        message):
        
        raise cherrypy.HTTPError(
            status,
            message)


    def handlePoll(self, pollDict, session):

        #print "handlePoll", "PAUSED", self.simPaused, "CITYTIME", self.cityTime, "DICT", pollDict

        messages = pollDict.get('messages', None)
        if messages:
            for messageDict in messages:
                #print "MESSAGEDICT", messageDict
                self.handleMessage(session, messageDict)

        self.tickEngine()


    def renderTiles(
        self,
        ctx,
        tileSize,
        col, row,
        cols, rows,
        alpha):

        if False:
            self.tengine.renderTiles(
                ctx,
                self.tilesSurface,
                self.tilesWidth,
                self.tilesHeight,
                None,
                None, #self.tileMap,
                tileSize,
                col,
                row,
                cols,
                rows,
                alpha)
        else:
            self.renderTilesLazy(
                ctx,
                tileSize,
                col, row,
                cols, rows,
                alpha)


    def renderTilesLazy(
        self,
        ctx,
        tileSize,
        col, row,
        cols, rows,
        alpha):

        tileSizeCache = self.tileSizeCache
        d = tileSizeCache.get(tileSize, None)
        if not d:
            d = {
                'tileSize': tileSize,
                'tileCache': array.array('i', (0, 0, 0, 0,) * (self.tileCount)),
                'tileCacheSurfaces': [],
                'tileCacheCount': 0,
            }
            tileSizeCache[tileSize] = d

        self.tengine.renderTilesLazy(
            ctx,
            None,
            self.tileMap,
            tileSize,
            col,
            row,
            cols,
            rows,
            alpha,
            lambda tile: self.generateTile(tile, d),
            d['tileCache'],
            d['tileCacheSurfaces'],
            None)


    # This function is called from the C++ code in self.tengine.renderTilesLazy.
    # It renders a tile, and returns a tuple with a surface index, tile x and tile y position.
    # This function is totally in charge of the scaled tile cache, and can implement a variety
    # of different policies.
    def generateTile(
        self,
        tile,
        d):
        #print "======== GENERATETILE", tile, d

        try:
            tileSize = d['tileSize']
            #print "======== tileSize", tileSize

            # Get the various tile measurements.
            sourceTileSize = micropolisengine.EDITOR_TILE_SIZE
            tilesSurface = self.tilesSurface
            tilesCols = self.tilesCols
            maxSurfaceSize = 512

            # Calculate the measurements per surface, each of which contains one or more tiles,
            # depending on the tile size.
            # If the tiles are small, we will put a lot of them per surface, but as they get
            # bigger, we limit the size of the surface by reducing the number of tiles, so the
            # surfaces to not get too big.

            tileColsPerSurface = max(1, int(math.floor(maxSurfaceSize / tileSize)))
            #print "tileColsPerSurface", tileColsPerSurface

            tilesPerSurface = tileColsPerSurface * tileColsPerSurface
            #print "tilesPerSurface", tilesPerSurface

            surfaceSize = tileColsPerSurface * tileSize
            #print "surfaceSize", surfaceSize

            cacheTile = d['tileCacheCount']
            d['tileCacheCount'] += 1

            surfaceIndex = int(math.floor(cacheTile / tilesPerSurface))
            #print "surfaceIndex", surfaceIndex

            tileCacheSurfaces = d['tileCacheSurfaces']
            while len(tileCacheSurfaces) <= surfaceIndex:
                #print "MAKING SURFACE", len(tileCacheSurfaces), tilesPerSurface, surfaceSize
                surface = self.tileSurface.create_similar(cairo.CONTENT_COLOR, surfaceSize, surfaceSize)
                tileCacheSurfaces.append(surface)
                #print "DONE"

            surface = tileCacheSurfaces[surfaceIndex]
            tileOnSurface = cacheTile % tilesPerSurface
            #print "tileOnSurface", tileOnSurface
            tileCol = tileOnSurface % tileColsPerSurface
            tileRow = int(math.floor(tileOnSurface / tileColsPerSurface))
            #print "tileCol", tileCol, "tileRow", tileRow
            tileX = tileCol * tileSize
            tileY = tileRow * tileSize
            #print "tileX", tileX, "tileY", tileY
            sourceTileCol = tile % tilesCols
            sourceTileRow = int(math.floor(tile / tilesCols))
            #print "sourceTileCol", sourceTileCol, "sourceTileRow", sourceTileRow

            # Make a temporary tile the size of a source tile.
            tileCtx = self.tileCtx
            tileCtx.set_source_surface(
                self.tilesSurface,
                -sourceTileCol * sourceTileSize,
                -sourceTileRow * sourceTileSize)
            tileCtx.paint()

            tilesCtx = cairo.Context(surface)
            tilesCtx.set_source_surface(tilesSurface, 0, 0)

            # Scale it down into the tilesSurface.
            tilesCtx.save()

            x = tileCol * tileSize
            y = tileRow * tileSize

            tilesCtx.rectangle(
                x,
                y,
                tileSize,
                tileSize)
            tilesCtx.clip()

            # Try to keep the tiles centered.
            fudge = 0 # (0.5 * (scale - tileSize))

            x += fudge
            y += fudge

            tilesCtx.translate(
                x,
                y)

            #print "X", x, "Y", y, "FUDGE", fudge, "SCALE", scale, "TILESIZE", tileSize

            # Make it a pixel bigger to eliminate the fuzzy black edges.
            #zoomScale = float(tileSize) / float(sourceTileSize)
            zoomScale = float(tileSize) / float(sourceTileSize - 1.0)

            #print "ZOOMSCALE", zoomScale, "TILESIZE", tileSize, "SOURCETILESIZE", sourceTileSize

            tilesCtx.scale(
                zoomScale,
                zoomScale)

            tilesCtx.set_source_surface(
                self.tileSurface,
                -0.5,
                -0.5)
            tilesCtx.paint()

            tilesCtx.restore()

            #print "GENERATETILE", tile, "surfaceIndex", surfaceIndex, "tileX", tileX, "tileY", tileY

            result = (surfaceIndex, tileX, tileY)
            #print "GENERATETILE", tile, "RESULT", result
            return result

        except Exception, e:
            print "GENERATE TILE ERROR", e


    def getTileData(
        self,
        col, row,
        cols, rows,
        code,
        **kw):

        tiles = self.tengine.getTileData(
            None,
            self.tileMap,
            col, row,
            cols, rows,
            code,
            None)

        return tiles
    

    def updateAll(self):
        #print "UPDATEALL"
        self.handle_update('funds')
        self.handle_update('date')
        self.handle_update('history')
        self.handle_update('evaluation')
        self.handle_update('paused')
        self.handle_update('virtualSpeed')
        self.handle_update('demand')
        self.handle_update('options')
        self.handle_update('gamelevel')
        self.handle_update('cityname')
        self.updateMapView()


    def updateMapView(self):
        #print "UPDATEMAPVIEW"
        self.handle_update('map')


    def handle_autoGoto(self, x, y):
        #print "handle_autoGoto(self, x, y)", (self, x, y)
        self.sendSessions({
            'message': 'autoGoto',
            'x': x,
            'y': y,
            'collapse': true,
        })
    

    def handle_didGenerateNewCity(self):
        #print "handle_didGenerateNewCity(self)", (self,)
        self.sendSessions({
            'message': 'didGenerateNewCity',
        })
        self.updateMapView()

    
    def handle_didLoadCity(self):
        #print "handle_didLoadCity(self)", (self,)
        self.sendSessions({
            'message': 'didLoadCity',
        })
        self.updateMapView()

    
    def handle_didLoadScenario(self):
        #print "handle_didLoadScenario(self)", (self,)
        self.sendSessions({
            'message': 'didLoadScenario',
            'scenario': self.scenario,
        })
        self.updateMapView()


    def handle_didSaveCity(self):
        #print "handle_didSaveCity(self)", (self,)
        self.sendSessions({
            'message': 'didSaveCity',
        })

    
    def handle_didTool(self, name, x, y):
        #print "handle_didTool(self, name, x, y)", (self, name, x, y)
        self.sendSessions({
            'message': 'didTool',
            'name': name,
            'x': x,
            'y': y,
        })

    
    def handle_didntLoadCity(self, msg):
        #print "handle_didntLoadCity(self, msg)", (self, msg)
        self.sendSessions({
            'message': 'didntLoadCity',
            'msg': msg,
        })

    
    def handle_didntSaveCity(self, msg):
        #print "handle_didntSaveCity(self, msg)", (self, msg)
        self.sendSessions({
            'message': 'didntSaveCity',
            'msg': msg,
        })

    
    def handle_loseGame(self):
        #print "handle_loseGame(self)", (self,)
        self.sendSessions({
            'message': 'loseGame',
        })

    
    def handle_makeSound(self, channel, sound, x, y):
        #print "handle_makeSound(self, channel, sound)", (self, channel, sound, x, y)
        self.sendSessions({
            'message': 'makeSound',
            'channel': channel,
            'sound': sound,
            'x': x,
            'y': y,
        })


    def handle_newGame(self):
        #print "handle_newGame(self)", (self,)
        self.sendSessions({
            'message': 'newGame',
        })
        self.updateAll()

    
    def handle_playNewCity(self):
        #print "handle_playNewCity(self)", (self,)
        self.sendSessions({
            'message': 'playNewCity',
        })

    
    def handle_reallyStartGame(self):
        #print "handle_reallyStartGame(self)", (self,)
        self.sendSessions({
            'message': 'reallyStartGame',
        })

    
    def handle_saveCityAs(self):
        #print "handle_saveCityAs(self)", (self,)
        self.sendSessions({
            'message': 'saveCityAs',
        })

    
    def handle_showBudgetAndWait(self):
        #print "handle_showBudgetAndWait(self)", (self,)
        self.sendSessions({
            'message': 'showBudgetAndWait',
        })

    
    def handle_showPicture(self, id):
        #print "handle_showPicture(self, id)", (self, id)
        self.sendSessions({
            'message': 'showPicture',
            'id': id,
        })

    
    def handle_showZoneStatus(self, str, s0, s1, s2, s3, s4, x, y):
        #print "handle_showZoneStatus(self, str, s0, s1, s2, s3, s4, x, y)", (self, str, s0, s1, s2, s3, s4, x, y)
        self.sendSessions({
            'message': 'showZoneStatus',
            'str': str,
            's0': s0,
            's1': s1,
            's2': s2,
            's3': s3,
            's4': s4,
            'x': x,
            'y': y,
            'collapse': True,
        })

    
    def handle_startEarthquake(self, magnitude):
        #print "handle_startEarthquake(self, magnitude)", (self, magnitude,)
        self.sendSessions({
            'message': 'startEarthquake',
            'magnitude': magnitude,
        })

    
    def handle_startLoad(self):
        #print "handle_startLoad(self)", (self,)
        self.sendSessions({
            'message': 'startLoad',
        })

    
    def handle_startScenario(self, scenario):
        #print "handle_startScenario(self, scenario)", (self, scenario)
        self.sendSessions({
            'message': 'startScenario',
            'scenario': scenario,
        })

    
    def handle_stopEarthquake(self):
        #print "handle_stopEarthquake(self)", (self,)
        self.sendSessions({
            'message': 'stopEarthquake',
        })


    def handle_winGame(self):
        #print "handle_winGame(self)", (self,)
        self.sendSessions({
            'message': 'winGame',
        })


    def handle_update(self, variable, *args):
        #print "==== handle_update(self, variable, args)", self, "variable", variable, "args", args

        # Enrich the messages with parameters that the client will
        # need.  The args parameter is the variable length array of
        # arguments passed from the C++ MicropolisCore code with the
        # message.

        # @todo: Refactor update message code. 

        try:

            message = {
                'message': 'update',
                'variable': variable,
                'args': args,
            }

            if variable == 'funds':

                message['funds'] = self.totalFunds
                message['collapse'] = True

            elif variable == 'date':

                cityTime = self.cityTime
                startingYear = self.startingYear
                year = int(cityTime / 48) + startingYear
                month = int(cityTime % 48) >> 2

                message['cityTime'] = cityTime
                message['startingYear'] = startingYear
                message['year'] = year
                message['month'] = month
                message['collapse'] = True

            elif variable == 'XXXhistory':

                # Scale the residential, commercial and industrial histories
                # together relative to the max of all three.  Up to 128 they
                # are not scaled. Starting at 128 they are scaled down so the
                # maximum is always at the top of the history.

                def calcScale(maxVal):
                    if maxVal < 128:
                        maxVal = 0
                    if maxVal > 0:
                        return 128.0 / float(maxVal)
                    else:
                        return 1.0

                scales = []
                history = {
                    'scales': scales
                }
                message['history'] = history
                message['collapse'] = True

                cityTime = self.cityTime
                startingYear = self.startingYear
                year = int(cityTime / 48) + startingYear
                month = int(cityTime % 48) >> 2
                message['year'] = year
                message['month'] = month

                getHistoryRange = self.getHistoryRange
                getHistory = self.getHistory

                for historyScale in range(0, micropolisengine.HISTORY_SCALE_COUNT):

                    resHistoryMin, resHistoryMax = getHistoryRange(
                        micropolisengine.HISTORY_TYPE_RES,
                        historyScale)
                    comHistoryMin, comHistoryMax = getHistoryRange(
                        micropolisengine.HISTORY_TYPE_COM,
                        historyScale)
                    indHistoryMin, indHistoryMax = getHistoryRange(
                        micropolisengine.HISTORY_TYPE_IND,
                        historyScale)
                    allMax = max(resHistoryMax,
                                 max(comHistoryMax,
                                     indHistoryMax))
                    rciScale = calcScale(allMax)

                    # Scale the money, crime and pollution histories
                    # independently of each other.

                    moneyHistoryMin, moneyHistoryMax = getHistoryRange(
                        micropolisengine.HISTORY_TYPE_MONEY,
                        historyScale)
                    crimeHistoryMin, crimeHistoryMax = getHistoryRange(
                        micropolisengine.HISTORY_TYPE_CRIME,
                        historyScale)
                    pollutionHistoryMin, pollutionHistoryMax = getHistoryRange(
                        micropolisengine.HISTORY_TYPE_POLLUTION,
                        historyScale)
                    moneyScale = calcScale(moneyHistoryMax)
                    crimeScale = calcScale(crimeHistoryMax)
                    pollutionScale = calcScale(pollutionHistoryMax)

                    historyRange = 128.0

                    valueScales = (
                        rciScale, rciScale, rciScale, # res, com, ind
                        moneyScale, crimeScale, pollutionScale, # money, crime, pollution
                    )

                    valueRanges = (
                        (resHistoryMin, resHistoryMax,),
                        (comHistoryMin, comHistoryMax,),
                        (indHistoryMin, indHistoryMax,),
                        (moneyHistoryMin, moneyHistoryMax,),
                        (crimeHistoryMin, crimeHistoryMax,),
                        (pollutionHistoryMin, pollutionHistoryMax,),
                    )

                    histories = []

                    scales.append({
                        'historyScale': historyScale,
                        'range': 128,
                        'histories': histories,
                    })

                    for historyType in range(0, micropolisengine.HISTORY_TYPE_COUNT):

                        valueScale = valueScales[historyType]
                        valueRange = valueRanges[historyType]

                        values = [
                                getHistory(
                                    historyType,
                                    historyScale,
                                    historyIndex)
                                for historyIndex in range(micropolisengine.HISTORY_COUNT - 1, -1, -1)
                        ]

                        histories.append({
                            'historyType': historyType,
                            'valueScale': valueScale,
                            'valueRange': valueRange,
                            'values': values,
                        })

                #print message

            elif variable == 'evaluation':

                problems = []
                for i in range(0, self.countProblems()):
                    problems.append((
                        self.getProblemNumber(i),
                        self.getProblemVotes(i)))

                message.update({
                    'year': self.currentYear(),
                    'population': self.cityPop,
                    'migration': self.cityPopDelta,
                    'assessedValue': self.cityAssessedValue,
                    'category': self.cityClass,
                    'gameLevel': self.gameLevel,
                    'currentScore': self.cityScore,
                    'annualChange': self.cityScoreDelta,
                    'goodJob': self.cityYes,
                    'worstProblems': problems,
                    'collapse': True,
                })

            elif variable == 'paused':

                paused = self.simPaused and 'true' or 'false'
                message['paused'] = paused
                message['collapse'] = True

            elif variable == 'tick':

                pass # return

            elif variable == 'passes':

                return

            elif variable == 'speed':

                return

            elif variable == 'delay':

                virtualSpeed = self.virtualSpeed
                speedConfiguration = SpeedConfigurations[virtualSpeed]
                print 'UPDATE DELAY', self.virtualSpeed, speedConfiguration
                message['pollDelay'] = speedConfiguration['pollDelay']
                message['animateDelay'] = speedConfiguration['animateDelay']
                message['collapse'] = True

            elif variable == 'demand':

                resDemand, comDemand, indDemand = self.getDemands()
                message['resDemand'] = resDemand
                message['comDemand'] = comDemand
                message['indDemand'] = indDemand
                message['collapse'] = True
                #print '======== DEMAND', message

            elif variable == 'options':

                pass # TODO: copy options to message
                message['collapse'] = True

            elif variable == 'gameLevel':

                message['gameLevel'] = self.gameLevel
                message['collapse'] = True

            elif variable == 'cityName':

                message['cityName'] = self.cityName
                message['collapse'] = True

            elif (variable == 'budget') or (variable == 'taxRate'):

                message['taxRate'] = self.cityTax
                message['totalFunds'] = self.totalFunds
                message['taxFund'] = self.taxFund

                message['firePercent'] = math.floor(self.firePercent * 100.0)
                message['fireFund'] = self.fireFund
                message['fireValue'] = self.fireValue

                message['policePercent'] = math.floor(self.policePercent * 100.0)
                message['policeFund'] = self.policeFund
                message['policeValue'] = self.policeValue

                message['roadPercent'] = math.floor(self.roadPercent * 100.0)
                message['roadFund'] = self.roadFund
                message['roadValue'] = self.roadValue

                message['cashFlow'] = (
                    message['taxFund'] -
                    message['fireValue'] -
                    message['policeValue'] -
                    message['roadValue']
                )

                message['previousFunds'] = message['totalFunds']
                message['currentFunds'] = message['cashFlow'] + message['totalFunds']
                message['taxesCollected'] = message['taxFund']

                message['collapse'] = True

                #print 'BUDGET', message

            elif variable == 'message':

                # Do no collapse messages.
                message['number'] = args[0]
                message['x'] = args[1]
                message['y'] = args[2]
                message['picture'] = args[3]
                message['important'] = args[4]
                message['args'] = None

            elif variable == 'virtualSpeed':

                #print 'VIRTUALSPEED', self, type(self), getattr(self, 'virtualSpeed', '???')
                virtualSpeed = self.virtualSpeed
                speedConfiguration = SpeedConfigurations[virtualSpeed]
                message['virtualSpeed'] = virtualSpeed
                message['pollDelay'] = speedConfiguration['pollDelay']
                message['animateDelay'] = speedConfiguration['animateDelay']
                message['collapse'] = True

            # Clean up the args parameter, which is usually empty, so
            # we don't send it unnecessarily.
            if 'args' in message:
                del message['args']

            self.sendSessions(message)

        except Exception, e:
            print '======== XXX handle_update ERROR:', e
            traceback.print_exc(10)


########################################################################


def CreateTurboGearsEngine(**params):

    # Get our nice scriptable subclass of the SWIG Micropolis wrapper object.
    engine = MicropolisTurboGearsEngine(**params)

    return engine


########################################################################