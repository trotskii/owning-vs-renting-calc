import numpy as np
import plotly.graph_objects as go

def prepare_networths_chart(simulation):
    output_df = simulation.copy()
    output_df["diff"] = np.abs(output_df["investments"] - output_df["house_net"])
    month_at_equal = output_df[1:]["diff"].argmin()
    equal_net_worth = output_df.at[month_at_equal, "investments"]
    loan_end = output_df.loc[output_df["loan_left"]==0].index[0]
    plot_df = output_df[["investments", "house_net"]].rename(columns={"investments": "Net worth renting", "house_net": "Net worth owning"})

    renting_at_loan_end = plot_df.at[loan_end, "Net worth renting"]
    owning_at_loan_end = plot_df.at[loan_end, "Net worth owning"]

    renting_at_end = plot_df.at[plot_df.index[-1], "Net worth renting"]
    owning_at_end = plot_df.at[plot_df.index[-1], "Net worth owning"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=plot_df.index,
        y=plot_df["Net worth renting"],
        mode="lines",
        name="Net worth renting",
        line={"color":"blue"}
    ))
    fig.add_trace(go.Scatter(
        x=plot_df.index,
        y=plot_df["Net worth owning"],
        mode="lines",
        name="Net worth owning",
        line={"color":"green"}
    ))
    fig.add_trace(go.Scatter(
        x=[month_at_equal, month_at_equal],
        y=[0, equal_net_worth],
        mode="lines",
        line={"color": "red", "dash":"dash"},
        showlegend=False
    ))
    fig.add_annotation(x=month_at_equal, y=0, text=f"{month_at_equal}", showarrow=False)
    fig.add_trace(go.Scatter(
        x=[0, month_at_equal],
        y=[equal_net_worth, equal_net_worth],
        mode="lines",
        line={"color": "red", "dash":"dash"},
        showlegend=False,
    ))
    fig.add_annotation(x=0, y=equal_net_worth, text=f"{int(equal_net_worth)}", showarrow=False)
    fig.add_vline(
        x=loan_end,
        line_dash="dash",
        annotation_text="Loan paid out",
        annotation_position="top"
    )
    fig.add_trace(go.Scatter(
        x=[0, loan_end],
        y=[renting_at_loan_end, renting_at_loan_end],
        mode="lines",
        line={"color": "red", "dash":"dash"},
        showlegend=False
    ))
    fig.add_annotation(x=0, y=renting_at_loan_end, text=int(renting_at_loan_end), showarrow=False)
    fig.add_trace(go.Scatter(
        x=[0, loan_end],
        y=[owning_at_loan_end, owning_at_loan_end],
        mode="lines",
        line={"color": "red", "dash":"dash"},
        showlegend=False
    ))
    fig.add_annotation(x=0, y=owning_at_loan_end, text=int(owning_at_loan_end), showarrow=False)
    fig.add_trace(go.Scatter(
        x=[0, plot_df.index[-1]],
        y=[owning_at_end, owning_at_end],
        mode="lines",
        line={"color": "red", "dash":"dash"},
        showlegend=False
    ))
    fig.add_annotation(x=0, y=owning_at_end, text=int(owning_at_end), showarrow=False)
    fig.add_trace(go.Scatter(
        x=[0, plot_df.index[-1]],
        y=[renting_at_end, renting_at_end],
        mode="lines",
        line={"color": "red", "dash":"dash"},
        showlegend=False
    ))
    fig.add_annotation(x=0, y=renting_at_end, text=int(renting_at_end), showarrow=False)
    fig.update_layout(
        title="Rening vs Owning",
        xaxis={"showgrid": True},
        yaxis={"showgrid": True},
        legend={"yanchor": "bottom", "y": 0.99, "xanchor": "left", "x": 0.01},
        margin={"b":50, "l":50, "r":50, "t":50}
    )
    return fig
