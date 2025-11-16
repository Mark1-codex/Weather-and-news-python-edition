import flet as ft
import requests
import pycountry
import random
import os

def main(page: ft.Page):
    page.title = "Weather searching app"
    page.theme_mode = ft.ThemeMode.DARK

    # ----- Title -----
    titleWeatherText = ft.Text(
        value="Weather dashboard",
        color="#FFFFFF",
        weight="bold",
        size=20
    )
    desc = ft.Text(
        value="Always be aware of weather\nin your region",
        text_align=ft.TextAlign.CENTER,
        weight="semibold"
    )
    titleWeatherContainer = ft.Container(
        content=ft.Column(spacing=10, controls=[titleWeatherText, desc]),
        alignment=ft.alignment.center
    )

    # ----- Region input -----
    regionInput = ft.TextField(label="Enter your region")

    # ----- Weather data output -----
    cityD = ft.Text(value="City", size=14)
    tempD = ft.Text(value="Temperature", size=14)
    feelsD = ft.Text(value="Feels like", size=14, text_align=ft.TextAlign.CENTER)
    humidityD = ft.Text(value="Humidity", size=10)
    mainwD = ft.Image(width=100, height=100)

    tempData = ft.Column(spacing=5, controls=[tempD, feelsD], alignment=ft.alignment.center)

    dataReturn = ft.Container(
        content=ft.Column(
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[mainwD, cityD, tempData, humidityD],
        ),
        alignment=ft.alignment.center,
        bgcolor="#263238",
        padding=20,
        border_radius=10,
        visible=False,
        width=320,
    )

    # ----- Forecast -----
    forecastTitle = ft.Text(value="5-day Forecast", size=16, weight="bold", color="#FFFFFF")
    forecastRow = ft.Row(scroll=ft.ScrollMode.ALWAYS, spacing=10)

    forecastContainer = ft.Container(
        content=ft.Column(
            controls=[forecastTitle, forecastRow],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        visible=False,
        width=350,
    )

    # ----- Weather API update -----
    def dataUpdate(e):
        apiKey = "a947a90ddd9465d09a1f1f6008351d94"
        CITY = regionInput.value

        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={apiKey}&units=metric"
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={apiKey}&units=metric"

        response = requests.get(url)
        forecast_response = requests.get(forecast_url)

        if response.status_code == 200:
            data = response.json()

            city = data["name"]
            temp = data["main"]["temp"]
            feels = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            icon_code = data["weather"][0]["icon"]

            dataReturn.visible = True
            cityD.value = f"City: {city}"
            tempD.value = f"Temperature: {int(temp)}℃"
            feelsD.value = f"Feels like: {int(feels)}℃"
            humidityD.value = f"Humidity: {humidity}%"
            mainwD.src = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

            # Forecast
            if forecast_response.status_code == 200:
                forecast_data = forecast_response.json()
                forecastRow.controls.clear()

                for i in range(0, len(forecast_data["list"]), 8):
                    item = forecast_data["list"][i]
                    dt_txt = item["dt_txt"].split(" ")[0]
                    temp = int(item["main"]["temp"])
                    icon = item["weather"][0]["icon"]

                    forecastCard = ft.Container(
                        content=ft.Column(
                            spacing=5,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Text(value=dt_txt, size=10, color="#FFFFFF"),
                                ft.Image(
                                    src=f"https://openweathermap.org/img/wn/{icon}.png",
                                    width=50,
                                    height=50,
                                ),
                                ft.Text(
                                    value=f"{temp}℃",
                                    size=12,
                                    color="#FFFFFF",
                                    weight="bold"
                                ),
                            ],
                        ),
                        bgcolor="#37474F",
                        padding=10,
                        border_radius=10,
                        width=80
                    )
                    forecastRow.controls.append(forecastCard)

                forecastContainer.visible = True

            page.update()

        else:
            dataReturn.visible = False
            forecastContainer.visible = False
            page.update()

    sendRegionButton = ft.ElevatedButton("Ok", on_click=dataUpdate)

    interractionContainer = ft.Container(
        content=ft.Column(controls=[regionInput, sendRegionButton]),
        alignment=ft.alignment.center
    )

    weatherStructure = ft.Column(
        spacing=40,
        controls=[titleWeatherContainer, interractionContainer, dataReturn, forecastContainer],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # ----- NEWS SECTION -----
    newsTitle = ft.Text(value="Top headlines today", weight="bold", size=20)
    newsDesc = ft.Text(value="View todays headlines\nto get information", text_align=ft.TextAlign.CENTER)
    newsTitleContainer = ft.Container(
        content=ft.Column(
            controls=[newsTitle, newsDesc],
        ),
        alignment=ft.alignment.center
    )

    newsInput = ft.TextField(label="Enter your city")

    titleND = ft.Text("Title", weight="semibold", size=15)
    descND = ft.Text("Description", size=10)
    photoCont = ft.Image(width=200, height=100)
    moreDataND = ft.Text(
        spans=[ft.TextSpan("Click for more info",
                           style=ft.TextStyle(color=ft.Colors.BLUE,
                                              decoration=ft.TextDecoration.UNDERLINE))]
    )

    newsDataReturn = ft.Container(
        content=ft.Column(
            controls=[titleND, descND, photoCont, moreDataND],
            alignment=ft.alignment.center,
        ),
        alignment=ft.alignment.center,
        width=250,
        height=350,
        padding=20,
        border_radius=10,
        bgcolor="#263268",
        visible=False,
    )
    newsCardContainer = ft.Container(
        content=newsDataReturn,
        alignment=ft.alignment.center,
    )
    # ----- NEWS API -----
    def newsUpdate(e):

        def countrynametocode(countryname):
            try:
                result = pycountry.countries.search_fuzzy(countryname)[0]
                return result.alpha_2.lower()
            except:
                return None

        def searchnews():
            if not newsInput.value:
                newsInput.label = "Enter your country first!"
                page.update()
                return

            countryToSearch = countrynametocode(newsInput.value.lower())

            if not countryToSearch:
                newsInput.label = "Invalid country name!"
                newsDataReturn.visible = False
                page.update()
                return

            API_KEY = "7d4815f8aa5a772ed3d154e769483231"
            api_link = "http://api.mediastack.com/v1/news"

            params = {
                "access_key": API_KEY,
                "countries": countryToSearch,
                "limit": 50,
            }

            response = requests.get(api_link, params=params)
            data = response.json()

            if "error" in data:
                newsDataReturn.visible = False
                page.update()
                return

            existingArticles = data["pagination"]["total"]

            if existingArticles == 0:
                newsInput.label = "No news found!"
                newsDataReturn.visible = False
                page.update()
                return

            showedArticleIndex = random.randint(0, data["pagination"]["count"] - 1)
            article = data["data"][showedArticleIndex]

            titleND.value = article.get("title", "No title available")
            descND.value = article.get("description", "No description available")
            photoCont.src = article.get("image", "https://png.pngtree.com/png-vector/20221125/ourmid/pngtree-no-image-available-icon-flatvector-illustration-pic-design-profile-vector-png-image_40966566.jpg")
            newsDataReturn.visible = True

            moreDataND.spans = [
                ft.TextSpan(
                    "Click for more info",
                    ft.TextStyle(color=ft.Colors.BLUE,
                                 decoration=ft.TextDecoration.UNDERLINE),
                    url=article.get("url", "")
                )
            ]

            page.update()

        searchnews()

    sendCountryButton = ft.ElevatedButton("Search for news", on_click=newsUpdate)

    newsInterractionContainer = ft.Container(
        content=ft.Column(controls=[newsInput, sendCountryButton], spacing=10)
    )

    newsStructure = ft.Container(
        content=ft.Column(
            controls=[newsTitleContainer, newsInterractionContainer, newsDataReturn],
            spacing=20
        ),
        alignment=ft.alignment.center,
    )
    # ----- Signature generator -----
    page.assets_dir = "assets"

    font_path = os.path.join(page.assets_dir, "./DancingScript-Regular.ttf")

    if not os.path.exists(font_path):
        print("❌ ERROR: Font file not found:", font_path)
    else:
        page.fonts = {
            "MyCustomFont": font_path
        }

    name_input = ft.TextField(
        label="Введіть ваше ім’я",
        hint_text="Наприклад: Олександр",
        autofocus=True,
        width=350,
        text_size=16,
    )

    signature_text = ft.Text(
        "",
        size=48,
        weight=ft.FontWeight.W_600,
        italic=True,
        text_align=ft.TextAlign.CENTER,
        font_family="MyCustomFont",
    )

    subtitle = ft.Text(
        "Натисніть кнопку, щоб згенерувати підпис",
        size=12,
        opacity=0.7,
        text_align=ft.TextAlign.CENTER,
    )

    def generate_signature(e):
        name = name_input.value.strip()
        if not name:
            signature_text.value = ""
            subtitle.value = "Будь ласка, введіть ім’я 🙂"
        else:
            signature_text.value = name
            subtitle.value = "Ваш підпис готовий ✨"
        page.update()

    generate_button = ft.ElevatedButton(
        text="Згенерувати підпис",
        on_click=generate_signature,
        width=200,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=20),
        ),
    )
    fontGeneratorContainer = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("Генератор підпису", size=26, weight=ft.FontWeight.BOLD),
                name_input,
                generate_button,
                ft.Divider(),
                subtitle,
                signature_text,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        )
    )
    # ----- Final page layout -----
    page.add(
        ft.Column(
            controls=[weatherStructure, newsStructure, fontGeneratorContainer],
            scroll="always",
            expand=True
        )
    )


ft.app(target=main)