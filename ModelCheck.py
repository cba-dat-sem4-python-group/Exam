import numpy as np
import tensorflow as tf
# import Card

def getHand(found_cards):
    text = str(len(found_cards)) + "/5 cards found"
    model = tf.keras.models.load_model("models/final_model.h5")

    if len(found_cards) >= 5:
        nums = [card.num for card in found_cards[:5]]
        suits = [card.suit for card in found_cards[:5]]
        arr = [[nums + suits]]

        num_dict = {0:"Nothing",1:"Pair",2:"Two Pair",3:"Three of a kind",4:"Straight",5:"Flush",6:"Full House",7:"Four of a kind",8:"Straight Flush",9:"Royal Flush"}

        prediction = np.argmax(model.predict_proba(arr))
        return num_dict[prediction]