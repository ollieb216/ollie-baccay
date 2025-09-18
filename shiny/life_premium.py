from shiny import App, ui, render, reactive
import numpy as np


# Life insurance premium calculation function
def calculate_premium(age, death_benefit, bmi, sex, nicotine, health, loading=0.2):
    prob_death = 0.001 * (age / 30)

    if sex=='Male':
        prob_death *=1.1

    if 40 > bmi >= 30:
        prob_death *= 1.3  # higher risk if obese
    elif bmi < 18.5:
        prob_death *= 1.1  # slightly higher risk if underweight
    elif bmi >= 40:
        prob_death *= 1.7 # higher risk if majorly obese

    if health == 'aboveavghealthy':
        prob_death *= 0.97
    elif health == 'belowavghealthy':
        prob_death *= 1.07

    if nicotine=='Cigarettes':
        prob_death *=2
    elif nicotine=='Occasional':
        prob_death *=1.1
    elif nicotine=='vaping':
        prob_death *=1.3


    expected_cost = prob_death * death_benefit
    premium = expected_cost * (1 + loading)
    return round(premium, 2)

# UI: inputs and output
height_options = {
    56: "4'8\"", 57: "4'9\"", 58: "4'10\"", 59: "4'11\"",
    60: "5'0\"", 61: "5'1\"", 62: "5'2\"", 63: "5'3\"", 64: "5'4\"", 65: "5'5\"",
    66: "5'6\"", 67: "5'7\"", 68: "5'8\"", 69: "5'9\"", 70: "5'10\"", 71: "5'11\"",
    72: "6'0\"", 73: "6'1\"", 74: "6'2\"", 75: "6'3\"", 76: "6'4\"", 77: "6'5\"",
    78: "6'6\"", 79: "6'7\"", 80: "6'8\"", 81: "6'9\"", 82: "6'10\"", 83: "6'11\""
}
db_options = {250000:"$250,000", 500000:"$500,000", 1000000:"$1,000,000",
              2000000:"$2,000,000", 5000000:"$5,000,000",10000000:"$10,000,000"}
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h4("Get a term life insurance quote:"),
        ui.input_select("gender", "Sex assigned at birth:", {"Male": "Male", "Female": "Female"}),
        ui.input_slider("age", "Age:", min=18, max=75, value=30),
        ui.input_slider("weight", "Weight (lbs):", min=50, max=450, value=150, step=1),
        ui.input_select("height", "Height", height_options, selected=67),
        ui.input_select("health", "How would you generally rate your health?",
                        {"aboveavghealthy":"Above Average", 'avghealthy':"Average", "belowavghealthy": "Below Average"}, selected='avghealthy'),
        ui.input_select(
            "nicotine", "Nicotine/tobacco usage?",
            {"No": "No", "Cigarettes": "Regular Smoker", "Occasional": "Occasional Smoker",
             "vaping": "Chewing Tobacco/Vaping"}
        ),
        ui.input_select("benefit", "Death Benefit:", db_options, selected=1000000),
        width=425
    ),
    ui.div(
        ui.h4("Here’s what term life might cost"),
        ui.output_text_verbatim("premium"),
        style="background-color: lightgrey; min-height: 10vh; padding: 305px;"
    )
)


# Server logic
def server(input, output, session):
    @reactive.Calc
    def bmi_value():
        weight = input.weight()
        height = int(input.height())  # inches
        if height > 0:
            return round((weight / (height * height)) * 703, 1)
        return 0

    @reactive.Calc
    def premium_value():
        return calculate_premium(input.age(), int(input.benefit()),
                                 bmi_value(), input.gender(), input.nicotine(),
                                 input.health())

    @output
    @render.text
    def premium():
        return f"Estimated Monthly Premium: ${np.round(premium_value()/12,2)}\nEstimated Annual Premium: ${premium_value()}"


app = App(app_ui, server)
