import pygame
import sys
import math

# 1. Initialize the Engine
pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
clock = pygame.time.Clock()


# 2. Stickman Coordinates & Physics | THE PANTRY (Variables defined ONCE)
pos = pygame.Vector2(960, 540)
speed = 5
gravity = 0.5
jump_height = -30
velocity_y = -12
is_jumping = False


# This sets up the 'ink' and 'paper' for the text / Shapes 'SQUARE'
font = pygame.font.SysFont("Arial", 48, bold=True)
rect_label_text = font.render("RECTANGLE", True, (0, 0, 255))
rect_label_rect = rect_label_text.get_rect(center=(960, 200)) # The 'hitbox' for the word
is_dragging = False # The 'Switch' to tell if we are holding it

# --- TRIANGLE LABEL SETUP ---
tri_label_text = font.render("TRIANGLE", True, (0, 255, 0))
tri_label_rect = tri_label_text.get_rect(center=(960,300)) # Start below
is_dragging_tri = False

# --- BOX LABEL SETUP ---
box_label_text = font.render("SQUARE", True, (255, 0, 0))
box_label_rect = box_label_text.get_rect(center=(960,400))
is_dragging_box = False

# -- CIRCLE LABEL SETUP ---
circle_label_text = font.render("CIRCLE", True, (255, 165, 0))
circle_label_rect = circle_label_text.get_rect(center=(960,600))
is_dragging_circle = False

# <<<<<<< END OF LABEL SECTION >>>>>>>>>


# The Blue Rect (x, y, width, height)
rect_x = 1000
rect_y = 770 # Height
rect_w = 300
rect_h = 100


# The Red Box (x, y, width, height)
box_x = 600 # Middle of 1920 is 960, so 960 - 100
box_y = 670 # Sitting on the floor (870 - 100)
box_w = 200
box_h = 200


# Triangle Points (X, Y)
# Let's put it to the left of the square
tri_p1 = (200, 870) # Bottom Left
tri_p2 = (400, 870) # Bottom Right
tri_p3 = (300, 700) # Top Point (The Peak)

# --- CIRCLE SETUP ---
circle_pos = pygame.Vector2(1600, 790) # Center point
circle_radius = 80
circle_color = (255, 165, 0) # Orange (RGB)



while True:
    # 3. Input Manifold (WASD / Arrows)
    for event in pygame.event.get():  # Just ONE loop for everything
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # --- MOUSE EVENTS ---
        if event.type == pygame.MOUSEBUTTONDOWN: # Check SQUARE
            if rect_label_rect.collidepoint(event.pos):
                is_dragging = True
            if tri_label_rect.collidepoint(event.pos): # Check TRIANGLE
                is_dragging_tri =True
            if box_label_rect.collidepoint(event.pos): # Check BOX
                is_dragging_box = True
            if circle_label_rect.collidepoint(event.pos): # Check CIRCLE
                is_dragging_circle = True
        if event.type == pygame.MOUSEBUTTONUP:
            is_dragging = False
            is_dragging_tri = False
            is_dragging_box = False
            is_dragging_circle = False

        # --- SNAP LOGIC ---
        if not is_dragging_box: # SQUARE
            dist_x = abs(box_label_rect.centerx - (box_x + 100))
            dist_y = abs(box_label_rect.centery - (box_y + 100))

            if dist_x < 100 and dist_y < 100:
                box_label_rect.center = (box_x + 100, box_y + 100)

        if not is_dragging: # RECTANGLE
            dist_x = abs(rect_label_rect.centerx - (rect_x + 150))
            dist_y = abs(rect_label_rect.centery - (rect_y + 50))

            if dist_x < 150 and dist_y < 50:
                rect_label_rect.center = (rect_x + 150, rect_y + 50)

        if not is_dragging_tri: # TRIANGLE
            dist_x = abs(tri_label_rect.centerx - 300)
            dist_y = abs(tri_label_rect.centery - 800)

            if dist_x < 100 and dist_y < 100:
                tri_label_rect.center = (300,800)

        if not is_dragging_circle: # CIRCLE
            dist_x = abs(circle_label_rect.centerx - circle_pos.x)
            dist_y = abs(circle_label_rect.centery - circle_pos.y)

            if dist_x < 80 and dist_y < 80:
                circle_label_rect.center = (int(circle_pos.x), int(circle_pos.y))


    # Get the state of keys (this stays outside the event loop)
    keys = pygame.key.get_pressed()

    # Left/Right movement
    if keys[pygame.K_a] or keys[pygame.K_LEFT]: pos.x -= speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]: pos.x += speed

    # JUMPING (Only if not already jumping)
    if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and not is_jumping:
        velocity_y = jump_height
        is_jumping = True

    # 4. PHYSICS (The "Math" Section)
    velocity_y += gravity    # Gravity pulls down
    pos.y += velocity_y      # Move the stickman

    # ---RED BOX COLLISION ---
    # Check if we are within the Left and Right sides of the box
    if box_x - 20 < pos.x < box_x + box_w + 20:
        if box_y <= pos.y + 110 <= box_y + 20: # Check if our feet are hitting the top of the box
            if velocity_y > 0:
                pos.y = box_y - 110
                velocity_y = 0
                is_jumping = False

    # ---BLUE RECT BOX ---
    if rect_x - 20 < pos.x < rect_x + rect_w + 20:
        if rect_y <= pos.y + 110 <= rect_y + 20:
            if velocity_y > 0:
                pos.y = rect_y - 110
                velocity_y = 0
                is_jumping = False



    # FLOOR COLLISION (The " GROUND" Check)
    if pos.y >= 870:
        pos.y = 870
        velocity_y = 0.0
        is_jumping = False

    # CEILING (Top of the Box)
    if pos.y <= 120: # 100 (line) + 20 (head radius)
        pos.y = 120
        velocity_y = 0 # Bonk

    # LEFT WALL (at 100)
    if pos.x <= 100:
        pos.x = 100
    # RIGHT WALL
    if pos.x >= 1820:
        pos.x = 1820

    # --- DRAG LOGIC ----
    # --- RECTANGLE ----
    if is_dragging:
        mouse_pos = pygame.mouse.get_pos()
        rect_label_rect.center = mouse_pos
    # --- TRIANGLE ----
    if is_dragging_tri:
        tri_label_rect.center = pygame.mouse.get_pos()
    # --- SQUARE ----
    if is_dragging_box:
        box_label_rect.center = pygame.mouse.get_pos()
    # --- CIRCLE ----
    if is_dragging_circle:
        circle_label_rect.center = pygame.mouse.get_pos()


    # --- TRIANGLE SLIDE & SOLID LOGIC ----
    # If stickman is between the left (400) and right (600) points of the triangle
    # Math: Calculate the 'height' of the triangle at the Stickman's current X
    # This creates a sloped floor
    if 200 < pos.x < 400:
        dist_from_center = abs(pos.x - 300)
        slope_height = 700 + (dist_from_center * 1.7)

        # If his feet (pos.y + 110) go below the slope
        if pos.y + 110 > slope_height:
            pos.y = slope_height - 110 # Snap him to the surface
            velocity_y = 0
            is_jumping = False

            # Now apply the slide push
            if pos.x < 300: pos.x -= 3
            else: pos.x += 3

    # --- CIRCLE COLLISION MATH ---
    # 1. Calculate distance from stickman's feet to the circle's center
    dx = pos.x - circle_pos.x
    dy = (pos.y + 110) - circle_pos.y
    distance = math.sqrt(dx**2 + dy**2)

    # 2. If he's touching or inside the circle's radius
    if distance < circle_radius:
        if velocity_y > 0:
            pos.y = circle_pos.y - circle_radius - 110
            velocity_y = 0
            is_jumping = False


    # 4. Rendering (The "Blu-ray" Visuals)
    screen.fill((30, 30, 30)) # Cyberpunk Dark Grey

    # DRAW THE STICKMAN (Relative to 'pos')
    # HEAD
    walk_swing = math.sin(pygame.time.get_ticks() * 0.01) * 20
    pygame.draw.circle(screen, (255,255, 255), (int(pos.x), int(pos.y)), 20, 2)
    # Body
    pygame.draw.line(screen, (0, 255, 255), (pos.x, pos.y + 20), (pos.x, pos.y + 70), 2)
    # Arms
    pygame.draw.line(screen, (0, 255, 255), (pos.x - 30, pos.y + 40), (pos.x + 30, pos.y + 40), 2)
    # Left Legs
    pygame.draw.line(screen, (0, 255, 255), (pos.x, pos.y + 70), (pos.x - 20 + walk_swing, pos.y + 110), 2)
    # Right Leg
    pygame.draw.line(screen, (0, 255, 255), (pos.x, pos.y + 70), (pos.x + 20 - walk_swing, pos.y + 110), 2)

    # Drawing the boundaries (white Lines)
    # Ceiling
    pygame.draw.line(screen, (255, 255, 255), (100, 100), (1820, 100), 2)
    # Floor
    pygame.draw.line(screen, (255, 255, 255), (100, 980), (1820, 980), 2)
    # Left Wall
    pygame.draw.line(screen, (255, 255, 255), (100, 100), (100, 980), 2)
    #Right wall
    pygame.draw.line(screen,(255, 255, 255), (1820, 100), (1820, 980), 2)


    # ARE SHAPE DRAW'S & COLORS
    # Draw the Solid Blue Rec
    pygame.draw.rect(screen, (0, 0, 255), (rect_x, rect_y, rect_w, rect_h))
    # Draw the Solid Red Box
    pygame.draw.rect(screen, (255, 0, 0), (box_x, box_y, box_w, box_h))
    # Draw a Green Triangle
    pygame.draw.polygon(screen, (0, 255, 0), [tri_p1, tri_p2, tri_p3])
    # Draw a Orange Circle
    pygame.draw.circle(screen, circle_color, (int(circle_pos.x), int(circle_pos.y)), circle_radius)

    # --- VISUALS/WORD/SHAPE ----
    screen.blit(rect_label_text, rect_label_rect) # Draws the RECTANGLE
    screen.blit(tri_label_text, tri_label_rect) # Draw the TRIANGLE
    screen.blit(box_label_text, box_label_rect) # Draw the SQUARE
    screen.blit(circle_label_text, circle_label_rect) # Draw the CIRCLE
    pygame.display.flip()


    clock.tick(60) # Capped at 60 FPS for stability

