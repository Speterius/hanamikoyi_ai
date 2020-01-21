from combinatoric_tools.tools import *
import pandas as pd

card_deck = "AABBCCDDDEEEFFFFGGGGG"

# _______ Case 1: Agent is player 1 _____________________

# All possible hand combinations with 7 cards:
a = all_hands(deck=card_deck, n=7)
current_hand = random.choice(list(a))
deckRemainder = card_deck
for card in current_hand:
    deckRemainder = deckRemainder.replace(card, '', 1)

action_mapping = {1: 'secret',
                  2: 'burn',
                  3: 'gift',
                  4: 'comp'}

option_mapping = {'secret': get_secret_options,
                  'burn': get_burn_options,
                  'gift': get_gift_options,
                  'comp': get_comp_options}


def recursive_mapping(depth, hand, deck_remaining, enemy_hand=None, actions_left=None, enemy_actions_left=None):
    print(depth)

    if depth > 4:
        return {}

    if depth == 1:
        actions_left = ['secret', 'burn', 'gift', 'comp']
        enemy_actions_left = ['secret', 'burn', 'gift', 'comp']

    turn_data = {'turn_counter': depth,
                 'hand': [],
                 'action': [],
                 'cards_played': [],
                 'enemy_response': [],
                 'enemy_hand': [],
                 'enemy_action': [],
                 'enemy_cards_played': [],
                 'agent_response': [],
                 'next_turn': []}

    counter = 1

    # Loop through all four available actions:
    for action in actions_left:
        options = option_mapping[action](cards_in_hand=hand)

        # Loop through each card choices:
        for cards_played in options:

            if action == 'comp':
                offer = [''.join(i) for i in cards_played]
            elif action == 'gift':
                offer = cards_played
            else:
                offer = 'N'

            # Loop through each enemy response if applicable:
            enemy_responses = set(itertools.combinations(offer, 1))
            for enemy_response in enemy_responses:
                enemy_response = tuple(enemy_response[0])

                # Loop through all the hands the enemy can have:
                if depth == 1:
                    opponent_hands = all_hands(deck=deck_remaining, n=7)
                else:
                    card_draw = set(itertools.combinations(deck_remaining, 1))
                    opponent_hands = set([join_tuples(enemy_hand, c) for c in card_draw])

                for enemy_hand in opponent_hands:

                    # Loop through all the options the enemy has:
                    for enemy_action in enemy_actions_left:

                        enemy_options = option_mapping[enemy_action](cards_in_hand=enemy_hand)
                        for enemy_cards_played in enemy_options:

                            if enemy_action == 'comp':
                                offer = [''.join(i) for i in enemy_cards_played]
                            elif enemy_action == 'gift':
                                offer = cards_played
                            else:
                                offer = 'N'

                            # Loop through each agent response if applicable:
                            agent_responses = set(itertools.combinations(offer, 1))
                            for agent_response in agent_responses:
                                agent_response = tuple(agent_response[0])

                                # Loop through all unique card draws in the next turn:
                                hand_after_this = neg_intersect(hand, flatten(cards_played))
                                for card_draw in set(itertools.combinations(deck_remaining, 1)):
                                    hand_next = join_tuples(hand_after_this, card_draw)

                                    turn_data['hand'].append(hand)
                                    turn_data['action'].append(action)
                                    turn_data['cards_played'].append(cards_played)
                                    turn_data['enemy_response'].append(enemy_response)

                                    turn_data['enemy_hand'].append(enemy_hand)
                                    turn_data['enemy_action'].append(enemy_action)
                                    turn_data['enemy_cards_played'].append(enemy_cards_played)

                                    turn_data['agent_response'].append(agent_response)

                                    actions_left.remove(action)
                                    enemy_actions_left.remove(enemy_action)

                                    deck_remaining_this_version = deck_remaining.replace(card_draw[0], '', 1)
                                    for c in enemy_hand:
                                        deck_remaining_this_version = deck_remaining_this_version.replace(c, '', 1)

                                    turn_data['next_turn'] = recursive_mapping(depth=depth+1,
                                                                               hand=hand_next,
                                                                               actions_left=actions_left,
                                                                               enemy_hand=enemy_hand,
                                                                               enemy_actions_left=enemy_actions_left,
                                                                               deck_remaining=deck_remaining_this_version)

                                    counter += 1

    return turn_data


data = recursive_mapping(depth=1, hand=current_hand, deck_remaining=deckRemainder)
