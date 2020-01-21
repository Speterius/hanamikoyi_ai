from combinatoric_tools.tools import *

# Setup
card_deck = "AABBCCDDDEEEFFFFGGGGG"
action_permutations = set(itertools.permutations(['secret', 'burn', 'gift', 'comp']))

option_mapping = {'secret': get_secret_options,
                  'burn': get_burn_options,
                  'gift': get_gift_options,
                  'comp': get_comp_options}

keys_of_a_turn = ['hand', 'action', 'cards', 'enemy_response', 'enemy_action', 'enemy_cards', 'response']
keys = [k+'_'+str(t) for t in range(1, 5) for k in keys_of_a_turn]
data = {k: [] for k in keys}


def action_generator(perm_agent, perm_enemy):
    """ Generate a sequence of actions based on two permutations: """
    for turn_count in range(4):
        action_agent = perm_agent[turn_count]
        action_enemy = perm_enemy[turn_count]
        yield turn_count+1, action_agent, action_enemy


def card_option_generator(action_to_map, cards_in_hand):

    options = option_mapping[action_to_map](cards_in_hand=cards_in_hand)

    for cards_played in options:

        if action == 'comp':
            offer_to_enemy = [''.join(i) for i in cards_played]
        elif action == 'gift':
            offer_to_enemy = cards_played
        else:
            offer_to_enemy = 'N'

        hand_after_playing_cards = neg_intersect(cards_in_hand, flatten(cards_played))

        yield cards_played, offer_to_enemy, hand_after_playing_cards


def enemy_card_option_generator(action_to_map, deck_remaining):
    if action_to_map == 'secret' or action_to_map == 'burn':
        yield 'N', 'N'
    elif action_to_map == 'gift':
        for triplet in set(itertools.combinations(deck_remaining, 3)):
            yield triplet, triplet
    elif action_to_map == 'comp':
        for quadruple in set(itertools.combinations(deck_remaining, 4)):
            yield quadruple, quadruple


def agent_hand_generator(current_turn, hands_before_drawing, deck_remaining):

    for h in hands_before_drawing:
        if current_turn == 1:
            yield h
        else:
            for card_draw in set(itertools.combinations(deck_remaining, 1)):
                hand_next = join_tuples(h, card_draw)
                yield hand_next


# Starting hand information:
hand_at_start = random.choice(list(all_hands(deck=card_deck, n=7)))
deck_remained_at_start = neg_intersect(tuple(card_deck), hand_at_start)
all_enemy_hands_at_start = all_hands(deck=deck_remained_at_start, n=7)

# All possible action sequences to simulate:
counter = 0

permutation_agent = next(iter(action_permutations))
permutation_enemy = next(iter(action_permutations))

# Reset the hand we have at the start of the game:
hands_before_draw = [hand_at_start]
en_hand_before_draw = None
deck_remained = deck_remained_at_start

# Loop through all 4 turns within this game:
for turn, action, enemy_action in action_generator(permutation_agent, permutation_enemy):

    print(f'Turn: {turn} __________________________')
    print(f'Action: {action}')

    # Loop through all possible card draws this turn:
    for hand in agent_hand_generator(current_turn=turn, hands_before_drawing=set(hands_before_draw),
                                     deck_remaining=deck_remained):

        print(f'Hand: {hand}')
        hands_before_draw = []
        # Loop through all the card choices that the agent has:
        for cards, offer, hand_before_draw, card_drawn in card_option_generator(action_to_map=action, cards_in_hand=hand):

            hands_before_draw.append(hand_before_draw)

            # Loop through all enemy responses possible:
            for enemy_response in set(itertools.combinations(offer, 1)):

                # Loop through all the card choices that the agent has:
                for en_cards, en_offer in enemy_card_option_generator(action_to_map=enemy_action, deck_remaining=deck_remained):

                    deck_remained_for_this_choie = neg_intersect(tuple(deck_remained), en_cards)

                    # Loop through all responses:
                    for response in set(itertools.combinations(en_offer, 1)):

                        data['hand_1'+str(turn)].append(hand_1)
                        data['action_1'+str(turn)].append(action)
                        data['cards_' + str(turn)].append(cards)
                        data['enemy_response_' + str(turn)].append(enemy_response)
                        data['enemy_action_' + str(turn)].append(enemy_action)
                        data['enemy_cards_' + str(turn)].append(en_cards)
                        data['response_' + str(turn)].append(response)

                        data['hand_2'+str(turn)].append(hand_2)
                        data['action_2'+str(turn)].append(action)
                        data['cards_' + str(turn)].append(cards)
                        data['enemy_response_' + str(turn)].append(enemy_response)
                        data['enemy_action_' + str(turn)].append(enemy_action)
                        data['enemy_cards_' + str(turn)].append(en_cards)
                        data['response_' + str(turn)].append(response)

                        data['hand_'+str(turn)].append(hand)
                        data['action_'+str(turn)].append(action)
                        data['cards_' + str(turn)].append(cards)
                        data['enemy_response_' + str(turn)].append(enemy_response)
                        data['enemy_action_' + str(turn)].append(enemy_action)
                        data['enemy_cards_' + str(turn)].append(en_cards)
                        data['response_' + str(turn)].append(response)

                        data['hand_'+str(turn)].append(hand)
                        data['action_'+str(turn)].append(action)
                        data['cards_' + str(turn)].append(cards)
                        data['enemy_response_' + str(turn)].append(enemy_response)
                        data['enemy_action_' + str(turn)].append(enemy_action)
                        data['enemy_cards_' + str(turn)].append(en_cards)
                        data['response_' + str(turn)].append(response)

                        counter += 1
