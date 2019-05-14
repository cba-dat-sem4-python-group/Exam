import pandas as pd
import numpy as np
import tensorflow as tf
from collections import Counter

hands = ['Nothing', 'One Pair', 'Two Pairs', 'Three of a kind', 'Straight',
        'Flush', 'Full house', 'Four of a kind', 'Straight flush', 'Royal flush', 'Invalid']
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
suits = ['♥', '♠', '♦', '♣']

def get_data() -> (pd.DataFrame, pd.Series, pd.DataFrame, pd.Series):
    train_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/poker/poker-hand-training-true.data'
    test_url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/poker/poker-hand-testing.data'

    col_names = {0:'Suit of card #1', 1:'Rank of card #1',
                 2:'Suit of card #2', 3:'Rank of card #2',
                 4:'Suit of card #3', 5:'Rank of card #3',
                 6:'Suit of card #4', 7:'Rank of card #4',
                 8:'Suit of card #5', 9:'Rank of card #5',
                 10:'Poker Hand'}

    train = pd.read_csv(train_url, header=None)
    train.rename(col_names, axis='columns', inplace=True)

    test = pd.read_csv(test_url, header=None)
    test.rename(col_names, axis='columns', inplace=True)

    x_train = train.iloc[:,0:10]
    y_train = train.iloc[:,10]
    x_test = train.iloc[:,0:10]
    y_test = train.iloc[:,10]
    
    return x_train, y_train, x_test, y_test

def train_model(epochs: int=5, inner_layers: int=512, save_as: str=None) -> tf.keras.models.Model:
    x_train, y_train, x_test, y_test = get_data()
    
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten(input_shape=(10,)))
    model.add(tf.keras.layers.Dense(inner_layers, activation='relu'))
    model.add(tf.keras.layers.Dense(10, activation='softmax'))

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(x_train.values, y_train.values, epochs=epochs)
    model.evaluate(x_test.values, y_test.values)
    if save_as is not None:
        model.save(save_as)
    return model

def load_model(model_path: str) -> tf.keras.models.Model:
    return tf.keras.models.load_model(model_path)

def predict(data: np.array) -> str:
    pred = new_model.predict_proba([arr])
    return hands[np.argmax(pred)]

def check_flush(suits):
    return len(set(suits)) == 1

def check_four_of_a_kind(ranks):
    return 4 in Counter(ranks).values()

def check_full_house(ranks):
    count = Counter(ranks).values()
    return 3 in count and 2 in count

def check_pair(ranks):
    return 2 in Counter(ranks).values()

def check_straight(ranks):
    sorted_ranks = sorted(ranks, key=int)
    consecutive = sorted_ranks[0]==sorted_ranks[1]-1==sorted_ranks[2]-2==sorted_ranks[3]-3==sorted_ranks[4]-4
    return consecutive or set(ranks) == {1,10,11,12,13}

def check_three_of_a_kind(ranks):
    return 3 in Counter(ranks).values()

def check_two_pairs(ranks):
    return 2 in Counter(Counter(ranks).values()).values()

def evaluate_hand(hand):
    r1, r2, r3, r4, r5, s1, s2, s3, s4, s5 = hand
    suits = [s1,s2,s3,s4,s5]
    ranks = [r1,r2,r3,r4,r5]
    cards = [(s1,r1),(s2,r2),(s3,r3),(s4,r4),(s5,r5)]
    
    if len(set(cards)) != 5:
        return -1
    elif check_flush(suits) and check_straight(ranks) and set(ranks) == {1,10,11,12,13}:
        return 9
    elif check_flush(suits) and check_straight(ranks):
        return 8
    elif check_four_of_a_kind(ranks):
        return 7
    elif check_full_house(ranks):
        return 6
    elif check_flush(suits):
        return 5
    elif check_straight(ranks):
        return 4
    elif check_three_of_a_kind(ranks):
        return 3
    elif check_two_pairs(ranks):
        return 2
    elif check_pair(ranks):
        return 1
    else:
        return 0

def print_hand(hand):
    card1 = '{:{}{}{}}'.format(ranks[hand[1]-1],' ','>',2)+suits[hand[0]-1]
    card2 = '{:{}{}{}}'.format(ranks[hand[3]-1],' ','>',2)+suits[hand[2]-1]
    card3 = '{:{}{}{}}'.format(ranks[hand[5]-1],' ','>',2)+suits[hand[4]-1]
    card4 = '{:{}{}{}}'.format(ranks[hand[7]-1],' ','>',2)+suits[hand[6]-1]
    card5 = '{:{}{}{}}'.format(ranks[hand[9]-1],' ','>',2)+suits[hand[8]-1]
    res = hands[evaluate_hand(hand)]
    print(card1, card2, card3, card4, card5, res)
