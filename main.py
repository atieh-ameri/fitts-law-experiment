import pygame, random, math, sys, csv, itertools, time, os
from datetime import datetime

# ---------- Config ----------
CIRCLE_DIAMETERS =  [40, 80, 120, 160]
DISTANCES = [180, 260, 360, 500]                   # px (amplitude)

DIRECTIONS = [1, -1]                     # 1=right, -1=left
BLOCKS = 10
BASE_COMBOS = list(itertools.product(CIRCLE_DIAMETERS, DISTANCES, DIRECTIONS))
CSV_PATH = ("fitts_trial_data.csv")
START_BTN_SIZE = 28

# ---------- Unique ID ----------
def generate_unique_id(csv_file, column_name="participant_id", lo=1000, hi=999999):
    used = set()
    if os.path.exists(csv_file):
        with open(csv_file, newline="") as f:
            for row in csv.DictReader(f):
                v = row.get(column_name, "").strip()
                if v.isdigit():
                    used.add(int(v))
    while True:
        pid = random.randint(lo, hi)
        if pid not in used:
            return pid

participant_id = generate_unique_id(CSV_PATH)
session_start_iso = datetime.now().isoformat(timespec="seconds")

# ---------- Pygame Setup ----------
pygame.init()
W, H = 1200, 800
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Fitts' Law Experiment")
clock = pygame.time.Clock()
CENTER = (W // 2, H // 2)
FONT = pygame.font.Font(None, 20)
FONT_SMALL = pygame.font.Font(None, 16)
FONT_BIG = pygame.font.Font(None, 40)

# ---------- UI Helpers ----------
def wait_for_click_on(rect=None):
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONUP:
                if rect is None or rect.collidepoint(e.pos):
                    return

def start_button_rect():
    half = START_BTN_SIZE // 2
    return pygame.Rect(CENTER[0]-half, CENTER[1]-half, START_BTN_SIZE, START_BTN_SIZE)

def wait_for_start_click(show_tip=False, tip_text="Click this"):
    # Center green square used to spawn each target
    btn = start_button_rect()
    normal_color = (0, 150, 0)
    pressed_color = (0, 100, 0)
    outline_color = (0, 0, 0)
    is_pressed_visual = False
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if btn.collidepoint(e.pos):
                    is_pressed_visual = True
            elif e.type == pygame.MOUSEBUTTONUP:
                if is_pressed_visual and btn.collidepoint(e.pos):
                    return
                is_pressed_visual = False

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, pressed_color if is_pressed_visual else normal_color, btn)
        pygame.draw.rect(screen, outline_color, btn, 2)

        if show_tip:
            tip = FONT_SMALL.render(tip_text, True, (0,0,0))
            tip_rect = tip.get_rect(midbottom=(btn.centerx, btn.top - 8))
            screen.blit(tip, tip_rect)

        pygame.display.flip()
        clock.tick(120)

def wait_for_center_button(label, subtitle="", colors=None, size=(360, 64), radius=12):
    """
    Centered button with hover/press states, border, and custom colors.
    colors keys: 'fill', 'hover', 'press', 'border', 'text', 'border_w'
    """
    if colors is None: colors = {}
    fill   = colors.get('fill',   (0, 102, 204))
    hover  = colors.get('hover',  (0, 119, 238))
    press  = colors.get('press',  (0, 85, 170))
    border = colors.get('border', (0, 0, 0))
    text_c = colors.get('text',   (255, 255, 255))
    bw     = colors.get('border_w', 3)

    btn = pygame.Rect(0, 0, *size)
    btn.center = CENTER
    pressed = False

    while True:
        mouse = pygame.mouse.get_pos()
        hovering = btn.collidepoint(mouse)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN and hovering:
                pressed = True
            elif e.type == pygame.MOUSEBUTTONUP:
                if pressed and hovering:
                    return
                pressed = False
            elif e.type == pygame.KEYDOWN and e.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                return

        screen.fill((255, 255, 255))

        if subtitle:
            sub = FONT_BIG.render(subtitle, True, (0, 0, 0))
            screen.blit(sub, sub.get_rect(center=(CENTER[0], CENTER[1] - 100)))

        color_now = press if pressed else (hover if hovering else fill)
        pygame.draw.rect(screen, color_now, btn, border_radius=radius)
        pygame.draw.rect(screen, border, btn, bw, border_radius=radius)

        cap = FONT.render(label, True, text_c)
        screen.blit(cap, cap.get_rect(center=btn.center))

        pygame.display.flip()
        clock.tick(120)

# ---------- Consent Page ----------
def consent_page():
    screen.fill((255, 255, 255))
    title = FONT_BIG.render("Consent Form", True, (0, 0, 0))
    screen.blit(title, (W//2 - title.get_width()//2, 120))

    box = pygame.Rect(150, 180, 900, 320)
    pygame.draw.rect(screen, (235, 235, 235), box, border_radius=4)
    pygame.draw.rect(screen, (0, 0, 0), box, 2, border_radius=4)
    text = (
        "Project Title: Evaluating Human Pointing Performance Using Fitts' Law\n\n"
        "Course: CIS 482 – Human-Computer Interaction\n"
        "Investigator: Atieh Ameri, Edlawit Gide, Varon Jones\n\n"
        "This project studies how quickly and accurately people move a pointer to targets "
        "of different sizes and distances.\n "
        "This experiment takes about 8-12 minutes. You can leave the experiment at any moment during the process.\n"
        "Participation involves minimal risk—no greater than those encountered in normal computer use. "
        "You may take breaks or withdraw at any time if you experience discomfort or fatigue. "
        "While there are no direct personal benefits, your participation will contribute"
        " to a better understanding of human–computer interaction. "
        "Only timing and accuracy data will be recorded. No personal information will "
        "be collected except age, mouse proficiency, and handedness.\n"
        "By clicking 'I Agree', you confirm you are 18+ and consent to participate."
    )
    lines = []
    for para in text.split("\n"):
        words = para.split(" ")
        line = ""
        for w in words:
            test = (line + " " + w).strip()
            if FONT.size(test)[0] <= box.width - 40:
                line = test
            else:
                lines.append(line); line = w
        if line: lines.append(line)
        lines.append("")
    y = box.top + 20
    for l in lines:
        screen.blit(FONT.render(l, True, (0,0,0)), (box.left + 10, y))
        y += FONT.get_height() + 3
    btn = pygame.Rect(W//2 - 100, box.bottom + 40, 200, 50)
    pygame.draw.rect(screen, (0,120,0), btn, border_radius=8)
    cap = FONT.render("I AGREE", True, (255,255,255))
    screen.blit(cap, cap.get_rect(center=btn.center))
    pygame.display.flip()
    wait_for_click_on(btn)

# ---------- Instructions ----------
def instructions_page():
    screen.fill((255, 255, 255))
    lines = [
        "Instructions",
        "1. Click the center square to make a target circle appear.",
        "2. Click the circle as quickly and accurately as possible.",
        "3. First you will do a short practice with 2 targets.",
        "4. Then the real experiment starts."
    ]
    y = 120
    for i, t in enumerate(lines):
        surf = FONT.render(t, True, (0,0,0))
        screen.blit(surf, (W//2 - surf.get_width()//2, y + i*30))


    btn = pygame.Rect(W//2 - 160, 640, 320, 56)
    pygame.draw.rect(screen, (30,30,150), btn, border_radius=8)
    lab = FONT.render("Begin Practice", True, (255,255,255))
    screen.blit(lab, lab.get_rect(center=btn.center))
    pygame.display.flip()
    wait_for_click_on(btn)

# ---------- Task Logic ----------
def dir_name(d): return "right" if d == 1 else "left"

def wait_for_hit(center_xy, radius_px, show_tip=False, tip_text="Click the circle"):
    errors = 0
    pygame.mouse.set_pos(CENTER)
    path = [CENTER]
    t0 = time.perf_counter()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif e.type == pygame.MOUSEMOTION:
                path.append(e.pos)
            elif e.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if math.dist(pos, center_xy) <= radius_px:
                    t1 = time.perf_counter()
                    straight = math.dist(CENTER, pos)
                    path_len = sum(math.dist(path[i], path[i+1]) for i in range(len(path)-1))
                    screen.fill((255,255,255)); pygame.display.flip()
                    pygame.mouse.set_pos(CENTER)
                    return (errors, round(path_len,2), round(straight,2), round(t1 - t0,4))
                else:
                    errors += 1

        screen.fill((255,255,255))
        pygame.draw.circle(screen, (0,0,0), center_xy, radius_px)
        if show_tip:
            tip = FONT_SMALL.render(tip_text, True, (0,0,0))
            tip_rect = tip.get_rect(midbottom=(center_xy[0], center_xy[1] - radius_px - 8))
            screen.blit(tip, tip_rect)
        pygame.display.flip()
        clock.tick(120)

def run_block(block_idx):
    combos = BASE_COMBOS[:]
    random.shuffle(combos)
    rows, t0 = [], time.perf_counter()
    trial = 1
    for diameter_px, amplitude_px, d in combos:
        pygame.mouse.set_pos(CENTER)
        # real trials: no labels
        wait_for_start_click(show_tip=False)
        target_center = (CENTER[0] + d*amplitude_px, CENTER[1])
        radius_px = diameter_px // 2
        errors, path_px, straight_px, t_trial = wait_for_hit(target_center, radius_px, show_tip=False)
        rows.append({
            "participant_id": participant_id,
            "session_start_iso": session_start_iso,
            "block": block_idx,
            "block_time_s": None,
            "trial": trial,
            "amplitude_px": amplitude_px,
            "direction": dir_name(d),
            "diameter_px": diameter_px,
            "radius_px": radius_px,
            "errors": errors,
            "path_distance_px": path_px,
            "center_to_click_px": straight_px,
            "trial_time_s": t_trial
        })
        trial += 1
    bt = round(time.perf_counter() - t0, 4)
    for r in rows: r["block_time_s"] = bt
    return rows

# ==== PRACTICE (labels shown here only) =======================
def run_practice():
    practice_trials = [
        (100, 200, 1),
        (100, 200, -1),
    ]
    for diameter_px, amplitude_px, d in practice_trials:
        screen.fill((255,255,255))
        txt = FONT.render("Practice trial — click center square", True, (0,0,0))
        screen.blit(txt, (W//2 - txt.get_width()//2, 120))
        pygame.display.flip()

        pygame.mouse.set_pos(CENTER)
        wait_for_start_click(show_tip=True, tip_text="Click this")

        target_center = (CENTER[0] + d*amplitude_px, CENTER[1])
        radius_px = diameter_px // 2
        wait_for_hit(target_center, radius_px, show_tip=True, tip_text="Click the circle")

    # No extra page here. Return directly to main to show first Start Block button.
    return
# ===============================================================

# ---------- Demographics (Age above Handedness) ----------
def collect_demographics():
    hand_opts = ["Left-handed", "Right-handed"]
    prof_opts = [
        ("Rarely use mouse", "Mostly touchscreen/keyboard"),
        ("Casual user", "Light use of mouse"),
        ("Regular user", "Daily computer work"),
        ("Power user", "Frequent precise tasks"),
        ("Gamer/Expert", "gaming or creative work.")
    ]
    selected_hand, selected_prof, age_txt = None, None, ""
    active_age = True

    # Layout positions
    age_label_pos = (100, 180)
    age_box = pygame.Rect(320, 174, 90, 30)

    hand_label_pos = (100, 240)
    hand_boxes, x = [], 200
    for opt in hand_opts:
        r = pygame.Rect(x, 237, 22, 22)
        hand_boxes.append((r, opt))
        x += 22 + 10 + FONT_SMALL.size(opt)[0] + 35

    prof_label_pos = (100, 300)
    prof_boxes = []
    x = 100
    base_y = 340
    spacing = (W - 200) // len(prof_opts)
    for (opt, desc) in prof_opts:
        r = pygame.Rect(x, base_y, 22, 22)
        prof_boxes.append((r, opt, desc))
        x += spacing

    btn = pygame.Rect(W//2 - 120, 440, 240, 54)

    def draw():
        screen.fill((255, 255, 255))
        title = FONT_BIG.render("Participant Information", True, (0,0,0))
        screen.blit(title, (W//2 - title.get_width()//2, 100))

        # Age first
        screen.blit(FONT.render("Age:", True, (0,0,0)), age_label_pos)
        mouse_on_box = age_box.collidepoint(pygame.mouse.get_pos())
        fill_color = (230, 245, 230) if active_age else ((240,240,240) if mouse_on_box else (255,255,255))
        border_color = (0,120,0) if active_age else (0,0,0)
        pygame.draw.rect(screen, fill_color, age_box)
        pygame.draw.rect(screen, border_color, age_box, 2)
        txt_surf = FONT.render(age_txt, True, (0,0,0))
        screen.blit(txt_surf, (age_box.x + 6, age_box.y + 6))
        if active_age and (pygame.time.get_ticks() // 500) % 2 == 0:
            caret_x = age_box.x + 6 + txt_surf.get_width() + 1
            pygame.draw.line(screen, (0,0,0), (caret_x, age_box.y + 6), (caret_x, age_box.y + age_box.height - 6), 2)

        # Handedness next
        screen.blit(FONT.render("Handedness:", True, (0,0,0)), hand_label_pos)
        for r, opt in hand_boxes:
            pygame.draw.rect(screen, (0,0,0), r, 2)
            if selected_hand == opt:
                pygame.draw.circle(screen, (0,0,0), r.center, 6)
            screen.blit(FONT.render(opt, True, (0,0,0)), (r.right + 8, r.top + 2))

        # Proficiency last
        screen.blit(FONT.render("Computer-Mouse Proficiency:", True, (0,0,0)), prof_label_pos)
        for r, opt, desc in prof_boxes:
            pygame.draw.rect(screen, (0,0,0), r, 2)
            if selected_prof == opt:
                pygame.draw.circle(screen, (0,0,0), r.center, 6)
            screen.blit(FONT.render(opt, True, (0,0,0)), (r.right + 8, r.top - 4))
            screen.blit(FONT_SMALL.render(desc, True, (90,90,90)), (r.right + 8, r.top + 14))

        ok = (selected_hand is not None and selected_prof is not None and age_txt.isdigit() and 5 <= int(age_txt) <= 120)
        pygame.draw.rect(screen, (0,120,0) if ok else (160,160,160), btn, border_radius=8)
        lab = FONT.render("Continue", True, (255,255,255))
        screen.blit(lab, lab.get_rect(center=btn.center))

        pygame.display.flip()
        return ok

    while True:
        ok = draw()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                # Age focus handling
                active_age = age_box.collidepoint(e.pos)
                # Handedness
                for r,opt in hand_boxes:
                    if r.collidepoint(e.pos):
                        selected_hand = opt
                # Proficiency
                for r,opt,desc in prof_boxes:
                    if r.collidepoint(e.pos):
                        selected_prof = opt
                if ok and btn.collidepoint(e.pos):
                    return {"handedness": selected_hand, "proficiency": selected_prof, "age": age_txt}
            elif e.type == pygame.KEYDOWN:
                if active_age:
                    if e.key == pygame.K_BACKSPACE:
                        age_txt = age_txt[:-1]
                    elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if ok:
                            return {"handedness": selected_hand, "proficiency": selected_prof, "age": age_txt}
                    elif e.unicode.isdigit() and len(age_txt) < 3:
                        age_txt += e.unicode
                else:
                    if e.key in (pygame.K_RETURN, pygame.K_KP_ENTER) and ok:
                        return {"handedness": selected_hand, "proficiency": selected_prof, "age": age_txt}

# ---------- Main ----------
def main():
    consent_page()
    demo = collect_demographics()
    instructions_page()

    try:
        pygame.mixer.init()
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
    except Exception:
        pass

    # Practice with labels; returns directly after last trial
    run_practice()

    # Real blocks without any extra "start experiment" page
    file_exists = os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="") as f:
        fieldnames = [
            "participant_id","session_start_iso",
            "handedness","proficiency","age",
            "block","block_time_s","trial",
            "amplitude_px","direction","diameter_px","radius_px",
            "errors","path_distance_px","center_to_click_px","trial_time_s"
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()

        for b in range(1, BLOCKS + 1):
            wait_for_center_button(
                "Start Block",
                subtitle=f"Block {b}/{BLOCKS}",
                colors={
                    'fill': (0, 102, 204),
                    'hover': (0, 119, 238),
                    'press': (0, 85, 170),
                    'border': (0, 0, 0),
                    'text': (255, 255, 255),
                    'border_w': 3
                },
                size=(360, 64),
                radius=12
            )

            rows = run_block(b)
            for r in rows:
                r.update(demo)
                writer.writerow(r)
            f.flush()

    screen.fill((255,255,255))
    done = FONT_BIG.render("Experiment complete. Thank you.", True, (0,0,0))
    screen.blit(done, done.get_rect(center=CENTER))
    pygame.display.flip()
    pygame.time.wait(1600)
    pygame.quit()

if __name__ == "__main__":
    main()