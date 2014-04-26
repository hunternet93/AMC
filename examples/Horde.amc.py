enemies = 50 # Total amount of enemy ships
enemy_time = [15, 45] # Range of random times between enemy ships appearing
enemy_raceKeys = 'Kralien enemy'
enemy_hullKeys = 'small warship'
enemy_name = 'K'
enemy_x, enemy_z, enemy_y = [1000, 99000], [500, 5000], [-500, 500]
enemy_angle = 180

start.add(Player('Artemis',x=50000,z=50500,y=0,angle=0),
    Station('DS1', x=50000,z=50000,y=0,angle=0, raceKeys = 'TSN friendly', hullKeys = 'base'))

for enemy in range(1, enemies+1):
    name = enemy_name + str(enemy)
    event = Event('enemy ' + str(enemy), 'once')
    event.triggers.add(IfTimerFinished('enemy ' + str(enemy) + ' timer'))
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
event.triggers.add(IfEnemyCount('=', 0))
event.actions.add(BigMessage('Misson Complete', 'Good work, Artemis.'),
                  EndMission())
events.add(winevent)

for obj in ['Artemis', 'DS1']:
    event = Event(obj + ' destroyed', 'once')
    event.triggers.add(IfNotExists(obj))
    event.actions.add(BigMessage('Mission Failed', obj + ' Has Been Destroyed'),
                      EndMission())
    events.add(event)
