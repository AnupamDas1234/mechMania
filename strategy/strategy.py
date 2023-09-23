# This defines the general layout your strategy method will inherit. Do not edit this.

from typing import Dict, List, Set, Tuple
from game.character.action.ability_action import AbilityAction
from game.character.action.attack_action import AttackAction
from game.character.action.move_action import MoveAction
from game.character.character import Character
from game.character.character_class_type import CharacterClassType
from game.game_state import GameState
from game.util.position import Position

teams: List[Tuple[Set[str], Position]] = []

class OurHumanStrategy:

    def decide_character_classes(
        self,
        possible_classes: list[CharacterClassType],
        num_to_pick: int,
        max_per_same_class: int,
    ) -> dict[CharacterClassType, int]:
        """
        Decide the character classes your humans will use (only called on humans first turn)

        possible_classes: A list of the possible classes you can select from
        num_to_pick: The total number of classes you are allowed to select
        max_per_same_class: The max number of characters you can have in the same class

        You should return a dictionary of class type to the number you want to use of that class
        """
        choices = {
            CharacterClassType.BUILDER: 5,
            CharacterClassType.MARKSMAN: 5,
            CharacterClassType.MEDIC: 5,
            CharacterClassType.TRACEUR: 1,
        }
        return choices

    def generate_teams(self, game_state: GameState):
        characters = sorted([character_id for character_id in game_state.characters])
        builders = [
            character_id
            for character_id in characters
            if game_state.characters[character_id].class_type == CharacterClassType.BUILDER
        ]
        marksmen = [
            character_id
            for character_id in characters
            if game_state.characters[character_id].class_type == CharacterClassType.MARKSMAN
        ]
        medics = [
            character_id
            for character_id in characters
            if game_state.characters[character_id].class_type == CharacterClassType.MEDIC
        ]
        traceurs = [
            character_id
            for character_id in characters
            if game_state.characters[character_id].class_type == CharacterClassType.TRACEUR
        ]
        normal = [
            character_id
            for character_id in characters
            if game_state.characters[character_id].class_type == CharacterClassType.NORMAL
        ]
        global teams
        teams = [
            (set(builders[:2] + marksmen[:1] + medics[:1]), Position(72, 50)),
            (set(builders[2:3] + traceurs[:1] + marksmen[1:3]), Position(10, 50)),
            (set(marksmen[3:4] + medics[1:3] + normal[:1]), Position(95, 70)),
            (set(medics[3:4] + normal[1:4]), Position(70, 95)),
        ]
        print(f"Teams: {teams}")

    def decide_moves(
        self,
        character_possible_moves: Dict[str, List[MoveAction]],
        game_state: GameState,
    ) -> list[MoveAction]:
        """
        Decide the moves for each character based on the current game state

        possible_moves: Maps character id to it's possible moves. You can use this to validate if a move is possible, or pick from this list.
        game_state: The current state of all characters and terrain on the map
        """
        ZOMBIE_THRESHOLD_DISTANCE = 10
        final_chosen_move_actions: list[MoveAction] = []
        global teams
        if len(teams) == 0:
            self.generate_teams(game_state)

        zombies: List[Character] = [
            character
            for character in game_state.characters.values()
            if character.is_zombie
        ]

        for character_id, possible_moves in character_possible_moves.items():
            if len(possible_moves) == 0:
                continue

            human_position = game_state.characters[character_id].position
            closest_zombie_position = human_position  # random initialization
            closest_zombie_distance = 1234  # random initialization

            for zombie in zombies:
                current_zombie_distance = abs(
                    zombie.position.x - human_position.x
                ) + abs(zombie.position.y - human_position.y)
                if current_zombie_distance < closest_zombie_distance:
                    closest_zombie_position = zombie.position
                    closest_zombie_distance = current_zombie_distance

            # if closest_zombie_distance < ZOMBIE_THRESHOLD_DISTANCE:
                # run
            max_zombie_distance = 0
            best_move = possible_moves[0]
            for move in possible_moves:
                move_position = move.destination
                destination_to_zombie_distance = abs(
                    move_position.x - closest_zombie_position.x
                ) + abs(move_position.y - closest_zombie_position.y)
                if destination_to_zombie_distance > max_zombie_distance:
                    max_zombie_distance = destination_to_zombie_distance
                    best_move = move
            final_chosen_move_actions.append(best_move)
            # else:
            #     # move toward target
            #     for team, target_position in teams:
            #         if character_id in team:
            #             min_target_distance = 1234
            #             best_move = possible_moves[0]
            #             for move in possible_moves:
            #                 move_position = move.destination
            #                 destination_to_target_distance = abs(
            #                     move_position.x - target_position.x
            #                 ) + abs(move_position.y - target_position.y)
            #                 if destination_to_target_distance < min_target_distance:
            #                     min_target_distance = destination_to_target_distance
            #                     best_move = move
            #             final_chosen_move_actions.append(best_move)
            #             break

        print(final_chosen_move_actions)
        return final_chosen_move_actions

    def decide_attacks(
        self,
        character_possible_attacks: dict[str, list[AttackAction]],
        game_state: GameState,
    ) -> list[AttackAction]:
        """
        Decide the attacks for each character based on the current game state
        """
        final_chosen_attack_actions: List[AttackAction] = []
        global teams

        if len(teams) == 0:
            self.generate_teams(game_state)

        for character_id, possible_attacks in character_possible_attacks.items():
            if len(possible_attacks) == 0:
                continue

            # human_position = game_state.characters[character_id].position
            # print(possible_attacks)

        return final_chosen_attack_actions

    def decide_abilities(
        self,
        character_possible_abilities: dict[str, list[AbilityAction]],
        game_state: GameState,
    ) -> list[AbilityAction]:
        """
        Decide the moves for each character based on the current game state

        possible_abilities: Maps character id to it's possible abilities. You can use this to validate if a ability is possible, or pick from this list.
        game_state: The current state of all characters and terrain on the map
        """
        final_chosen_ability_actions: List[AbilityAction] = []
        global teams

        if len(teams) == 0:
            self.generate_teams(game_state)

        for character_id, possible_abilities in character_possible_abilities.items():
            if len(possible_abilities) == 0:
                continue

            # human_position = game_state.characters[character_id].position
            # print(possible_abilities)

        return final_chosen_ability_actions
