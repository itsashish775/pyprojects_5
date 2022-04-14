import tkinter as tk
import cv2
import numpy as np
from PIL import Image
import pandas as pd
m=tk.Tk()
m.geometry("500x300")

# declaring global variables (are used later on)
clicked = False
r = g = b = x_pos = y_pos = 0
def liveDetection():
    def PIX(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:    
            r, g, b = rgbimg.getpixel((x, y))
            txt = str(r)+","+str(g)+","+str(b)
            bg = np.zeros((200, 400, 3), np.uint8)
            bg[:, 0:400] = (b, g, r)
            font = cv2.FONT_ITALIC
            cv2.putText(bg, txt, (10, 100), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow('rgb', bg)

    cap = cv2.VideoCapture(0)

    while(True):
        ret, frame = cap.read()
        flipped = cv2.flip(frame, 1)
        cv2.imshow('vid', flipped)
        if cv2.waitKey(1) & 0xFF == ord('c'): # press c to capture
            cv2.imwrite('1.png', flipped)
            imge = Image.open('1.png')
            rgbimg = imge.convert('RGB')
            cv2.imshow('pic', flipped)
            # function that captures the current pixel
            # and displays on a window
            cv2.setMouseCallback('pic', PIX)
        elif cv2.waitKey(1) & 0xFF == ord(' '): # hit space to quit
            break

        key2 = cv2.waitKey(1) & 0xFF
        if key2 == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
def colorDetection():
    global b, g, r, x_pos, y_pos, clicked
    img_path = r'colorpic3.jpg'
    img = cv2.imread(img_path)

    

    # Reading csv file with pandas and giving names to each column
    index = ["color", "color_name", "hex", "R", "G", "B"]
    csv = pd.read_csv('colors.csv', names=index, header=None)


    # function to calculate minimum distance from all colors and get the most matching color
    def get_color_name(R, G, B):
        minimum = 10000
        for i in range(len(csv)):
            d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
            if d <= minimum:
                minimum = d
                cname = csv.loc[i, "color_name"]
        return cname


    # function to get x,y coordinates of mouse double click
    def draw_function(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            global b, g, r, x_pos, y_pos, clicked
            clicked = True
            x_pos = x
            y_pos = y
            b, g, r = img[y, x]
            b = int(b)
            g = int(g)
            r = int(r)


    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_function)

    while True:

        cv2.imshow("image", img)
        if clicked:

            # cv2.rectangle(image, start point, endpoint, color, thickness)-1 fills entire rectangle
            cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

            # Creating text string to display( Color name and RGB values )
            text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

            # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
            cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

            # For very light colours we will display text in black colour
            if r + g + b >= 600:
                cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

            clicked = False

        # Break the loop when user hits 'esc' key
        if cv2.waitKey(20) & 0xFF == 27:
            break
        
        key2 = cv2.waitKey(1) & 0xFF
        if key2 == ord('q'):
            break

    cv2.destroyAllWindows()
if __name__ == "__main__":
    button = tk.Button(m, text='Live Detection', width=25,command=liveDetection)
    button.pack()
    button2 = tk.Button(m, text='Image Detection', width=25,command=colorDetection)
    button2.pack()
    
    m.mainloop()
    
    
    