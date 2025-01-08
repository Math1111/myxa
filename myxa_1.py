from tkinter import *
from random import *
from winsound import *
from time import *

def play_sound_ok():
    files = []
    for i in range(1, 7):
        files.append(f"hit{i}.wav")
    file = choice(files)
    PlaySound(file, SND_ASYNC | SND_FILENAME)

def play_sound_fail():
    files = []
    for i in range(1, 8):
        files.append(f"fail{i}.wav")
    file = choice(files)
    PlaySound(file, SND_ASYNC | SND_FILENAME)

def collision_detection(x, y):
    position = canvas.coords(npc_id)
    left = position[0]
    right = position[0] + npc_width
    top = position[1]
    bottom = position[1] + npc_height
    return left <= x <= right and top <= y <= bottom

def hit():
    global score
    score += 1
    update_points()
    play_sound_ok()
    spawn()

def missclick():
    global score
    score -= 1
    if score < 0:
        game_over()
    else:
        update_points()
        play_sound_fail()

def spawn():
    for i in range(100):
        x = randint(1, 400)
        y = randint(1, 400)
        if abs(mouse_x - x) > 200 or abs(mouse_y - y) > 200:
            break
    canvas.moveto(npc_id, x, y)

def game_update():
    global canvas
    spawn()
    if randint(1, 2) == 1:
        canvas.itemconfig(npc_id, image=bottom_image)
    else:
        canvas.itemconfig(npc_id, image=top_image)
    window.after(1000, game_update)

def update_points():
    canvas.itemconfigure(text_id, text=f'Очки: {score}')

def game_over():
    global gameover
    canvas.itemconfigure(text_id, text='Потрачено')
    gameover = True
    PlaySound('gameover.wav', SND_ASYNC | SND_FILENAME)

def mouse_click(e):
    if gameover:
        return
    if collision_detection(e.x, e.y):
        hit()
    else:
        missclick()

def mouse_motion(event):
    global mouse_x, mouse_y
    mouse_x, mouse_y = event.x, event.y

def show_start_screen():
    global start_message
    canvas.config(bg="blue")
    start_message = canvas.create_text(game_width / 2, game_height / 2, text="Поймай как можно больше мух", fill="black", font="Arial 30")
    window.after(3000, hide_start_screen)

def hide_start_screen():
    canvas.delete(start_message)
    start_game()

def start_game():
    global game_time_left, gameover
    game_time_left = 25000
    gameover = False
    canvas.config(bg="white")
    canvas.itemconfig(npc_id, state='normal')  # Показываем изображение при старте игры
    update_timer()
    game_update()

def update_timer():
    global game_time_left
    if game_time_left > 0:
        game_time_left -= 1000
        timer_label.config(text=f"Время: {game_time_left // 1000}")
        window.after(1000, update_timer)
    else:
        end_game()

def end_game():
    global gameover
    gameover = True
    canvas.config(bg="purple")
    canvas.delete("all")
    final_score_label = Label(canvas, text=f"Конец игры!\nВаш счёт: {score}", font="Arial 40", fg="white", bg="purple")
    final_score_label.place(relx=0.5, rely=0.5, anchor=CENTER)

game_width = 720
game_height = 720
npc_width = 120
npc_height = 95
score = 10
mouse_x = mouse_y = 0
gameover = False
game_time_left = 0
window = Tk()

bottom_image = PhotoImage(file='myxa_niz.png')
top_image = PhotoImage(file='myxa_verx.png')

window.title('Проучи тролля')
window.resizable(width=False, height=False)
canvas = Canvas(window, width=game_width, height=game_height, bg="black")
npc_id = canvas.create_image(0, 0, anchor='nw', image=bottom_image)
canvas.itemconfig(npc_id, state='hidden')  # Скрываем изображение перед началом игры
timer_label = Label(canvas, text="", font="Arial 16", fg="black", bg="white")
timer_label.place(x=10, y=10)

text_id = canvas.create_text(
    game_width - 10, 10,
    fill='black',
    font='Times 20 bold',
    text=f'Очки: {score}',
    anchor=NE)

screamer_image = PhotoImage(file='screamer.png')
screamer_id = canvas.create_image(0, 0, image=screamer_image,
                                  anchor=NW)
canvas.itemconfig(screamer_id, state='hidden')

canvas.bind('<Button>', mouse_click)
canvas.bind('<Motion>', mouse_motion)

canvas.pack()
show_start_screen()
window.mainloop()