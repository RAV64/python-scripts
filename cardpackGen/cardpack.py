from random import randrange, shuffle


def make(cardamount, packamount, suitamount):
    pack = []
    cards = list(range(cardamount))
    while packamount:
        for card in cards:
            for letter in range(97, (97 + suitamount)):
                pack.append(chr(letter) + str(card))
        packamount -= 1
    return pack


def standardizer(pack):
    """♣️♦️♥️♠️ and 𝗔 𝗝 𝗤 𝗞"""
    newpack = []
    for card in pack:

        if card[0] == 'a':
            if card[1:] == '0':
                newpack.append('♣️ ' + '𝗔')
            elif int(card[1:]) > 0 and int(card[1:]) < 10:
                newpack.append('♣️ ' + str(int(card[1:]) + 1))
            elif card[1:] == '10':
                newpack.append('♣️ ' + '𝗝')
            elif card[1:] == '11':
                newpack.append('♣️ ' + '𝗤')
            elif card[1:] == '12':
                newpack.append('♣️ ' + '𝗞')
            else:
                newpack.append('♣️ ' + str(int(card[1:]) + 1))

        elif card[0] == 'b':
            if card[1:] == '0':
                newpack.append('♦️ ' + '𝗔')
            elif 0 < int(card[1:]) < 10:
                newpack.append('♦️ ' + str(int(card[1:]) + 1))
            elif card[1:] == '10':
                newpack.append('♦️ ' + '𝗝')
            elif card[1:] == '11':
                newpack.append('♦️ ' + '𝗤')
            elif card[1:] == '12':
                newpack.append('♦️ ' + '𝗞')
            else:
                newpack.append('♦️ ' + str(int(card[1:]) + 1))

        elif card[0] == 'c':
            if card[1:] == '0':
                newpack.append('♥️ ' + '𝗔')
            elif 0 < int(card[1:]) < 10:
                newpack.append('♥️ ' + str(int(card[1:]) + 1))
            elif card[1:] == '10':
                newpack.append('♥️ ' + '𝗝')
            elif card[1:] == '11':
                newpack.append('♥️ ' + '𝗤')
            elif card[1:] == '12':
                newpack.append('♥️ ' + '𝗞')
            else:
                newpack.append('♥️ ' + str(int(card[1:]) + 1))

        elif card[0] == 'd':
            if card[1:] == '0':
                newpack.append('♠️ ' + '𝗔')
            elif 0 < int(card[1:]) < 10:
                newpack.append('♠️ ' + str(int(card[1:]) + 1))
            elif card[1:] == '10':
                newpack.append('♠️ ' + '𝗝')
            elif card[1:] == '11':
                newpack.append('♠️ ' + '𝗤')
            elif card[1:] == '12':
                newpack.append('♠️ ' + '𝗞')
            else:
                newpack.append('♠️ ' + str(int(card[1:]) + 1))

        else:
            if card[1:] == '0':
                newpack.append(card[0] + '𝗔')
            elif 0 < int(card[1:]) < 10:
                newpack.append(card[0] + str(int(card[1:]) + 1))
            elif card[1:] == '10':
                newpack.append(card[0] + '𝗝')
            elif card[1:] == '11':
                newpack.append(card[0] + '𝗤')
            elif card[1:] == '12':
                newpack.append(card[0] + '𝗞')
            else:
                newpack.append(card[0] + str(int(card[1:]) + 1))

    return newpack


def pick(pack, random=False, remove=True):
    if random:
        if remove:
            card = pack.pop(randrange(len(pack)))
        else:
            card = pack[randrange(len(pack))]
    else:
        if remove:
            card = pack.pop()
        else:
            card = pack[len(pack)]

    return card


def shuffler(pack):
    shuffle(pack)
    return pack


def init(cardamount, packamount, suitamount, standardize, shuffled):
    pack = make(cardamount, packamount, suitamount)
    if standardize != 'n':
        pack = standardizer(pack)
    if shuffled != 'n':
        pack = shuffler(pack)
    return pack


def setup():
    print("\n\n\n\n")
    print("Input 𝘅 to enter settings or")
    setup = input("Press 𝗘𝗡𝗧𝗘𝗥 to skip settings:\t")

    if setup == 'x':

        print("\nDeck properties part, please answer with a valid whole number\n")
        cardamount = int(input("How many cards per pack (default=13):\t"))
        packamount = int(input("How many decks mixed together (default=1):\t"))
        suitamount = int(input("How many suits per deck (default=4):\t"))

        print("\nYES or NO part, please answer with enter for YES or 'n' for NO\n")
        standardize = input("Standardize pack(default=YES):\t")
        shuffled = input("Shuffle pack(default=YES):\t")

    else:
        cardamount, packamount, suitamount, standardize, shuffled = 13, 1, 4, 'y', 'y'

    return cardamount, packamount, suitamount, standardize, shuffled


if __name__ == '__main__':
    cards, packs, suits, standardize, shuffled = setup()
    pack = init(cards, packs, suits, standardize, shuffled)

    print("\n")
    print(pack)
