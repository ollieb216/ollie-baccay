from shiny import App, ui, render, reactive


# Life insurance premium calculation function
def calculate_premium(age, death_benefit, loading=0.2):
    prob_death = 0.001 * (age / 30)
    expected_cost = prob_death * death_benefit
    premium = expected_cost * (1 + loading)
    return round(premium, 2)


# UI: inputs and output
app_ui = ui.page_fluid(
    ui.input_slider("age", "Age:", min=18, max=80, value=30),
    ui.input_numeric("benefit", "Death Benefit ($):", value=100000, step=1000),
    ui.output_text_verbatim("premium")
)


# Server logic
def server(input, output, session):
    @reactive.Calc
    def premium_value():
        return calculate_premium(input.age(), input.benefit())

    @output
    @render.text
    def premium():
        return f"Estimated Annual Premium: ${premium_value()}"


# Create app
app = App(app_ui, server)