import pytmx
import pyscroll
import pygame
import random
from dataclasses import dataclass

from player import NPC

white = (255, 255, 255)


@dataclass
class Portal:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str


@dataclass
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portal]
    npcs: list[NPC]


class MapManager:
    def __init__(self, screen, player):
        self.maps = dict()
        self.snow = "snow"
        self.current_map = "world"
        self.screen = screen
        self.player = player
        # enregistrer le monde par défaut
        self.register_map("world", portals=[Portal(from_world="world", origin_point="enter_house", target_world="house",
                                                   teleport_point="spawn_house"),
                                            Portal(from_world="world", origin_point="enter_house2",
                                                   target_world="house2",
                                                   teleport_point="spawn_house"),

                                            Portal(from_world="world", origin_point="enter_dungeon",
                                                   target_world="dungeon",
                                                   teleport_point="spawn_dungeon"),

                                            Portal(from_world="world", origin_point="go_snow",
                                                   target_world="snow",
                                                   teleport_point="spawn_snow")],
                          npcs=[NPC("paul", nb_points=4, dialog=["Le professeur Agassa n'est pas là",
                                                                 "Il reviendra de Osaka demain avec Kudo", ]),
                                NPC("robin", nb_points=2, dialog=["Il y a un homme en noir dans le donjon"])])

        self.register_map("house", portals=[Portal(from_world="house", origin_point="exit_house", target_world="world",
                                                   teleport_point="enter_house_exit"),
                                            Portal(from_world="house", origin_point="etage_sup",
                                                   target_world="etage2",
                                                   teleport_point="etage_spawn")],

                          npcs=[NPC("hom1", nb_points=4,
                                    dialog=["Bienvenue chez moi oh oh oh !", "Tu dois être Nathan"])])

        self.register_map("house2", portals=[
            Portal(from_world="house2", origin_point="exit_house", target_world="world",
                   teleport_point="exit_house2")])

        self.register_map("dungeon", portals=[
            Portal(from_world="dungeon", origin_point="exit_dungeon", target_world="world",
                   teleport_point="dungeon_exit_spawn")],
                          npcs=[NPC("boss", nb_points=2, dialog=["Gin veut que je t'élimine sale petit détetive",
                                                                 "Tu ne découvriras jamais qui est le boss",
                                                                 "dis Adieu à ce monde Bwhahaahahaha!"])])
        self.register_map("etage2", portals=[
            Portal(from_world="etage2", origin_point="return_back", target_world="house", teleport_point="return_point")
        ],
                          npcs=[NPC("reception", nb_points=2, dialog=["Votre chambre est prête monsieur"])])
        self.register_map("snow", portals=[
            Portal(from_world="snow", origin_point="go_world", target_world="world", teleport_point="return_world"),
            Portal(from_world="snow", origin_point="go_mountain", target_world="mountain",
                   teleport_point="spawn_mountain")

        ], npcs=[NPC("bike1", nb_points=2, dialog=["BIENVENUE A SNOWLAND ",
                                                   "LA VILLE DE LA NEIGE ICI IL NEIGE 5JOURS SUR 7",
                                                   "GO SNOW GO !"]),
                 NPC("sasuke", nb_points=2, dialog=["Je m'appelle Sasuke Uchiwa", "Tremble devant moi!",
                                                    "Non je plaisante je sui juste un fan d'animé",
                                                    " et de manga faisant du sport "]),
                 NPC("hawk", nb_points=2,
                     dialog=["Mon nom est Sun-Zéro", "Je crois qu'on peut dire que je brille de mille feu",
                             "AH AH AHA AHAH"]),
                 NPC("hom2", nb_points=4,
                     dialog=["ça doit être cool de partir à l'aventure", "Moi aussi je partirai à l'aventure",
                             "Quand je serai plus grand", "dans deux ans", "Et vous verai que le roi des pirates",
                             "CE SERA MOI!!!"])])
        self.register_map("mountain", portals=[
            Portal(from_world="mountain", origin_point="mountain_world", target_world="snow",
                   teleport_point="return_snow"),
            Portal(from_world="mountain", origin_point="go_centre", target_world="centre_nakemon",
                   teleport_point="spawn_centre"),
            Portal(from_world="mountain", origin_point="go_sanctuaire", target_world="sanctuaire1",
                   teleport_point="spawn_sanctuaire"),
            Portal(from_world="mountain", origin_point="enter_cabane", target_world="cabane",
                   teleport_point="spawn_cabane")],
                          npcs=[NPC("villageois1", nb_points=4, dialog=["Il faut s'activer!",
                                                                        "le feu qui a ravagé au nord",
                                                                        "n'a heuresement pas atteint mes plantes"]),
                                NPC("poulet1", nb_points=2,
                                    dialog=["Va au sanctuaire", "la déesse de notre temple s'y trouve",
                                            "Elle te bénira"]),
                                NPC("vendeuse", nb_points=2, dialog=["Bouge de là j'ai du travail!",
                                                                     "mes légumes ne se vendront pas toutes seules!"])])

        self.register_map("centre_nakemon", portals=[
            Portal(from_world="centre_nakemon", origin_point="go_back", target_world="mountain",
                   teleport_point="centre_out")
        ],
                          npcs=[NPC("femme1", nb_points=2, dialog=["Bienvenue au centre Nakemon"])])
        self.register_map("sanctuaire1", portals=[
            Portal(from_world="sanctuaire1", origin_point="return_mountain", target_world="mountain",
                   teleport_point="sanctuaire_out")],
                          npcs=[NPC("prêtresse", nb_points=4, dialog=["Jeune aventurier tu as du faire un long voyage",
                                                                      "Ceci est le sanctuaire de notre déesse ",
                                                                      "Je te bénis par tous les pouvoirs",
                                                                      "qu'elle m'a conférée"]),
                                NPC("brigand", nb_points=2, dialog=["Tu as vu toute ces pierres précieuses au sol",
                                                                    "Ce qui m'interre en particulier c'est la pierre",
                                                                    "OUI la pierre philosophale",
                                                                    "les habitants pensent que c'est une deesse ",
                                                                    "mais non", "En réussisant à la prendre je serai",
                                                                    "Bwahahah un homme vraiment riche",
                                                                    "Oui moi le plus grand pirate des 7mers",
                                                                    "je jure de la dérober"])])
        self.register_map("cabane", portals=[
            Portal(from_world="cabane", origin_point="go_back", target_world="mountain", teleport_point="cabane_out")])

        self.teleport_player("player")
        self.teleport_npcs()

    def check_npc_collisions(self, dialog_box):
        for sprite in self.get_group().sprites():
            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:
                dialog_box.execute(sprite.dialog)

    def check_collisions(self):
        # portail
        for portal in self.get_map().portals:
            if portal.from_world == self.current_map:
                point = self.get_object(portal.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)
                if self.player.feet.colliderect(rect):
                    copy_portal = portal
                    self.current_map = portal.target_world
                    self.teleport_player(copy_portal.teleport_point)

                    # collision
        for sprite in self.get_group().sprites():
            if type(sprite) is NPC:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 0.8
            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def register_map(self, name, portals=[], npcs=[]):
        # Creer la fenêtre du jeu

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Nakemon-Aventure")

        # charger la carte en format tmx
        tmx_data = pytmx.util_pygame.load_pygame(f"../map/{name}.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # définir une liste qui va stcoker les rectangles de collission
        walls = []
        # for name in Map:
        #     if Map.name == "snow":
        #         for i in range(50):
        #             x = random.randrange(0, 400)
        #             y = random.randrange(0, 400)
        #             pygame.draw.circle(self.screen, white, [x, y], 2)

        for obj in tmx_data.objects:
            if obj.type == "collision":
                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        # dessiner le groupe de claques
        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)
        group.add(self.player)

        # récupérer tous les Npc et les afficher
        for npc in npcs:
            group.add(npc)

        self.maps[name] = Map(name, walls, group, tmx_data, portals, npcs)

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name):
        return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):
        for map in self.maps:
            map_data = self.maps[map]
            npcs = map_data.npcs
            for npc in npcs:
                npc.load_points(map_data.tmx_data)
                npc.teleport_spawn()

    # setter qui va permettre de dessiner la carte
    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)
        # Faire tomber la neige
        if self.current_map == self.snow:
            star_list = []
            for i in range(300):
                x = random.randrange(0, 800)
                y = random.randrange(0, 600)
                star_list.append([x, y])
            for item in star_list:
                item[1] += 1
                pygame.draw.circle(self.screen, white, item, 4)
                if item[1] > 500:
                    item[1] = random.randrange(-20, -5)
                    item[0] = random.randrange(0, 800)

    def upadate(self):
        self.get_group().update()
        self.check_collisions()
        for npc in self.get_map().npcs:
            npc.move()
