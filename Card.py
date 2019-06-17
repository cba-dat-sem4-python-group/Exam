import numpy as np
import cv2
import math

class Card:
    def __init__(self):
        
        self.contour = []    #card contour
        self.width = 0       #contour max width?
        self.height = 0      #contour max height?
        self.center = []
        self.coords = []     #the rects 4 corners
        self.warped = []     #warped img of the card
        self.warped_thresh = []
        
        self.num_img = []
        self.suit_img = []
        
        self.num = None
        self.suit = None
        
    def draw_warped(self):
        cv2.imshow(self.num+self.suit+str(self.height)+str(self.width), self.warped)
        
    def draw_card_outlines(self, img):
        cv2.polylines(img, np.array([self.coords]), True, (0,255,255), 2)
        
    def draw_suit(self):
        cv2.imshow(str(np.sum(self.suit_img)), self.suit_img)
        
    def draw_num(self):
        cv2.imshow(str(np.sum(self.num_img)), self.num_img)
        
    def draw_text(self, img):
    
        suit_text = ["Hearts", "Spades", "Diamonds", "Clubs"]
        num_text = ['Ace','Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King']
    
        FONT = cv2.FONT_HERSHEY_SIMPLEX
        TEXT = num_text[self.num-1] + " " + suit_text[self.suit-1]
        FONT_SIZE = 0.8
        FONT_COLOR = (0, 255, 0)
        THICKNESS = 2
        
        ######
        
        # get boundary of this text
        textsize = cv2.getTextSize(TEXT, FONT, FONT_SIZE, THICKNESS)[0]

        # get coords based on boundary
        text_x = int(self.center[0] - (textsize[0]/2))
        text_y = int(self.center[1] + (textsize[1]/2))
        
        text_y = text_y - int(self.height/2) - 25
        
        
        # Add text centered on image
        cv2.putText(img, TEXT, (text_x, text_y), FONT, FONT_SIZE, FONT_COLOR, thickness=THICKNESS)
    
    def set_center(self):
        
        # Adds x's together & y's together and takes the avg
        pts_sum = np.sum(self.coords, axis=0)/len(self.coords)
        
        # Lav til int fordi vi ikke kan lande mellem 2 pixels
        x = int(pts_sum[0])
        y = int(pts_sum[1])
        
        self.center = [x, y]
        
        
    def find_warped_card(self, img):
        
        order_rect = lambda p: math.atan2(p[1]-self.center[1], p[0]-self.center[0])
        
        self.coords = sorted(self.coords, key=order_rect)
        
        w, h = 200, 300 # width, height

        # lav firkant i det format vi vil warp til
        dst = np.array([[0, 0], [w-1, 0], [w-1, h-1], [0, h-1]], dtype = "float32")
        
        ###################################

        # Lav første firkant ud fra self.coords og konverter til float
        rect1 = np.array(self.coords, dtype = "float32").reshape((4,2))
        
        # Compute the perspective transformation matrix
        transformation_matrix = cv2.getPerspectiveTransform(rect1, dst)
        
        # Lav første warp
        warp1 = cv2.warpPerspective(img, transformation_matrix, (w, h))
        
        ###################################
        
        # Anden firkant er samme firkant som før bare startende fra et nabo-punkt
        rect2 = np.array(self.coords[1:] + [self.coords[0]], dtype = "float32").reshape((4,2))
        
        # Compute the perspective transformation matrix
        transformation_matrix = cv2.getPerspectiveTransform(rect2, dst)
        
        # Lav anden warp
        warp2 = cv2.warpPerspective(img, transformation_matrix, (w, h))
        
        ####################################
        
        # Sæt self.warped til den warp som har den mindste værdi i det øverste venstre hjørne.
        # Den warp der har mindst hvidt (og derfor lavest værdi) burde være den, der vender den tigtige vej.
        self.warped = min(warp1, warp2, key=lambda x: np.sum(x[12:75, 9:39]))
        
        
    def find_icons(self):
        
        # FOUND BY SLAVE LABOR
        CORNER_WIDTH, CORNER_HEIGHT = 48, 140
        
        # Taken from comparison imgs
        NUM_WIDTH, NUM_HEIGHT = 70, 125
        SUIT_WIDTH, SUIT_HEIGHT = 70, 100

        #####
        
        # 1.Cut corner out 2. Make it bigger 3. Make it grayscale
        corner = self.warped[0:CORNER_HEIGHT, 0:CORNER_WIDTH]
        corner_big = cv2.resize(corner, (0,0), fx=3, fy=3)
        corner_big_gray = cv2.cvtColor(corner_big, cv2.COLOR_BGR2GRAY)
        

        # Make it black & white and more crisp
        thresh = cv2.threshold(corner_big_gray, 180, 255, cv2.THRESH_BINARY_INV)[1]
        thresh = cv2.adaptiveThreshold(corner_big_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 115, 1)
        
        self.warped_thresh = thresh
        
        # Divide img into number & suit
        num  = thresh[0:255, 0:144]
        suit = thresh[256:420, 0:144]
        
        self.num_img  = self.crop_and_resize_icon(num, NUM_WIDTH, NUM_HEIGHT)
        self.suit_img = self.crop_and_resize_icon(suit, SUIT_WIDTH, SUIT_HEIGHT)
    
        
        self.find_num()  # find numerisk værdi fra icon
        self.find_suit() # find numerisk værdi fra icon
        
    def crop_and_resize_icon(self, img, new_width, new_height):
    
        #find contours
        contours = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

        # Check om der blev fundet noget icon
        if(len(contours) == 0): return 

        # Find det icon med det største areal
        c = max(contours, key=cv2.contourArea)

        # Find afgrænsende firkant
        x, y, w, h = cv2.boundingRect(c)

        # Crop icon
        icon = img[y:y+h, x:x+w]

        #return resized icon
        return cv2.resize(icon, (new_width, new_height), 0, 0)
    
    def find_num(self):
        
        if self.num_img is None: return
        
        # lav et dict med key=filnavn og value=img
        num_img_dict = {x: cv2.imread("./test_cards/"+str(x)+".jpg", cv2.IMREAD_GRAYSCALE) for x in range(1,14)}
        
        # lav nyt dict med key=filnavn og value=absdiff (jo mindre et tal jo bedre et match)
        best_match_dict = {k: np.sum(cv2.absdiff(self.num_img, v)) for k, v in num_img_dict.items()}
        
        # sætter self.num til det bedste match
        self.num = min(best_match_dict, key=best_match_dict.get)

        
    def find_suit(self):
        
        if self.suit_img is None: return
        
        suits = ["h", "s", "d", "c"]
        
        # lav et dict med key=filnavn og value=img
        suit_img_dict = {x:cv2.imread("./test_cards/"+x+".jpg", cv2.IMREAD_GRAYSCALE) for x in suits}
        
        # lav nyt dict med key=filnavn og value=absdiff (jo mindre et tal jo bedre et match)
        best_match_dict = {k: np.sum(cv2.absdiff(self.suit_img, v)) for k, v in suit_img_dict.items()}
        
        # sætter self.suit til det bedste match
        self.suit = suits.index(min(best_match_dict, key=best_match_dict.get)) + 1
        
        
    def validate(self): return self.num is not None and self.suit is not None