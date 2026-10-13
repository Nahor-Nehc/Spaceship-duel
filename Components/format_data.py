def unformat_data(str_):
    str_ = str_.split(",")
    return [int(x) for x in str_]

def format_data(list_):
    return ",".join([str(x) for x in list_])

def convert_initial_message(arg):
    if type(arg) == str:
        return unformat_data(arg)
    elif type(arg) == list:
        return format_data(arg)
    else:
        raise ValueError("Argument not string or list type")

def iterable_to_csv_string(iterable):
    return ",".join([str(x) for x in list(iterable)])

def csv_string_to_iterable(string) -> list[tuple[int, int]]:
    """only for a string of a list of integers"""
    #                                                                                                string = "(1, 2),(3, 4),(5, 6),(7, 8)"
    a = string.split("),")                                                 # a = ['(1, 2', '(3, 4', '(5, 6', '(7, 8)']
    a = [a[x][1:] for x in range(len(a))]                    # a = ['1, 2', '3, 4', '5, 6', '7, 8)']
    a[-1] = a[-1][:-1]                                                         # a = ['1, 2', '3, 4', '5, 6', '7, 8']
    b = [tuple(map(int, x.split(","))) for x in a] # b = [(1, 2), (3, 4), (5, 6), (7, 8)]
    return b

def build_server_reply(current_player, spaceship_positions, bullets, ammo, sb_charge):
    enemy_number = int(not current_player)
    ship = iterable_to_csv_string(spaceship_positions[enemy_number]) #"0,0,76,32"
    bullet_enemy = iterable_to_csv_string(bullets[current_player].get_bullets())     #"(1, 2),(3, 4)"
    bullet_player = iterable_to_csv_string(bullets[enemy_number].get_bullets())        #"(1, 2),(3, 4)"
    enemy_ammo = str(ammo[enemy_number])                                                         #"3.0"
    enemy_sb_charge = str(sb_charge[enemy_number])                                     #"6.0"
    
    reply = "|".join([ship, bullet_enemy, bullet_player, enemy_ammo, enemy_sb_charge])
    # "0,0,76,32|(1, 2),(3, 4)|(1, 2),(3, 4)|3.0|6.0"
    return reply

def unpack_server_reply(string) -> tuple[tuple, list[tuple[int, ...]], list[tuple[int, ...]], float, float]:
    #string = "0,0,76,32|(1, 2),(3, 4)|(1, 2),(3, 4)|3.0|6.0"
    ship, bullet_enemy, bullet_player, enemy_ammo, enemy_sb_charge = string.split("|")
    ship = tuple(ship.split(","))
    if not bullet_enemy:
        bullet_enemy = ()
    else:
        bullet_enemy = csv_string_to_iterable(bullet_enemy)
    if not bullet_player:
        bullet_player = ()
    else:
        bullet_player = csv_string_to_iterable(bullet_player)
    enemy_ammo = float(enemy_ammo)
    enemy_sb_charge = float(enemy_sb_charge)
    
    return ship, bullet_enemy, bullet_player, enemy_ammo, enemy_sb_charge

def build_client_reply(ship_position, bullet_created):
    # ship_position = (x, y, width, height)
    # bullet_created = (x, y)
    ship_position = iterable_to_csv_string(ship_position)
    if bullet_created == tuple():
        bullet_created = ""
    else:
        bullet_created = iterable_to_csv_string(bullet_created)
    
    reply = "|".join([ship_position, bullet_created])
    return reply
    
def unpack_client_reply(string):
    ship_position, bullet_created = string.split("|")
    ship_position = tuple(map(int, ship_position.split(",")))
    try:
        bullet_created = tuple(map(int, bullet_created.split(",")))
    except ValueError:
        print("no bullet created")
        bullet_created = ()
        
    return ship_position, bullet_created