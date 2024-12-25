import taipy as tp
import taipy.gui.builder as tgb
import pandas as pd
from taipy import Config, Scope, Gui
from src.simulations.owning_renting import simulate_returns, calc_mortgage_payment
from src.visual.plots import prepare_networths_chart

def init_simulation(
    interest_rate,
    house_cost,
    rent,
    maintenance,
    down_payment,
    house_appreciation,
    stocks_returns,
    loan_duration,
) -> pd.DataFrame:
    output_df = simulate_returns(
        interest_rate/100,
        house_cost,
        rent,
        maintenance,
        down_payment/100,
        house_appreciation/100,
        stocks_returns/100,
        loan_duration,
        loan_duration+10
    )
    return output_df

def on_values_updated(
    state
) -> pd.DataFrame():
    state.simulation = simulate_returns(
        state.interest_rate/100,
        state.house_cost,
        state.rent,
        state.maintenance,
        state.down_payment/100,
        state.house_appreciation/100,
        state.stocks_returns/100,
        state.loan_duration,
        state.loan_duration+10
    )
    mortgage_updated(state)

def mortgage_updated(
    state
):
    state.mortgage = calc_mortgage_payment(state.house_cost*(1-state.down_payment/100), state.loan_duration, state.interest_rate/100)
    state.total_owning_cost = state.mortgage + state.maintenance
    state.investing = state.total_owning_cost - state.rent


interest_rate = 3.27
house_cost = 469400
rent = 1290
maintenance = 320.35
down_payment = 10
house_appreciation = 2.5
stocks_returns = 7
loan_duration = 30
years_to_simulate = loan_duration + 10
mortgage = calc_mortgage_payment(
    house_cost*(1-down_payment/100),
    loan_duration,
    interest_rate/100
)
total_owning_cost = mortgage + maintenance
investing = total_owning_cost - rent
simulation = init_simulation(
    interest_rate,
    house_cost,
    rent,
    maintenance,
    down_payment,
    house_appreciation,
    stocks_returns,
    loan_duration,
)
markdown_intro = """
## Key assumptions
- Euribor / interest rates stay constant during the simulation.
- All rates (i.e. stock market returns and house appreciation) are inflation adjusted. This means that all net
    worth values are in today's euros.
- As a consequence of the previous one: rents are raised based on inflation level.
- All expences for both rening and owning are constant (only affected by inflation level).
- Mortgage repayment type is annuity (equal payments) - the most common one.
## Simulation description
- Simulation shows net worth fow owning housing vs renting over time.
- In case of owning, net worth is calculated as <current house price> - <loan left>. 
After the loan is fully repaid the mortgage payments go toward investing into the stock market with the same return as in renting case.
- In case of renting, the initial downpayment is invested into the stock market as a lump sum. Then the difference between 
<mortgage payment> + <maintenance> and <rent> is invested monthly into the stock market.
- The simulation continues for 10 years after the full loan repayment. 
"""
calculated_parameters = """
- __Mortgage payment__ = {mortgage} Eur
- __Total ownership monthly cost__ = {total_owning_cost:.2f} Eur
- __Monthly investments while rening__ = {investing:.2f} Eur
"""
with tgb.Page() as page:
    tgb.text(value="# Renting vs owning calculator", mode="markdown")
    with tgb.expandable(title="Key assumptions and description", expanded=True):
        tgb.text("{markdown_intro}" ,mode="markdown")
    with tgb.layout(columns="4*1"):
        tgb.number(value="{house_cost}", label="House price [Eur]", on_change=on_values_updated, step=1000)
        tgb.number(value="{maintenance}", label="Maintenance cost [Eur]", on_change=on_values_updated, step=10)
        tgb.number(value="{down_payment}", label="Downpayment [%]", on_change=on_values_updated, step=1)
        tgb.number(value="{house_appreciation}", label="Expected house appreciation [%]", on_change=on_values_updated, step=0.1)
        tgb.number(value="{interest_rate}", label="Loan interest rate [%]", on_change=on_values_updated, step=0.1)
        tgb.number(value="{loan_duration}", label="Loan duration [years]", on_change=on_values_updated, step=1)
        tgb.number(value="{rent}", label="Comparable rent [Eur]", on_change=on_values_updated, step=100)
        tgb.number(value="{stocks_returns}", label="Expected stock market returns [%]", on_change=on_values_updated, step=0.1)
    with tgb.expandable(title="Calculated parameters", expanded=True):
        tgb.text("__Mortgage payment__ = {mortgage:.2f} Eur", mode="markdown" )
        tgb.text("__Total ownership monthly cost__ = {total_owning_cost:.2f} Eur", mode="markdown")
        tgb.text("__Monthly investments while renting__ = {investing:.2f} Eur", mode="markdown")
    tgb.chart(figure=lambda simulation: prepare_networths_chart(simulation))

if __name__ == "__main__":
    Gui(page=page).run(debug=True, use_reloader=True, title="Renting/Owning calc", port=3333)