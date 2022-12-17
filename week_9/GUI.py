import math
import pygame
import copy
import csv
from csv import reader
from tkinter import *
from tkinter import filedialog
import os
import sys
import json
import time
from types import DynamicClassAttribute



################Set how you want your state angle defined (Set only one as true)###########
#Positive unbounded degree: Angles larger than 0 that can go higher than 365 degrees, useful if only moving counterclockwise.
positive_unbounded_degree = True
#Positive Bounded Radians: Radians 0-2pi, never negative and always between theses numbers
positive_bounded_radians = False
#Degree Bounded


###############Set which polcy you want to use ##############################
#quick algo soley checks unbounded positve angle try and predict future movements
quick_algo = False
#IRL algo, not yet defined
IRL_algo = False
#multiple character algo, set number of char want to recognize
mult_char_algo = False
num_policy = 0
#Imitation policy
imitation_algo = True


#######Set how many chars/policies going to check######
num_char = 3

#function to reset screen
def reset_screen():
    global start_surgery 
    global surgery_end 
    global surgery_restart_ready
    global last_pos_doctor
    global last_pos_robot
    global need_to_find_policy 
    global state_doc 
    global state_robot 
    global last_angle_rob
    global over_365_rob
    global num_over_rob
    global last_angle_doc
    global over_365_doc
    global num_over_doc
    global training
    global first_angle
    global avg_imit_angle_1
    global avg_imit_angle_2
    global imimtation_policy_1 
    global imimtation_policy_2 
    
   
    # Fill the background with white
    screen.fill((255, 255, 255))
    # draw surgery box
    pygame.draw.rect(screen, (0, 0, 0), (150, 0, 700 - 150, 500), width=5)
    # draw mimic box
    pygame.draw.rect(screen, (0, 0, 0), (700, 0, 700 - 150, 500), width=7)
    #draw robot state
    pygame.draw.rect(screen, color_light, (0, 75, 150, 115)) #x start, y start, width height
    #draw doc state
    pygame.draw.rect(screen, color_light, (0, 200, 150, 90)) #x start, y start, width height
    #train button
    pygame.draw.rect(screen, (0,100,0), (0, 290, 150, 60))
    pygame.draw.rect(screen, (0,0,0), (0, 290, 150, 60), width =3)
    #draw policy button
    pygame.draw.rect(screen, color_light, (0, 0, 150, 75)) #x start, y start, width height
    #draw joystick box
    pygame.draw.rect(screen, (0, 0, 255), (0, 350, 150, 150), width=1)
    # draw joystick circle
    pygame.draw.circle(screen, (255, 0, 0), (75, 500 - 75), 70)
    #draw text states
    start_surgery = False
    surgery_end = False
    surgery_restart_ready = False
    last_pos_doctor = None
    last_pos_robot = None
    need_to_find_policy = True
    training = False
    first_angle = []
    avg_imit_angle_1 = None
    avg_imit_angle_2 = None
    imimtation_policy_1 = []
    imimtation_policy_2 = []
    #State
    state_doc = [0, 0] #[length, angle] 
    state_robot = [0, 0]

    #accurate angle robot and doc
    last_angle_rob = 0
    over_365_rob = 0
    num_over_rob = 0
    last_angle_doc = 0
    over_365_doc = 0
    num_over_doc = 0

    pygame.display.flip()

def open_file():
    my_file = filedialog.askopenfilename()
    return my_file

def import_policy():
    global policy_available
    try:
        file_to_draw = open_file()
        
        with open(file_to_draw, "r") as read_obj:
            csv_reader = reader(read_obj)
            policy = list(csv_reader)      
        policy.pop(0)
        int_data = []
        #create int data set with proper int or float type
        for set in policy:
            point = []
            point.append(int(set[5]))   #dx
            point.append(int(set[6]))  #dy
            point.append(float(set[8]))  #distance_traveled
            point.append(float(set[10]))  #accurate Angle
            int_data.append(point)
        running = True
        policy_available = True
        return int_data, running
    except:
        print("Warning! policy did not load correctly, please restart and load policy")
        running = True
        null_policy = []
        return(null_policy, running)

def import_imitation_policy():
    global policy_available
    global avg_imit_angle_1
    global avg_imit_angle_2
    try:
        #file_to_draw = open_file()
        
        file_to_draw = "C:/Final_proj/branch_week_6/Tele_operation-Computatinon/Mouse_Operation_Mimick/a/imitation_policy.csv"
        print(file_to_draw)
        with open(file_to_draw, "r") as read_obj:
            csv_reader = reader(read_obj)
            policy = list(csv_reader)      
        policy.pop(0)
        #initialize what the firts angles are
        if type(avg_imit_angle_1) == float:
            avg_imit_angle_2 = float(policy[0][6])
        else:
            avg_imit_angle_1 = float(policy[0][6])
        int_data = []
        #create int data set with proper int or float type
        for set in policy:
            point = []
            point.append(int(set[0]))  #state in degrees
            point.append(float(set[4]))  #dx 
            point.append(float(set[5]))  #dy
            int_data.append(point)
        running = True
        policy_available = True
        return int_data, running
    except:
        print("Warning! policy did not load correctly, please restart and load policy")
        running = True
        null_policy = []
        return(null_policy, running)

def mult_char_policy():
    global policy_available
    global num_policy
    
    try:
        file_to_draw = open_file()
        
        with open(file_to_draw, "r") as read_obj:
            csv_reader = reader(read_obj)
            policy = list(csv_reader)      
        policy.pop(0)
        int_data_1 = []
        #create int data set with proper int or float type
        for set in policy:
            point = []
            point.append(int(set[5]))   #dx
            point.append(int(set[6]))  #dy
            point.append(float(set[8]))  #distance_traveled
            point.append(float(set[10]))  #accurate Angle
            int_data_1.append(point)
        running = True
        policy_available = True

        file_to_draw = open_file()
        
        with open(file_to_draw, "r") as read_obj:
            csv_reader = reader(read_obj)
            policy = list(csv_reader)      
        policy.pop(0)
        int_data_2 = []
        #create int data set with proper int or float type
        for set in policy:
            point = []
            point.append(int(set[5]))   #dx
            point.append(int(set[6]))  #dy
            point.append(float(set[8]))  #distance_traveled
            point.append(float(set[10]))  #accurate Angle
            int_data_2.append(point)
        running = True
        policy_available = True
        return int_data_1, int_data_2, running
    except:
        print("Warning! policy did not load correctly, please restart and load policy")
        running = True
        null_policy = []
        return(null_policy,null_policy, running)

def len_change(old_pos, new_pos):
    mag = math.sqrt((old_pos[0] - new_pos[0]) ** 2 + (old_pos[1] - new_pos[1]) ** 2)
    return(mag)

#using if want unbounded angle in degrees
def angle_calc(old_pos, new_pos):
    dy = new_pos[1] - old_pos[1]
    dx = new_pos[0] - old_pos[0]
    angle_rad = math.atan2((-dy), dx)
    if angle_rad < 0:
        angle_rad += 2*3.14159
    angle_deg = math.degrees(angle_rad)
    return(angle_deg)

#using if want unbounded angle in degrees
def angle_calc_rob(old_pos, new_pos): 
    global last_angle_rob
    global over_365_rob
    global num_over_rob
    dy = new_pos[1] - old_pos[1]
    dx = new_pos[0] - old_pos[0]
    if abs(dx) + abs(dy) < 5:
        return(last_angle_rob + 365*num_over_rob)
    angle_rad = math.atan2((-dy), dx)
    if angle_rad < 0:
        angle_rad += 2*3.14159
    angle_deg = math.degrees(angle_rad)
    if last_angle_rob == None:  
        last_angle_rob = angle_deg
        return(angle_deg)
        # if angles passes 360 lin from bottom to top, add 365 to angle
    elif (last_angle_rob - angle_deg) > 200:
        num_over_rob += 1
        last_angle_rob = angle_deg
        angle_deg += 365*num_over_rob
        over_365_rob = True
        return(angle_deg)
    elif over_365_rob:
        last_angle_rob = angle_deg
        angle_deg += 365*num_over_rob
        return(angle_deg)
    last_angle_rob = angle_deg
    return(angle_deg)

#using if want unbounded angle in degrees
def angle_calc_doc(old_pos, new_pos):

    global last_angle_doc
    global over_365_doc
    global num_over_doc
    dy = new_pos[1] - old_pos[1]
    dx = new_pos[0] - old_pos[0]
    if abs(dx) + abs(dy) < 5:
        return(last_angle_doc + 365*num_over_doc)
    angle_rad = math.atan2((-dy), dx)
    if angle_rad < 0:
        angle_rad += 2*3.14159
    angle_deg = math.degrees(angle_rad)
    if last_angle_doc == None:  
        last_angle_doc = angle_deg
        return(angle_deg)
        # if angles passes 360 lin from bottom to top, add 365 to angle
    elif (last_angle_doc - angle_deg) > 200:
        num_over_doc += 1
        last_angle_doc = angle_deg
        angle_deg += 365*num_over_doc
        over_365_doc = True
        return(angle_deg)
    elif over_365_doc:
        last_angle_doc = angle_deg
        angle_deg += 365*num_over_doc
        return(angle_deg)
    last_angle_doc = angle_deg
    return(angle_deg)

 #calculate in radians   

#calculate in radians
def radian_calc(old_pos, new_pos):

    dy = new_pos[1] - old_pos[1]
    dx = new_pos[0] - old_pos[0]
    angle_rad = math.atan2((-dy), dx)
    return(angle_rad)

#choose which angle calculations to use
def calc_choose(old_pos, new_pos, is_robot):
    if positive_unbounded_degree:
        if is_robot:
            return(angle_calc_rob(old_pos,new_pos))
        else:
            return(angle_calc_doc(old_pos,new_pos))
    if positive_bounded_radians:
        return(radian_calc(old_pos,new_pos))


###INITIALIZATIONS of variables and game
pygame.init()
pygame.display.set_caption('Surgery Boiiii')
#Declare to initialize positions/equations
scalpelPos = [200, 200]
nextScalpelPos = [200, 200]
mimicPos = [200+550, 200]
vectorPos = [75, 500-75]
vectorBase = [75, 500-75]
mcoords = [0,0]
state_doc = [0, 0] #[length, angle] 
state_robot = [0, 0]
#Flags and indictators
start_surgery = False
surgery_end = False
surgery_restart_ready = False
last_pos_doctor = None
last_pos_robot = None
training = False
policy_available = False
first_angle = []
avg_imit_angle_1 = None
avg_imit_angle_2 = None
imimtation_policy_1 = []
imimtation_policy_2 = []
#policy, running = import_policy()
running = True
need_to_find_policy = True
last_angle_rob = 0
over_365_rob = 0
num_over_rob = 0
last_angle_doc = 0
over_365_doc = 0
num_over_doc = 0
last_imit_angle = 0
#Define tuple for mouse clicks, part or pygame library
LEFT = 1
RIGHT = 3

####GUI GRAPHICAL TEXT INFO Init
#color define
color_light = (100,100,100)
color_dark = (0,0,0)
# defining a font
smallfont = pygame.font.SysFont('Corbel', 35)
smallerfont = pygame.font.SysFont('Corbel', 25)
# add policy button and train button text
text = smallerfont.render('Add Policy' , True , (255,255,255))
train_text = smallfont.render('Train' , True , (255,255,255))
#Doc and robot state text
doc_text = smallerfont.render('DOC State:' , True , (255,255,255))
doc_state_L_text = smallerfont.render("Length " + str(state_doc[0]), True , (255,255,255))
doc_state_A_text = smallerfont.render("Angle " + str(state_doc[1]), True , (255,255,255))
robot_text = smallerfont.render('Robot State:' , True , (255,255,255))
robot_state_L_text = smallerfont.render("Length " + str(state_robot[0]), True , (255,255,255))
robot_state_A_text = smallerfont.render("Angle " + str(state_robot[1]), True , (255,255,255))
# Set up the drawing window
screen = pygame.display.set_mode([700+550, 500])
reset_screen()
clock = pygame.time.Clock()
time_since_last_run = 0


###### MAIN LOOP FOR DOC/ROBOT OPERATION, EVERY event is a detection of something
while running:  
    dt = clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_screen()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # when r is pressed, reset screen and re-align mimic position
                pygame.draw.rect(screen, color_dark, (0, 0, 150, 75)) #x star, y start, width height
                start_surgery = False
                screen.blit(text , (20,300))
                robot_state_L_text = smallerfont.render("Length " + str(0), True , (255,255,255))
                robot_state_A_text = smallerfont.render("Angle " + str(0), True , (255,255,255))
                doc_state_L_text = smallerfont.render("Length " + str(0), True , (255,255,255))
                doc_state_A_text = smallerfont.render("Angle " + str(0), True , (255,255,255))
                screen.blit(robot_state_L_text, (20,120))
                screen.blit(robot_state_A_text, (20,150))
                screen.blit(doc_state_L_text, (20,230))
                screen.blit(doc_state_A_text, (20,260))
                reset_screen()
                reset_screen()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
            #Add Policy button if clicked
            if (mcoords[0] <= 150) and (mcoords[1] <=75) and (quick_algo == True):   
                policy, running = import_policy()
                pygame.draw.rect(screen, color_dark, (0, 0, 150, 75)) #x star, y start, width height
                start_surgery = False
                screen.blit(text , (20,300))
                robot_state_L_text = smallerfont.render("Length " + str(0), True , (255,255,255))
                robot_state_A_text = smallerfont.render("Angle " + str(0), True , (255,255,255))
                doc_state_L_text = smallerfont.render("Length " + str(0), True , (255,255,255))
                doc_state_A_text = smallerfont.render("Angle " + str(0), True , (255,255,255))
                screen.blit(robot_state_L_text, (20,120))
                screen.blit(robot_state_A_text, (20,150))
                screen.blit(doc_state_L_text, (20,230))
                screen.blit(doc_state_A_text, (20,260))
                reset_screen()
            elif (mcoords[0] <= 150) and (mcoords[1] <=75) and (mult_char_algo == True):
                policy_1, policy_2, running = mult_char_policy()
                pygame.draw.rect(screen, color_dark, (0, 0, 150, 75)) #x star, y start, width height
                start_surgery = False
                screen.blit(text , (20,300))
                robot_state_L_text = smallerfont.render("Length " + str(0), True , (255,255,255))
                robot_state_A_text = smallerfont.render("Angle " + str(0), True , (255,255,255))
                doc_state_L_text = smallerfont.render("Length " + str(0), True , (255,255,255))
                doc_state_A_text = smallerfont.render("Angle " + str(0), True , (255,255,255))
                screen.blit(robot_state_L_text, (20,120))
                screen.blit(robot_state_A_text, (20,150))
                screen.blit(doc_state_L_text, (20,230))
                screen.blit(doc_state_A_text, (20,260))
                reset_screen()
            elif (mcoords[0] <= 150) and (mcoords[1] <=75) and (imitation_algo == True):
                imimtation_policy_1, running = import_imitation_policy()
                imimtation_policy_2, running = import_imitation_policy()
                pygame.draw.rect(screen, color_dark, (0, 0, 150, 75)) #x star, y start, width height
                start_surgery = False
                screen.blit(text , (20,300))
                robot_state_L_text = smallerfont.render("Length " + str(0), True , (255,255,255))
                robot_state_A_text = smallerfont.render("Angle " + str(0), True , (255,255,255))
                doc_state_L_text = smallerfont.render("Length " + str(0), True , (255,255,255))
                doc_state_A_text = smallerfont.render("Angle " + str(0), True , (255,255,255))
                screen.blit(robot_state_L_text, (20,120))
                screen.blit(robot_state_A_text, (20,150))
                screen.blit(doc_state_L_text, (20,230))
                screen.blit(doc_state_A_text, (20,260))
            #Train button clicked
            elif (mcoords[0] <= 150) and (290 <=mcoords[1] <=350):
                pygame.draw.rect(screen, (0, 0, 0), (0, 290, 150, 60)) #x star, y start, width height
                screen.blit(train_text , (20,305))
                training = True
                running = False          
            #starting surgery
            else:
                pygame.draw.rect(screen, (0, 200, 0), (700, 0, 700 - 150, 500), width =7)
                mimic_surgery = True
                start_surgery = True
            print("detect left click")
        if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:   
            mimic_surgery = False
            if start_surgery == True:
                pygame.draw.rect(screen, (255,0 , 0), (700, 0, 700 - 150, 500), width =5)
            print("detect let up left click")
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
            if surgery_end == True:
                surgery_end = False
                start_surgery = False
                reset_screen()
            else:
                surgery_end = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == RIGHT:
            surgery_restart_ready = True
        
        #########MAIN LOOP, anytime mouse movement detected, update states
        if event.type == pygame.MOUSEMOTION:
            mcoords = pygame.mouse.get_pos()    
            #Check if in Bounds of drawing GUI
            if (150 < mcoords[0] < 700 and 0 < mcoords[1] < 500):
                
                #####Doctor STATE/Draw Position Arguments
                if last_pos_doctor == None:
                    last_pos_doctor = mcoords
                if (start_surgery == True) and (mimic_surgery == True) and (surgery_end == False):
                    robot_move_relative = [mcoords[0]- last_pos_doctor[0] ,  mcoords[1]- last_pos_doctor[1]]
                    pygame.draw.circle(screen, (0, 0, 0), mcoords, 2)
                    pygame.draw.line(screen, (0,0,0), last_pos_doctor, mcoords, 4)
                    if positive_unbounded_degree == False:    
                        state_doc[0] += len_change(last_pos_doctor,mcoords) 
                        state_doc[1] = angle_calc(last_pos_doctor,mcoords)
                    else:
                        state_doc[0] += len_change(last_pos_doctor,mcoords) 
                        state_doc[1] = angle_calc_doc(last_pos_doctor,mcoords)
                elif (start_surgery == True) and (mimic_surgery == False) and (surgery_end == False):
                    pygame.draw.circle(screen, (255, 0, 255), mcoords, 2) #option to change color upon dropout
                    pygame.draw.line(screen, (255,0,255), last_pos_doctor, mcoords, 4)       
                    if positive_unbounded_degree == False:    
                        state_doc[0] += len_change(last_pos_doctor,mcoords) #
                        state_doc[1] = angle_calc(last_pos_doctor,mcoords)
                    else:
                        state_doc[0] += len_change(last_pos_doctor,mcoords) 
                        state_doc[1] = angle_calc_doc(last_pos_doctor,mcoords)
                last_pos_doctor = copy.deepcopy(mcoords)

                #####Robot STATE/Draw Position Arguments
                mimicPos[0] = mcoords[0] + 700 - 150
                mimicPos[1] = mcoords[1]
                if last_pos_robot == None:
                   last_pos_robot = mimicPos
                #If there is a wifi connection, follow the doctor
                if (start_surgery == True) and (mimic_surgery == True) and (surgery_end == False):
                    next_pos_rob = [last_pos_robot[0]+ robot_move_relative[0], last_pos_robot[1]+ robot_move_relative[1]]
                    if (700 < next_pos_rob[0] < 700 +550 and 0 <next_pos_rob[1] < 500):
                        pygame.draw.circle(screen, (0, 0, 0), next_pos_rob, 2)
                        pygame.draw.line(screen, (0, 0, 0), last_pos_robot, next_pos_rob, 4)
                    state_robot[0] += len_change(last_pos_robot, next_pos_rob) 
                    if positive_unbounded_degree == False:    
                        state_robot[1] = angle_calc(last_pos_robot, next_pos_rob)
                        first_angle.append(state_robot[1])
                    else:
                        state_robot[1] = angle_calc_rob(last_pos_robot, next_pos_rob)
                        first_angle.append(state_robot[1])
                    last_pos_robot = copy.deepcopy(next_pos_rob)
                ###########THE BELOW WILL CHANGE WITH HOW WE IMPLEMENT A POLICY for the robot!###############
                #######If there is no wifi connection to a doctor, implement a policy 
                ############################################################################################
                elif (start_surgery == True) and (mimic_surgery == False) and (surgery_end == False):
                    if policy_available == False:
                        next_pos_robot =last_pos_robot
                        print("no policy to execute")
                        break
                    #######Quick non-compuationally expensive algorithem
                    if quick_algo == True:
                        if need_to_find_policy == True:
                            minimum_diff = 100 #assumes there will be a state within 100 degrees
                            policy_index = -1
                            for sets in policy:
                                policy_index += 1
                                if abs(sets[3] - state_robot[1]) < minimum_diff:
                                    mininum_diff = abs(sets[3] - state_robot[1])
                                    policy_index_start = policy_index - 20
                            need_to_find_policy = False
                            #print("closest state angle was " + str(mininum_diff + state_robot[1]))
                            move_index = 0  
                        try:
                            x_rob_policy = int(last_pos_robot[0]) + int(policy[policy_index_start + move_index][0])
                            y_rob_policy = int(last_pos_robot[1]) + int(policy[policy_index_start + move_index][1])
                        except:
                            break
                        next_pos_policy_robot = [x_rob_policy, y_rob_policy] 
                        pygame.draw.circle(screen, (255, 0, 255), next_pos_policy_robot, 2)
                        pygame.draw.line(screen, (255,0,255), last_pos_robot, next_pos_policy_robot, 4)
                        state_robot[0] += len_change(last_pos_robot, next_pos_policy_robot)
                        state_robot[1] = angle_calc_rob(last_pos_robot, next_pos_policy_robot)
                        last_pos_robot = copy.deepcopy(next_pos_policy_robot)
                        move_index += 1
                        # if (700 < next_pos_robot[0] < 700 +550 and 0 <next_pos_robot[1] < 500):
                        #     if (state_robot[0]) < state_doc[0]:
                        #         move_index += 1
                        #         pygame.draw.circle(screen, (90, 100, 90), next_pos_robot, 2)
                        #         pygame.draw.line(screen, (90,100,90), last_pos_robot, next_pos_robot, 4)
                        #         state_robot[0] += len_change(last_pos_robot, next_pos_robot) #length traversed
                        #         if positive_unbounded_degree == False:    
                        #             state_robot[1] = angle_calc(last_pos_robot, next_pos_rob)
                        #         else:
                        #             state_robot[1] = angle_calc_rob(last_pos_robot, next_pos_rob)
                        #         last_pos_robot = copy.deepcopy(next_pos_rob)
                    if IRL_algo == TRUE:
                        ####Where we implement IRL_ALGO
                        next_pos_robot =last_pos_robot
                    if mult_char_algo == True:
                        if need_to_find_policy == True:
                            policy_1_diff = policy_1[0][3] - first_angle[3]
                            policy_2_diff = policy_2[0][3] - first_angle[3]
                            # print(first_angle[3])
                            # print(policy_1[0][3])
                            # print(policy_2[0][3])
                            # print(policy_1_diff)
                            # print(policy_2_diff)
                            if abs(policy_1_diff) < abs(policy_2_diff):
                                policy =policy_1
                            else:
                                policy = policy_2
                            minimum_diff = 100 #assumes there will be a state within 100 degrees
                            policy_index = -1
                            for sets in policy:
                                policy_index += 1
                                if abs(sets[3] - state_robot[1]) < minimum_diff:
                                    mininum_diff = abs(sets[3] - state_robot[1])
                                    policy_index_start = policy_index - 20
                            need_to_find_policy = False
                            #print("closest state angle was " + str(mininum_diff + state_robot[1]))
                            move_index = 0  
                        try:
                            x_rob_policy = int(last_pos_robot[0]) + int(policy[policy_index_start + move_index][0])
                            y_rob_policy = int(last_pos_robot[1]) + int(policy[policy_index_start + move_index][1])
                        except:
                            break
                        next_pos_policy_robot = [x_rob_policy, y_rob_policy] 
                        pygame.draw.circle(screen, (255, 0, 255), next_pos_policy_robot, 2)
                        pygame.draw.line(screen, (255,0,255), last_pos_robot, next_pos_policy_robot, 4)
                        state_robot[0] += len_change(last_pos_robot, next_pos_policy_robot)
                        state_robot[1] = angle_calc_rob(last_pos_robot, next_pos_policy_robot)
                        last_pos_robot = copy.deepcopy(next_pos_policy_robot)
                        move_index += 1
                    if imitation_algo:
                        if need_to_find_policy == True:
                            avg_imit_angle_1 = 130
                            avg_imit_angle_2 = 130
                            policy_1_diff = avg_imit_angle_1 - first_angle[2]
                            policy_2_diff = avg_imit_angle_2 - first_angle[2]
                            if abs(policy_1_diff) < abs(policy_2_diff):
                                policy = imimtation_policy_1
                            else:
                                policy = imimtation_policy_2
                            policy, running = import_imitation_policy()
                            print("policy imitation " + str(policy[0]) )
                            need_to_find_policy = False
                            imit_state_last = 0
                            num_state_repeat = 0
                            imit_x_carry = 0
                            imit_y_carry = 0
                            index_last = 0
                            
                            new_imit_angle =1
                        minimum_diff = 100 #assumes there will be a state within 100 degrees
                        print("angle is " + str(state_robot[1]))
                        print("last imit angle is " + str(last_imit_angle))
                        for index, sets in enumerate(policy):
                            diff_state = abs(sets[0] - state_robot[1])
                            if diff_state < minimum_diff:
                                #print(str(diff_state) + ", minimum diff: "  + str(minimum_diff))
                                minimum_diff = diff_state
                                #print("new minimum_diff is " + str(minimum_diff))
                                imit_policy = index        
                        try:
                            print("closest state angle policy found is " + str(policy[imit_policy][0])) 
                            imit_state_now = int(policy[imit_policy][0])
                            if imit_state_now == int(imit_state_last):
                                num_state_repeat += 1
                            else:
                                num_state_repeat = 0
                            if  imit_policy < index_last:  
                                print("this angle is " + str(state_robot[1]))
                                imit_policy = index_last + 4
                                print("backpeddled, jump forward")
                                num_state_repeat = 0
                            ## If it has been in the same state for more than 4 policy prescriptions, continue to next index state
                            if num_state_repeat > 5:
                                imit_policy += 10
                            try:
                                imit_state_now = int(policy[imit_policy][0])
                                print("imit state after " + str(imit_state_now))
                                imit_state_last = imit_state_now
                                print("policy is " + str(policy[imit_policy]))
                            except:
                                break
                            
                            try:
                                imit_x_move = round(imit_x_carry + policy[imit_policy][1])
                                imit_y_move = round(imit_y_carry + policy[imit_policy][2])
                                imit_x_carry = (policy[imit_policy][1] + imit_x_carry) - imit_x_move
                                imit_y_carry = (policy[imit_policy][2] + imit_y_carry) - imit_y_move
                                x_rob_policy = int(last_pos_robot[0] + imit_x_move)
                                y_rob_policy = int(last_pos_robot[1] + imit_y_move) 
                            except:
                                break
                            last_imit_angle = copy.deepcopy(state_robot[1])
                            next_pos_policy_robot = [x_rob_policy, y_rob_policy] 
                            print(next_pos_policy_robot)
                            pygame.draw.circle(screen, (255, 0, 255), next_pos_policy_robot, 2)
                            pygame.draw.line(screen, (255,0,255), last_pos_robot, next_pos_policy_robot, 4)
                            state_robot[0] += len_change(last_pos_robot, next_pos_policy_robot)
                            state_robot[1] = angle_calc_rob(last_pos_robot, next_pos_policy_robot)
                            last_pos_robot = copy.deepcopy(next_pos_policy_robot)
                            index_last = imit_policy
                            print("index last = " + str(index_last))
                        except:
                            need_to_find_policy = True
                            continue
        #####CHARACTER/GUI VISUAL UPDATES after every mouse move/state update           
        ##Add Policy BUTTON
        if (mcoords[0] <= 150) and ( mcoords[1] <=75):   
           pygame.draw.rect(screen, color_dark, (0, 0, 150, 75)) #x star, y start, width height
        else:
            pygame.draw.rect(screen, color_light, (0, 0, 150, 75)) #x star, y start, width height
        screen.blit(text , (20,20))
        ##TRAIN BUTTON
        if (mcoords[0] <= 150) and (290 <=mcoords[1] <=350):
            pygame.draw.rect(screen, (0, 100, 0), (0, 290, 150, 60)) #x star, y start, width height
        else: 
            pygame.draw.rect(screen, (0, 200, 0), (0, 290, 150, 60)) #x star, y start, width height 
        screen.blit(train_text , (20,305))  
        ##STATE OF DOC
        pygame.draw.rect(screen, color_light, (0, 190, 150, 100)) #x start, y start, width height
        pygame.draw.rect(screen, (0,0,0), (0, 190, 150, 100), width = 1) #x start, y start, width height
        screen.blit(doc_text, (20,205))
        doc_state_L_text = smallerfont.render("Length " + str(round(state_doc[0])), True , (255,255,255))
        if (state_doc[1] != 0) and (state_doc[1] !=  180) and (state_doc[1] != 90) and (state_doc[1] != 270):
            doc_state_A_text = smallerfont.render("Angle " + str(round(state_doc[1])), True , (255,255,255))
        screen.blit(doc_state_L_text, (20,230))
        screen.blit(doc_state_A_text, (20,260))
        ##STATE of ROBOT
        pygame.draw.rect(screen, color_light, (0, 75, 150, 115)) #x start, y start, width height
        pygame.draw.rect(screen, (0,0,0), (0, 75, 150, 115), width = 1) #x start, y start, width height
        screen.blit(robot_text, (20,90))
        robot_state_L_text = smallerfont.render("Length " + str(round(state_robot[0])), True , (255,255,255))
        if (state_robot[1] != 0) and (state_robot[1] !=  180) and (state_robot[1] != 90) and (state_robot[1] != 270):
            robot_state_A_text = smallerfont.render("Angle " + str(round(state_robot[1])), True , (255,255,255))
        screen.blit(robot_state_L_text, (20,120))
        screen.blit(robot_state_A_text, (20,150))
        ##Joystick circle to overwite last vector
        pygame.draw.circle(screen, (255, 0, 0), (75, 500-75), 70)

    ##FORCE JOYSTICK CALC
    vectorLength = math.sqrt((scalpelPos[0] - mcoords[0]) ** 2 + (scalpelPos[1] - mcoords[1]) ** 2)
    if vectorLength == 0:
        vectorNorm = [0, 0]
    else:
        vectorNorm = [(mcoords[0] - scalpelPos[0]) / vectorLength, (scalpelPos[1] - mcoords[1]) / vectorLength]
    if vectorLength < 70:
        vectorPos[0] = round(vectorBase[0] + vectorNorm[0] * vectorLength)
        vectorPos[1] = round(vectorBase[1] - vectorNorm[1] * vectorLength)
        pygame.draw.line(screen, (0, 0, 0), vectorBase, vectorPos, 4)
    else:
        vectorPos[0] = round(vectorBase[0] + vectorNorm[0] * 65)  #look at next comment
        vectorPos[1] = round(vectorBase[1] - vectorNorm[1] * 65)  #67 is a wierd hack to prevent drawing outside circle
        pygame.draw.line(screen, (0, 0, 0), vectorBase, vectorPos, 4)
    if vectorLength > 2: #2 pixel per 1/60th of a second (max for width 3 circle
        scalpelSpeed = 2
    else:
        scalpelSpeed = vectorLength
    scalpelPos[0] = scalpelPos[0] + vectorNorm[0] * scalpelSpeed
    scalpelPos[1] = scalpelPos[1] - vectorNorm[1] * scalpelSpeed
    if scalpelPos[0] < 150:
        scalpelPos[0] = 150
    if scalpelPos[0] > 700:
        scalpelPos[0] = 700
    if scalpelPos[1] < 0:
        scalpelPos[1] = 0
    if scalpelPos[1] > 500:
        scalpelPos[1] = 500
    
    #update display
    pygame.display.flip()
#######END MAIN LOOP






###WARNING: Leave a clear seperation from above, everything below is for training only, basically another script which geneartes csvs and jsons for creating policies!

while training:
    drawing = [] #where data will go
    list_of_actions = []# what is getting stored for json
    json_dict =[] #list of list of actions for each charter
    app_open = False #if paint app open or closed
    drawing_available = False #start with no drawing present
    last_pos = None #initially no last position
    headers = ["x_pos", "y_pos", "Magnitudue", "Radians", "Degrees", "Dx", "Dy", "Length Change", "Total dist Traveled", "percent traveled","accurate angle", "Delta Theta"]
    time_to_train = True
    last_angle = None # use to check if gone more than 365 degrees in angle calc
    over_365 = False #check if gone more than 365 deg
    num_over =0 #number of times over 365

    def len_change(dx, dy):
        mag = math.sqrt((dx) ** 2 + (dy) ** 2)
        return(mag)
    def angle_calc(dy, dx):
        global last_angle
        global over_365
        global num_over
        angle_rad = math.atan2((-dy), dx)
        if angle_rad < 0:
            angle_rad += 2*3.14159
        angle_deg = math.degrees(angle_rad)
        if last_angle == None:  
            last_angle = angle_deg
            return(angle_deg)
            # if angles passes 360 lin from bottom to top, add 365 to angle
        elif (last_angle - angle_deg) > 200:
            num_over += 1
            last_angle = angle_deg
            angle_deg += 365*num_over
            over_365 = True
            return(angle_deg)
        elif over_365:
            last_angle = angle_deg
            angle_deg += 365*num_over
            return(angle_deg)
        last_angle = angle_deg
        return(angle_deg)
    def delta_theta(previous_angle, current_angle):
        degree_change = (current_angle - previous_angle)
        delta_theta = degree_change *3.14159/180
        return(delta_theta)

    #create directory with you name choosing, chane working directory to that folder
    folder_name = input('Hey!!!!!!!!!!! Time to start training, name the folder here:')
    og_dir = os.getcwd()
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
        print("Directory " , folder_name ,  " Created ")
    else:
        print("Directory " , folder_name ,  " already exists, quitting")
        sys.exit()
    os.chdir(folder_name)

    pygame.init()
    pygame.display.set_caption('Surgery Learning')
    print("Click the pygame icon, and use left click down to start drawing, and lift up to stop")
    def reset_screen():
        # Fill the background with white
        screen.fill((255, 255, 255))
        # draw surgery box
        pygame.draw.rect(screen, (0, 0, 0), (150, 0, 700 - 150, 500), width=7)
        # draw mimic box
        pygame.draw.rect(screen, (0, 0, 0), (700, 0, 700 - 150, 500), width=7)
        #draw joystick box
        pygame.draw.rect(screen, (0, 0, 255), (0, 500-150, 150, 150), width=1)
        # draw joystick circle
        pygame.draw.circle(screen, (255, 0, 0), (75, 500 - 75), 70)
        pygame.display.flip()
        
        pygame.draw.rect(screen, (100, 140, 70), (700, 0, 700 - 150, 500))
        largefont = pygame.font.SysFont('Corbel', 20)
        info_text = largefont.render('1. Left click + HOLD down to START recording' , True , (255,255,255))
        info_text_2 = largefont.render('2. Lift up left click to STOP recording, and start new' , True , (255,255,255))
        info_text_3 = largefont.render('3. When Done, exit out in using top right corner exit' , True , (255,255,255))
        screen.blit(info_text, (730,200))
        screen.blit(info_text_2, (730,230))
        screen.blit(info_text_3, (730,260))
    screen = pygame.display.set_mode([700+550, 500])
    reset_screen()

    #Define tuple mouse clicks
    LEFT = 1
    left_click = False

    #Clock
    clock = pygame.time.Clock()
    time_since_last_run = 0
    pygame.display.flip()

    while time_to_train:  
        dt = clock.tick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                json_dictionary = {}
                json_dictionary[folder_name] = json_dict
                with open ("actions.json","w") as fp:
                    json.dump(json_dictionary, fp)
                print("actions.json data file saved")
                time_to_train = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                left_click = True
                pygame.draw.rect(screen, (0, 70, 0), (150, 0, 700 - 150, 500), width=7)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                pygame.draw.rect(screen, (0, 0, 0), (150, 0, 700 - 150, 500), width=7)
                left_click = False
                last_pos = None
            if event.type == pygame.MOUSEMOTION:
                mcord = pygame.mouse.get_pos()
                if left_click == True:
                    if (150 < mcord[0] < 700 and 0 < mcord[1] < 500):
                        ##Live Surgeon Position
                        if last_pos == None:
                            last_pos = mcord
                        pygame.draw.circle(screen, (0, 0, 0), mcord, 2)
                        pygame.draw.line(screen, (0,0,0), last_pos, mcord, 4)
                        last_pos = mcord
                        x = mcord[0]
                        y = mcord[1]
                        drawing.append([x,y])
                        time.sleep(.001)
                        drawing_available = True  
        if (drawing_available== True) and (left_click == False):   #let go of left click and drawing available, stop recording    
            i= 0
            #add magnitude of vector movement and angle
            for index, cordinates in enumerate(drawing):
                if index - 1 >= 0:
                    dy = (cordinates[1]-drawing[index-1][1])
                    dx = (cordinates[0]-drawing[index-1][0])
                    #magnitude of vector formula
                    mag = math.sqrt((dx ** 2) + (dy ** 2))
                    angle_rad = math.atan2((-dy), dx)
                    angle_deg = math.degrees(angle_rad)
                    length_change = len_change(dx,dy)
                    tot_traveled += length_change
                else:
                    mag = 0 # if first element, no magnitude
                    angle_deg = 0
                    angle_rad = 0
                    dx = 0
                    dy = 0
                    length_change = 0
                    tot_traveled = 0
                cordinates.append(mag)
                cordinates.append(angle_rad)
                cordinates.append(angle_deg)
                cordinates.append(dx)
                cordinates.append(dy)
                cordinates.append(length_change)
                cordinates.append(tot_traveled)
                 #add delta theta
                
                list_of_actions.append([mag,angle_rad])
            #set min distance traveled to check angle
            for index, cordinates in enumerate(drawing):
                int_distance_cells = 1
                pix_traveled = 0
                pixel_min_traveled_check = 20
                x_start = drawing[index][0]
                y_start = drawing[index][1]
                percent_goal = drawing[index][-1]/tot_traveled
                drawing[index].append(percent_goal)

                #add accurate angle based on minimum pixels traveled
                while pix_traveled < pixel_min_traveled_check:
                    #exit check if reached last cell
                    try:
                        a =drawing[index+int_distance_cells][-1] 
                    except:
                        break
                    pix_traveled += drawing[index+int_distance_cells][-2]
                    x_finish = drawing[index+int_distance_cells][0]
                    y_finish = drawing[index+int_distance_cells][1]
                    int_distance_cells +=1
                #middle_cell = int(round(int_distance_cells/2))
                ddx =  x_finish - x_start
                ddy =  y_finish - y_start
                ac_angle_deg = angle_calc(ddy, ddx)
                drawing[index].append(ac_angle_deg)
            for index, row in enumerate(drawing):
                if row[9] == 0:
                    delta_th = drawing[index][10]
                else:
                    delta_th = delta_theta((drawing[index-1][10]), (drawing[index][10]))
                    row.append(delta_th)  
                list_of_actions[index][1] = delta_th
            list_of_actions[0][1] = drawing[1][3]
            #add headers to csv
            drawing.insert(0, headers)

            #iterate file saving with numbers
            while os.path.exists(str(folder_name) + "_%s.csv" % i): #if the file already exists name it with incrementing number
                i += 1
            with open(str(folder_name) + "_%s.csv" % i, "w", newline ='') as f:
                wr = csv.writer(f)
                wr.writerows(drawing)
                print("file saved as " + str(folder_name) + "_%s.csv" % i)
            drawing = [] #where data will go
            app_open = False #if paint app open or closed
            drawing_available = False #start with no drawing present
            reset_screen()
            #add to database file, list of actions
            json_dict.append(list_of_actions)
            list_of_actions = []
            #redeclare angles
            last_angle = None # use to check if gone more than 365 degrees in angle calc
            over_365 = False #check if gone more than 365 deg
            num_over = 0 #number of times over 365
        pygame.draw.circle(screen, (255, 0, 0), (75, 500-75), 70)
        pygame.display.flip()
    print("exiting")
    pygame.quit()
    training = False
    running = True
    os.chdir(og_dir)
    os.system('python graph_signatures.py')
# Done! Time to quit.
pygame.quit()
#...or is it??? restart 
if running:
    os.execv(sys.executable, ['python'] + sys.argv)