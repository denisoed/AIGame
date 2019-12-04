import model


class MyStrategy:
    def __init__(self):
        self.health_packs = []

    def get_health_packs(self, game):
        if len(self.health_packs) == 0:
            for box in game.loot_boxes:
                if type(box.item) == model.item.HealthPack:
                    self.health_packs.append(box)

    def get_nearest_health_pack(self, user_pos):
        for pack in self.health_packs:
            # Найти минимальное число
            print(round(pack.position.x, 1), round(user_pos.x, 1))

    def get_unit_health(self, unit):
        if unit.health < 55:
            nearest_health = self.get_nearest_health_pack(unit.position)

        # if unit.health < 50:
    def get_action(self, unit, game, debug):
        self.get_health_packs(game)
        self.get_unit_health(unit)
        # Replace this code with your own
        def distance_sqr(a, b):
            return (a.x - b.x) ** 2 + (a.y - b.y) ** 2
        nearest_enemy = min(
            filter(lambda u: u.player_id != unit.player_id, game.units),
            key=lambda u: distance_sqr(u.position, unit.position),
            default=None)
        nearest_weapon = min(
            filter(lambda box: isinstance(
                box.item, model.Item.Weapon), game.loot_boxes),
            key=lambda box: distance_sqr(box.position, unit.position),
            default=None)
        target_pos = unit.position
        if unit.weapon is None and nearest_weapon is not None:
            target_pos = nearest_weapon.position
        elif nearest_enemy is not None:
            target_pos = nearest_enemy.position
        debug.draw(model.CustomData.Log("Target pos: {}".format(target_pos)))
        aim = model.Vec2Double(0, 0)
        if nearest_enemy is not None:
            aim = model.Vec2Double(
                nearest_enemy.position.x - unit.position.x,
                nearest_enemy.position.y - unit.position.y)
        jump = target_pos.y > unit.position.y
        if target_pos.x > unit.position.x and game.level.tiles[int(unit.position.x + 1)][int(unit.position.y)] == model.Tile.WALL:
            jump = True
        if target_pos.x < unit.position.x and game.level.tiles[int(unit.position.x - 1)][int(unit.position.y)] == model.Tile.WALL:
            jump = True
        return model.UnitAction(
            velocity=target_pos.x - unit.position.x,
            jump=jump,
            jump_down=not jump,
            aim=aim,
            shoot=False,
            reload=False,
            swap_weapon=False,
            plant_mine=False)
