import pygame
import os

pygame.init()
pygame.mixer.init()

music_folder = r'C:\Users\Акниет\Desktop\practice_pp2\Practice9\music_player\music'
songs = [os.path.join(music_folder, f) for f in os.listdir(music_folder) 
         if f.endswith(('.mp3', '.wav'))]

if not songs:
    print("No .mp3 or .wav files found in", music_folder)
    pygame.quit()
    exit()

durations = []
for song in songs:
    durations.append(pygame.mixer.Sound(song).get_length())

music_index = 0
num = len(songs)

screen = pygame.display.set_mode((600, 400))
BG = (255, 255, 255)
CARD = (200, 200, 200)
ACCENT = (0, 200, 150)
TEXT = (240, 240, 240)
SUBTEXT = (140, 140, 140)
HIGHLIGHT = (255, 80, 80)
BLACK = (0, 0, 0)
cur_pos = 0

font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 22)

done = False

clock = pygame.time.Clock()

def play_next():
    global music_index
    music_index = (music_index + 1) % num
    pygame.mixer.music.load(songs[music_index])
    pygame.mixer.music.play()

def play_prev():
    global music_index
    music_index = (music_index - 1) % num
    pygame.mixer.music.load(songs[music_index])
    pygame.mixer.music.play()

def get_start(h,m,s):
    if (h < 10):
        if (m < 10):
            if (s < 10):
                return font.render(f"0{h:.0f}:0{m:.0f}:0{s:.0f}", True, BLACK)
            else:
                return font.render(f"0{h:.0f}:0{m:.0f}:{s:.0f}", True, BLACK)
        elif (s < 10):
            return font.render(f"0{h:.0f}:{m:.0f}:0{s:.0f}", True, BLACK)
        else:
            return font.render(f"0{h:.0f}:{m:.0f}:{s:.0f}", True, BLACK)
    elif (m < 10):
        if (s < 10):
            return font.render(f"{h:.0f}:0{m:.0f}:0{s:.0f}", True, BLACK)
        else:
            return font.render(f"{h:.0f}:0{m:.0f}:{s:.0f}", True, BLACK)
    else:
        return font.render(f"{h:.0f}:{m:.0f}:{s:.0f}", True, BLACK)

current_times = 0

is_paused = False

while not done:
    if durations[music_index] > 0:                     # avoid division by zero
        progress_ratio = current_times / durations[music_index]
        circle_x = 200 + progress_ratio * 900
    else:
        circle_x = 200
    if pygame.mixer.music.get_busy():
        current_times = pygame.mixer.music.get_pos() / 1000
    screen.fill(BG)

# карточка
    pygame.draw.rect(screen, CARD, (20, 20, 560, 360), border_radius=15)

# текущий трек (центр)
    song_name = os.path.basename(songs[music_index])
    name_surface = font.render(song_name, True, TEXT)
    screen.blit(name_surface, (50, 60))

# прогресс бар
    pygame.draw.line(screen, SUBTEXT, (50, 200), (550, 200), 3)

    if durations[music_index] > 0:
     progress_ratio = current_times / durations[music_index]
     circle_x = 50 + progress_ratio * 500
    else:
     circle_x = 50

    pygame.draw.line(screen, ACCENT, (50, 200), (circle_x, 200), 4)
    pygame.draw.circle(screen, ACCENT, (circle_x, 200), 6)

# время
    h = current_times // 3600
    m = current_times // 60
    s = current_times % 60

    start = get_start(h, m, s)
    end = get_start(durations[music_index]//3600,
                durations[music_index]//60,
                durations[music_index]%60)

    screen.blit(start, (50, 220))
    screen.blit(end, (470, 220))

# список треков (компактный)
    for i, s in enumerate(songs):
     s0 = os.path.basename(s)
     color = TEXT if s0 != song_name else HIGHLIGHT
     name = small_font.render(f'{i+1}. {s0}', True, color)
     screen.blit(name, (50, 260 + i*20))

# управление
    controls = small_font.render("P Play | S Pause | N Next | B Back | Q Quit", True, SUBTEXT)
    screen.blit(controls, (50, 330))

    w = 300
    
    pygame.draw.line(screen, BLACK, (200, 450), (1100,450), 2)

    add = durations[music_index]/900

    h = current_times//3600
    m = current_times//60
    s = current_times%60

    start = get_start(h,m,s)
    end = get_start(durations[music_index]//3600, durations[music_index]//60, durations[music_index]%60)        
    # end = font.render(f"{durations[music_index]//3600:.0f}:{durations[music_index]//60:.0f}:{durations[music_index]%60:.0f}", True, BLACK)

    screen.blit(start, (210,420))
    screen.blit(end, (1050,420))

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                done = True
            elif event.key == pygame.K_p:
                if is_paused:
                    pygame.mixer.music.unpause()
                    is_paused = False
                elif not pygame.mixer.music.get_busy():
                    pygame.mixer.music.load(songs[music_index])
                    pygame.mixer.music.play()
                    pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
            elif event.key == pygame.K_s:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.pause()
                    is_paused = True
            elif event.key == pygame.K_n:
                cur_pos = 0
                play_next()
                is_paused = False
            elif event.key == pygame.K_b:
                play_prev()
                is_paused = False
        elif event.type == pygame.USEREVENT + 1:
            play_next()       

    pygame.display.flip()
    clock.tick(15)  

pygame.quit()