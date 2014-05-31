enemies = 50 # Total amount of enemy ships
enemy_time = [10, 30] # Range of random times between enemy ships appearing
enemy_raceKeys = 'Kralien enemy'
enemy_hullKeys = 'small warship'
enemy_name = 'K'
enemy_x, enemy_z, enemy_y = [1000, 99000], [500, 5000], [-500, 500]
enemy_angle = 180

start.add(Player('Artemis',x=50000,z=48000,y=0,angle=0),
    Station('DS1', x=50000,z=50000,y=0,angle=0, raceKeys = 'TSN friendly', hullKeys = 'base'),
    SetTimer('enemy 1 timer', 10),
    BigMessage('Horde','Defend DS1 from the Kralien horde', 'by Isaac Smith'))

for enemy in range(1, enemies+1):
    name = enemy_name + str(enemy)
    event = Event('enemy ' + str(enemy), 'once')
    event.conditions.add(IfTimerFinished('enemy ' + str(enemy) + ' timer'))
    event.actions.add(Enemy(name, x=random.randint(*enemy_x), z=random.randint(*enemy_z), y=random.randint(*enemy_y), angle=enemy_angle,
                            hullKeys=enemy_hullKeys, raceKeys=enemy_raceKeys),
                      ClearAI(name),
                      AddAI(name, 'TRY_TO_BECOME_LEADER'),
                      AddAI(name, 'CHASE_STATION', value1=100000),
                      AddAI(name, 'CHASE_PLAYER', value1=20000),
                      AddAI(name, 'CHASE_ANGER'),
                      SetTimer('enemy ' + str(enemy+1) + ' timer', random.randint(*enemy_time)))
    events.add(event)

winevent = Event('you win!', 'once')
winevent.conditions.add(IfEnemyCount('=', 0),
                        IfVariable('enemy 50_triggered', '=', 1))
winevent.actions.add(BigMessage('Misson Complete', 'Good work, Artemis.'),
                     SetTimer('end timer', 7))
events.add(winevent)

for obj in ['Artemis', 'DS1']:
    event = Event(obj + ' destroyed', 'once')
    event.conditions.add(IfNotExists(obj))
    event.actions.add(BigMessage('Mission Failed', obj + ' Has Been Destroyed'),
                      SetTimer('end timer', 7))
    events.add(event)

endevent = Event('end', 'once')
endevent.conditions.add(IfTimerFinished('end timer'))
endevent.actions.add(EndMission())
events.add(endevent)

cheatevent = Event('bwa ha ha', 'once')
cheatevent.conditions.add(IfDifficulty('=', 11))
cheatevent.actions.add(SetObjectProperty('Artemis', 'countNuke', 50),
                       SetObjectProperty('Artemis', 'countECM', 25),
                       SetObjectProperty('Artemis', 'energy', 2000),
                       SetObjectProperty('Artemis', 'totalCoolant', 100))
events.add(cheatevent)

cheatrefuelevent = Event('refuel', 'all')
cheatrefuelevent.conditions.add(IfDifficulty('=', 11),
                          IfObjectProperty('Artemis', 'energy', 'LESS', 500))
cheatrefuelevent.actions.add(SetObjectProperty('Artemis', 'energy', 2000))
events.add(cheatrefuelevent)
