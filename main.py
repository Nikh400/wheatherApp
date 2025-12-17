from tkinter import *
import tkinter as tk
from tkinter import messagebox
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz
import os

# ------------------ PATH SETUP ------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_image(name):
    try:
        return PhotoImage(file=os.path.join(BASE_DIR, name))
    except:
        return None

# ------------------ MAIN WINDOW ------------------
root = Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False, False)

# ------------------ WEATHER FUNCTION ------------------
def getweather():
    try:
        city = textfield.get().strip()
        if not city:
            raise Exception("City name cannot be empty")

        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city)
        if location is None:
            raise Exception("City not found")

        tf = TimezoneFinder()
        timezone = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        home = pytz.timezone(timezone)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")

        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")

        API_KEY = "caa81fee8a05114d79df4a4e7f553b3e"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

        json_data = requests.get(url).json()
        if json_data.get("cod") != 200:
            raise Exception(json_data.get("message"))

        condition = json_data["weather"][0]["description"].title()
        temp = int(json_data["main"]["temp"] - 273.15)

        t.config(text=f"{temp}°")
        c.config(text=f"{condition} | FEELS LIKE {temp}°")
        w.config(text=f"{json_data['wind']['speed']} m/s")
        h.config(text=f"{json_data['main']['humidity']}%")
        d.config(text=condition)
        p.config(text=f"{json_data['main']['pressure']} hPa")

    except Exception as e:
        messagebox.showerror("Weather App", str(e))

# ------------------ SEARCH BOX ------------------
search_image = load_image("search.png")
if search_image:
    search_label = Label(root, image=search_image)
    search_label.image = search_image
else:
    search_label = Label(root, text="Search", font=("Arial", 20))

search_label.place(x=20, y=20)

textfield = Entry(
    root,
    justify="center",
    width=17,
    font=("Poppins", 25, "bold"),
    bg="#404040",
    border=0,
    fg="white"
)
textfield.place(x=50, y=40)
textfield.focus()

search_icon = load_image("search_icon.png")
search_btn = Button(
    root,
    image=search_icon if search_icon else None,
    text="🔍" if not search_icon else "",
    borderwidth=0,
    cursor="hand2",
    bg="#404040",
    command=getweather
)
search_btn.image = search_icon
search_btn.place(x=400, y=34)

# ------------------ LOGO ------------------
logo_img = load_image("logo.png")
logo = Label(root, image=logo_img if logo_img else None)
logo.image = logo_img
logo.place(x=150, y=100)

# ------------------ BOTTOM FRAME ------------------
box_img = load_image("box.png")
frame = Label(root, image=box_img if box_img else None)
frame.image = box_img
frame.pack(side=BOTTOM, pady=5)

# ------------------ TIME ------------------
name = Label(root, font=("Arial", 15, "bold"))
name.place(x=30, y=100)

clock = Label(root, font=("Helvetica", 20))
clock.place(x=30, y=130)

# ------------------ LABELS ------------------
Label(root, text="WIND", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef").place(x=120, y=400)
Label(root, text="HUMIDITY", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef").place(x=250, y=400)
Label(root, text="DESCRIPTION", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef").place(x=430, y=400)
Label(root, text="PRESSURE", font=("Helvetica", 15, "bold"), fg="white", bg="#1ab5ef").place(x=650, y=400)

# ------------------ WEATHER DATA ------------------
t = Label(root, font=("Arial", 70, "bold"), fg="#ee666d")
t.place(x=400, y=150)

c = Label(root, font=("Arial", 15, "bold"))
c.place(x=400, y=250)

w = Label(root, text="...", font=("Arial", 20, "bold"), bg="#1ab5ef")
w.place(x=120, y=430)

h = Label(root, text="...", font=("Arial", 20, "bold"), bg="#1ab5ef")
h.place(x=280, y=430)

d = Label(root, text="...", font=("Arial", 20, "bold"), bg="#1ab5ef")
d.place(x=450, y=430)

p = Label(root, text="...", font=("Arial", 20, "bold"), bg="#1ab5ef")
p.place(x=670, y=430)

# ------------------ RUN ------------------
root.mainloop()
