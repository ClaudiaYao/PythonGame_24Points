

import pgzrun
from pgzhelper import *
from operators import *
from ctypes import windll
import random
import os


WIDTH = 800
HEIGHT = 600

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
exponent_btn = Exp_operator("power")
# root_btn = Actor("root")

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

exponent_btn.scale = 0.26
exponent_btn.x, exponent_btn.y = WIDTH - 90, 215

# root_btn.scale = 0.26
# root_btn.x, root_btn.y = WIDTH - 40, 215

mode_btn.scale = 0.6
mode_btn.x, mode_btn.y = (WIDTH - 170, 40)

skip_btn.scale = 0.45
skip_btn.x, skip_btn.y = (WIDTH - 210, HEIGHT - 55)
hint_btn.scale = 0.4
hint_btn.x, hint_btn.y = (WIDTH - 130, HEIGHT - 60)
submit_btn.scale = 0.4
submit_btn.x, submit_btn.y = (WIDTH - 50, HEIGHT - 60)

operators = [plus_btn, minus_btn, multiply_btn, divide_btn, parent_left_btn, parent_right_btn, exponent_btn]

correct_banner = Actor("correct")
correct_banner.x, correct_banner.y = (WIDTH//2, HEIGHT + 100)
wrong_banner = Actor("wrong")
wrong_banner.x, wrong_banner.y = (WIDTH//2, HEIGHT + 100)
banners = [correct_banner, wrong_banner]
display_loop = -1
banner = None
correct_status = False
wrong_status = False
error_text = ""

mode = "train"
test_data = []
test_data_index = -1

nums = []
for i in range(4):
    num = Actor("num_" + str(random.randint(1, 9)))
    num.scale = 0.8
    num.x, num.y = 100 + 130*i, 150
    nums.append(num)

operator_clones = []
dragging = False
drag_num_index = -1
drag_operator_clone_index = -1
disappear_operator_clone_index = -1
drag_power_operator_clone_index = -1
mouse_pos = (-100, -100)

evaluate_result = None
power_operator_clones = []
root_operators = []

def evaluate_expression():
    expression_ls = [None] * (WIDTH // 20)
    used_num = 0
    for num in nums:
        if num.x > -1 and num.y > HEIGHT // 2:
            # get the number
            expression_ls[int(num.x // 20)] = num.image[4]
            used_num += 1

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
    return expression


def save_data(data):

    path = './test_data.txt'
    file_exists = os.path.exists(path)
    if file_exists:
        fh = open(path, "a")
    else:
        fh = open(path, "w")

    text = ""
    for num in nums:
        text += num.image[4]

    text += "|"
    text += data
    fh.write(text + "\n")
    fh.close()


def load_data():
    global error_text, test_data

    path = './test_data.txt'
    file_exists = os.path.exists(path)
    if not file_exists:
        error_text = "no test data."
    else:
        fh = open(path, "r")

    test_data.clear()
    lines = fh.readlines()
    fh.close()

    for line in lines:
        test_data.append(line[:-1])
    return test_data


def get_hint():
    data = test_data[test_data_index]
    operator_clones.clear()

    # define a local function because it is only used by this one function
    def unparse_operator(operator_type):
        if operator_type == "+":
            return "add"
        elif operator_type == "-":
            return "minus"
        elif operator_type == "*":
            return "multiply"
        elif operator_type == "/":
            return "divide"
        elif operator_type == "(":
            return "parent-left"
        elif operator_type == ")":
            return "parent-right"

    for i in range(len(nums)):
        nums[i].x, nums[i].y = 100 + 130 * i, 150

    # hint means not giving the full solution
    for i in range(5, len(data)-3):
        if "9" >= data[i] >= "1":
            for num in nums:
                if num.image[4] == data[i] and num.y != HEIGHT - 150:
                    num.x, num.y = 50 + (i-5)*90, HEIGHT - 150
                    print(num)
                    break
        else:
            operator_name = Actor(unparse_operator(data[i]))
            operator_name.x, operator_name.y = 50 + (i-5)*90, HEIGHT - 150
            operator_clones.append(operator_name)


def on_mouse_down(pos):
    global dragging, drag_operator_clone_index, drag_num_index, correct_status
    global display_loop, wrong_status, error_text, mouse_pos, score, mode, test_data_index
    global drag_power_operator_clone_index
    # when mouse is down, but mouse is not moved yet, the mouse position might be still (-100, -100)
    # the number or operator might disappear under this condition
    mouse_pos = pos
    if not dragging:
        for i in range(len(operators)):
            if operators[i].collidepoint(pos):
                # Create a clone of operator
                if operators[i].image == "power":
                    ope_clone = Exp_operator("power_template")
                    ope_clone.scale = operators[i].scale * 4
                    power_operator_clones.append(ope_clone)
                    drag_power_operator_clone_index = len(power_operator_clones) - 1
                else:
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
        if (correct_status is False and wrong_status is False) and submit_btn.collidepoint(pos):
            result_str = evaluate_expression()

            if result_str == "invalid":
                error_text = "Should use all the four number only once."
            elif eval(result_str) == 24:
                correct_status = True
                score += 400
                if mode == "train":
                    save_data(result_str)
            else:
                wrong_status = True

            display_loop = 80

        if skip_btn.collidepoint(pos):
            test_data_index += 1
            if test_data_index >= len(test_data):
                test_data_index = 0
            reset_numbers()

        # mouse_down will catch the mouse pressing down event once. That means, if the mouse keeps
        # pressing down, the code within this function will only run once, so do not need to
        # worry about the repeated value setting
        if mode_btn.collidepoint(pos):
            if mode == "train":
                mode = "test"
                mode_btn.image = "test_mode"
                # after loading data, test_data list is filled with the existing questions
                # and solutions
                load_data()
                if error_text == "":
                    test_data_index = random.randint(0, len(test_data)-1)
                else:
                    display_loop = 50
            elif mode == "test":
                mode = "train"
                mode_btn.image = "training_mode"

            reset_numbers()

        if hint_btn.collidepoint(pos):
            if mode == "test":
                get_hint()


def on_mouse_move(pos):
    global mouse_pos
    if dragging:
        mouse_pos = pos
        print(mouse_pos)
        if drag_operator_clone_index > -1:
            if operator_clones[drag_operator_clone_index].image == "power_template":
                operator_clones[drag_operator_clone_index].move(pos)


def on_mouse_up(pos):
    global dragging, drag_num_index, drag_operator_clone_index, mouse_pos, disappear_operator_clone_index
    global drag_power_operator_clone_index

    if dragging:
        dragging = False
        if drag_operator_clone_index > -1 and pos[1] < HEIGHT // 2:
            disappear_operator_clone_index = drag_operator_clone_index

        # this is todo...........
        if drag_num_index > -1:
            num = nums[drag_num_index]
            for operator in power_operator_clones:
                if operator.colliderect(num):
                    if operator.is_first_operand(num):
                        # print("first operand")
                        operator.first_operand = num
                    elif operator.is_second_operand(num):
                        operator.second_operand = num
                    print(power_operator_clones[0].first_operand)
                    print(power_operator_clones[0].second_operand)
                    break

            drag_num_index = -1

        drag_operator_clone_index = -1
        drag_power_operator_clone_index = -1
        mouse_pos = (-100, -100)


def reset_numbers():
    global test_data_index

    if mode == "train":
        for i in range(len(nums)):
            nums[i].image = "num_" + str(random.randint(1, 9))
            nums[i].x, nums[i].y = 100 + 130*i, 150

    elif mode == "test":
        data = test_data[test_data_index][:4]
        for i in range(len(nums)):
            nums[i].image = "num_" + str(data[i])
            nums[i].x, nums[i].y = 100 + 130 * i, 150
        # test_data_index +=1
        #
        # if test_data_index >= len(test_data):
        #     test_data_index = 0
    operator_clones.clear()


def update():
    global score, disappear_operator_clone_index, dragging, banner, correct_status, wrong_status
    global display_loop, error_text

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

    if correct_status is True:
        banner = banners[0]
    elif wrong_status is True:
        banner = banners[1]

    if display_loop > -1:
        if error_text == "":
            if display_loop >= 55:
                banner.y -= (banner.y - HEIGHT//2) * 0.1
            elif display_loop < 25:
                banner.y += (banner.y - HEIGHT//2) * 0.1

        display_loop -= 1
    else:
        if correct_status is True:
            reset_numbers()
            correct_status = False

        wrong_status = False
        banner = None
        error_text = ""


def draw():
    global score
    background.draw()

    screen.draw.text("Score: " + str(score), centerx=100, centery=20, color=(255, 255, 255), fontsize=30)

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

    if error_text != "":
        screen.draw.text(error_text, centerx=250, centery=HEIGHT-30, color=(80, 50, 60), fontsize=30)

    if correct_status:
        correct_banner.draw()
    elif wrong_status:
        wrong_banner.draw()


pgzrun.go()  # Must be last line
