# Simulate a sports tournament

import csv
import sys
import random

# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []
    # TODO: Read teams into memory from file
    with open(sys.argv[1]) as myfile:
        # Creates a new object called reader, each element in reader is a dictionary with keys from the first row and values from each row after
        reader = csv.DictReader(myfile)
        # this treats each row of the csv file as a dict, with the key on the first row
        # When you iterate over a CSV file, each iteration of the loop produces a dictionary from strings to strings.
        # They keys are the names of the columns (from the first row of the file), and the values are the data from the row being read.
        for myrow in reader:
            # convert the whole 'rating' column insidr the reader object to int
            myrow["rating"] = int(myrow["rating"])
            # adding the dictionary to the teams list.
            teams.append(myrow)

    counts = {}
    # TODO: Simulate N tournaments and keep track of win counts
    for i in range(N):
        # new temp var winner stores the overeall competition winner for that simulation
        winner = simulate_tournament(teams)
        if winner in counts:
            counts[winner] += 1
        else:
            counts[winner] = 1

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""
    # TODO
    while len(teams) > 1:
        # simulate_round returns a list of winners only of that round
        teams = simulate_round(teams)
    return teams[0]["team"]


if __name__ == "__main__":
    main()
