# solar_system_with_moons_and_gui.py
import turtle
import math
import time
import os
import tkinter as tk
from PIL import Image, ImageTk

# ---------- Configuration: edit image paths if you want ----------
earth_path = r"C:\Users\TUF\OneDrive\Desktop\project TD\earth.gif"
bg_image = r"C:\Users\TUF\OneDrive\Desktop\project TD\space.gif"
sun_path = r"C:\Users\TUF\OneDrive\Desktop\project TD\sun.gif"
mercury_path = r"C:\Users\TUF\OneDrive\Desktop\project TD\mercury.gif"
venus_path = r"C:\Users\TUF\OneDrive\Desktop\project TD\venus.gif"
mars_path = r"C:\Users\TUF\OneDrive\Desktop\project TD\mar.gif"
jupiter_path = r"C:\Users\TUF\OneDrive\Desktop\project TD\jupiter.gif"
saturn_path = r"C:\Users\TUF\OneDrive\Desktop\project TD\saturn.gif"
uranus_path = r"C:\Users\TUF\OneDrive\Desktop\project TD\uranus.gif"
neptune_path = r"C:\Users\TUF\OneDrive\Desktop\project TD\neptune.gif"
# ----------------------------------------------------------------

# Set up the screen
screen = turtle.Screen()
screen.setup(width=1000, height=800)
screen.bgcolor("black")
screen.title("Solar System Simulation with Elliptical Orbits & Moons")
screen.tracer(0)

# safe add shape helper
def safe_addshape(path):
    if os.path.exists(path):
        try:
            screen.addshape(path)
            return path
        except Exception:
            return None
    return None

# Try to add shapes (falls back to "circle" if not found)
mercury_path = safe_addshape(mercury_path) or "circle"
earth_path = safe_addshape(earth_path) or "circle"
venus_path = safe_addshape(venus_path) or "circle"
mars_path = safe_addshape(mars_path) or "circle"
jupiter_path = safe_addshape(jupiter_path) or "circle"
saturn_path = safe_addshape(saturn_path) or "circle"
uranus_path = safe_addshape(uranus_path) or "circle"
neptune_path = safe_addshape(neptune_path) or "circle"
sun_image = safe_addshape(sun_path) or "circle"

# Optional background image
if os.path.exists(bg_image):
    try:
        screen.bgpic(bg_image)
    except Exception:
        pass

# ---------- global UI state ----------
speed_multiplier = 1.0
paused = False
show_orbits = True
show_labels = True
update_interval_ms = 50  # timer interval

# ---------- starfield background (drawn once) ----------
def draw_stars(n=120):
    star_t = turtle.Turtle()
    star_t.hideturtle()
    star_t.penup()
    star_t.speed(0)
    screen_x = screen.window_width() // 2
    screen_y = screen.window_height() // 2
    import random
    for _ in range(n):
        x = random.randint(-screen_x, screen_x)
        y = random.randint(-screen_y, screen_y)
        star_t.goto(x, y)
        star_t.dot(random.choice([1, 2, 2, 3]))
    star_t.hideturtle()

draw_stars(180)

# Info display turtle (bottom)
info_turtle = turtle.Turtle()
info_turtle.hideturtle()
info_turtle.penup()
info_turtle.color("white")
info_turtle.goto(0, -360)
info_turtle.write("Solar System (click a planet for info)", align="center", font=("Arial", 14, "bold"))

# ---------- Details dictionary (extended) ----------
planet_details = {
    "Mercury": "Mercury\nRadius: 2,439 km\nOrbit: 88 days\nTemp: -173 to 427 °C",
    "Venus": "Venus\nRadius: 6,052 km\nOrbit: 225 days\nTemp: 462 °C",
    "Earth": "Earth\nRadius: 6,371 km\nOrbit: 365 days\nTemp: -88 to 58 °C",
    "Mars": "Mars\nRadius: 3,390 km\nOrbit: 687 days\nTemp: -125 to 20 °C",
    "Jupiter": "Jupiter\nRadius: 69,911 km\nOrbit: 11.9 years\nTemp: -145 °C",
    "Saturn": "Saturn\nRadius: 58,232 km\nOrbit: 29 years\nTemp: -178 °C",
    "Uranus": "Uranus\nRadius: 25,362 km\nOrbit: 84 years\nTemp: -224 °C",
    "Neptune": "Neptune\nRadius: 24,622 km\nOrbit: 165 years\nTemp: -214 °C",
    "Moon": "Moon\nRadius: 1,737 km\nOrbit: 27 days\nTemp: -173 to 127 °C",
    "Phobos": "Phobos (Mars)\nRadius: 11 km\nOrbit: 7h 39m",
    "Deimos": "Deimos (Mars)\nRadius: 6 km\nOrbit: 30h 18m",
    "Io": "Io (Jupiter)\nRadius: 1,821 km\nOrbit: 1.8 days\nVolcanically active",
    "Europa": "Europa (Jupiter)\nRadius: 1,560 km\nOrbit: 3.5 days\nSubsurface ocean",
    "Ganymede": "Ganymede (Jupiter)\nRadius: 2,634 km\nOrbit: 7.1 days\nLargest moon",
    "Callisto": "Callisto (Jupiter)\nRadius: 2,410 km\nOrbit: 16.7 days",
    "Titan": "Titan (Saturn)\nRadius: 2,575 km\nOrbit: 15.9 days\nThick atmosphere",
}

# ---------- Image paths dictionary ----------
planet_image_paths = {
    "Mercury": r"C:\Users\TUF\OneDrive\Desktop\project TD\Mercury1.gif",
    "Venus": r"C:\Users\TUF\OneDrive\Desktop\project TD\Venus1.gif",
    "Earth": r"C:\Users\TUF\OneDrive\Desktop\project TD\Earth1.gif",
    "Mars": r"C:\Users\TUF\OneDrive\Desktop\project TD\Mars1.gif",
    "Jupiter": r"C:\Users\TUF\OneDrive\Desktop\project TD\jupiter1.gif",
    "Saturn": r"C:\Users\TUF\OneDrive\Desktop\project TD\saturn1.gif",
    "Uranus": r"C:\Users\TUF\OneDrive\Desktop\project TD\uranus1.gif",
    "Neptune": r"C:\Users\TUF\OneDrive\Desktop\project TD\neptune1.gif",
    "Moon": "moon.gif",
    "Phobos": "phobos.gif",
    "Deimos": "deimos.gif",
    "Io": "io.gif",
    "Europa": "europa.gif",
    "Ganymede": "ganymede.gif",
    "Callisto": "callisto.gif",
    "Titan": "titan.gif",
}
planet_images = {}

# ---------- Classes ----------
class Planet(turtle.Turtle):
    def __init__(self, name, color, semi_major_axis, semi_minor_axis,
                 sim_speed_deg_per_step, angle_offset, image,
                 real_a_km=None, orbit_days=None):
        super().__init__(visible=False)
        self.name = name
        self.sim_speed_base = sim_speed_deg_per_step
        self.angle = angle_offset
        self.semi_major_axis = semi_major_axis
        self.semi_minor_axis = semi_minor_axis
        self.real_a_km = real_a_km
        self.orbit_days = orbit_days

        if self.real_a_km is not None and self.orbit_days is not None:
            self.v_kmh = (2 * math.pi * self.real_a_km) / (self.orbit_days * 24.0)
        else:
            self.v_kmh = None

        try:
            self.shape(image)
        except Exception:
            self.shape("circle")
            self.shapesize(0.6)
        self.color(color)
        self.penup()
        self.speed(0)
        self.showturtle()

        self.name_turtle = turtle.Turtle(visible=False)
        self.name_turtle.hideturtle()
        self.name_turtle.penup()
        self.name_turtle.speed(0)
        self.name_turtle.color("white")

        self.orbit_turtle = turtle.Turtle(visible=False)
        self.orbit_turtle.hideturtle()
        self.orbit_turtle.penup()
        self.orbit_turtle.speed(0)
        self.orbit_turtle.color("darkgrey")
        if show_orbits:
            self.draw_orbit()

        self.moons = []
        # self.onclick(self.show_info)
        self.onclick(lambda x, y: show_body_info(self.name, self.v_kmh, self.orbit_days))

    def draw_orbit(self):
        self.orbit_turtle.clear()
        self.orbit_turtle.penup()
        first = True
        for i in range(361):
            ang = math.radians(i)
            x = self.semi_major_axis * math.cos(ang)
            y = self.semi_minor_axis * math.sin(ang)
            if first:
                self.orbit_turtle.goto(x, y)
                self.orbit_turtle.pendown()
                first = False
            else:
                self.orbit_turtle.goto(x, y)
        self.orbit_turtle.penup()

    def set_orbit_visible(self, visible: bool):
        global show_orbits
        if not visible:
            self.orbit_turtle.clear()
        else:
            self.draw_orbit()

    def set_label_visible(self, visible: bool):
        if not visible:
            self.name_turtle.clear()

    def move(self, speed_mul=1.0):
        step = self.sim_speed_base * speed_mul
        x = self.semi_major_axis * math.cos(math.radians(self.angle))
        y = self.semi_minor_axis * math.sin(math.radians(self.angle))
        self.goto(x, y)

        self.name_turtle.clear()
        if show_labels:
            self.name_turtle.goto(x, y + 12)
            self.name_turtle.write(self.name, align="center", font=("Arial", 9, "normal"))

        for moon in self.moons:
            moon.move(speed_mul)

        self.angle = (self.angle + step) % 360


class Moon(turtle.Turtle):
    def __init__(self, name, parent_planet: Planet, semi_major_axis, semi_minor_axis,
                 sim_speed_deg_per_step, angle_offset, color="lightgrey", size=0.2):
        super().__init__(visible=False)
        self.name = name
        self.parent = parent_planet
        self.semi_major_axis = semi_major_axis
        self.semi_minor_axis = semi_minor_axis
        self.sim_speed_base = sim_speed_deg_per_step
        self.angle = angle_offset

        self.penup()
        self.speed(0)
        self.shape("circle")
        self.shapesize(size)
        self.color(color)
        self.showturtle()

        self.name_turtle = turtle.Turtle(visible=False)
        self.name_turtle.hideturtle()
        self.name_turtle.penup()
        self.name_turtle.speed(0)
        self.name_turtle.color("white")

        self.onclick(lambda x, y: show_body_info(self.name))

    def move(self, speed_mul=1.0):
        parent_x, parent_y = self.parent.position()
        step = self.sim_speed_base * speed_mul
        x_rel = self.semi_major_axis * math.cos(math.radians(self.angle))
        y_rel = self.semi_minor_axis * math.sin(math.radians(self.angle))
        self.goto(parent_x + x_rel, parent_y + y_rel)

        self.name_turtle.clear()
        if show_labels:
            self.name_turtle.goto(parent_x + x_rel, parent_y + y_rel + 8)
            try:
                self.name_turtle.write(self.name, align="center", font=("Arial", 7, "normal"))
            except Exception:
                pass

        self.angle = (self.angle + step) % 360

# ---------- Real orbital data dictionary ----------
A = {
    "Mercury": (57_909_227, 87.969),
    "Venus":   (108_209_475, 224.701),
    "Earth":   (149_598_023, 365.256),
    "Mars":    (227_943_824, 686.980),
    "Jupiter": (778_340_821, 4332.59),
    "Saturn":  (1_426_666_422, 10759),
    "Uranus":  (2_870_658_186, 30687),
    "Neptune": (4_498_396_441, 60190),
}

# ---------- create Sun ----------
sun = turtle.Turtle()
sun.hideturtle()
try:
    sun.shape(sun_image)
except Exception:
    sun.shape("circle")
sun.color("yellow")
sun.shapesize(2.5)
sun.penup()
sun.goto(0, 0)
sun.showturtle()

# ---------- Create planets ----------
mercury = Planet("Mercury", "gray",     60,  42, 4.4,   0,  mercury_path, *A["Mercury"])
venus   = Planet("Venus",   "orange",   95,  70, 3.5,  45,  venus_path,   *A["Venus"])
earth   = Planet("Earth",   "green",   140, 105, 2.8,  90,  earth_path,   *A["Earth"])
mars    = Planet("Mars",    "red",     190, 145, 2.4, 135,  mars_path,    *A["Mars"])
jupiter = Planet("Jupiter", "brown",   260, 200, 1.8, 180,  jupiter_path, *A["Jupiter"])
saturn  = Planet("Saturn",  "yellow",  330, 260, 1.3, 225,  saturn_path,  *A["Saturn"])
uranus  = Planet("Uranus",  "lightblue",400,320, 1.0, 270,  uranus_path,  *A["Uranus"])
neptune = Planet("Neptune", "blue",    470, 360, 0.9, 315,  neptune_path, *A["Neptune"])

planets = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

# ---------- Add moons ----------
earth_moon = Moon("Moon", earth, 20, 16, 8.0, 0, size=0.35)
earth.moons.append(earth_moon)

phobos = Moon("Phobos", mars, 12, 9, 12.0, 10, size=0.12)
deimos = Moon("Deimos", mars, 18, 13, 8.0, 200, size=0.12)
mars.moons += [phobos, deimos]

io = Moon("Io", jupiter, 28, 22, 6.0, 0, size=0.22)
europa = Moon("Europa", jupiter, 40, 34, 4.2, 90, size=0.24)
ganymede = Moon("Ganymede", jupiter, 55, 46, 3.0, 210, size=0.3)
callisto = Moon("Callisto", jupiter, 72, 60, 2.0, 320, size=0.28)
jupiter.moons += [io, europa, ganymede, callisto]

titan = Moon("Titan", saturn, 40, 33, 2.5, 60, size=0.26)
saturn.moons.append(titan)

# ---------- GUI controls ----------
root = screen.getcanvas().winfo_toplevel()

# Info panel (LEFT)
info_frame = tk.Frame(root, bg="white", width=200, height=600)
info_frame.pack(side="left", anchor="n", padx=6, pady=6, fill="y")

info_image_label = tk.Label(info_frame, bg="white")
info_image_label.pack(pady=(10, 5))

info_label = tk.Label(info_frame, text="Click a planet or moon\nfor details",
                      justify="left", anchor="nw", bg="white",
                      font=("Arial", 11), padx=8, pady=8, wraplength=180)
info_label.pack(fill="both", expand=True)

# Control panel (RIGHT)
control_frame = tk.Frame(root)
control_frame.pack(side="right", anchor="n", padx=6, pady=6)

def on_speed_change(val):
    global speed_multiplier
    try:
        speed_multiplier = float(val)
    except:
        speed_multiplier = 1.0

tk.Label(control_frame, text="Simulation speed").pack(anchor="center")
speed_slider = tk.Scale(control_frame, from_=0.1, to=5.0, resolution=0.1,
                        orient="horizontal", length=180, command=on_speed_change)
speed_slider.set(1.0)
speed_slider.pack()

def toggle_pause():
    global paused
    paused = not paused
    pause_btn.config(text="Resume" if paused else "Pause")

pause_btn = tk.Button(control_frame, text="Pause", width=12, command=toggle_pause)
pause_btn.pack(pady=(8, 4))

def toggle_orbits():
    global show_orbits
    show_orbits = not show_orbits
    for p in planets:
        p.set_orbit_visible(show_orbits)
    orbit_btn.config(text="Hide Orbits" if show_orbits else "Show Orbits")

orbit_btn = tk.Button(control_frame, text="Hide Orbits", width=12, command=toggle_orbits)
orbit_btn.pack(pady=4)

def toggle_labels():
    global show_labels
    show_labels = not show_labels
    for p in planets:
        p.set_label_visible(show_labels)
        for m in p.moons:
            m.name_turtle.clear()
    label_btn.config(text="Hide Labels" if show_labels else "Show Labels")

label_btn = tk.Button(control_frame, text="Hide Labels", width=12, command=toggle_labels)
label_btn.pack(pady=4)

def reset_view():
    for p in planets:
        p.angle = 0
        p.draw_orbit() if show_orbits else None
    info_turtle.clear()
    info_turtle.goto(0, -360)
    info_turtle.write("Solar System (click a planet for info)", align="center", font=("Arial", 14, "bold"))
    info_label.config(text="Click a planet\nfor details")

reset_btn = tk.Button(control_frame, text="Reset", width=12, command=reset_view)
reset_btn.pack(pady=(8,0))

# ---------- Shared info display function ----------
def show_body_info(name, v_kmh=None, orbit_days=None):
    # bottom text
    info_turtle.clear()
    info_turtle.goto(0, -360)
    if v_kmh is not None and orbit_days is not None:
        msg = f"{name} → {v_kmh:,.0f} km/h | Orbit: {orbit_days:,} days"
    else:
        msg = f"{name}"
    info_turtle.write(msg, align="center", font=("Arial", 14, "bold"))

    # left text
    details = planet_details.get(name, "No details available.")
    info_label.config(text=details)

    # left image
    path = planet_image_paths.get(name)
    if path and os.path.exists(path):
        if name not in planet_images:
            try:
                img = Image.open(path).resize((120, 120))
                planet_images[name] = ImageTk.PhotoImage(img)
            except Exception:
                planet_images[name] = None
        if planet_images[name]:
            info_image_label.config(image=planet_images[name], text="")
            info_image_label.image = planet_images[name]
        else:
            info_image_label.config(image="", text=f"[No image for {name}]")
    else:
        info_image_label.config(image="", text=f"[No image for {name}]")

# ---------- animation update ----------
def update():
    if not paused:
        for p in planets:
            p.move(speed_mul=speed_multiplier)
        screen.update()
    screen.ontimer(update, update_interval_ms)

for p in planets:
    if show_orbits:
        p.draw_orbit()

update()
turtle.done()
