import time
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont ,ImageSequence
from adafruit_rgb_display import st7789
import numpy as np
import random
import pygame 
import os
import sys


class Joystick:
    def __init__(self):
        self.cs_pin = DigitalInOut(board.CE0)
        self.dc_pin = DigitalInOut(board.D25)
        self.reset_pin = DigitalInOut(board.D24)
        self.BAUDRATE = 24000000

        self.spi = board.SPI()
        self.disp = st7789.ST7789(
                    self.spi,
                    height=240,
                    y_offset=80,
                    rotation=180,
                    cs=self.cs_pin,
                    dc=self.dc_pin,
                    rst=self.reset_pin,
                    baudrate=self.BAUDRATE,
                    )

        # Input pins:
        self.button_A = DigitalInOut(board.D5)
        self.button_A.direction = Direction.INPUT

        self.button_B = DigitalInOut(board.D6)
        self.button_B.direction = Direction.INPUT

        self.button_L = DigitalInOut(board.D27)
        self.button_L.direction = Direction.INPUT

        self.button_R = DigitalInOut(board.D23)
        self.button_R.direction = Direction.INPUT

        self.button_U = DigitalInOut(board.D17)
        self.button_U.direction = Direction.INPUT

        self.button_D = DigitalInOut(board.D22)
        self.button_D.direction = Direction.INPUT

        self.button_C = DigitalInOut(board.D4)
        self.button_C.direction = Direction.INPUT

        # Turn on the Backlight
        self.backlight = DigitalInOut(board.D26)
        self.backlight.switch_to_output()
        self.backlight.value = True

        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for color.
        self.width = self.disp.width
        self.height = self.disp.height



class Character:
    def __init__(self, width, height):

        image_path = "/home/JOEY/esw project/extra/man_stay1_.png"
        character_image = Image.open(image_path)
        c_width, c_height = character_image.size
        new_width = c_width * 2  
        new_height = c_height * 2  
        character_image = character_image.resize((new_width, new_height))

        self.state = None
        self.position = np.array([width/2 - 20, height - c_height*2-10, width/2 + 20, height-50])
        self.outline = "#FFFFFF"
        self.appearance = character_image

    def move(self, command = None):
        if command['move'] == False:
            self.state = None
            
        
        else:
            self.state = 'move'
            

            if command['up_pressed']:
                self.position[1] -= 5
                self.position[3] -= 5

            if command['down_pressed']:
                self.position[1] += 5
                self.position[3] += 5

            if command['left_pressed']:
                self.position[0] -= 7
                self.position[2] -= 7
                
            if command['right_pressed']:
                self.position[0] += 7
                self.position[2] += 7
         
joystick = Joystick()
my_image = Image.new("RGB", (joystick.width, joystick.height)) #도화지!
my_draw = ImageDraw.Draw(my_image) #그리는 도구!
pygame.init()


#브금 함수
def bgm(audio_path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()




def monologue(text): 
    while True:
         if joystick.button_A.value ==False:
             
            my_draw.rectangle((0, joystick.height-70, joystick.width, joystick.height), fill=(255, 255, 255))
            text_width, text_height = my_draw.textsize(text, font=font)
            text_position = ((joystick.width - text_width) // 2, joystick.height - 70 + (70 - text_height) // 2)
            my_draw.text(text_position, text, font=font, fill=(0, 0, 0))  
            joystick.disp.image(my_image)
            time.sleep(0.5) 
            break

my_man = Character(joystick.width, joystick.height)
def stay():
    if joystick.button_L.value and joystick.button_R.value :
        image_path1 = "/home/JOEY/esw project/extra/man_stay1_.png"
        image_path2 = "/home/JOEY/esw project/extra/man_stay2_.png"
        image_paths = [image_path1,image_path1,image_path1,image_path1,image_path1,image_path1,image_path2,image_path2,image_path2,image_path2,image_path2,image_path2]
        
        character_image = Image.open(image_paths[background_index])
        c_width, c_height = character_image.size
        new_width = c_width * 2  
        new_height = c_height * 2  
        character_image = character_image.resize((new_width, new_height))
        my_man.appearance = character_image


font_size = 20
font = ImageFont.truetype("/home/JOEY/esw project/extra/tt.ttf", font_size)  
text = "Press the A button \n      to start game"  
text_width, text_height = my_draw.textsize(text, font=font)
text_position = ((joystick.width - text_width) // 2, (joystick.height - text_height) // 2)

my_draw.rectangle((0, 0, joystick.width, joystick.height), fill=(255, 255, 255))  



bgm("/home/JOEY/esw project/extra/startpg_bgm.mp3")


while joystick.button_A.value:  
    my_draw.rectangle((text_position[0], text_position[1], text_position[0] + text_width, text_position[1] + text_height + 10), fill=(255, 255, 255))  
    joystick.disp.image(my_image)

    time.sleep(0.5)  
    
    my_draw.text(text_position, text, font=font, fill=(0, 0, 0))  
    joystick.disp.image(my_image)

    time.sleep(0.5)  






background_image_1 = Image.open("/home/JOEY/esw project/extra/first_background_1.png")
background_image_2 = Image.open("/home/JOEY/esw project/extra/first_background_2.png")
background_images = [background_image_1,background_image_1,background_image_1,background_image_1,background_image_1,background_image_1 ,background_image_2,background_image_2,background_image_2,background_image_2,background_image_2,background_image_2]

bgm("/home/JOEY/esw project/extra/pg1_peace.mp3")

start_time = time.time()
end_time = start_time + 10   # Run for 7 seconds
background_index = 0
Rwalking_index = 0
Lwalking_index = 0


while time.time() < end_time:
    command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}

    if not joystick.button_L.value:  # left pressed
        command['left_pressed'] = True
        command['move'] = True

        image_Lpath_a = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_1.png"
        image_Lpath_b = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_2.png"
        image_Lpath_c ="/home/JOEY/esw project/extra/Lwalking/man_Lwalking_3.png"
        image_Lpath_d = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_4.png"
        image_Lwalking = [image_Lpath_a,image_Lpath_a,image_Lpath_b,image_Lpath_b,image_Lpath_c,image_Lpath_c,image_Lpath_d,image_Lpath_d]
        Lwalking_index = (Lwalking_index + 1) % len(image_Lwalking)
        character_image = Image.open(image_Lwalking[Lwalking_index])
        c_width, c_height = character_image.size
        new_width = c_width * 2  
        new_height = c_height * 2  
        character_image = character_image.resize((new_width, new_height))
        my_man.appearance = character_image
    

    if not joystick.button_R.value:  # right pressed
        command['right_pressed'] = True
        command['move'] = True

        image_Rpath_a = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_1.png"
        image_Rpath_b = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_2.png"
        image_Rpath_c ="/home/JOEY/esw project/extra/Rwalking/man_Rwalking_3.png"
        image_Rpath_d = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_4.png"
        image_Rwalking = [image_Rpath_a,image_Rpath_a,image_Rpath_b,image_Rpath_b,image_Rpath_c,image_Rpath_c,image_Rpath_d,image_Rpath_d]
        Rwalking_index = (Rwalking_index + 1) % len(image_Rwalking)
        character_image = Image.open(image_Rwalking[Rwalking_index])
        c_width, c_height = character_image.size
        new_width = c_width * 2  
        new_height = c_height * 2  
        character_image = character_image.resize((new_width, new_height))
        my_man.appearance = character_image

    stay()


    my_man.move(command)

    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
    my_image.paste(background_images[background_index], (0, 0))

    my_image.paste(my_man.appearance, (int(my_man.position[0]), int(my_man.position[1])), my_man.appearance)

    joystick.disp.image(my_image)
    background_index = (background_index + 1) % len(background_images)

    
    


bgm("/home/JOEY/esw project/extra/thrill.mp3")
text="평화로운 날이었다."
my_draw.rectangle((0, joystick.height-70, joystick.width, joystick.height), fill=(255, 255, 255))
text_width, text_height = my_draw.textsize(text, font=font)
text_position = ((joystick.width - text_width) // 2, joystick.height - 70 + (70 - text_height) // 2)
my_draw.text(text_position, text, font=font, fill=(0, 0, 0))  
joystick.disp.image(my_image)

monologue("하지만")
monologue("평화는 잠시였다.")
time.sleep(1)

pygame.mixer.music.stop()


frame_index = 0
frames = []

for i in range(263):
    filename = f"/home/JOEY/esw project/extra/2/first scene{i:03d}.png"
    frames.append(Image.open(filename))
bgm("/home/JOEY/esw project/extra/kidnap.mp3")
while frame_index < len(frames)-40:
    my_image.paste(frames[frame_index], (0, 0))
    joystick.disp.image(my_image)
    frame_index = (frame_index + 1) % len(frames)




Rwalking_index = 0
Lwalking_index = 0
stay_index = 0
background_image = Image.open("/home/JOEY/esw project/extra/second_background.png")
start_time = time.time()
end_time = start_time + 4   # Run for 7 seconds


while time.time() < end_time:
    command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}

    if not joystick.button_L.value:  # left pressed
        command['left_pressed'] = True
        command['move'] = True
        image_Lpath_a = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_1.png"
        image_Lpath_b = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_2.png"
        image_Lpath_c ="/home/JOEY/esw project/extra/Lwalking/man_Lwalking_3.png"
        image_Lpath_d = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_4.png"
        image_Lwalking = [image_Lpath_a,image_Lpath_a,image_Lpath_b,image_Lpath_b,image_Lpath_c,image_Lpath_c,image_Lpath_d,image_Lpath_d]
        Lwalking_index = (Lwalking_index + 1) % len(image_Lwalking)
        character_image = Image.open(image_Lwalking[Lwalking_index])

        my_man.appearance = character_image
    

    if not joystick.button_R.value:  # right pressed
        command['right_pressed'] = True
        command['move'] = True
        image_Rpath_a = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_1.png"
        image_Rpath_b = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_2.png"
        image_Rpath_c ="/home/JOEY/esw project/extra/Rwalking/man_Rwalking_3.png"
        image_Rpath_d = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_4.png"
        image_Rwalking = [image_Rpath_a,image_Rpath_a,image_Rpath_b,image_Rpath_b,image_Rpath_c,image_Rpath_c,image_Rpath_d,image_Rpath_d]
        Rwalking_index = (Rwalking_index + 1) % len(image_Rwalking)
        character_image = Image.open(image_Rwalking[Rwalking_index])

        my_man.appearance = character_image

    if joystick.button_L.value and joystick.button_R.value :
        image_path1 = "/home/JOEY/esw project/extra/man_stay1_.png"
        image_path2 = "/home/JOEY/esw project/extra/man_stay2_.png"
        image_paths = [image_path1,image_path1,image_path1,image_path1,image_path1,image_path1,image_path2,image_path2,image_path2,image_path2,image_path2,image_path2]
        
        character_image = Image.open(image_paths[stay_index])

        my_man.appearance = character_image


    my_man.move(command)

    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
    my_image.paste(background_image, (0, 0),)

    my_image.paste(my_man.appearance, (int(my_man.position[0]), int(my_man.position[1])-10), my_man.appearance)

    joystick.disp.image(my_image)
    stay_index = (stay_index + 1) % len(image_paths)




bgm("/home/JOEY/esw project/extra/choice.mp3")
text="마법사가 있다."
my_draw.rectangle((0, joystick.height-70, joystick.width, joystick.height), fill=(255, 255, 255))
text_width, text_height = my_draw.textsize(text, font=font)
text_position = ((joystick.width - text_width) // 2, joystick.height - 70 + (70 - text_height) // 2)
my_draw.text(text_position, text, font=font, fill=(0, 0, 0)) 
joystick.disp.image(my_image) 

monologue("마법사에게 대화를 \n 걸어보자.")
monologue("a를 눌러 대화를 \n 시작해보자.")   




Rwalking_index = 0
Lwalking_index = 0
stay_index = 0
background_image = Image.open("/home/JOEY/esw project/extra/second_background.png")
bgm("/home/JOEY/esw project/extra/pg2_peace.mp3")

while True:
    command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}

    if not joystick.button_L.value:  # left pressed
        command['left_pressed'] = True
        command['move'] = True
        image_Lpath_a = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_1.png"
        image_Lpath_b = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_2.png"
        image_Lpath_c ="/home/JOEY/esw project/extra/Lwalking/man_Lwalking_3.png"
        image_Lpath_d = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_4.png"
        image_Lwalking = [image_Lpath_a,image_Lpath_a,image_Lpath_b,image_Lpath_b,image_Lpath_c,image_Lpath_c,image_Lpath_d,image_Lpath_d]
        Lwalking_index = (Lwalking_index + 1) % len(image_Lwalking)
        character_image = Image.open(image_Lwalking[Lwalking_index])

        my_man.appearance = character_image
    

    if not joystick.button_R.value:  # right pressed
        command['right_pressed'] = True
        command['move'] = True
        image_Rpath_a = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_1.png"
        image_Rpath_b = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_2.png"
        image_Rpath_c ="/home/JOEY/esw project/extra/Rwalking/man_Rwalking_3.png"
        image_Rpath_d = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_4.png"
        image_Rwalking = [image_Rpath_a,image_Rpath_a,image_Rpath_b,image_Rpath_b,image_Rpath_c,image_Rpath_c,image_Rpath_d,image_Rpath_d]
        Rwalking_index = (Rwalking_index + 1) % len(image_Rwalking)
        character_image = Image.open(image_Rwalking[Rwalking_index])

        my_man.appearance = character_image

    if joystick.button_L.value and joystick.button_R.value :
        image_path1 = "/home/JOEY/esw project/extra/man_stay1_.png"
        image_path2 = "/home/JOEY/esw project/extra/man_stay2_.png"
        image_paths = [image_path1,image_path1,image_path1,image_path1,image_path1,image_path1,image_path2,image_path2,image_path2,image_path2,image_path2,image_path2]
        
        character_image = Image.open(image_paths[stay_index])

        my_man.appearance = character_image
    if not joystick.button_A.value and 130<(my_man.position[0])<160:
        
        bgm("/home/JOEY/esw project/extra/choice.mp3")
        background_image = Image.open("/home/JOEY/esw project/extra/magician_quest1.png")
        my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
        my_image.paste(background_image, (0, 0),)
        my_image.paste(my_man.appearance, (int(my_man.position[0]), int(my_man.position[1])-10), my_man.appearance)
        joystick.disp.image(my_image)
        time.sleep(0.02)

        background_image = Image.open("/home/JOEY/esw project/extra/magician_quest2.png")
        my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
        my_image.paste(background_image, (0, 0),)
        my_image.paste(my_man.appearance, (int(my_man.position[0]), int(my_man.position[1])-10), my_man.appearance)
        joystick.disp.image(my_image)
        time.sleep(0.02)

        background_image = Image.open("/home/JOEY/esw project/extra/magician_quest1.png")
        my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
        my_image.paste(background_image, (0, 0),)
        my_image.paste(my_man.appearance, (int(my_man.position[0]), int(my_man.position[1])-10), my_man.appearance)
        joystick.disp.image(my_image)
        time.sleep(1.5)

        text="마법사: 공주가 잡혀갔다네. "
        my_draw.rectangle((0, joystick.height-70, joystick.width, joystick.height), fill=(255, 255, 255))
        text_width, text_height = my_draw.textsize(text, font=font)
        text_position = ((joystick.width - text_width) // 2, joystick.height - 70 + (70 - text_height) // 2)
        my_draw.text(text_position, text, font=font, fill=(0, 0, 0)) 
        joystick.disp.image(my_image) 
        while True:
            if joystick.button_A.value ==False:
                break
        break
    
    my_man.move(command)

    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
    my_image.paste(background_image, (0, 0),)

    my_image.paste(my_man.appearance, (int(my_man.position[0]), int(my_man.position[1])-10), my_man.appearance)

    joystick.disp.image(my_image)
    stay_index = (stay_index + 1) % len(image_paths)


def rip():

    frame_index = 0
    frames = []
    for i in range(1000, 1124):
        filename = f"/home/JOEY/esw project/sadending/render029_{i:03d}.png"
        frames.append(Image.open(filename))

    bgm("/home/JOEY/esw project/extra/sad_ending_bgm.mp3")
    while frame_index < len(frames)-10:
        my_image.paste(frames[frame_index], (0, 0))
        joystick.disp.image(my_image)
        frame_index = (frame_index + 1) % len(frames)




monologue("마법사:공주를 구해주게나.")
time.sleep(0.5)
while True:
    text="모험가:네 알겠습니다.(A)\n모험가:제가 왜요?(B)"
    my_draw.rectangle((0, joystick.height-70, joystick.width, joystick.height), fill=(255, 255, 255))
    text_width, text_height = my_draw.textsize(text, font=font)
    text_position = ((joystick.width - text_width) // 2, joystick.height - 70 + (70 - text_height) // 2)
    my_draw.text(text_position, text, font=font, fill=(0, 0, 0))  
    joystick.disp.image(my_image)
    time.sleep(1) 


    while True:
        if joystick.button_A.value ==False:
            text="모험가:네 알겠습니다."
            my_draw.rectangle((0, joystick.height-70, joystick.width, joystick.height), fill=(255, 255, 255))
            text_width, text_height = my_draw.textsize(text, font=font)
            text_position = ((joystick.width - text_width) // 2, joystick.height - 70 + (70 - text_height) // 2)
            my_draw.text(text_position, text, font=font, fill=(0, 0, 0))  
            joystick.disp.image(my_image)
            time.sleep(0.5)
            break

        if joystick.button_B.value == False:

            text="모험가:제가 왜요?"
            my_draw.rectangle((0, joystick.height-70, joystick.width, joystick.height), fill=(255, 255, 255))
            text_width, text_height = my_draw.textsize(text, font=font)
            text_position = ((joystick.width - text_width) // 2, joystick.height - 70 + (70 - text_height) // 2)
            my_draw.text(text_position, text, font=font, fill=(0, 0, 0))  
            joystick.disp.image(my_image)
            time.sleep(0.5)
            font_size = 15
            font = ImageFont.truetype("/home/JOEY/esw project/extra/tt.ttf", font_size)  
            monologue("마법사:공주를 구한다면\n 왕국의 왕자가 될 수 있다네!")
            monologue("모험가:오 그럼 노력하겠습니다.(A)\n 모험가:그래도 싫어요.(B)")
            while True:
                if joystick.button_A.value ==False:
                    text="모험가:오 그럼 노력하겠습니다."
                    my_draw.rectangle((0, joystick.height-70, joystick.width, joystick.height), fill=(255, 255, 255))
                    text_width, text_height = my_draw.textsize(text, font=font)
                    text_position = ((joystick.width - text_width) // 2, joystick.height - 70 + (70 - text_height) // 2)
                    my_draw.text(text_position, text, font=font, fill=(0, 0, 0))  
                    joystick.disp.image(my_image)
                    time.sleep(0.5)
                    break

                if joystick.button_B.value == False:
                    text="모험가:그래도 싫어요."
                    my_draw.rectangle((0, joystick.height-70, joystick.width, joystick.height), fill=(255, 255, 255))
                    text_width, text_height = my_draw.textsize(text, font=font)
                    text_position = ((joystick.width - text_width) // 2, joystick.height - 70 + (70 - text_height) // 2)
                    my_draw.text(text_position, text, font=font, fill=(0, 0, 0))  
                    joystick.disp.image(my_image)
                    time.sleep(0.5)
                    rip()
                    break 
            break
    break


my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
joystick.disp.image(my_image)
bgm("/home/JOEY/esw project/extra/walking.mp3")
time.sleep(2)


bgm("/home/JOEY/esw project/extra/quizbgm.mp3")
background_image = Image.open("/home/JOEY/esw project/extra/back1.png")
n = random.randint(1, 10)
a = random.randint(1, 10)
random_quiz = f"{n} × {a}"
random_quiz_answer = n * a
c = random.randint(random_quiz_answer + 1 , random_quiz_answer + 20)
d = random.randint(random_quiz_answer + 1 , random_quiz_answer + 11)


options = [c, d, random_quiz_answer]
random.shuffle(options)  # 리스트를 섞음
L, R, C = options

font_size = 22
font = ImageFont.truetype("/home/JOEY/esw project/extra/tt.ttf", font_size)  

text_width, text_height = my_draw.textsize(random_quiz, font=font)
text_position = ((joystick.width - text_width) // 2, 10)

text_width_C, text_height_C = my_draw.textsize(str(C), font=font)
text_width_L, text_height_L = my_draw.textsize(str(L), font=font)
text_width_R, text_height_R = my_draw.textsize(str(R), font=font)


text_position_C = ((joystick.width - text_width_C) // 2 , 160)
text_position_L = ((joystick.width - text_width_L) // 2 - 80, 160) 
text_position_R = ((joystick.width - text_width_R) // 2 + 80, 160) 

while True:
    command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}

    if not joystick.button_L.value:  # left pressed
        command['left_pressed'] = True
        command['move'] = True
        image_Lpath_a = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_1.png"
        image_Lpath_b = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_2.png"
        image_Lpath_c ="/home/JOEY/esw project/extra/Lwalking/man_Lwalking_3.png"
        image_Lpath_d = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_4.png"
        image_Lwalking = [image_Lpath_a,image_Lpath_a,image_Lpath_b,image_Lpath_b,image_Lpath_c,image_Lpath_c,image_Lpath_d,image_Lpath_d]
        Lwalking_index = (Lwalking_index + 1) % len(image_Lwalking)
        character_image = Image.open(image_Lwalking[Lwalking_index])

        my_man.appearance = character_image
    

    if not joystick.button_R.value:  # right pressed
        command['right_pressed'] = True
        command['move'] = True
        image_Rpath_a = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_1.png"
        image_Rpath_b = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_2.png"
        image_Rpath_c ="/home/JOEY/esw project/extra/Rwalking/man_Rwalking_3.png"
        image_Rpath_d = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_4.png"
        image_Rwalking = [image_Rpath_a,image_Rpath_a,image_Rpath_b,image_Rpath_b,image_Rpath_c,image_Rpath_c,image_Rpath_d,image_Rpath_d]
        Rwalking_index = (Rwalking_index + 1) % len(image_Rwalking)
        character_image = Image.open(image_Rwalking[Rwalking_index])

        my_man.appearance = character_image

    
    
    my_man.move(command)
    
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
    my_image.paste(background_image, (0, 0))
    my_draw.rectangle((text_position[0]-15, text_position[1], text_position[0] + text_width + 15, text_position[1] + text_height + 10), fill=(0, 0, 0)) #문제
    
    my_draw.rectangle((text_position_C[0], text_position_C[1], text_position_C[0] + text_width_C, text_position_C[1] + text_height_C ), fill=(0, 0, 255))#가운데
    my_draw.text(text_position_C, str(C), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_L[0], text_position_L[1], text_position_L[0] + text_width_L , text_position_L[1] + text_height_L), fill=(0, 255, 0))#왼쪽
    my_draw.text(text_position_L, str(L), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_R[0], text_position_R[1], text_position_R[0] + text_width_R , text_position_R[1] + text_height_R ), fill=(255, 255, 0))#오른쪽
    my_draw.text(text_position_R, str(R), font=font, fill=(0, 0, 0))
    C_L =text_position_C[0]-20
    C_R =text_position_C[0] + text_width_C + 20
    L_L =text_position_L[0]-20
    L_R =text_position_L[0] + text_width_L + 20
    R_L =text_position_R[0]+20
    R_R =text_position_R[0] + text_width_R + 20
    
    
    


    my_draw.text(text_position, random_quiz, font=font, fill=(255, 255, 255))
    my_image.paste(my_man.appearance, (int(my_man.position[0]), int(my_man.position[1]+35)), my_man.appearance)
    
    joystick.disp.image(my_image)
    if joystick.button_A.value == False:
        if C_L < my_man.position[0] < C_R: #가운데
            if C == random_quiz_answer:
               break 
            else:
                rip()
                break
        if L_L < my_man.position[0] < L_R: #왼쪽
            if L == random_quiz_answer:
                break
            else:
                rip()
                break
        if R_L < my_man.position[0] < R_R: #오른쪽
            if R == random_quiz_answer:
               break
            else:
                rip()
                break
    

my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
joystick.disp.image(my_image)
bgm("/home/JOEY/esw project/extra/walking.mp3")
time.sleep(2)

bgm("/home/JOEY/esw project/extra/quizbgm.mp3")


background_image = Image.open("/home/JOEY/esw project/extra/back2.png")
n = random.randint(1, 10)
a = random.randint(1, 10)
random_quiz = f"{n} × {a}"
random_quiz_answer = n * a
c = random.randint(random_quiz_answer + 1 , random_quiz_answer + 20)
d = random.randint(random_quiz_answer + 1 , random_quiz_answer + 11)


options = [c, d, random_quiz_answer]
random.shuffle(options)  # 리스트를 섞음
L, R, C = options

font_size = 22
font = ImageFont.truetype("/home/JOEY/esw project/extra/tt.ttf", font_size)  

text_width, text_height = my_draw.textsize(random_quiz, font=font)
text_position = ((joystick.width - text_width) // 2, 10)

text_width_C, text_height_C = my_draw.textsize(str(C), font=font)
text_width_L, text_height_L = my_draw.textsize(str(L), font=font)
text_width_R, text_height_R = my_draw.textsize(str(R), font=font)


text_position_C = ((joystick.width - text_width_C) // 2 , 160)
text_position_L = ((joystick.width - text_width_L) // 2 - 80, 160) 
text_position_R = ((joystick.width - text_width_R) // 2 + 80, 160) 

while True:
    command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}

    if not joystick.button_L.value:  # left pressed
        command['left_pressed'] = True
        command['move'] = True
        image_Lpath_a = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_1.png"
        image_Lpath_b = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_2.png"
        image_Lpath_c ="/home/JOEY/esw project/extra/Lwalking/man_Lwalking_3.png"
        image_Lpath_d = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_4.png"
        image_Lwalking = [image_Lpath_a,image_Lpath_a,image_Lpath_b,image_Lpath_b,image_Lpath_c,image_Lpath_c,image_Lpath_d,image_Lpath_d]
        Lwalking_index = (Lwalking_index + 1) % len(image_Lwalking)
        character_image = Image.open(image_Lwalking[Lwalking_index])

        my_man.appearance = character_image
    

    if not joystick.button_R.value:  # right pressed
        command['right_pressed'] = True
        command['move'] = True
        image_Rpath_a = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_1.png"
        image_Rpath_b = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_2.png"
        image_Rpath_c ="/home/JOEY/esw project/extra/Rwalking/man_Rwalking_3.png"
        image_Rpath_d = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_4.png"
        image_Rwalking = [image_Rpath_a,image_Rpath_a,image_Rpath_b,image_Rpath_b,image_Rpath_c,image_Rpath_c,image_Rpath_d,image_Rpath_d]
        Rwalking_index = (Rwalking_index + 1) % len(image_Rwalking)
        character_image = Image.open(image_Rwalking[Rwalking_index])

        my_man.appearance = character_image

    
    
    my_man.move(command)
    
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
    my_image.paste(background_image, (0, 0))
    my_draw.rectangle((text_position[0]-15, text_position[1], text_position[0] + text_width + 15, text_position[1] + text_height + 10), fill=(0, 0, 0)) #문제
    
    my_draw.rectangle((text_position_C[0], text_position_C[1], text_position_C[0] + text_width_C, text_position_C[1] + text_height_C ), fill=(0, 0, 255))#가운데
    my_draw.text(text_position_C, str(C), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_L[0], text_position_L[1], text_position_L[0] + text_width_L , text_position_L[1] + text_height_L), fill=(0, 255, 0))#왼쪽
    my_draw.text(text_position_L, str(L), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_R[0], text_position_R[1], text_position_R[0] + text_width_R , text_position_R[1] + text_height_R ), fill=(255, 255, 0))#오른쪽
    my_draw.text(text_position_R, str(R), font=font, fill=(0, 0, 0))
    C_L =text_position_C[0]-10
    C_R =text_position_C[0] + text_width_C + 10
    L_L =text_position_L[0]-10
    L_R =text_position_L[0] + text_width_L + 10
    R_L =text_position_R[0]+10
    R_R =text_position_R[0] + text_width_R + 10
    
    
    


    my_draw.text(text_position, random_quiz, font=font, fill=(255, 255, 255))
    my_image.paste(my_man.appearance, (int(my_man.position[0]), int(my_man.position[1]+35)), my_man.appearance)
    
    joystick.disp.image(my_image)
    if joystick.button_A.value == False:
        if C_L < my_man.position[0] < C_R: #가운데
            if C == random_quiz_answer:
               break 
            else:
                rip()
                break
        if L_L < my_man.position[0] < L_R: #왼쪽
            if L == random_quiz_answer:
                break
            else:
                rip()
                break
        if R_L < my_man.position[0] < R_R: #오른쪽
            if R == random_quiz_answer:
               break
            else:
                rip()
                break
    

my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
joystick.disp.image(my_image)
bgm("/home/JOEY/esw project/extra/walking.mp3")
time.sleep(2)

bgm("/home/JOEY/esw project/extra/quizbgm.mp3")
background_image = Image.open("/home/JOEY/esw project/extra/back3.png")

l1 = "6개"
l2 = "7개"
l3 = "9개"
l4 = "10개"
l5 ="0"
font_size = 15
font = ImageFont.truetype("/home/JOEY/esw project/extra/tt.ttf", font_size)  
random_quiz = "태양계에 몇 개의 행성이 있을까요?"
random_quiz_answer = "8개"




options = [l1, l2, random_quiz_answer, l3, l4]
random.shuffle(options)  # 리스트를 섞음
l1, l2, l3 , l4 , l5 = options


text_width, text_height = my_draw.textsize(random_quiz, font=font)
text_position = ((joystick.width - text_width) // 2, 10)

text_width_l1, text_height_l1 = my_draw.textsize(l1, font=font)
text_width_l2, text_height_l2 = my_draw.textsize(l2, font=font)
text_width_l3, text_height_l3 = my_draw.textsize(l3, font=font)
text_width_l4, text_height_l4 = my_draw.textsize(l4, font=font)
text_width_l5, text_height_l5 = my_draw.textsize(l5, font=font)

text_position_l1 = ((joystick.width - text_width_l1) // 2 - 95, 155)
text_position_l2 = ((joystick.width - text_width_l2) // 2 - 45, 120) 
text_position_l3 = ((joystick.width - text_width_l3) // 2, 155) 
text_position_l4 = ((joystick.width - text_width_l4) // 2 + 45, 120) 
text_position_l5 = ((joystick.width - text_width_l5) // 2 + 90, 155) 

while True:
    command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}

    if not joystick.button_L.value:  # left pressed
        command['left_pressed'] = True
        command['move'] = True
        image_Lpath_a = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_1.png"
        image_Lpath_b = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_2.png"
        image_Lpath_c ="/home/JOEY/esw project/extra/Lwalking/man_Lwalking_3.png"
        image_Lpath_d = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_4.png"
        image_Lwalking = [image_Lpath_a,image_Lpath_a,image_Lpath_b,image_Lpath_b,image_Lpath_c,image_Lpath_c,image_Lpath_d,image_Lpath_d]
        Lwalking_index = (Lwalking_index + 1) % len(image_Lwalking)
        character_image = Image.open(image_Lwalking[Lwalking_index])

        my_man.appearance = character_image
    

    if not joystick.button_R.value:  # right pressed
        command['right_pressed'] = True
        command['move'] = True
        image_Rpath_a = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_1.png"
        image_Rpath_b = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_2.png"
        image_Rpath_c ="/home/JOEY/esw project/extra/Rwalking/man_Rwalking_3.png"
        image_Rpath_d = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_4.png"
        image_Rwalking = [image_Rpath_a,image_Rpath_a,image_Rpath_b,image_Rpath_b,image_Rpath_c,image_Rpath_c,image_Rpath_d,image_Rpath_d]
        Rwalking_index = (Rwalking_index + 1) % len(image_Rwalking)
        character_image = Image.open(image_Rwalking[Rwalking_index])

        my_man.appearance = character_image

    
    
    my_man.move(command)
    
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
    my_image.paste(background_image, (0, 0))
    my_draw.rectangle((text_position[0]-15, text_position[1], text_position[0] + text_width + 15, text_position[1] + text_height + 10), fill=(0, 0, 0)) #문제
    
    my_draw.rectangle((text_position_l1[0], text_position_l1[1] , text_position_l1[0] + text_width_l1 , text_position_l1[1] + text_height_l1 ), fill=(255, 255, 0))#l1
    my_draw.text(text_position_l1, str(l1), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_l2[0], text_position_l2[1] , text_position_l2[0] + text_width_l2 , text_position_l2[1] + text_height_l2 ), fill=(255, 255, 0))#l2
    my_draw.text(text_position_l2, str(l2), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_l3[0] , text_position_l3[1], text_position_l3[0] + text_width_l3 , text_position_l3[1] + text_height_l3), fill=(255, 255, 0))#l3
    my_draw.text(text_position_l3, str(l3), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_l4[0], text_position_l4[1] , text_position_l4[0] + text_width_l4 , text_position_l4[1] + text_height_l4 ), fill=(255, 255, 0))#l4
    my_draw.text(text_position_l4, str(l4), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_l5[0], text_position_l5[1] , text_position_l5[0] + text_width_l5 , text_position_l5[1] + text_height_l5 ), fill=(255, 255, 0))#l4
    my_draw.text(text_position_l5, str(l5), font=font, fill=(0, 0, 0))



    
    
    

    my_draw.text(text_position, random_quiz, font=font, fill=(255, 255, 255))
    my_image.paste(my_man.appearance, (int(my_man.position[0]), int(my_man.position[1]+35)), my_man.appearance)
    
    joystick.disp.image(my_image)
    if joystick.button_A.value == False:
        if text_position_l1[0] - 7 < my_man.position[0] < text_position_l1[0] + text_width_l1 + 7 : #l1
            if l1 == random_quiz_answer:
               break 
            else:
                rip()
                break
        if text_position_l2[0] - 7< my_man.position[0] < text_position_l2[0] + text_width_l2 + 7: #l2
            if l2 == random_quiz_answer:
               break 
            else:
                rip()
                break
        if text_position_l3[0] - 7< my_man.position[0] < text_position_l3[0] + text_width_l3 + 7 : #l3
            if l3 == random_quiz_answer:
               break 
            else:
                rip()
                break
        if text_position_l4[0] - 7< my_man.position[0] < text_position_l4[0] + text_width_l4 + 7: #l4
            if l4 == random_quiz_answer:
               break 
            else:
                rip()
                break
        if text_position_l5[0] - 7< my_man.position[0] < text_position_l5[0] + text_width_l5 + 7: #l5
            if l5 == random_quiz_answer:
               break 
            else:
                rip()
                break        
    

my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
joystick.disp.image(my_image)
bgm("/home/JOEY/esw project/extra/walking.mp3")
time.sleep(2)

bgm("/home/JOEY/esw project/extra/quizbgm.mp3")
background_image = Image.open("/home/JOEY/esw project/extra/back4.png")

l1 = "목성"
l2 = "금성"
l3 = "화성"
l4 = "수성"
l5 ="0"
font_size = 15
font = ImageFont.truetype("/home/JOEY/esw project/extra/tt.ttf", font_size)  
random_quiz = "태양계에서 세 번째로 가까운 행성은?"
random_quiz_answer = "지구"




options = [l1, l2, random_quiz_answer, l3, l4]
random.shuffle(options)  # 리스트를 섞음
l1, l2, l3 , l4 , l5 = options


text_width, text_height = my_draw.textsize(random_quiz, font=font)
text_position = ((joystick.width - text_width) // 2, 10)

text_width_l1, text_height_l1 = my_draw.textsize(l1, font=font)
text_width_l2, text_height_l2 = my_draw.textsize(l2, font=font)
text_width_l3, text_height_l3 = my_draw.textsize(l3, font=font)
text_width_l4, text_height_l4 = my_draw.textsize(l4, font=font)
text_width_l5, text_height_l5 = my_draw.textsize(l5, font=font)

text_position_l1 = ((joystick.width - text_width_l1) // 2 - 95, 155)
text_position_l2 = ((joystick.width - text_width_l2) // 2 - 45, 120) 
text_position_l3 = ((joystick.width - text_width_l3) // 2, 155) 
text_position_l4 = ((joystick.width - text_width_l4) // 2 + 45, 120) 
text_position_l5 = ((joystick.width - text_width_l5) // 2 + 90, 155) 

while True:
    command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}

    if not joystick.button_L.value:  # left pressed
        command['left_pressed'] = True
        command['move'] = True
        image_Lpath_a = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_1.png"
        image_Lpath_b = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_2.png"
        image_Lpath_c ="/home/JOEY/esw project/extra/Lwalking/man_Lwalking_3.png"
        image_Lpath_d = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_4.png"
        image_Lwalking = [image_Lpath_a,image_Lpath_a,image_Lpath_b,image_Lpath_b,image_Lpath_c,image_Lpath_c,image_Lpath_d,image_Lpath_d]
        Lwalking_index = (Lwalking_index + 1) % len(image_Lwalking)
        character_image = Image.open(image_Lwalking[Lwalking_index])

        my_man.appearance = character_image
    

    if not joystick.button_R.value:  # right pressed
        command['right_pressed'] = True
        command['move'] = True
        image_Rpath_a = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_1.png"
        image_Rpath_b = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_2.png"
        image_Rpath_c ="/home/JOEY/esw project/extra/Rwalking/man_Rwalking_3.png"
        image_Rpath_d = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_4.png"
        image_Rwalking = [image_Rpath_a,image_Rpath_a,image_Rpath_b,image_Rpath_b,image_Rpath_c,image_Rpath_c,image_Rpath_d,image_Rpath_d]
        Rwalking_index = (Rwalking_index + 1) % len(image_Rwalking)
        character_image = Image.open(image_Rwalking[Rwalking_index])

        my_man.appearance = character_image

    
    
    my_man.move(command)
    
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
    my_image.paste(background_image, (0, 0))
    my_draw.rectangle((text_position[0]-15, text_position[1], text_position[0] + text_width + 15, text_position[1] + text_height + 10), fill=(0, 0, 0)) #문제
    
    my_draw.rectangle((text_position_l1[0], text_position_l1[1] , text_position_l1[0] + text_width_l1 , text_position_l1[1] + text_height_l1 ), fill=(255, 255, 0))#l1
    my_draw.text(text_position_l1, str(l1), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_l2[0], text_position_l2[1] , text_position_l2[0] + text_width_l2 , text_position_l2[1] + text_height_l2 ), fill=(255, 255, 0))#l2
    my_draw.text(text_position_l2, str(l2), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_l3[0] , text_position_l3[1], text_position_l3[0] + text_width_l3 , text_position_l3[1] + text_height_l3), fill=(255, 255, 0))#l3
    my_draw.text(text_position_l3, str(l3), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_l4[0], text_position_l4[1] , text_position_l4[0] + text_width_l4 , text_position_l4[1] + text_height_l4 ), fill=(255, 255, 0))#l4
    my_draw.text(text_position_l4, str(l4), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_l5[0], text_position_l5[1] , text_position_l5[0] + text_width_l5 , text_position_l5[1] + text_height_l5 ), fill=(255, 255, 0))#l4
    my_draw.text(text_position_l5, str(l5), font=font, fill=(0, 0, 0))



    
    
    

    my_draw.text(text_position, random_quiz, font=font, fill=(255, 255, 255))
    my_image.paste(my_man.appearance, (int(my_man.position[0]), int(my_man.position[1]+35)), my_man.appearance)
    
    joystick.disp.image(my_image)
    if joystick.button_A.value == False:
        if text_position_l1[0] - 7 < my_man.position[0] < text_position_l1[0] + text_width_l1 + 7 : #l1
            if l1 == random_quiz_answer:
               break 
            else:
                rip()
                break
        if text_position_l2[0] - 7< my_man.position[0] < text_position_l2[0] + text_width_l2 + 7: #l2
            if l2 == random_quiz_answer:
               break 
            else:
                rip()
                break
        if text_position_l3[0] - 7< my_man.position[0] < text_position_l3[0] + text_width_l3 + 7 : #l3
            if l3 == random_quiz_answer:
               break 
            else:
                rip()
                break
        if text_position_l4[0] - 7< my_man.position[0] < text_position_l4[0] + text_width_l4 + 7: #l4
            if l4 == random_quiz_answer:
               break 
            else:
                rip()
                break
        if text_position_l5[0] - 7< my_man.position[0] < text_position_l5[0] + text_width_l5 + 7: #l5
            if l5 == random_quiz_answer:
               break 
            else:
                rip()
                break        
    

my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
joystick.disp.image(my_image)
bgm("/home/JOEY/esw project/extra/walking.mp3")
time.sleep(2)

bgm("/home/JOEY/esw project/extra/quizbgm.mp3")
background_image = Image.open("/home/JOEY/esw project/extra/back5.png")



l1 = "석유"
l2 = "황산"
l3 = "산소"
l4 = "소수"
l5 ="0"
font_size = 15
font = ImageFont.truetype("/home/JOEY/esw project/extra/tt.ttf", font_size)  
random_quiz = "화학에서 H2O는 무엇일까요?"
random_quiz_answer = "물"




options = [l1, l2, random_quiz_answer, l3, l4]
random.shuffle(options)  # 리스트를 섞음
l1, l2, l3 , l4 , l5 = options


text_width, text_height = my_draw.textsize(random_quiz, font=font)
text_position = ((joystick.width - text_width) // 2, 10)

text_width_l1, text_height_l1 = my_draw.textsize(l1, font=font)
text_width_l2, text_height_l2 = my_draw.textsize(l2, font=font)
text_width_l3, text_height_l3 = my_draw.textsize(l3, font=font)
text_width_l4, text_height_l4 = my_draw.textsize(l4, font=font)
text_width_l5, text_height_l5 = my_draw.textsize(l5, font=font)

text_position_l1 = ((joystick.width - text_width_l1) // 2 - 95, 155)
text_position_l2 = ((joystick.width - text_width_l2) // 2 - 45, 120) 
text_position_l3 = ((joystick.width - text_width_l3) // 2, 155) 
text_position_l4 = ((joystick.width - text_width_l4) // 2 + 45, 120) 
text_position_l5 = ((joystick.width - text_width_l5) // 2 + 90, 155) 

while True:
    command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}

    if not joystick.button_L.value:  # left pressed
        command['left_pressed'] = True
        command['move'] = True
        image_Lpath_a = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_1.png"
        image_Lpath_b = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_2.png"
        image_Lpath_c ="/home/JOEY/esw project/extra/Lwalking/man_Lwalking_3.png"
        image_Lpath_d = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_4.png"
        image_Lwalking = [image_Lpath_a,image_Lpath_a,image_Lpath_b,image_Lpath_b,image_Lpath_c,image_Lpath_c,image_Lpath_d,image_Lpath_d]
        Lwalking_index = (Lwalking_index + 1) % len(image_Lwalking)
        character_image = Image.open(image_Lwalking[Lwalking_index])

        my_man.appearance = character_image
    

    if not joystick.button_R.value:  # right pressed
        command['right_pressed'] = True
        command['move'] = True
        image_Rpath_a = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_1.png"
        image_Rpath_b = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_2.png"
        image_Rpath_c ="/home/JOEY/esw project/extra/Rwalking/man_Rwalking_3.png"
        image_Rpath_d = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_4.png"
        image_Rwalking = [image_Rpath_a,image_Rpath_a,image_Rpath_b,image_Rpath_b,image_Rpath_c,image_Rpath_c,image_Rpath_d,image_Rpath_d]
        Rwalking_index = (Rwalking_index + 1) % len(image_Rwalking)
        character_image = Image.open(image_Rwalking[Rwalking_index])

        my_man.appearance = character_image

    
    
    my_man.move(command)
    
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
    my_image.paste(background_image, (0, 0))
    my_draw.rectangle((text_position[0]-15, text_position[1], text_position[0] + text_width + 15, text_position[1] + text_height + 10), fill=(0, 0, 0)) #문제
    
    my_draw.rectangle((text_position_l1[0], text_position_l1[1] , text_position_l1[0] + text_width_l1 , text_position_l1[1] + text_height_l1 ), fill=(255, 255, 0))#l1
    my_draw.text(text_position_l1, str(l1), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_l2[0], text_position_l2[1] , text_position_l2[0] + text_width_l2 , text_position_l2[1] + text_height_l2 ), fill=(255, 255, 0))#l2
    my_draw.text(text_position_l2, str(l2), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_l3[0] , text_position_l3[1], text_position_l3[0] + text_width_l3 , text_position_l3[1] + text_height_l3), fill=(255, 255, 0))#l3
    my_draw.text(text_position_l3, str(l3), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_l4[0], text_position_l4[1] , text_position_l4[0] + text_width_l4 , text_position_l4[1] + text_height_l4 ), fill=(255, 255, 0))#l4
    my_draw.text(text_position_l4, str(l4), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_l5[0], text_position_l5[1] , text_position_l5[0] + text_width_l5 , text_position_l5[1] + text_height_l5 ), fill=(255, 255, 0))#l4
    my_draw.text(text_position_l5, str(l5), font=font, fill=(0, 0, 0))



    
    
    

    my_draw.text(text_position, random_quiz, font=font, fill=(255, 255, 255))
    my_image.paste(my_man.appearance, (int(my_man.position[0]), int(my_man.position[1]+35)), my_man.appearance)
    
    joystick.disp.image(my_image)
    if joystick.button_A.value == False:
        if text_position_l1[0] - 7 < my_man.position[0] < text_position_l1[0] + text_width_l1 + 7 : #l1
            if l1 == random_quiz_answer:
               break 
            else:
                rip()
                break
        if text_position_l2[0] - 7< my_man.position[0] < text_position_l2[0] + text_width_l2 + 7: #l2
            if l2 == random_quiz_answer:
               break 
            else:
                rip()
                break
        if text_position_l3[0] - 7< my_man.position[0] < text_position_l3[0] + text_width_l3 + 7 : #l3
            if l3 == random_quiz_answer:
               break 
            else:
                rip()
                break
        if text_position_l4[0] - 7< my_man.position[0] < text_position_l4[0] + text_width_l4 + 7: #l4
            if l4 == random_quiz_answer:
               break 
            else:
                rip()
                break
        if text_position_l5[0] - 7< my_man.position[0] < text_position_l5[0] + text_width_l5 + 7: #l5
            if l5 == random_quiz_answer:
               break 
            else:
                rip()
                break        
    

my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
joystick.disp.image(my_image)
bgm("/home/JOEY/esw project/extra/walking.mp3")
time.sleep(2)

bgm("/home/JOEY/esw project/extra/quizbgm.mp3")
background_image = Image.open("/home/JOEY/esw project/extra/back6.png")
my_image.paste(background_image, (0, 0))
joystick.disp.image(my_image)

time.sleep(0.5)
bgm("/home/JOEY/esw project/extra/scram.mp3")
text="꺄아악"             
my_draw.rectangle((0, joystick.height-70, joystick.width, joystick.height), fill=(255, 255, 255))
text_width, text_height = my_draw.textsize(text, font=font)
text_position = ((joystick.width - text_width) // 2, joystick.height - 70 + (70 - text_height) // 2)
my_draw.text(text_position, text, font=font, fill=(0, 0, 0))  
joystick.disp.image(my_image)
monologue("빨리 구해야 할 듯하다.(10초)")
time.sleep(0.5)

while True:
    if joystick.button_A.value == False:
        break
time.sleep(0.5)

l1 = "태양"
l2 = "수성"
l3 = "화성"
l4 = "금성"
l5 ="0"
font_size = 15
font = ImageFont.truetype("/home/JOEY/esw project/extra/tt.ttf", font_size)  
random_quiz = "태양계에서 가장 큰 행성은?"
random_quiz_answer = "목성"




options = [l1, l2, random_quiz_answer, l3, l4]
random.shuffle(options)  # 리스트를 섞음
l1, l2, l3 , l4 , l5 = options


text_width, text_height = my_draw.textsize(random_quiz, font=font)
text_position = ((joystick.width - text_width) // 2, 10)
end_time = 0
start_time = time.time()
end_time = start_time + 10



text_width_l1, text_height_l1 = my_draw.textsize(l1, font=font)
text_width_l2, text_height_l2 = my_draw.textsize(l2, font=font)
text_width_l3, text_height_l3 = my_draw.textsize(l3, font=font)
text_width_l4, text_height_l4 = my_draw.textsize(l4, font=font)
text_width_l5, text_height_l5 = my_draw.textsize(l5, font=font)

text_position_l1 = ((joystick.width - text_width_l1) // 2 - 95, 155)
text_position_l2 = ((joystick.width - text_width_l2) // 2 - 45, 120) 
text_position_l3 = ((joystick.width - text_width_l3) // 2, 155) 
text_position_l4 = ((joystick.width - text_width_l4) // 2 + 45, 120) 
text_position_l5 = ((joystick.width - text_width_l5) // 2 + 90, 155) 



while True:
    command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}

    if not joystick.button_L.value:  # left pressed
        command['left_pressed'] = True
        command['move'] = True
        image_Lpath_a = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_1.png"
        image_Lpath_b = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_2.png"
        image_Lpath_c ="/home/JOEY/esw project/extra/Lwalking/man_Lwalking_3.png"
        image_Lpath_d = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_4.png"
        image_Lwalking = [image_Lpath_a,image_Lpath_a,image_Lpath_b,image_Lpath_b,image_Lpath_c,image_Lpath_c,image_Lpath_d,image_Lpath_d]
        Lwalking_index = (Lwalking_index + 1) % len(image_Lwalking)
        character_image = Image.open(image_Lwalking[Lwalking_index])

        my_man.appearance = character_image

    if not joystick.button_R.value:  # right pressed
        command['right_pressed'] = True
        command['move'] = True
        image_Rpath_a = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_1.png"
        image_Rpath_b = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_2.png"
        image_Rpath_c ="/home/JOEY/esw project/extra/Rwalking/man_Rwalking_3.png"
        image_Rpath_d = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_4.png"
        image_Rwalking = [image_Rpath_a,image_Rpath_a,image_Rpath_b,image_Rpath_b,image_Rpath_c,image_Rpath_c,image_Rpath_d,image_Rpath_d]
        Rwalking_index = (Rwalking_index + 1) % len(image_Rwalking)
        character_image = Image.open(image_Rwalking[Rwalking_index])

        my_man.appearance = character_image
    my_man.move(command)
    
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
    my_image.paste(background_image, (0, 0))
    my_draw.rectangle((text_position[0]-15, text_position[1], text_position[0] + text_width + 15, text_position[1] + text_height + 10), fill=(0, 0, 0)) #문제
    
    my_draw.rectangle((text_position_l1[0], text_position_l1[1] , text_position_l1[0] + text_width_l1 , text_position_l1[1] + text_height_l1 ), fill=(255, 255, 0))#l1
    my_draw.text(text_position_l1, str(l1), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_l2[0], text_position_l2[1] , text_position_l2[0] + text_width_l2 , text_position_l2[1] + text_height_l2 ), fill=(255, 255, 0))#l2
    my_draw.text(text_position_l2, str(l2), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_l3[0] , text_position_l3[1], text_position_l3[0] + text_width_l3 , text_position_l3[1] + text_height_l3), fill=(255, 255, 0))#l3
    my_draw.text(text_position_l3, str(l3), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_l4[0], text_position_l4[1] , text_position_l4[0] + text_width_l4 , text_position_l4[1] + text_height_l4 ), fill=(255, 255, 0))#l4
    my_draw.text(text_position_l4, str(l4), font=font, fill=(0, 0, 0))

    my_draw.rectangle((text_position_l5[0], text_position_l5[1] , text_position_l5[0] + text_width_l5 , text_position_l5[1] + text_height_l5 ), fill=(255, 255, 0))#l4
    my_draw.text(text_position_l5, str(l5), font=font, fill=(0, 0, 0))


    if time.time() >= end_time:
        rip()
    
    
    

    my_draw.text(text_position, random_quiz, font=font, fill=(255, 255, 255))
    my_image.paste(my_man.appearance, (int(my_man.position[0]), int(my_man.position[1]+35)), my_man.appearance)
    
    joystick.disp.image(my_image)
    if joystick.button_A.value == False:
        if text_position_l1[0] - 5 < my_man.position[0] < text_position_l1[0] + text_width_l1 + 5 : #l1
            if l1 == random_quiz_answer:
               break 
            else:
                rip()
                break
        if text_position_l2[0] - 5< my_man.position[0] < text_position_l2[0] + text_width_l2 + 5: #l2
            if l2 == random_quiz_answer:
               break 
            else:
                rip()
                break
        if text_position_l3[0] - 5< my_man.position[0] < text_position_l3[0] + text_width_l3 + 5 : #l3
            if l3 == random_quiz_answer:
               break 
            else:
                rip()
                break
        if text_position_l4[0] - 5< my_man.position[0] < text_position_l4[0] + text_width_l4 + 5: #l4
            if l4 == random_quiz_answer:
               break 
            else:
                rip()
                break
        if text_position_l5[0] - 5< my_man.position[0] < text_position_l5[0] + text_width_l5 + 5: #l5
            if l5 == random_quiz_answer:
               break 
            else:
                rip()
                break        
    

my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
joystick.disp.image(my_image)
bgm("/home/JOEY/esw project/extra/walking.mp3")
time.sleep(2)

bgm("/home/JOEY/esw project/extra/quizbgm.mp3")

Rwalking_index = 0
Lwalking_index = 0
stay_index = 0
background_image = Image.open("/home/JOEY/esw project/extra/last_background.png")



while True:
    command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}

    if not joystick.button_L.value:  # left pressed
        command['left_pressed'] = True
        command['move'] = True
        image_Lpath_a = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_1.png"
        image_Lpath_b = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_2.png"
        image_Lpath_c ="/home/JOEY/esw project/extra/Lwalking/man_Lwalking_3.png"
        image_Lpath_d = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_4.png"
        image_Lwalking = [image_Lpath_a,image_Lpath_a,image_Lpath_b,image_Lpath_b,image_Lpath_c,image_Lpath_c,image_Lpath_d,image_Lpath_d]
        Lwalking_index = (Lwalking_index + 1) % len(image_Lwalking)
        character_image = Image.open(image_Lwalking[Lwalking_index])

        my_man.appearance = character_image
    

    if not joystick.button_R.value:  # right pressed
        command['right_pressed'] = True
        command['move'] = True
        image_Rpath_a = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_1.png"
        image_Rpath_b = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_2.png"
        image_Rpath_c ="/home/JOEY/esw project/extra/Rwalking/man_Rwalking_3.png"
        image_Rpath_d = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_4.png"
        image_Rwalking = [image_Rpath_a,image_Rpath_a,image_Rpath_b,image_Rpath_b,image_Rpath_c,image_Rpath_c,image_Rpath_d,image_Rpath_d]
        Rwalking_index = (Rwalking_index + 1) % len(image_Rwalking)
        character_image = Image.open(image_Rwalking[Rwalking_index])

        my_man.appearance = character_image

    if joystick.button_L.value and joystick.button_R.value :
        image_path1 = "/home/JOEY/esw project/extra/man_stay1_.png"
        image_path2 = "/home/JOEY/esw project/extra/man_stay2_.png"
        image_paths = [image_path1,image_path1,image_path1,image_path1,image_path1,image_path1,image_path2,image_path2,image_path2,image_path2,image_path2,image_path2]
        
        character_image = Image.open(image_paths[stay_index])

        my_man.appearance = character_image


    my_man.move(command)

    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
    my_image.paste(background_image, (0, 0),)

    my_image.paste(my_man.appearance, (int(my_man.position[0]), int(my_man.position[1])-10), my_man.appearance)

    joystick.disp.image(my_image)
    stay_index = (stay_index + 1) % len(image_paths)

    
    if joystick.button_A.value ==False:
        text="모험가:너가 공주를 납치했나?"     
        my_draw.rectangle((0, joystick.height-70, joystick.width, joystick.height), fill=(255, 255, 255))
        text_width, text_height = my_draw.textsize(text, font=font)
        text_position = ((joystick.width - text_width) // 2, joystick.height - 70 + (70 - text_height) // 2)
        my_draw.text(text_position, text, font=font, fill=(0, 0, 0))  
        joystick.disp.image(my_image)
        time.sleep(0.5) 
        break


monologue("마왕:그래 나다!")
monologue("마왕:그래서 너는 누구지?")
monologue("모험가:공주를 구할")
monologue("모험가:나는 용사다!")
monologue("마왕:그래 그래 그래")
monologue("마왕:공주를 구하고 싶다면")
monologue("마왕:내가 내는 수수께끼를 풀어라")

monologue("마왕:문제를 내주지")
monologue("아침에는 발이 4개고")
monologue("점심에는 발이 2개고")
monologue("저녁에는 발이 3개인 것은 무엇일까?")
monologue("보기를 알려주지")

text = "1.사람(A)\n2.개(B)\n3.유니콘(C)"
my_draw.rectangle((0, joystick.height-70, joystick.width, joystick.height), fill=(255, 255, 255))
text_width, text_height = my_draw.textsize(text, font=font)
text_position = ((joystick.width - text_width) // 2, joystick.height - 70 + (70 - text_height) // 2)
my_draw.text(text_position, text, font=font, fill=(0, 0, 0))  
joystick.disp.image(my_image)
time.sleep(0.5)
while True:
    if joystick.button_A.value ==False:
        text="모험가:1.사람"  
        my_draw.rectangle((0, joystick.height-70, joystick.width, joystick.height), fill=(255, 255, 255))
        text_width, text_height = my_draw.textsize(text, font=font)
        text_position = ((joystick.width - text_width) // 2, joystick.height - 70 + (70 - text_height) // 2)
        my_draw.text(text_position, text, font=font, fill=(0, 0, 0))  
        joystick.disp.image(my_image)
        time.sleep(0.5) 
        break
    if joystick.button_B.value ==False:
        text="모험가:2.개"  
        my_draw.rectangle((0, joystick.height-70, joystick.width, joystick.height), fill=(255, 255, 255))
        text_width, text_height = my_draw.textsize(text, font=font)
        text_position = ((joystick.width - text_width) // 2, joystick.height - 70 + (70 - text_height) // 2)
        my_draw.text(text_position, text, font=font, fill=(0, 0, 0))  
        joystick.disp.image(my_image)
        time.sleep(0.5)
        monologue("마왕:틀렸다")
        monologue("마왕:멍청한 놈") 
        monologue("마왕:죽어라")
        rip()
        break
    if joystick.button_C.value ==False:
        text="모험가:3.유니콘"  
        my_draw.rectangle((0, joystick.height-70, joystick.width, joystick.height), fill=(255, 255, 255))
        text_width, text_height = my_draw.textsize(text, font=font)
        text_position = ((joystick.width - text_width) // 2, joystick.height - 70 + (70 - text_height) // 2)
        my_draw.text(text_position, text, font=font, fill=(0, 0, 0))  
        joystick.disp.image(my_image)
        time.sleep(0.5)
        monologue("마왕:틀렸다")
        monologue("마왕:멍청한 놈") 
        monologue("마왕:죽어라") 
        rip()
        break


monologue("마왕:맞았군")
monologue("마왕:주르륵")
monologue("모험가:왜 울지?")

frames = []

for i in range(29):
    filename = f"/home/JOEY/esw project/extra/dead/render{i:03d}.png"
    frames.append(Image.open(filename))
filename_index = 0

while True:
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
    my_image.paste(frames[filename_index], (0, 0))
    joystick.disp.image(my_image)
    if filename_index == 28:
        break
    else:
        filename_index += 1
monologue("마왕:고맙다.")


time.sleep(2)



Rwalking_index = 0
Lwalking_index = 0
stay_index = 0
background_image = Image.open("/home/JOEY/esw project/extra/escape/ending open001.png")

key_position = (joystick.width//2, joystick.height//2)

while True:
    command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}

    if not joystick.button_L.value:  # left pressed
        command['left_pressed'] = True
        command['move'] = True
        image_Lpath_a = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_1.png"
        image_Lpath_b = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_2.png"
        image_Lpath_c ="/home/JOEY/esw project/extra/Lwalking/man_Lwalking_3.png"
        image_Lpath_d = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_4.png"
        image_Lwalking = [image_Lpath_a,image_Lpath_a,image_Lpath_b,image_Lpath_b,image_Lpath_c,image_Lpath_c,image_Lpath_d,image_Lpath_d]
        Lwalking_index = (Lwalking_index + 1) % len(image_Lwalking)
        character_image = Image.open(image_Lwalking[Lwalking_index])

        my_man.appearance = character_image
    

    if not joystick.button_R.value:  # right pressed
        command['right_pressed'] = True
        command['move'] = True
        image_Rpath_a = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_1.png"
        image_Rpath_b = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_2.png"
        image_Rpath_c ="/home/JOEY/esw project/extra/Rwalking/man_Rwalking_3.png"
        image_Rpath_d = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_4.png"
        image_Rwalking = [image_Rpath_a,image_Rpath_a,image_Rpath_b,image_Rpath_b,image_Rpath_c,image_Rpath_c,image_Rpath_d,image_Rpath_d]
        Rwalking_index = (Rwalking_index + 1) % len(image_Rwalking)
        character_image = Image.open(image_Rwalking[Rwalking_index])

        my_man.appearance = character_image

    if joystick.button_L.value and joystick.button_R.value :
        image_path1 = "/home/JOEY/esw project/extra/man_stay1_.png"
        image_path2 = "/home/JOEY/esw project/extra/man_stay2_.png"
        image_paths = [image_path1,image_path1,image_path1,image_path1,image_path1,image_path1,image_path2,image_path2,image_path2,image_path2,image_path2,image_path2]
        
        character_image = Image.open(image_paths[stay_index])

        my_man.appearance = character_image
    if joystick.button_A.value == False:
        if key_position[0] - 25 < my_man.position[0] < key_position[0] + 25: #l1
            break

    my_man.move(command)

    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
    my_image.paste(background_image, (0, 0))

    my_image.paste(my_man.appearance, (int(my_man.position[0]), int(my_man.position[1])-10), my_man.appearance)
    my_draw.rectangle((key_position[0] - 5, key_position[0] + 35, key_position[0] + 5, key_position[0] + 45), fill=(0, 0, 0))

    joystick.disp.image(my_image)
    stay_index = (stay_index + 1) % len(image_paths)


frames = []

for i in range(1, 21):
    filename = f"/home/JOEY/esw project/extra/escape/ending open{i:03d}.png"
    frames.append(Image.open(filename))
filename_index = 0
bgm("/home/JOEY/esw project/extra/iron.mp3")
while True:
    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
    my_image.paste(frames[filename_index], (0, 0))
    my_image.paste(my_man.appearance, (int(my_man.position[0]), int(my_man.position[1])-10), my_man.appearance)

    joystick.disp.image(my_image)
    if filename_index == 19:
        break
    else:
        filename_index += 1

time.sleep(1)


bgm("/home/JOEY/esw project/extra/happy ending.mp3")
Rwalking_index = 0
Lwalking_index = 0
stay_index = 0
background_image = Image.open("/home/JOEY/esw project/extra/escape/ending open021.png")

wo_position = (joystick.width//2, joystick.height//2)

while True:
    command = {'move': False, 'up_pressed': False, 'down_pressed': False, 'left_pressed': False, 'right_pressed': False}

    if not joystick.button_L.value:  # left pressed
        command['left_pressed'] = True
        command['move'] = True
        image_Lpath_a = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_1.png"
        image_Lpath_b = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_2.png"
        image_Lpath_c ="/home/JOEY/esw project/extra/Lwalking/man_Lwalking_3.png"
        image_Lpath_d = "/home/JOEY/esw project/extra/Lwalking/man_Lwalking_4.png"
        image_Lwalking = [image_Lpath_a,image_Lpath_a,image_Lpath_b,image_Lpath_b,image_Lpath_c,image_Lpath_c,image_Lpath_d,image_Lpath_d]
        Lwalking_index = (Lwalking_index + 1) % len(image_Lwalking)
        character_image = Image.open(image_Lwalking[Lwalking_index])

        my_man.appearance = character_image
    

    if not joystick.button_R.value:  # right pressed
        command['right_pressed'] = True
        command['move'] = True
        image_Rpath_a = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_1.png"
        image_Rpath_b = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_2.png"
        image_Rpath_c ="/home/JOEY/esw project/extra/Rwalking/man_Rwalking_3.png"
        image_Rpath_d = "/home/JOEY/esw project/extra/Rwalking/man_Rwalking_4.png"
        image_Rwalking = [image_Rpath_a,image_Rpath_a,image_Rpath_b,image_Rpath_b,image_Rpath_c,image_Rpath_c,image_Rpath_d,image_Rpath_d]
        Rwalking_index = (Rwalking_index + 1) % len(image_Rwalking)
        character_image = Image.open(image_Rwalking[Rwalking_index])

        my_man.appearance = character_image

    if joystick.button_L.value and joystick.button_R.value :
        image_path1 = "/home/JOEY/esw project/extra/man_stay1_.png"
        image_path2 = "/home/JOEY/esw project/extra/man_stay2_.png"
        image_paths = [image_path1,image_path1,image_path1,image_path1,image_path1,image_path1,image_path2,image_path2,image_path2,image_path2,image_path2,image_path2]
        
        character_image = Image.open(image_paths[stay_index])

        my_man.appearance = character_image
    if joystick.button_A.value == False:
        if wo_position[0] - 95 < my_man.position[0] < wo_position[0] - 70 : #l1
            text="모험가:공주 괜찮소?"
            my_draw.rectangle((0, joystick.height-70, joystick.width, joystick.height), fill=(255, 255, 255))
            text_width, text_height = my_draw.textsize(text, font=font)
            text_position = ((joystick.width - text_width) // 2, joystick.height - 70 + (70 - text_height) // 2)
            my_draw.text(text_position, text, font=font, fill=(0, 0, 0))  
            joystick.disp.image(my_image)
            break

    my_man.move(command)

    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
    my_image.paste(background_image, (0, 0))

    my_image.paste(my_man.appearance, (int(my_man.position[0]), int(my_man.position[1])-10), my_man.appearance)

    joystick.disp.image(my_image)
    stay_index = (stay_index + 1) % len(image_paths)


monologue("모험가:왜 내게 고맙다는 말을?")
monologue("공주:네?")
monologue("모험가:아무것도 아니오.")
monologue("공주:절 구해주신건가요?")
monologue("모험가:그렇소")
monologue("공주:감사합니다")
monologue("모험가:...")
monologue("모험가:일단 탈출합시다.")
monologue("공주:네")




background_image_1 = Image.open("/home/JOEY/esw project/extra/happyend/happy ending1.png")
background_image_2 = Image.open("/home/JOEY/esw project/extra/happyend/happy ending2.png")
background_images = [background_image_1,background_image_1,background_image_1,background_image_1,background_image_1,background_image_1 ,background_image_2,background_image_2,background_image_2,background_image_2,background_image_2,background_image_2]

bgm("/home/JOEY/esw project/extra/happy ending.mp3")


while True:

    my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
    my_image.paste(background_images[background_index], (0, 0))


    joystick.disp.image(my_image)
    background_index = (background_index + 1) % len(background_images)
    if joystick.button_A.value == False:
        pygame.mixer.music.stop()
        my_draw.rectangle((0, 0, joystick.width, joystick.height), fill="#000000")  # Assuming black background
        font_size = 20
        font = ImageFont.truetype("/home/JOEY/esw project/extra/tt.ttf", font_size)  
        text = "THE END\nthanks for playing"  
        text_width, text_height = my_draw.textsize(text, font=font)
        text_position = ((joystick.width - text_width) // 2, (joystick.height - text_height) // 2)
        my_draw.text(text_position, text, font=font, fill=(255, 255, 255))
        joystick.disp.image(my_image)

        break


    


