Artemis Mission Compiler
========================

Artemis Mission Compiler (AMC) is a mission script generation tool for Artemis: Spaceship Bridge Compiler. It requires only Python 3 to run.

Usage:
    python3 amc.py mission.amc.py <mission.xml>

Tutorial
--------

AMC scripts are written in the Python programming language, familiarity with Python and with Artemis mission scripting is recommended.

A minimal example script:

    start.add(Player('Artemis', x = 50000, y = 0, z = 50000, angle = 0),
              Enemy('Simetra', x = 50500, y = 0, z = 50000, angle = 180))
    
    event = Event('enemy destroyed', 'once')
    event.conditions.add(IfNotExists('Simetra'))
    event.actions.add(BigMessage('Mission Complete'),
                      EndMission())
    events.add(event)
    
    event = Event('artemis destroyed', 'once')
    event.conditions.add(IfNotExists('Artemis'))
    event.actions.add(BigMessage('Mission Failed'),
                      EndMission())

In AMC, actions such as creating a ship, displaying a message, or ending the mission are added to events. Events are created from the Event generator:

    event = Event(event name, fire mode)

An event's fire mode can be set to 'all', which causes the event to be run every time the event's conditions are met, or to 'once', which causes the event to be run once only.

An event's conditions determine when the event will be run, AMC supports all if-conditions supported by Artemis. To add an condition:

    event.conditions.add(IfVariable('variable', '=', 'value'))

An event's actions will be performed when the event's conditions are met.

    event.actions.add(Destroy('Simetra'))

Once an event is defined, it is added to the events variable:

    events.add(event)

The start event is a special event that is run at the start of the game:

    start.add(Station('DS1', x=100,z=100,y=0,raceKeys='friendly',hullKeys='friendly'))

At the time of this writing, not all of Artemis' actions have been added to AMC. Any action can be added with the Tag object:

    Tag('play_sound_now', filename = 'sound.wav')

Credits
-------

The Bunch library heavily used in AMC was created by David Schoonover: https://github.com/dsc/bunch/tree/master/bunch
Artemis is created by Thom Robertson: http://www.artemis.eochu.com/
