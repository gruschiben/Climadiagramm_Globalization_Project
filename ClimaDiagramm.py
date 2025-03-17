import requests
import argparse
import matplotlib.pyplot as plt
from datetime import datetime#


PROGRAMM_VERSION = "1.0.0"

parser = argparse.ArgumentParser(description="A Script to Create an Climadiagramm.")


parser.add_argument(
    '--version', 
    action='version', 
    version=f'%(prog)s {PROGRAMM_VERSION}', 
    help="Programm version."
)


args = parser.parse_args()
print(PROGRAMM_VERSION)


city = input("city name: ")
timezone = input("timezone: ")
latitude = float(input("Latitude: "))
longitude = float(input("longitude: "))

# API-Request for Weather Data
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

    # extract Data from the API request
    dates = weather_data['daily']['time']
    temp_max = weather_data['daily']['temperature_2m_max']
    temp_min = weather_data['daily']['temperature_2m_min']
    precipitation = weather_data['daily']['precipitation_sum']

    # Initialize months
    monate = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monatliche_temp_max = {monat: [] for monat in monate}
    monatliche_temp_min = {monat: [] for monat in monate}
    monatlicher_niederschlag = {monat: 0 for monat in monate}

    # Assign data to the months
    for i in range(len(dates)):
        monat = datetime.strptime(dates[i], "%Y-%m-%d").strftime("%b")
        monatliche_temp_max[monat].append(temp_max[i])
        monatliche_temp_min[monat].append(temp_min[i])
        monatlicher_niederschlag[monat] += precipitation[i]

    # Calculate monthly average
    temp_max_avg = [sum(monatliche_temp_max[m]) / len(monatliche_temp_max[m]) if monatliche_temp_max[m] else 0 for m in monate]
    temp_min_avg = [sum(monatliche_temp_min[m]) / len(monatliche_temp_min[m]) if monatliche_temp_min[m] else 0 for m in monate]
    niederschlag_sum = [monatlicher_niederschlag[m] for m in monate]

    # **Calculate annual average (Currently not needed)**
    #jahresmittel_temp = (sum(temp_max_avg) + sum(temp_min_avg)) / (2 * len(monate))
    #jahressumme_niederschlag = sum(niederschlag_sum)

    # **Larger figure for more space**
    fig, axs = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={'width_ratios': [2.5, 1]})  

    # Diagramm on the left side
    ax1 = axs[0]
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Temperature (°C)", color="red")
    ax1.plot(monate, temp_max_avg, color="red", marker="o", label="Max. Temperature", linestyle="--")
    ax1.plot(monate, temp_min_avg, color="orange", marker="o", label="Min. Temperature", linestyle="--")
    ax1.tick_params(axis="y", labelcolor="red")
    ax1.legend(loc="upper left")

    # Second axis for precipitation
    ax2 = ax1.twinx()
    ax2.set_ylabel("Precipitation (mm)", color="blue")
    ax2.bar(monate, niederschlag_sum, color="blue", alpha=0.5, label="Precipitation")
    ax2.tick_params(axis="y", labelcolor="blue")
    ax2.legend(loc="upper right")

    # Common scale for temperature & precipitation
    ax1.set_ylim(min(temp_min_avg) - 5, max(temp_max_avg) + 5)
    ax2.set_ylim(0, max(niederschlag_sum) * 1.2)

    # Grid &amp; Guide lines
    ax1.grid(True, linestyle="--", alpha=0.6)

    # **Table on the right-hand side (own axis)**
    ax_table = axs[1]
    ax_table.axis("off")  # Make axes invisible

    
    # Tabell content
    table_data = [[monate[i], f"{temp_max_avg[i]:.1f}°C", f"{temp_min_avg[i]:.1f}°C", f"{niederschlag_sum[i]:.1f} mm"] for i in range(12)]

    # Set table in the axis
    table = ax_table.table(cellText=table_data,
                           colLabels=["Month", "Max Temp", "Min Temp", "Precipitation"],
                           cellLoc="center",
                           loc="center",
                           colColours=["lightgray"]*4)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)  #
    

    # save diagramm
    plt.suptitle(f"Climadiagramm for {city} (2024) \n")
    plt.tight_layout()
    plt.savefig(f"Climadiagramm_{city}.jpg", dpi=300)
    plt.show()

    print(f"Save File as climadiagramm_{city}.jpg")

else:
    print(f"Error: Could not retrieve weather data (Status-code {response.status_code}) ")
