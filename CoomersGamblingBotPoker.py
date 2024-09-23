import discord
from discord.ext import commands
import random
from collections import Counter

# Replace with your bot's token
TOKEN = 'YOUR_TOKEN'

# Create intents
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

# Initialize the bot with intents
bot = commands.Bot(command_prefix='$', intents=intents)

# Card values and suits
card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 11, 'Q': 12, 'K': 13, 'A': 14
}
suits = ['♠', '♥', '♦', '♣']  # List of suits

# Player economy dictionary
economy = {}

# Initialize new player with starting balance
def initialize_player(player_id):
    if player_id not in economy:
        economy[player_id] = 1000  # Starting balance of 1000

# Function to evaluate poker hands
def evaluate_hand(hand):
    ranks = sorted([card_values[card[:-1]] for card in hand], reverse=True)  # Sort by rank
    suits = [card[-1] for card in hand]
    
    is_flush = len(set(suits)) == 1
    is_straight = all(ranks[i] - 1 == ranks[i + 1] for i in range(len(ranks) - 1))

    counts = Counter(ranks)
    count_values = sorted(counts.values(), reverse=True)
    unique_ranks = list(counts.keys())

    # Determine the best hand
    if is_flush and is_straight and ranks[0] == 14:
        return (10, ranks)  # Royal flush
    elif is_flush and is_straight:
        return (9, ranks)  # Straight flush
    elif count_values == [4, 1]:
        return (8, unique_ranks)  # Four of a kind
    elif count_values == [3, 2]:
        return (7, unique_ranks)  # Full house
    elif is_flush:
        return (6, ranks)  # Flush
    elif is_straight:
        return (5, ranks)  # Straight
    elif count_values == [3, 1, 1]:
        return (4, unique_ranks)  # Three of a kind
    elif count_values == [2, 2, 1]:
        return (3, unique_ranks)  # Two pair
    elif count_values == [2, 1, 1, 1]:
        return (2, unique_ranks)  # One pair
    else:
        return (1, ranks)  # High card

@bot.command()
async def balance(ctx):
    player_id = ctx.author.id
    initialize_player(player_id)  # Ensure the player is initialized
    player_balance = economy[player_id]
    await ctx.send(f"{ctx.author.mention}, your balance is: {player_balance}")

@bot.command()
async def poker(ctx):
    player_id = ctx.author.id
    initialize_player(player_id)  # Ensure the player is initialized
    player_balance = economy[player_id]

    pot = 0
    player_bet = 0

    # Deck creation
    deck = [f'{value}{suit}' for value in card_values.keys() for suit in suits]  # 4 suits for a standard deck
    random.shuffle(deck)

    # Dealing hole cards with random suits
    player_hand = [deck.pop(), deck.pop()]  # Player's hole cards
    dealer_hand = [deck.pop(), deck.pop()]  # Dealer's hole cards

    await ctx.send(f"{ctx.author.mention}, your hole cards: {player_hand[0]}, {player_hand[1]} (hidden for the dealer)")

    # Pre-flop betting
    await ctx.send(f"{ctx.author.mention}, your balance: {player_balance}. Type 'call', 'raise [amount]', or 'fold'.")

    # Pre-flop actions
    while True:
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        if msg.content.lower() == 'call':
            if player_balance < 10:
                await ctx.send(f"{ctx.author.mention}, you do not have enough balance to call.")
                continue
            pot += 10  # Example call amount
            player_bet += 10
            economy[player_id] -= 10
            await ctx.send(f"{ctx.author.mention} called. Pot is now {pot}. Your balance: {economy[player_id]}.")
            break
        elif msg.content.lower().startswith('raise'):
            try:
                raise_amount = int(msg.content.split()[1])
                if raise_amount > economy[player_id]:
                    await ctx.send(f"{ctx.author.mention}, you do not have enough balance to raise.")
                    continue
                pot += raise_amount
                player_bet += raise_amount
                economy[player_id] -= raise_amount
                # Dealer must match the raise
                pot += raise_amount
                await ctx.send(f"{ctx.author.mention} raised to {pot}. Dealer matches the raise. Your balance: {economy[player_id]}.")
                break
            except (IndexError, ValueError):
                await ctx.send("Invalid raise amount. Please type 'call', 'raise [amount]', or 'fold'.")
        elif msg.content.lower() == 'fold':
            await ctx.send(f"{ctx.author.mention} folded. Dealer wins the pot of {pot}!")
            return

    # Flop
    flop = [deck.pop() for _ in range(3)]  # 3 community cards
    await ctx.send(f"The flop is: {flop}")

    # Betting after the flop
    await ctx.send(f"{ctx.author.mention}, your turn to bet again. Your balance: {economy[player_id]}. Type 'call', 'raise [amount]', or 'fold'.")

    while True:
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        if msg.content.lower() == 'call':
            if player_balance < 10:
                await ctx.send(f"{ctx.author.mention}, you do not have enough balance to call.")
                continue
            pot += 10  # Example call amount
            player_bet += 10
            economy[player_id] -= 10
            await ctx.send(f"{ctx.author.mention} called. Pot is now {pot}. Your balance: {economy[player_id]}.")
            break
        elif msg.content.lower().startswith('raise'):
            try:
                raise_amount = int(msg.content.split()[1])
                if raise_amount > economy[player_id]:
                    await ctx.send(f"{ctx.author.mention}, you do not have enough balance to raise.")
                    continue
                pot += raise_amount
                player_bet += raise_amount
                economy[player_id] -= raise_amount
                # Dealer must match the raise
                pot += raise_amount
                await ctx.send(f"{ctx.author.mention} raised to {pot}. Dealer matches the raise. Your balance: {economy[player_id]}.")
                break
            except (IndexError, ValueError):
                await ctx.send("Invalid raise amount. Please type 'call', 'raise [amount]', or 'fold'.")
        elif msg.content.lower() == 'fold':
            await ctx.send(f"{ctx.author.mention} folded. Dealer wins the pot of {pot}!")
            return

    # Turn
    turn = deck.pop()
    await ctx.send(f"The turn is: {turn}")

    # Display all community cards
    all_community_cards = flop + [turn]
    await ctx.send(f"Community cards now: {all_community_cards}")

    # Betting after the turn
    await ctx.send(f"{ctx.author.mention}, your turn to bet again. Your balance: {economy[player_id]}. Type 'call', 'raise [amount]', or 'fold'.")

    while True:
        msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        if msg.content.lower() == 'call':
            if player_balance < 10:
                await ctx.send(f"{ctx.author.mention}, you do not have enough balance to call.")
                continue
            pot += 10  # Example call amount
            player_bet += 10
            economy[player_id] -= 10
            await ctx.send(f"{ctx.author.mention} called. Pot is now {pot}. Your balance: {economy[player_id]}.")
            break
        elif msg.content.lower().startswith('raise'):
            try:
                raise_amount = int(msg.content.split()[1])
                if raise_amount > economy[player_id]:
                    await ctx.send(f"{ctx.author.mention}, you do not have enough balance to raise.")
                    continue
                pot += raise_amount
                player_bet += raise_amount
                economy[player_id] -= raise_amount
                # Dealer must match the raise
                pot += raise_amount
                await ctx.send(f"{ctx.author.mention} raised to {pot}. Dealer matches the raise. Your balance: {economy[player_id]}.")
                break
            except (IndexError, ValueError):
                await ctx.send("Invalid raise amount. Please type 'call', 'raise [amount]', or 'fold'.")
        elif msg.content.lower() == 'fold':
            await ctx.send(f"{ctx.author.mention} folded. Dealer wins the pot of {pot}!")
            return

    # River
    river = deck.pop()
    await ctx.send(f"The river is: {river}")

    # Display all community cards
    all_community_cards = flop + [turn, river]
    await ctx.send(f"Final community cards: {all_community_cards}")

    # Show dealer's hand
    await ctx.send(f"Dealer's hand: {dealer_hand}")

    # Determine the best hands
    player_best_hand = evaluate_hand(player_hand + all_community_cards)
    dealer_best_hand = evaluate_hand(dealer_hand + all_community_cards)

    # Compare hands
    if player_best_hand > dealer_best_hand:
        winnings = pot
        economy[player_id] += winnings
        await ctx.send(f"{ctx.author.mention} wins the pot of {winnings}! Your new balance: {economy[player_id]}.")
    elif player_best_hand < dealer_best_hand:
        await ctx.send(f"Dealer wins the pot of {pot}!")
    else:
        # Tie situation
        split_pot = pot // 2
        economy[player_id] += split_pot
        await ctx.send(f"It's a tie! Pot is split. You receive {split_pot}. Your new balance: {economy[player_id]}.")

# Run the bot
bot.run(TOKEN)

