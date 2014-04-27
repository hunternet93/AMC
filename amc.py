#!/usr/bin/env python3
# Artemis Mission Compiler: https://github.com/hunternet93/AMC
# by Isaac Smith
# Released under the MIT license, please see LICENSE for more info

import sys, random, copy
import xml.etree.cElementTree as ET
from bunch import *

class AddList(list):
    def add(self, *items): [self.append(item) for item in items]

Mission = lambda: Bunch(tag = 'mission', start = AddList(), events = AddList())
Event = lambda name, f='all': Bunch(name = name, tag = 'event', fire = f, conditions = AddList(), actions = AddList())
Tag = lambda tag, **args: Bunch(tag = tag, **args)

SetVariable = lambda name, value: Bunch(tag = 'set_variable', name = name, value = value)
SetTimer = lambda name, seconds: Bunch(tag = 'set_timer', name = name, seconds = seconds)
SetObjectProperty = lambda name, property, value: Bunch(tag = 'set_object_property', name = name, property = property, value = value)
AddToObjectProperty = lambda name, property, value: Bunch(tag = 'addto_object_property', name = name, property = property, value = value)
CopyObjectProperty = lambda name1, name2, value: Bunch(tag = 'copy_object_property', name1 = name1, name2 = name2, value = value)
SetFleetProperty = lambda fleetIndex, property, value: Bunch(tag = 'set_fleet_property', fleetIndex = fleetIndex, property = property, value = value)
ClearAI = lambda name: Bunch(tag = 'clear_ai', name = name)
AddAI = lambda name, type, **args: Bunch(tag = 'add_ai', name = name, type = type, **args)
EndMission = lambda: Bunch(tag = 'end_mission')
BigMessage = lambda title, subtitle1 = '', subtitle2 = '': Bunch(tag = 'big_message', title = title, subtitle1 = subtitle1, subtitle2 = subtitle2)
IncomingCommsText = lambda from_, body: Bunch(tag = 'incoming_comms_text', from_ = from_, body = body)
Destroy = lambda name: Bunch(tag = 'destroy', name = name)
Log = lambda text: bunch(tag = 'log', text = text)

IfVariable = lambda name, comparator, value: Bunch(tag = 'if_variable', name = name, comparator = comparator, value = value)
IfTimerFinished = lambda name: Bunch(tag = 'if_timer_finished', name = name)
IfExists = lambda name: Bunch(tag = 'if_exists', name = name)
IfNotExists = lambda name: Bunch(tag = 'if_not_exists', name = name)
IfInsideBox = lambda name, leastX, leastZ, mostX, mostZ: Bunch(tag = 'if_inside_box', name = name, leastX = leastX, leastZ = leastZ, mostX = mostX, mostZ = mostZ)
IfOutsideBox = lambda name, leastX, leastZ, mostX, mostZ: Bunch(tag = 'if_outside_box', name = name, leastX = leastX, leastZ = leastZ, mostX = mostX, mostZ = mostZ)
IfInsideSphere = lambda name, centerX, centerY, centerZ, radius: Bunch(tag = 'if_inside_sphere', name = name, centerX = centerX, centerY = centerY, centerZ = centerZ, radius = radius)
IfOutsideSphere = lambda name, centerX, centerY, centerZ, radius: Bunch(tag = 'if_outside_sphere', name = name, centerX = centerX, centerY = centerY, centerZ = centerZ, radius = radius)
IfDistance = lambda name1, name2, comparator, value: Bunch(tag = 'if_distance', name1 = name1, name2 = name2, comparator = comparator, value = value)
IfDamconMembers = lambda team_index, comparator, value: Bunch(tag = 'if_damcom_members', team_index = team_index, comparator = comparator, value = value)
IfDifficulty = lambda comparator, value: Bunch(tag = 'if_difficulty', comparator = comparator, value = value)
IfFleetCount = lambda fleetnumber, comparator, value: Bunch(tag = 'if_fleet_count', fleetnumber = fleetnumber, comparator = comparator, value = value)
IfEnemyCount = lambda comparator, value: Bunch(tag = 'if_fleet_count', comparator = comparator, value = value)
IfDocked = lambda name: Bunch(tag = 'if_docked', name = name)
IfPlayerIsTargeting = lambda name: Bunch(tag = 'if_player_is_targeting', name = name)
IfObjectProperty = lambda name, property, comparator, value: Bunch(tag = 'if_object_property', name = name, property = property, comparator = comparator, value = value)

Player = lambda name, **args: Bunch(name = name, tag = 'create', type = 'player', **args)
Enemy = lambda name, **args: Bunch(name = name, tag = 'create', type = 'enemy', **args)
Station = lambda name, **args: Bunch(name = name, tag = 'create', type = 'station', **args)
Neutral = lambda name, **args: Bunch(name = name, tag = 'create', type = 'neutral', **args)
Anomaly = lambda name, **args: Bunch(name = name, tag = 'create', type = 'anomaly', **args)
BlackHole = lambda name, **args: Bunch(name = name, tag = 'create', type = 'blackhole', **args)
Monster = lambda name, **args: Bunch(name = name, tag = 'create', type = 'monster', **args)
GenericMesh = lambda name, **args: Bunch(name = name, tag = 'create', type = 'genericmesh', **args)
Whale = lambda name, **args: Bunch(name = name, tag = 'create', type = 'whale', **args)
Nebulas = lambda **args: Bunch(tag = 'create', type = 'nebulas', **args)
Asteroids = lambda **args: Bunch(tag = 'create', type = 'asteroids', **args)
Mines = lambda **args: Bunch(tag = 'create', type = 'mines', **args)

def create_tag(item, parent):
    tag = ET.SubElement(parent, item.pop('tag'))
    if item.get('body'): 
        tag.text = item.pop('body')

    for argument in item.items():
        tag.set(str(argument[0]).replace('_', ""), str(argument[1]))

def create_entity(item, parent):
    entity = ET.SubElement(parent, item.pop('tag'))
    entity.set('type', item.pop('type'))

    if item.get('properties'):
        properties = item.pop('properties')
    else:
        properties = False

    if item.get('ai'):
        ai = item.pop('ai')
    else:
        ai = False

    for attribute in item.items():
        entity.set(str(attribute[0]), str(attribute[1]))

    if ai:
        ET.SubElement(parent, 'clear_ai').set('name', name)
        for block in ai:
            add_ai = ET.SubElement(parent, 'add_ai')
            add_ai.set('name', name)
            for argument in command.items():
                add_ai.set(str(argument[0]), str(argument[1]))


def parse_items(items, parent):
    for item in items:
        if item.tag == 'create':
            create_entity(item, parent)
        else:
            create_tag(item, parent)


def parse_event(event, parent):
    tag = ET.SubElement(parent, 'event')

    if event['fire'] == 'once':
        event.conditions.add(IfVariable(event.name + '_triggered', '!=', 1))
        event.actions.add(SetVariable(event.name + '_triggered', 1))

    for condition in event.conditions:
        create_tag(condition, tag)

    parse_items(event.actions, tag)

def parse(mission):
    root = ET.Element('mission')
    root.set('version', '1')
    
    start = ET.SubElement(root, 'start')
    parse_items(mission.start, start)

    if mission.get('events'):
        for event in mission['events']:
            parse_event(event, root)

    return ET.tostring(root)

if __name__ == "__main__":
    if not len(sys.argv) >= 2:
        print('Usage: amc.py mission.amc.py <mission.xml>')
        quit()
    else:
        mission_file = open(sys.argv[1], "r")
        if len(sys.argv) == 3:
            output = open(sys.argv[2], "w")
        else:
            output = sys.stdout

    mission = Mission()
    start = mission.start
    events = mission.events
    exec(mission_file.read(), globals())
    output.write(parse(mission).decode())
    output.write("\n")
    output.close()
