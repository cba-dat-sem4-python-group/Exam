from collections import Counter

def flush(suits:list) -> bool:
    return len(set(suits)) == 1

def four_of_a_kind(ranks:list) -> bool:
    return 4 in Counter(ranks).values()

def full_house(ranks:list) -> bool:
    count = Counter(ranks).values()
    return 3 in count and 2 in count

def pair(ranks:list) -> bool:
    return 2 in Counter(ranks).values()

def straight(ranks:list) -> bool:
    sorted_ranks = sorted(ranks, key=int)
    consecutive = sorted_ranks[0]==sorted_ranks[1]-1==sorted_ranks[2]-2==sorted_ranks[3]-3==sorted_ranks[4]-4
    return consecutive or set(ranks) == {1,10,11,12,13}

def three_of_a_kind(ranks:list) -> bool:
    return 3 in Counter(ranks).values()

def two_pairs(ranks:list) -> bool:
    return 2 in Counter(Counter(ranks).values()).values()

def check(hand):

    ranks = hand[:5]
    suits = hand[5:]

    if flush(suits) and straight(ranks) and set(ranks) == {1,10,11,12,13}: return 9
    elif flush(suits) and straight(ranks): return 8
    elif four_of_a_kind(ranks): return 7
    elif full_house(ranks): return 6
    elif flush(suits): return 5
    elif straight(ranks): return 4
    elif three_of_a_kind(ranks): return 3
    elif two_pairs(ranks): return 2
    elif pair(ranks): return 1
    else: return 0