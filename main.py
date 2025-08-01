# ======== IMPORTS ========
import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

# ======== GLOBAL VARIABLES ========
api_key = "470b42ce0d46d2fc5ccbd150f33aa4c9"  # <-- Replace with your API Key
last_weather = {}

# ======== GET WEATHER FUNCTION ========
def get_weather():
    city = entry.get()

    if not city:
        messagebox.showwarning("Missing Input", "Please enter a city name.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            messagebox.showerror("Error", f"City '{city}' not found.")
            return

        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"]
        icon_code = data["weather"][0]["icon"]

        # Update text result
        result_label.config(
            text=f"📍 {city.title()}\n\n🌡 Temp: {temp}°C\n💧 Humidity: {humidity}%\n☁️ Condition: {condition.title()}"
        )

        # Show weather icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_data = requests.get(icon_url).content
        image = Image.open(BytesIO(icon_data))
        icon = ImageTk.PhotoImage(image)
        icon_label.config(image=icon)
        icon_label.image = icon  # Prevent garbage collection

        # Store last data for export
        global last_weather
        last_weather = {
            "city": city,
            "temp": temp,
            "humidity": humidity,
            "condition": condition
        }

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ======== EXPORT FUNCTION ========
def export_report():
    if last_weather:
        city = last_weather["city"]
        temp = last_weather["temp"]
        humidity = last_weather["humidity"]
        condition = last_weather["condition"]

        filename = f"{city}_weather_report.txt"
        with open(filename, "w") as f:
            f.write(f"Weather Report for {city.title()}\n")
            f.write("-------------------------------\n")
            f.write(f"Temperature: {temp}°C\n")
            f.write(f"Humidity: {humidity}%\n")
            f.write(f"Condition: {condition.title()}\n")

        messagebox.showinfo("Exported", f"Report saved as '{filename}'")
    else:
        messagebox.showwarning("No Data", "Please get weather info first.")

# ======== GUI SETUP ========
root = tk.Tk()
root.title("Weather Dashboard")
root.geometry("370x460")
root.configure(bg="#f0faff")
root.resizable(False, False)

# Title
tk.Label(root, text="🌤 Weather Dashboard", font=("Helvetica", 16, "bold"), bg="#f0faff", fg="#0d47a1").pack(pady=10)

# Entry
entry = tk.Entry(root, font=("Arial", 12), width=30)
entry.pack(pady=5)

# Get Weather Button
tk.Button(root, text="Get Weather", command=get_weather, font=("Arial", 11), bg="#4CAF50", fg="white").pack(pady=10)

# Result Label
result_label = tk.Label(root, text="", bg="#f0faff", font=("Arial", 12), justify="left")
result_label.pack(pady=10)

# Weather Icon
icon_label = tk.Label(root, bg="#f0faff")
icon_label.pack()

# Export Button
tk.Button(root, text="Export Report", command=export_report, font=("Arial", 11), bg="#2196F3", fg="white").pack(pady=15)

# Start App
root.mainloop()
