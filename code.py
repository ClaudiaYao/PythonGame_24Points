
import pygame
import pgzrun
from pgzhelper import *
from ctypes import windll
import random


WIDTH=800
HEIGHT=600

hwnd = pygame.display.get_wm_info()['window']
windll.user32.MoveWindow(hwnd, 0, 0, WIDTH, HEIGHT, False)

my_font = pygame.font.SysFont('Comic Sans MS', 30)

background = Actor("background")
plus_btn = Actor('add')
minus_btn = Actor('minus')
multiply_btn = Actor("multiply")
divide_btn = Actor('divide')
parent_left_btn = Actor("parent-left")
parent_right_btn = Actor('parent-right')

skip_btn = Actor('skip')
submit_btn = Actor('submit')
hint_btn = Actor("hint")

mode_btn = Actor("training_mode")

score = 0
test_data = []

plus_btn.scale = 0.6
plus_btn.x, plus_btn.y = (WIDTH - 90, 40)
minus_btn.scale = 0.4
minus_btn.x, minus_btn.y = (WIDTH - 40, 36)

multiply_btn.scale = 0.56
multiply_btn.x, multiply_btn.y = (WIDTH - 90, 105)
divide_btn.scale = 0.45
divide_btn.x, divide_btn.y = (WIDTH - 40, 100)

parent_left_btn.scale = 0.3
parent_left_btn.x, parent_left_btn.y = (WIDTH - 90, 160)
parent_right_btn.scale = 0.3
parent_right_btn.x, parent_right_btn.y = (WIDTH - 40, 160)

mode_btn.scale = 0.6
mode_btn.x, mode_btn.y = (WIDTH - 170, 40)

skip_btn.scale = 0.45
skip_btn.x, skip_btn.y = (WIDTH - 210, HEIGHT - 55)
hint_btn.scale = 0.4
hint_btn.x, hint_btn.y = (WIDTH - 130, HEIGHT - 60)
submit_btn.scale = 0.4
submit_btn.x, submit_btn.y = (WIDTH - 50, HEIGHT - 60)

operators = [plus_btn, minus_btn, multiply_btn, divide_btn, parent_left_btn, parent_right_btn]

correct_banner = Actor("correct")
correct_banner.x, correct_banner.y = (WIDTH//2, HEIGHT + 100)
wrong_banner = Actor("wrong")
wrong_banner.x, wrong_banner.y = (WIDTH//2, HEIGHT + 100)
banners = [correct_banner, wrong_banner]
banner_loop = -1
banner = None
correct_status = False
wrong_status = False
error_text = ""

nums = []
for i in range(4):
    num = Actor( "num_" + str(random.randint(1, 9)))
    num.scale = 0.8
    num.x, num.y = 100 + 130*i, 150
    nums.append(num)

operator_clones = []
dragging = False
drag_num_index = -1
drag_operator_clone_index = -1
disappear_operator_clone_index = -1
mouse_pos = (-100, -100)

evaluate_result = None


def evaluate_expression():
    expression_ls = [None] * (WIDTH // 20)
    used_num = 0
    for num in nums:
        if num.x > -1 and num.y > HEIGHT // 2:
            # get the number
            expression_ls[int(num.x // 20)] = num.image[4]
            used_num +=1

    if used_num < 4:
        return "invalid"

    def parse_operator(operator_name):
        if operator_name == "add":
            return "+"
        elif operator_name == "minus":
            return "-"
        elif operator_name == "multiply":
            return "*"
        elif operator_name == "divide":
            return "/"
        elif operator_name == "parent-left":
            return "("
        elif operator_name == "parent-right":
            return ")"

    for operator_clone in operator_clones:
        expression_ls[int(operator_clone.x // 20)] = parse_operator(operator_clone.image)

    expression = ""
    for item in expression_ls:
        if item is not None:
            expression += item
    print(expression, eval(expression))
    return eval(expression)



def on_mouse_down(pos):
    global dragging, drag_operator_clone_index, drag_num_index, correct_status
    global banner_loop, wrong_status, error_text, mouse_pos, score

    # when mouse is down, but mouse is not moved yet, the mouse position might be still (-100, -100)
    # the number or operator might disappear under this condition
    mouse_pos = pos
    if not dragging:
        for i in range(len(operators)):
            if operators[i].collidepoint(pos):
                # Create a clone of operator
                ope_clone = Actor(operators[i].image)
                ope_clone.scale = operators[i].scale * 1.5
                ope_clone.x, ope_clone.y = pos
                operator_clones.append(ope_clone)
                # this signal ensures that there is only one operator or number
                # in dragging status
                drag_operator_clone_index = len(operator_clones) - 1
                dragging = True
                break

    if not dragging:
        for i in range(len(operator_clones)):
            if operator_clones[i].collidepoint(pos):
                # this signal ensures that there is only one operator or number
                # in dragging status
                dragging = True
                drag_operator_clone_index = i
                break

    if not dragging:
        for i in range(len(nums)):
            if nums[i].collidepoint(pos):
                # this signal ensures that there is only one operator or number
                # in dragging status
                dragging = True
                drag_num_index = i
                break

    if not dragging:
        if (correct_status == False and wrong_status == False) and submit_btn.collidepoint(pos):
            result = evaluate_expression()
            if result == "invalid":
                error_text = "Should use all the four number only once."
            elif result == 24:
                correct_status = True
                score += 400
            else:
                wrong_status = True

            banner_loop = 80


        if skip_btn.collidepoint(pos):
            reset_numbers()


def on_mouse_move(pos):
    global mouse_pos
    if dragging:
        mouse_pos = pos
        print(mouse_pos)

def on_mouse_up(pos):
    global dragging, drag_num_index, drag_operator_clone_index, mouse_pos, disappear_operator_clone_index

    if dragging:
        dragging = False
        if drag_operator_clone_index > -1 and pos[1] < HEIGHT // 2:
            disappear_operator_clone_index = drag_operator_clone_index

        drag_num_index = -1
        drag_operator_clone_index = -1
        mouse_pos = (-100, -100)

def reset_numbers():
    for i in range(len(nums)):
        nums[i].image = "num_" + str(random.randint(1, 9))
        nums[i].x, nums[i].y = 100 + 130*i, 150

    operator_clones.clear()


def update():
    global score, disappear_operator_clone_index, dragging, banner, correct_status, wrong_status
    global banner_loop, error_text

    if dragging:
        if drag_num_index > -1:
            nums[drag_num_index].x, nums[drag_num_index].y = mouse_pos
            print("dragging ... ", drag_num_index, mouse_pos)
        elif drag_operator_clone_index > -1:
            operator_clones[drag_operator_clone_index].x, operator_clones[drag_operator_clone_index].y = mouse_pos
            print("dragging operator clone: ", drag_operator_clone_index)

    if disappear_operator_clone_index > -1:
        operator_clones[disappear_operator_clone_index].scale *= 0.9
        if operator_clones[disappear_operator_clone_index].scale < 0.1:
            operator_clones.pop(disappear_operator_clone_index)
            print("deleted: ", disappear_operator_clone_index)
            disappear_operator_clone_index = -1

    if correct_status == True:
        banner = banners[0]
    elif wrong_status == True:
        banner = banners[1]

    if banner_loop > -1:
        if error_text == "":
            if banner_loop >= 55:
                banner.y -= (banner.y - HEIGHT//2) * 0.1
            elif banner_loop < 25:
                banner.y += (banner.y - HEIGHT//2) * 0.1

        banner_loop -= 1
    else:
        if correct_status == True:
            reset_numbers()
            correct_status = False

        wrong_status = False
        banner = None
        error_text = ""


def draw():
    global score, game_over
    background.draw()

    screen.draw.text("Score: " + str(score), centerx=100, centery=20, color=(255,255,255), fontsize=30)

    skip_btn.draw()
    submit_btn.draw()
    hint_btn.draw()
    mode_btn.draw()

    for operator_clone in operator_clones:
        operator_clone.draw()

    for operator in operators:
        operator.draw()

    for num in nums:
        num.draw()

    if error_text !="":
        screen.draw.text(error_text, centerx=250, centery=HEIGHT-30, color=(80, 50, 60), fontsize=30)


    if correct_status:
        correct_banner.draw()
    elif wrong_status:
        wrong_banner.draw()
    # if game_over:
    #     screen.draw.text('Game Over', centerx=400, centery=270, color=(255,255,255), fontsize=60)
    #     screen.draw.text('Score: ' + str(score), centerx=400, centery=330, color=(255,255,255), fontsize=60)
    # else:
    #     runner.draw()
    #     for actor in obstacles:
    #         actor.draw()

    # screen.draw.text('Score: ' + str(score), (15,10), color=(0,0,0), fontsize=30)

pgzrun.go() # Must be last line
