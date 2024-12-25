import pandas as pd
import math
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

INTEREST_RATE = 0.02461+0.005
HOUSE_COST = 469400
RENT = 1290
MAINTENANCE = 320.35
DOWN_PAYMENT = 0.1
HOUSE_APPRECIATION = 0.025
STOCKS_RETURNS = 0.07
LOAN_DURATION = 30
YEARS_TO_SIMULATE = LOAN_DURATION+10

def calc_mortgage_payment(size: float, duration: float, interest_rate: float) -> float:
   """
   :param size : loan size
   :param duration : loan duration in years
   :param interest_rate : interest rate as fraction
   :return: monthly payment
   """
   P = (interest_rate * duration) / (1 - math.exp(-interest_rate*duration))
   base_payment = size/(duration*12)
   return P*base_payment

def calc_principal_left(duration: float, interest_rate: float, payments_done: int) -> float:
    """
    :param duration: loan duration in years
    :param interest_rate: interest rate as fraction
    :param payments_done: number of payments done
    :return: proportion of owed principal (does not count downpayment)
    """
    return (1 - math.exp(-interest_rate*(duration - payments_done/12)))/(1 - math.exp(-interest_rate*duration))

def simulate_returns(
        interest_rate: float,
        house_cost: float,
        rent: float,
        maintenance: float,
        down_payment: float,
        house_appreciation: float,
        stock_returns: float,
        loan_duration: float,
        years_to_simulate: float,
) -> pd.DataFrame:
    output_df = pd.DataFrame(columns=["investments", "house_net", "house_price", "loan_left", "investments_owning"], index=list(range(int(years_to_simulate)*12 + 1)))
    output_df = output_df.astype(float)
    output_df = output_df.fillna(0.0)
    initial_capital = house_cost*down_payment
    monthly_payment = calc_mortgage_payment(house_cost-initial_capital, loan_duration, interest_rate)
    total_ownership_expences = monthly_payment + maintenance
    monthly_investments = total_ownership_expences - rent

    output_df.at[0, "investments"] = initial_capital
    output_df.at[0, "house_price"] = house_cost
    output_df.at[0, "house_net"] = initial_capital
    output_df.at[0, "loan_left"] = house_cost-initial_capital
    for i in range(1, int(loan_duration)*12+1):
        output_df.at[i, "investments"] = output_df.at[i-1, "investments"]*(1+stock_returns/12) + monthly_investments
        output_df.at[i, "house_price"] = output_df.at[i-1, "house_price"]*(1+house_appreciation/12)
        output_df.at[i, "loan_left"] = (house_cost-initial_capital)*calc_principal_left(loan_duration, interest_rate, i)
        output_df.at[i, "house_net"] = output_df.at[i, "house_price"] - output_df.at[i, "loan_left"]



    for i in range(int(loan_duration)*12+1, int(years_to_simulate)*12+1):
        output_df.at[i, "investments"] = output_df.at[i-1, "investments"]*(1+stock_returns/12) + monthly_investments
        output_df.at[i, "house_price"] = output_df.at[i-1, "house_price"]*(1+house_appreciation/12)
        output_df.at[i, "investments_owning"] = output_df.at[i-1, "investments_owning"]*(1+stock_returns/12) + monthly_payment
        output_df.at[i, "house_net"] = output_df.at[i, "house_price"] + output_df.at[i, "investments_owning"]

    return output_df


def plot_result(output_df: pd.DataFrame) -> None:
    output_df["diff"] = np.abs(output_df["investments"] - output_df["house_net"])
    month_at_equal = output_df[1:]["diff"].argmin()
    equal_net_worth = output_df.at[month_at_equal, "investments"]

    plot_df = output_df[["investments", "house_net"]].rename(columns={"investments": "Net worth renting", "house_net": "Net worth owning"})
    plt.figure(figsize=(16,10))
    sns.lineplot(plot_df["Net worth renting"], color="blue", label="Net worth renting")
    sns.lineplot(plot_df["Net worth owning"], color="green", label="Net worth owning")
    plt.plot()
    plt.vlines(x=month_at_equal, ymax=equal_net_worth, ymin=0, linestyles="dashed", colors="red")
    plt.hlines(y=equal_net_worth, xmax=month_at_equal, xmin=0, linestyles="dashed", colors="red")
    plt.axvline(x=LOAN_DURATION*12, color="black", linestyle="dashed")
    plt.xticks(list(plt.xticks()[0]) + [month_at_equal])
    plt.yticks(list(plt.yticks()[0]) + [equal_net_worth])
    plt.xlabel("Months")
    plt.ylabel("Net worth [eur]")
    plt.title("Renting vs owning")
    plt.grid()
    plt.subplots_adjust(bottom=0.05, left=0.10)
    ax = plt.gca()
    plt.xlim((0, YEARS_TO_SIMULATE*12+20))
    ax.set_ylim(bottom=0)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _ : f"{x:,.0f}"))

    plt.savefig("/Users/igor/Documents/calculator.png")

def main():

    output_df = simulate_returns(
        INTEREST_RATE,
        HOUSE_COST,
        RENT,
        MAINTENANCE,
        DOWN_PAYMENT,
        HOUSE_APPRECIATION,
        STOCKS_RETURNS,
        LOAN_DURATION,
        YEARS_TO_SIMULATE
    )
    plot_result(output_df)

if __name__ == "__main__":
    main()