import cv2
import numpy as np
import mediapipe as mp 
import math
import time 

def is_fit(lm):
    bout=[8, 12, 16, 20]
    articulations=[6, 10, 14, 18]
    return sum(lm[t].y > lm[b].y for t, b in zip(bout, articulations)) >= 3


def hand_dis(lm):
    return math.hypot(lm[4].x - lm[8].x, lm[4].y - lm[8].y)


def draw_skeleton(img, landmarks, w, h ):
    #les connections entre les points de la main 
    connections=mp_hands.HAND_CONNECTIONS

    #dessiner les lignes 
    for connection in connections:
        pt1=landmarks[connection[0]]
        pt2=landmarks[connection[1]]

        x1,y1=int(pt1.x*w), int(pt1.y*h)
        x2,y2=int(pt2.x*w), int(pt2.y*h)

         # ligne épaisse sombre (halo)
        cv2.line(img, (x1, y1), (x2, y2), (20, 20, 80), 6)
        # ligne fine brillante par dessus
        cv2.line(img, (x1, y1), (x2, y2), (255, 180, 50), 1)

        #dssiner les points 
    for i ,lm in enumerate(landmarks):
        x,y= int(lm.x*w), int(lm.y*h)

        if i == 0:   # poignet
            cv2.circle(img, (x, y), 10, (20, 20, 80), -1)
            cv2.circle(img, (x, y), 10, (255, 180, 50), 2)
            cv2.circle(img, (x, y), 4,  (255, 255, 255), -1)

        elif i in [4, 8, 12, 16, 20]:   # bouts des doigts
            cv2.circle(img, (x, y), 8, (20, 20, 80), -1)
            cv2.circle(img, (x, y), 8, (255, 100, 50), 2)
            cv2.circle(img, (x, y), 3, (255, 255, 255), -1)

        else:   # articulations normales
            cv2.circle(img, (x, y), 5, (20, 20, 80), -1)
            cv2.circle(img, (x, y), 5, (255, 180, 50), 1)
            cv2.circle(img, (x, y), 2, (255, 220, 100), -1)





# setup mediapipe
mp_hands   = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# OUVRIR LE WEBCAM 
cap = cv2.VideoCapture(0)

cols = 100
charset = "@&%WQNM0gB$#DR8mHXKAUbGOpV4d9h6Pkqws2E]ayj[xY5ZoeN[uLt13IfC}{iF|()7J(vTLs?zr*/cri+!><^,_:'.`- "  # les caractères utilisés pour représenter les différentes nuances de gris, du plus sombre au plus clair
ascii_mode   = False
poing_prev    = False
poing_start_t = None


with mp_hands.Hands(
    max_num_hands=1,         # nombre maximum de mains à détecter
    min_detection_confidence=0.7,  # confiance minimale pour la détection des mains
    min_tracking_confidence=0.6     # confiance minimale pour le suivi des mains
) as hands:
    
    while True:
        ret, frame = cap.read()     # ret est un bouléen qui indique si la capture a réussi ou non, frame est l'image capturée

        frame= cv2.flip(frame, 1)   # le 1 indique flipe horizontalement, -1 pour les deux axes, 0 pour verticalement

        h , w = frame.shape[:2]     # récupère la hauteur et la largeur de l'image 

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result=hands.process(rgb)
        

        poing_now=False
        now=time.time()

        if result.multi_hand_landmarks:
            lm=result.multi_hand_landmarks[0].landmark
            poing_now=is_fit(lm)
            distance=hand_dis(lm)

            if not poing_now and ascii_mode:
                # distance 0.02 → 0.30 devient cols 130 → 15
                t    = (distance - 0.02) / (0.30 - 0.02)   # 0.0 → 1.0
                t    = max(0.0, min(1.0, t))                # clamp entre 0 et 1
                cols = int(130 - t * (130 - 15))            # 130 → 15

        if poing_now :
            if not poing_prev:
                poing_start_t=now  
        else: 
            poing_start_t=None

        poing_tenu =(now - poing_start_t)   if poing_start_t else 0.0

        if not ascii_mode:
            if poing_now and poing_tenu >= 1.0:  # si le poing est maintenu pendant plus de 1 seconde
                ascii_mode = True     
                poing_start_t=None
        else:
            if poing_now and poing_tenu >= 2.0:
                ascii_mode = False
                poing_start_t=None

        poing_prev=poing_now

        if ascii_mode:

            case_w = w / cols         # C'est la largeur d'une case en pixels réels 
            rows = int(h / (case_w * 2))       # calcule le nombre de pixels par ligne en divisant la largeur de l'image par le nombre de lignes souhaité

            gray =cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convertit l'image en niveaux de gris
            small=cv2.resize(gray, (cols,rows))   # redimensionne l'image 

            indices = (small / 255.0 * (len(charset)-1)).astype(int)
            indices = np.clip(indices, 0, (len(charset)-1))

            img_noire = np.zeros((h,w, 3), dtype=np.uint8)   # crée une image noire de la même taille que le cadre capturé

            case_h=h/rows # calcule la hauteur d'une case en pixels réels

            small_color = cv2.resize(frame, (cols, rows))   # image couleur rétrécie
            
            for r  in range(rows):
                for c in range(cols):
                    char=charset[indices[r, c]]  # récupère le caractère correspondant à l'intensité de gris de la case
                    x=int(c*case_w)
                    y=int(r*case_h+case_h)

                    # ── couleur réelle du pixel ──
                    b, g, rv = small_color[r, c]
                    couleur  = (int(b), int(g), int(rv))

                    cv2.putText(img_noire, char, (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                max(0.3, case_w / 18),         # taille de la police
                                couleur,         # couleur réelle
                                1)
                    
            if result.multi_hand_landmarks:
                draw_skeleton(img_noire,
                                    result.multi_hand_landmarks[0].landmark,
                                    w, h)
    
            cv2.imshow("ASCII", img_noire)
        else:
            if result.multi_hand_landmarks:
                draw_skeleton(frame,
                                    result.multi_hand_landmarks[0].landmark,
                                    w, h)
            cv2.imshow('ASCII', frame)


        if cv2.waitKey(1)== ord('q'):  # ord() convertit le caractère 'q' en son code ASCII, waitKey(1) attend 1 milliseconde pour une touche et retourne son code ASCII si une touche est pressée  
            break

cap.release()
cv2.destroyAllWindows()
 

