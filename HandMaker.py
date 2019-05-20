import random

def royal_flush():
    suit = random.choice(range(1,5))
    ranks = [1,10,11,12,13]
    random.shuffle(ranks)
    return ranks+[suit,suit,suit,suit,suit,9]

def straight_flush():
    suit = random.choice(range(1,5))
    low_card = random.choice(range(1,10))
    ranks = [low_card,low_card+1,low_card+2,low_card+3,low_card+4]
    random.shuffle(ranks)
    return ranks+[suit,suit,suit,suit,suit,8]

def four_of_a_kind():
    rank = random.choice(range(1,14))
    suits = [1,2,3,4]
    random.shuffle(suits)
    last_suit = random.choice(range(1,5))
    last_rank = rank
    while rank == last_rank:
        last_rank = random.choice(range(1,14))
    cards = [(rank,suits[0]),(rank,suits[1]),(rank,suits[2]),(rank,suits[3]),(last_rank,last_suit)]
    random.shuffle(cards)
    res = list(range(10))
    for x in range(len(cards)):
        res[x] = cards[x][0]
        res[x+5] = cards[x][1]
    return res + [7]

def full_house():
    suits = list(range(1,5))
    ranks = list(range(1,14))

    twos_1 = (random.choice(ranks), random.choice(suits))
    suits.remove(twos_1[1])
    twos_2 = (twos_1[0], random.choice(suits))

    ranks.remove(twos_1[0])
    suits = list(range(1,5))

    threes_1 = (random.choice(ranks), random.choice(suits))
    suits.remove(threes_1[1])
    threes_2 = (threes_1[0], random.choice(suits))
    suits.remove(threes_2[1])
    threes_3 = (threes_1[0], random.choice(suits))

    arr = [twos_1,twos_2,threes_1,threes_2,threes_3]
    random.shuffle(arr)

    res = list(range(10))

    for x in range(len(arr)):
        res[x] = arr[x][0]
        res[x+5] = arr[x][1]

    return res + [6]

def flush():
    suit = random.choice(range(1,5))
    ranks = []
    for _ in range(5):
        while True:
            randomCard = random.choice(range(1,14))
            if randomCard not in ranks:
                ranks.append(randomCard)
                break
    random.shuffle(ranks)
    return ranks+[suit]*5+[5]

def straight():
    low_card = random.choice(range(1,11))
    ranks = [low_card,low_card+1,low_card+2,low_card+3,1 if low_card==10 else low_card+4]
    suits = []
    for _ in range(5):
        while True:
            randomCard = random.choice(range(1,5))
            if suits.count(randomCard) < 4:
                suits.append(randomCard)
                break
    random.shuffle(ranks)
    random.shuffle(suits)
    return ranks+suits+[4]

def three_of_a_kind():
    rank = random.choice(range(1,14))
    suits = [1,2,3,4]
    random.shuffle(suits)
    ex_suits = []
    for _ in range(2):
        ex_suits.append(random.choice(range(1,5)))
    ranks = []
    for _ in range(2):
        while True:
            randomCard = random.choice(range(1,14))
            if randomCard not in ranks and randomCard != rank:
                ranks.append(randomCard)
                break
    random.shuffle(ranks)
    random.shuffle(ex_suits)
    cards = [(rank,suits[0]),(rank,suits[1]),(rank,suits[2]),(ranks[0],ex_suits[0]),(ranks[1],ex_suits[1])]
    random.shuffle(cards)

    res = list(range(10))
    for x in range(len(cards)):
        res[x] = cards[x][0]
        res[x+5] = cards[x][1]
    return res + [3]

def two_pairs():
    ranks=[]
    suits=[]
    arr=[]

    for _ in range(3):
        while True:
            num = random.choice(range(1,14))
            if num not in ranks:
                suit = random.choice(range(1,5))

                ranks.append(num)
                suits.append(suit)

                arr.append((num, suit))
                break

    one = (ranks[0], (suits[0] + 4 + random.choice(range(3)))%4+1)
    two = (ranks[1], (suits[1] + 4 + random.choice(range(3)))%4+1)

    arr.extend([one,two])
    random.shuffle(arr)

    res = list(range(10))
    for x in range(len(arr)):
        res[x] = arr[x][0]
        res[x+5] = arr[x][1]
    return res + [2]

def pair():
    ranks=[]
    suits=[]
    arr=[]

    for _ in range(4):
        while True:
            num = random.choice(range(1,14))
            if num not in ranks:
                suit = random.choice(range(1,5))

                ranks.append(num)
                suits.append(suit)

                arr.append((num, suit))
                break

    one = (ranks[0], (suits[0] + 4 + random.choice(range(3)))%4+1)

    arr.extend([one])
    random.shuffle(arr)

    res = list(range(10))

    for x in range(len(arr)):
        res[x] = arr[x][0]
        res[x+5] = arr[x][1]

    return res + [1]

def nothing():
    suit_list = list(range(1,5))
    rank_list = list(range(1,14))

    ranks = []
    suits = []

    one = random.choice(rank_list)
    ranks.append(one)
    rank_list.remove(one)

    two = (one + 5 + random.choice(range(4)) + 12) % 13 + 1 #range(4) 0->3 ||  ( n+5+(rand 0 -> 3) + len-1 ) % len+1
    ranks.append(two)
    rank_list.remove(two)


    for x in range(3):
        ranks.append(random.choice(rank_list))
        rank_list.remove(ranks[x+2]) # +2 cus we added those manually

    #########################################

    for x in range(4):
        suits.append(random.choice(suit_list))

    if suits.count(suits[0]) == 4: suit_list.remove(suits[0])

    suits.append(random.choice(suit_list))


    random.shuffle(ranks)
    random.shuffle(suits)

    res = ranks + suits

    return res + [0]

def rand():
    rand_num = random.choice(range(10))
    
    switcher = {
        0: nothing,
        1: pair,
        2: two_pairs,
        3: three_of_a_kind,
        4: straight,
        5: flush,
        6: full_house,
        7: four_of_a_kind,
        8: straight_flush,
        9: royal_flush
    }
  
    return switcher.get(rand_num)()