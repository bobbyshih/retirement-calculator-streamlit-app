### Import packages --------------------------------------------------------------
import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.title("Retirement Savings Calculator")

st.write("Hi there! This is a simple python app to calculate how much you need to save in order to retire!")
st.write("To get started, please input values in all of the fields below.")
st.write("IMPORTANT: I AM NOT A FINANCIAL ADVISOR. THIS IS NOT FINANCIAL ADVICE. PLEASE READ THE DISCLAIMERS BELOW.")

### Toggle section for the inspiration --------------------------------------------------------------
with st.expander("Why did I make this app?"):
    st.write("One of the challenges with thinking about retirement is that you can't just use current income and cost of living (COL) numbers when thinking about retirement. Why is this? Well, inflation! If you estimate your current COL at ~50,000 USD, do you think that's still going to be true 10, 20, or 30 years in the future? Absolutely not! In fact, at a 2% inflation rate your COL will double in roughly 36 years.")
    st.write("It's for this reason that the classic advice of taking your current COL and dividing it by expected return on investment (ROI) in retirement to calculate the amount needed to achieve financial freedom is inherently false. It might go something like this: if you could live on ~50,000 USD per year and you anticipate a conservative 3% ROI in retirement, then you need ~1.7M USD to retire and you could live off the appreciation without touching the principal.") 
    st.write("But if you did this, your income in retirement would be fixed, but inflation would continue to erode your buying power! 20 years after retirement, your fixed income would be the equivalent of ~33,600 USD in today's dollars.")
    st.write("Naturally, you could begin to withdraw the principal amount as you near the expected end of retirement, but how do we model a way to do this while ensuring we don't running out of funds? And how can we reliably ensure a given standard of living throughout retirement?")
    st.markdown("**:red[That's where this calculator comes in!]**")
    st.write("The best part about this app is that it dynamically re-calculates retirement savings targets as you adjust these variables. So, if you find that the savings targets are too high then you may consider increasing your retirement age or decreasing your current COL (i.e., learn to live with less in retirement). On the other hand, if you've got retirement in the bag and you're saving way in excess of what this calculator is outputting, you can consider decreasing retirement age or increasing your current COL.")

### Toggle section for methodology --------------------------------------------------------------
with st.expander("How does this calculator work?"):
    st.write("This calculator will consider inflation based on your estimated current COL to estimate monthly expenses up until the point at which you plan to exhaust your retirement savings. From there, I work backwards to calculate how much you need in order to retire at a given age.")
    st.write("Given the amount needed to retire, I calculate the current year level of monthly contribution necessary using the below formula:")
    st.latex(r'''
    \text{ret.bal} = \text{curr.bal} \cdot \text{ROI}^{\text{YTR}} + 
    \sum_{i = 0}^{\text{MTR} - 1} X \cdot \text{inflation}^{Y} \cdot \text{monthly.ROI}^{\text{MTR} - i}
    ''')
    st.markdown("Where $Y = i / 12$ and $i$ is months.")
    st.write("X represents monthly contribution in TODAY dollars (your contributions are assumed to track inflation).")
    st.write("ROI and monthly.ROI represent yearly and monthly expected return on investment. This should be lower than retirement ROI, given that retirement savings should be placed in a more conservative but safer investment vehicle.")
    st.write("YTR and MTR are Years and Months to retirement.")
    st.write("This formula assumes that your monthly contributions increase with inflation. However, this does not take into account major pay raises above inflation such as job changes or large events such as unemployment.")
    st.write("Solve for X")

### Toggle section for disclaimers --------------------------------------------------------------
with st.expander("Some disclaimers"):
    st.markdown("""
    - This calculator assumes a constant rate of inflation and ROI, which may or may not be true. Sometimes your investment portfolio will do fantastic and other years it might actually go down. Sometimes inflation is almost 7%. I can't model this!
    - I assume that your entire net worth is in liquidable assets such as stocks and bonds. If you plan to own property this calculator is likely not for you, but this is something I am looking into modelling!
    - This tool uses a separate ROI pre- and post-retirement. However, in reality you are more likely to slowly shift your investments towards safer assets as you near retirement, meaning your ROI is higher when you are younger and slowly decreases as you approach retirement. Here, we basically assume that your portfolio ROI is essentially constant pre-retirement and then suddenly shifts to safer assets. In practice, this is not realistic. A future version may include this change in ROI over time.
    - This tool assumes no social security benefits. I would like to add that in, but it's currently not possible to accurately predict how much social security will pay out in the future.
    - This tool is currency agnostic. Just be consistent across all fields. The pre-filled values are USD.
    - Here, I assume that your ability to save scales with inflation. That means that, at your job, you receive raises purely in line with inflation (which is assumed constant). In reality, most of us will experience periods of unemployment or get big raises when we job hop or get a promotion. Just keep this in mind.
    - This calculator assumes you are aiming to spend down the entirety of your retirement savings within your lifetime. A future version of this calculator may include a feature to allow for leaving behind a set amount at the end, for instance in the case of wanting to leave behind an inheritance.
    """)

### Input values --------------------------------------------------------------
st.write("### Input values - Retirement")
col1, col2 = st.columns(2)
current_age = col1.number_input("Current Age", min_value = 0, value = 35)
retirement_age = col2.number_input("Desired Retirement Age", min_value = current_age, value = 65)
life_expectancy = col1.number_input("Life Expectancy", min_value = retirement_age, value = 90)
desired_buffer = col2.number_input("Desired retirement buffer (in years)", min_value = 0, value = 5)
inflation_input = col1.number_input("Inflation rate (%)", min_value = 0, value = 3)
retirement_expected_ROI_input = col2.number_input("Expected ROI in retirement", min_value = 0, value = 3)
current_COL = col1.number_input("Current cost of living (yearly)", min_value = 0, value = 70000)

st.write("### Input values - Pre-retirement")
col1, col2 = st.columns(2)
current_savings = col1.number_input("Current retirement savings", min_value = 0, value = 100000)
savings_expected_ROI_input = col2.number_input("Pre-retirement ROI (%)", min_value = 0, value = 7)

### BACKEND - GENERATE SAVINGS AND RETIREMENT retirement_df --------------------------------------------------------------
# Convert percentage inputs for compatibility
inflation = 1 + (inflation_input / 100)
retirement_expected_ROI = 1 + (retirement_expected_ROI_input / 100)
savings_expected_ROI = 1 + (savings_expected_ROI_input / 100)

## Calculate amount needed to RETIRE 
# Calculate monthly values
monthly_inflation = inflation ** (1/12)
retirement_monthly_ROI = retirement_expected_ROI ** (1/12)
months_retirement = ((life_expectancy + desired_buffer) - retirement_age) * 12

# Generate empty df
retirement_df = pd.DataFrame(columns=["Age", "COL (Monthly)", "Balance (Beginning of Month)"])
time_formatted = [f"{years} Y, {months} M" for value in (np.arange(0, months_retirement + 1) + retirement_age * 12) for years, months in [divmod(value, 12)]]
retirement_df["Age"] = time_formatted

# Work backwards to calculate how much money you need to retire factoring in inflation and growth of the entire retirement portfolio
for i in np.arange(0, months_retirement + 1)[::-1] :   
    # Inflation will be calculated monthly
    COL = (current_COL/12) * monthly_inflation ** (i + ((retirement_age - current_age) * 12))
    COL = round(COL, 2)
    retirement_df.loc[i, "COL (Monthly)"] = COL

    # The goal is to have zero dollars at the end of this, so we will start from there and work backwards
    if i == months_retirement:
        retirement_df.loc[i, "Balance (Beginning of Month)"] = COL
    else:
        # Withdraw monthly living expenses just after the beginning of month
        balance = retirement_df.loc[i + 1, "Balance (Beginning of Month)"] / retirement_monthly_ROI + COL
        balance = round(balance, 2)
        retirement_df.loc[i, "Balance (Beginning of Month)"] = balance

## Calculate SAVINGS needed to reach retirement
# Given the above equation, solve for X, monthly contribution in TODAY dollars
retirement_bal = retirement_df.loc[0, "Balance (Beginning of Month)"]
year_to_retirement = retirement_age - current_age
month_to_retirement = (retirement_age - current_age) * 12
savings_monthly_ROI = savings_expected_ROI ** (1/12)
month_to_retirement = (retirement_age - current_age) * 12
curr_bal_infl_adj = current_savings * (savings_expected_ROI ** year_to_retirement)
sum_term = sum((monthly_inflation ** i) * (savings_monthly_ROI ** (month_to_retirement - i - 1)) for i in np.arange(0, month_to_retirement))
contribution = (retirement_bal - curr_bal_infl_adj) / sum_term

# Work forwards to show monthly contribution.
savings_df = pd.DataFrame(columns=["Age", "Contribution (Beginning of Month)", "Balance (Beginning of Month)"]) # Generate empty retirement_df
time_formatted = [f"{years} Y, {months} M" for value in (np.arange(0, month_to_retirement + 1) + current_age*12) for years, months in [divmod(value, 12)]]
savings_df["Age"] = time_formatted
savings_df["Contribution (Beginning of Month)"] = [0] + [round(contribution * (monthly_inflation ** i), 2) for i in np.arange(0, month_to_retirement)] # First value must be 0

# For loop to fill retirement balance
for i in np.arange(0, month_to_retirement + 1) :   
    if (i == 0):
        savings_df.loc[i, "Balance (Beginning of Month)"] = round(current_savings, 2)
    else:
        prev_balance = savings_df.loc[i-1, "Balance (Beginning of Month)"]
        curr_contribution = savings_df.loc[i, "Contribution (Beginning of Month)"]
        savings_df.loc[i, "Balance (Beginning of Month)"] = round(prev_balance * savings_monthly_ROI + curr_contribution, 2)

### BACKEND - GENERATE PLOTS --------------------------------------------------------------
# Plot pre-retirement savings
def plot_retirement_savings(savings_df, months_retirement):
    # Create the figure and axis objects directly
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Primary y-axis for 'Total retirement savings'
    ax1.plot(savings_df['Age'], savings_df['Balance (Beginning of Month)'], 
             label='Total retirement savings', color='blue')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Total Retirement Savings', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Adding labels, title, and grid
    ax1.set_xticks(range(0, months_retirement + 1, 12))
    ax1.tick_params(axis='x', rotation=45)
    ax1.ticklabel_format(style='plain', axis='y')  # Disable scientific notation
    ax1.set_title('Retirement Balance and Monthly COL over Time')
    ax1.grid(True)

    # Creating a secondary y-axis for 'Monthly Contribution'
    ax2 = ax1.twinx()
    ax2.plot(savings_df['Age'].iloc[1:], 
             savings_df['Contribution (Beginning of Month)'].iloc[1:], 
             label='Monthly Contribution', color='red')
    ax2.set_ylabel('Monthly Contribution', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Adding legends for both axes
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Return the figure object instead of showing it
    return fig

# Plot post-retirement
def plot_retirement(retirement_df, months_retirement):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Primary y-axis for 'Total retirement savings'
    ax1.plot(retirement_df['Age'], retirement_df['Balance (Beginning of Month)'], label='Total retirement savings', color='blue')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Total Retirement Savings', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Adding labels, title, and grid
    plt.xticks(range(0, months_retirement + 1, 12), rotation=45, ha='right')
    plt.ticklabel_format(style='plain', axis='y') # Disable scientific notation
    plt.title('Retirement Balance and Monthly COL over Time')
    plt.grid(True)

    # Creating a secondary y-axis for 'Monthly COL'
    ax2 = ax1.twinx()  
    ax2.plot(retirement_df['Age'], retirement_df['COL (Monthly)'], label='Monthly COL', color='red')
    ax2.set_ylabel('Monthly COL', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Adding legends for both axes
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Return the figure object instead of showing it
    return fig

### DISPLAY RESULTS --------------------------------------------------------------
st.divider()
# Display savings results
st.write("### Results - Pre-Retirement Savings")
st.markdown('<div class="centered-frame">', unsafe_allow_html=True)
st.dataframe(data = savings_df)
st.markdown('</div>', unsafe_allow_html=True)
st.pyplot(fig = plot_retirement_savings(savings_df, months_retirement))

# Display retirement results
st.write("### Results - Retirement Balance in Retirement")
st.dataframe(data = retirement_df)
st.pyplot(fig = plot_retirement(retirement_df, months_retirement))
