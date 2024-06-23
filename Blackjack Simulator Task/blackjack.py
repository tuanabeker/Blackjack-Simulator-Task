import random

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8',
         '9', '10', 'Jack', 'Queen', 'King', 'Ace']

# Create four standard decks of cards
deck = [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits] * 4

random.shuffle(deck)


# Function to calculate total hand value
def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        if card['rank'] in ['Jack', 'Queen', 'King']:
            value += 10
        elif card['rank'] == 'Ace':
            aces += 1
        else:
            value += int(card['rank'])

    # Decide if Aces count as 1 or 11
    for _ in range(aces):
        if value + 11 <= 21:
            value += 11
        else:
            value += 1

    return value

# Function to print the hand


def print_hand(player, hand, hide_dealer_card=False):
    if hide_dealer_card and player == 'Dealer':
        hand_str = f"{hand[0]['rank']} of {hand[0]['suit']}, Hidden"
    else:
        hand_str = ', '.join(
            [f"{card['rank']} of {card['suit']}" for card in hand])
        # Include hand value here
        hand_str += f" (value: {calculate_hand_value(hand)})"
    print(f"{player}'s hand: {hand_str}")


# Function to check for bust
def is_bust(hand):
    return calculate_hand_value(hand) > 21


# Initialize scores and rounds
scores = {'Player 1': 0, 'Player 2': 0, 'Dealer': 0}
rounds_played = 0
total_rounds = 5  # Total rounds to be played can be changed

# Game loop
# Each player needs at least 2 cards, so we need 6 cards minimum for each round
while rounds_played < total_rounds and len(deck) >= 6:
    rounds_played += 1
    print(f"\n--- Round {rounds_played} ---")

    # Deal initial cards
    player1_hand = [deck.pop(), deck.pop()]
    player2_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    # Print initial hands
    print_hand('Player 1', player1_hand)
    print_hand('Player 2', player2_hand)
    print_hand('Dealer', dealer_hand, hide_dealer_card=True)

    # Player 1's turn
    while not is_bust(player1_hand) and input("Player 1, do you want to hit (h) or stand (s)? ") == 'h':
        player1_hand.append(deck.pop())
        print_hand('Player 1', player1_hand)

    if is_bust(player1_hand):
        print("Player 1 busts!")

    # Player 2's turn
    while not is_bust(player2_hand) and input("Player 2, do you want to hit (h) or stand (s)? ") == 'h':
        player2_hand.append(deck.pop())
        print_hand('Player 2', player2_hand)

    if is_bust(player2_hand):
        print("Player 2 busts!")

    # Dealer's turn
    print_hand('Dealer', dealer_hand)  # Reveal dealer's full hand
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
        print_hand('Dealer', dealer_hand)

    if is_bust(dealer_hand):
        print("Dealer busts!")

    # Determine winner
    player1_value = calculate_hand_value(player1_hand)
    player2_value = calculate_hand_value(player2_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    # Find the closest total to 21 without busting
    valid_totals = [value for value in [player1_value,
                                        player2_value, dealer_value] if value <= 21]
    if valid_totals:
        closest_total = max(valid_totals)
    else:
        closest_total = 0

    # Determine the winner based on closest total and tie-break by number of cards
    if player1_value == closest_total:
        player1_tiebreaker = len(player1_hand)
    else:
        player1_tiebreaker = float('inf')

    if player2_value == closest_total:
        player2_tiebreaker = len(player2_hand)
    else:
        player2_tiebreaker = float('inf')

    if dealer_value == closest_total:
        dealer_tiebreaker = len(dealer_hand)
    else:
        dealer_tiebreaker = float('inf')

    tiebreakers = {'Player 1': player1_tiebreaker,
                   'Player 2': player2_tiebreaker, 'Dealer': dealer_tiebreaker}
    winners = [player for player, tiebreaker in tiebreakers.items(
    ) if tiebreaker == min(tiebreakers.values())]

    if len(winners) == 1:
        winner = winners[0]
    else:
        winner = None

    if winner:
        scores[winner] += 1
        print(f"{winner} wins the round with a total of {closest_total}!")
    else:
        print("Tie, No winner this round!")

    # Display current score
    print("\nCurrent scores:")
    for player, score in scores.items():
        print(f"{player}: {score}")

# Game over - display final score
print("\n--- Game Over ---")
print(f"Total rounds played: {rounds_played}")
print("Final scores:")
for player, score in sorted(scores.items(), key=lambda item: item[1], reverse=True):
    print(f"{player}: {score}")
