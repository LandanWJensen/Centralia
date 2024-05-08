import random
import json
import os

class SlotMachine:
    def __init__(self, filename="bank.json"):
        self.cherry = '\U0001F352'
        self.orange = '\U0001F34A'
        self.grape = '\U0001F347'
        self.bell = '\U0001F514'
        self.watermelon = '\U0001F349'
        self.number_7 = '\U00000037\uFE0F\u20E3'
        self.dollar = '\U0001F4B5'
        self.symbols = [self.cherry, self.grape, self.orange, self.bell, self.number_7, self.dollar]
        self.filename = filename
        self.bank_dict = self.load_bank()

    def load_bank(self):
        os.chdir(r'\Users\landa\PycharmProjects\InfluenceBot')
        try:
            with open("bank.json", 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON data: {e}")
            return {}  # Return an empty dictionary on JSON decoding error

    def save_bank(self):
        with open(self.filename, 'w') as file:
            json.dump(self.bank_dict, file)

    def reload_bank(self):
        self.bank_dict = self.load_bank()
    def create_bank_entry(self, user_id, initial_balance = 5000):
        if user_id not in self.bank_dict:
            self.bank_dict[user_id] = initial_balance
            self.save_bank()
            print(f'creating bank account')

    async def calculate_payout(self, result, user_id, bet):
        payouts= {
            self.cherry: {1: 1, 2: 5, 3: 10},
            self.orange: {3: 15},
            self.grape: {3: 20},
            self.bell: {3: 50},
            self.number_7: {3: 100},
            self.dollar: {3: 500}
        }

        for symbol, payouts_for_symbol in payouts.items():
            if result.count(symbol) in payouts_for_symbol:
                payout_multiplier = payouts_for_symbol[result.count(symbol)]
                payout = int(bet) * payout_multiplier
                self.bank_dict[user_id] += payout
                self.save_bank()
                return (f"Winner! Payout: {payout}")
        else:
            self.bank_dict[user_id] -= int(bet)
            self.save_bank()
            return (f"Loser. Bet deducted: {bet}")

    async def check_funds(self, ctx, bet, no_of_spins):
        user_id = str(ctx.author.id)
        await self.check_bank(ctx)
        try:
            bet = int(bet)
            if bet <= 0:
                await ctx.reply ("Please enter a positive integer as your bet.")
                return 0
        except ValueError:
            await ctx.reply("Please enter a valid integer as your bet.")
        
        if self.bank_dict[user_id] - int(bet) * no_of_spins < 0:
            print("Insufficient funds:", self.bank_dict[user_id], bet)
            await ctx.reply (f"Insufficient funds \nBalance: {await self.check_bank(ctx)}")
            await self.check_bank(ctx)
            return 0

    async def spin(self, ctx, bet):
        user_id = str(ctx.author.id)
        result = [random.choice(self.symbols) for _ in range(3)]
        payout = await self.calculate_payout(result, user_id, bet)
        outcome = [result, payout]
        return outcome

    async def check_bank(self,ctx):
        user_id = str(ctx.author.id)
        balance = self.bank_dict.get(user_id, "none")
        if balance == "none":
            await ctx.reply(f"creating bank account for <@{user_id}>")
            self.create_bank_entry(user_id)
        return balance
    
    async def leaderboard(self, ctx):

        sorted_scores = sorted(self.bank_dict.items(), key=lambda item: item[1], reverse=True)
        top_10 = sorted_scores[:10]
        leaderboard_message = "Leaderboard:\n"

        for idx, (user_id, score) in enumerate(top_10, 1):
            leaderboard_message += f"> {idx}. <@{user_id}> - {score} points\n"

        author_id = str(ctx.author.id)
        user_position = next((idx for idx, (user_id, score) in enumerate(sorted_scores, 1) if user_id == author_id), None)
        user_score = self.bank_dict[author_id]

        if user_position > 10:
            leaderboard_message += f"> ... \n" f"> {user_position}. <@{author_id}> - {user_score} points"
        return leaderboard_message

        
    async def leaderboard_webhook(self, ctx):

        # Sort the dictionary by points in descending order and get the top 10
        sorted_scores = sorted(self.bank_dict.items(), key=lambda item: item[1], reverse=True)[:10]

        # Create a formatted leaderboard string
        leaderboard_message = "Leaderboard:\n"
        for idx, (user_id, score) in enumerate(sorted_scores, 1):
            leaderboard_message += f"{idx}. <@{user_id}> - {score} points\n"

        # Send the message to the Discord channel
        data = {
            "content": leaderboard_message,
            "username" : "Arcade"
        }

        return data