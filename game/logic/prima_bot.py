import random
from typing import Optional, List
from game.logic.base import BaseLogic
from game.models import GameObject, Board, Position
from ..util import get_direction


class Prima(BaseLogic):
    def __init__(self):
        # inisiasi data awal
        self.directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.goal_position: Optional[Position] = None
        self.current_direction = 0

    ##############################################
    #Batas Meng-tactile maks 3 langkah doang     #
    ##############################################
        self.blacklist_targets = {}  
        self.blacklist_duration = 10 
        self.max_chase_steps = 3  # maks 3 langkaah lepas
        self.current_chase_target = None
        self.current_chase_steps = 0

    ##############################################
    # menghitung jarak manhattan antara dua titik #
    ##############################################
    def needed_steps(self, starting_pos: Position, diamond_pos: Position) -> int:
        return abs(starting_pos.x - diamond_pos.x) + abs(starting_pos.y - diamond_pos.y)

    ####################################################
    # menghitung kepadatan suatu efisiensi suatu objek #
    ####################################################
    # membagi point dari objek tersebut lalu dibagi dengan step yang dibutuhkan untuk menuju objek tersebut
    def get_density(self, diamond: GameObject, bot_pos: Position) -> float:
        return diamond.properties.points / self.needed_steps(bot_pos, diamond.position)

    #################################################################################
    # mencari diamond dengan kepadatan efisiensi tertinggi dan menjadikannya tujuan #
    #################################################################################
    def generate_best_density(
        self,
        diamonds: List[GameObject],
        board_bot: GameObject,
        start_teleporter_position: Position,
        end_teleporter_position: Position,
        distance_to_targetTeleporter: int,
    ) -> None:
        curr_density_max = 0
        curr_density_max_pos = diamonds[0].position
        bot_position = board_bot.position

        best_direct = (0, None)
        best_teleport = (0, None)

        for diamond in diamonds:
            d = self.get_density(diamond, bot_position)
            if d > best_direct[0]:
                best_direct = (d, diamond.position)

            td = diamond.properties.points / (
                distance_to_targetTeleporter + self.needed_steps(diamond.position, end_teleporter_position)
            )
            if td > best_teleport[0]:
                best_teleport = (td, start_teleporter_position)

        # Pilih yang paling tinggi di antara keduanya
        if best_direct[0] >= best_teleport[0]:
            self.goal_position = best_direct[1]
        else:
            self.goal_position = best_teleport[1]

    ################################
    # menghitung jarak bot ke base #
    ################################
    def basedistance(self, board_bot: GameObject):
        # mencari jarak bot dengan base
        current_position = board_bot.position
        base = board_bot.properties.base
        return abs(base.x - current_position.x) + abs(base.y - current_position.y)

    #############################
    # logic gerakan selanjutnya #
    #############################
    def next_move(self, board_bot: GameObject, board: Board) -> tuple:
        props = board_bot.properties
        base = props.base
        list_diamonds = board.diamonds
        current_position = board_bot.position

        #############################
        # menginisiasi teleporter    #
        #############################
        list_teleporters = [d for d in board.game_objects if d.type == "TeleportGameObject"]
        marco = list_teleporters[0]
        polo = list_teleporters[1]
        targetTeleporter = marco
        exitTeleporter = polo

        # -- cari jarak manhattan dan simpan ke variable -- #
        dm = self.needed_steps(marco.position, current_position)
        dp = self.needed_steps(polo.position, current_position)

        # -- ubah teleporter terdekat dan terjauh sesuai posisi saat ini -- #
        if dp < dm:
            targetTeleporter = polo
            exitTeleporter = marco

        diamond_button = [d for d in board.game_objects if d.type == "DiamondButtonGameObject"]
        distance_to_targetTeleporter = self.needed_steps(targetTeleporter.position, current_position)

        ##########################
        # logic move selanjutnya  #
        ##########################
        # -- logika kembali ke rumah -- #
        if props.diamonds >= 3 or (
            props.milliseconds_left < (1000 * self.needed_steps(base, board_bot.position) + 2000)
            and props.milliseconds_left < 8000
        ):  # stack diamond yang dipegang cukup 3 saja agar tidak terlalu beresiko
            teleporter_base_distance = self.needed_steps(exitTeleporter.position, base)
            td = teleporter_base_distance + distance_to_targetTeleporter
            distanceBotBase = self.needed_steps(base, current_position)

            # -- jika jarak bot ke rumah menggunakan teleport lebih dekat dibandingkan jarak yang tanpa teleport, masuk teleport -- #
            if td < distanceBotBase and distance_to_targetTeleporter != 0:
                delta_x, delta_y = get_direction(
                    current_position.x,
                    current_position.y,
                    targetTeleporter.position.x,
                    targetTeleporter.position.y,
                )
                return delta_x, delta_y
            else:
                self.goal_position = base

        # -- logika jika diamond sudah sedikit (di bawah 3) dan jarak ke diamond lebih kecil dibanding jarak ke reset button maka ubah arah tujuan ke reset button -- #
        elif (
            len(list_diamonds) < 3
            and self.goal_position is not None
            and self.needed_steps(board_bot.position, self.goal_position) > self.needed_steps(diamond_button[0].position, board_bot.position)
        ):
            self.goal_position = diamond_button[0].position

        # -- logika jika diamond, teleporter atau memang tidak ada tujuan maka buat tujuan -- #
        elif (
            all(self.goal_position != diamond.position for diamond in list_diamonds)
            or all(targetTeleporter.position != teleporter.position for teleporter in list_teleporters)
            or self.goal_position is None
        ):
            self.generate_best_density(list_diamonds, board_bot, targetTeleporter.position, exitTeleporter.position, distance_to_targetTeleporter)

        # -- logika jika lewat base ketika mencari diamond, akan kembali ke base -- #
        elif (self.basedistance(board_bot) == 2 and props.diamonds > 2) or (self.basedistance(board_bot) == 1 and props.diamonds > 0):
            self.goal_position = base

        ############
        # override #
        ############
        # jika terjadi keadaan tertentu maka goal sekarang akan di override atau di tumpuk oleh goal yang lebih baik

        # -- logika jika bot menuju rumah dan ketika diperjalanan sejauh 1 petak ada diamond dan storage < 5, maka akan mengambil diamond tersebut -- #
        if self.goal_position == base and props.diamonds < 5:
            for diamond in list_diamonds:
                if self.needed_steps(current_position, diamond.position) == 1:
                    self.goal_position = diamond.position
                    break

        ########################################
        # logic mengejar dan membunuh bot musuh #
        ########################################
        bots = [obj for obj in board.game_objects if obj.type == "BotGameObject"]

        chased_this_turn = False  # cek apakah bot mengejar target sekarang

        for bot in bots:
            if bot.properties.name != board_bot.properties.name:
                if bot.properties.diamonds == 0: #jika bot musuh tidak membawa diamond, skipaja
                    continue

                dist = self.needed_steps(current_position, bot.position)
                if bot.properties.name in self.blacklist_targets:
                    self.blacklist_targets[bot.properties.name] += 1
                    if self.blacklist_targets[bot.properties.name] > self.blacklist_duration:
                        del self.blacklist_targets[bot.properties.name] 
                    continue

                if dist == 1 or (dist < 3 and bot.properties.diamonds > 2):
                    if self.current_chase_target == bot.properties.name:
                        self.current_chase_steps += 1
                    else:
                        self.current_chase_target = bot.properties.name
                        self.current_chase_steps = 1

                    # Jika sudah terlalu lama mengejar target yang sama, blacklist target
                    if self.current_chase_steps > self.max_chase_steps:
                        self.blacklist_targets[bot.properties.name] = 0
                        print(f"Meninggalkan pengejaran bot musuh {bot.properties.name} karena terlalu lama tidak tackle.")
                        self.current_chase_target = None
                        self.current_chase_steps = 0
                        continue

                    delta_x, delta_y = get_direction(current_position.x, current_position.y, bot.position.x, bot.position.y)
                    print(f"Mengejar bot musuh: {bot.properties.name} di {bot.position}")
                    chased_this_turn = True
                    return delta_x, delta_y

        # Reset target pengejaran jika tidak mengejar siapapun
        if not chased_this_turn:
            self.current_chase_target = None
            self.current_chase_steps = 0

        # Jika tidak ada kondisi khusus, gerak ke goal_position yang sudah ditentukan
        if self.goal_position:
            delta_x, delta_y = get_direction(current_position.x, current_position.y, self.goal_position.x, self.goal_position.y)
            return delta_x, delta_y

        # Jika goal_position belum ditentukan, tetap diam (0,0)
        return 0, 0
