import requests
import matplotlib.pyplot as plt
from datetime import datetime

# Feste Koordinaten für Kabul
#latitude = 34.5553
#longitude = 69.2075

city = input("city name: ")
timezone = input("timezone: ")
latitude = float(input("Latitude: "))
longitude = float(input("longitude: "))

# API-Request für Wetterdaten
weather_url = "https://archive-api.open-meteo.com/v1/archive"
params = {
    'latitude': latitude,
    'longitude': longitude,
    'start_date': '2024-01-01',
    'end_date': '2024-12-31',
    'daily': ['temperature_2m_max', 'temperature_2m_min', 'precipitation_sum'],
    'timezone': timezone
}

response = requests.get(weather_url, params=params)

if response.status_code == 200:
    weather_data = response.json()

    # Daten extrahieren
    dates = weather_data['daily']['time']
    temp_max = weather_data['daily']['temperature_2m_max']
    temp_min = weather_data['daily']['temperature_2m_min']
    precipitation = weather_data['daily']['precipitation_sum']

    # Monate initialisieren
    monate = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monatliche_temp_max = {monat: [] for monat in monate}
    monatliche_temp_min = {monat: [] for monat in monate}
    monatlicher_niederschlag = {monat: 0 for monat in monate}

    # Daten den Monaten zuordnen
    for i in range(len(dates)):
        monat = datetime.strptime(dates[i], "%Y-%m-%d").strftime("%b")
        monatliche_temp_max[monat].append(temp_max[i])
        monatliche_temp_min[monat].append(temp_min[i])
        monatlicher_niederschlag[monat] += precipitation[i]

    # Monatsdurchschnitt berechnen
    temp_max_avg = [sum(monatliche_temp_max[m]) / len(monatliche_temp_max[m]) if monatliche_temp_max[m] else 0 for m in monate]
    temp_min_avg = [sum(monatliche_temp_min[m]) / len(monatliche_temp_min[m]) if monatliche_temp_min[m] else 0 for m in monate]
    niederschlag_sum = [monatlicher_niederschlag[m] for m in monate]

    # **Jahresdurchschnitt berechnen**
    jahresmittel_temp = (sum(temp_max_avg) + sum(temp_min_avg)) / (2 * len(monate))
    jahressumme_niederschlag = sum(niederschlag_sum)

    # **Größere Figur für mehr Platz**
    fig, axs = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [2.5, 1]})  

    # Diagramm auf der linken Seite
    ax1 = axs[0]
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Temperature (°C)", color="red")
    ax1.plot(monate, temp_max_avg, color="red", marker="o", label="Max. Temperature", linestyle="--")
    ax1.plot(monate, temp_min_avg, color="orange", marker="o", label="Min. Temperature", linestyle="--")
    ax1.tick_params(axis="y", labelcolor="red")
    ax1.legend(loc="upper left")

    # Zweite Achse für Niederschlag
    ax2 = ax1.twinx()
    ax2.set_ylabel("Precipitation (mm)", color="blue")
    ax2.bar(monate, niederschlag_sum, color="blue", alpha=0.5, label="Precipitation")
    ax2.tick_params(axis="y", labelcolor="blue")
    ax2.legend(loc="upper right")

    # Gemeinsame Skala für Temperatur & Niederschlag
    ax1.set_ylim(min(temp_min_avg) - 5, max(temp_max_avg) + 5)
    ax2.set_ylim(0, max(niederschlag_sum) * 1.2)

    # Gitternetz & Hilfslinien
    ax1.grid(True, linestyle="--", alpha=0.6)

    # **Tabelle auf der rechten Seite (eigene Achse)**
    ax_table = axs[1]
    ax_table.axis("off")  # Achsen unsichtbar machen

    # Tabelleninhalt
    table_data = [[monate[i], f"{temp_max_avg[i]:.1f}°C", f"{temp_min_avg[i]:.1f}°C", f"{niederschlag_sum[i]:.1f} mm"] for i in range(12)]

    # Tabelle in die Achse setzen
    table = ax_table.table(cellText=table_data,
                           colLabels=["Month", "Max Temp", "Min Temp", "Precipitation"],
                           cellLoc="center",
                           loc="center",
                           colColours=["lightgray"]*4)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)  # Tabelle etwas größer machen

    

    # Diagramm speichern
    plt.suptitle(f"Climadiagramm for {city} (2024) \n")
    plt.tight_layout()
    plt.savefig(f"Climadiagramm_{city}.jpg", dpi=300)
    plt.show()

    print("✅ Diagramm gespeichert als Klimadiagramm_Kabul_mit_Tabelle_und_Summary.jpg")

else:
    print(f"❌ Fehler: Konnte Wetterdaten nicht abrufen (Status-Code {response.status_code})")
