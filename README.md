A simple python application built using Streamlit to model savings needed to reach retirement.

To access this application, visit: https://retirement-calculator-app.streamlit.app/

# Why did I make this app?
One of the challenges with thinking about retirement is that you can't just use current income and cost of living (COL) numbers when thinking about retirement. Why is this? Well, inflation! If you estimate your current COL at ~50,000 USD, do you think that's still going to be true 10, 20, or 30 years in the future? Absolutely not! In fact, at a 2% inflation rate your COL will double in roughly 36 years.

It's for this reason that the classic advice of taking your current COL and dividing it by expected return on investment (ROI) in retirement to calculate the amount needed to achieve financial freedom is inherently false. It might go something like this: if you could live on ~50,000 USD per year and you anticipate a conservative 3% ROI in retirement, then you need ~1.7M USD to retire and you could live off the appreciation without touching the principal.

But if you did this, your income in retirement would be fixed, but inflation would continue to erode your buying power! 20 years after retirement, your fixed income would be the equivalent of ~33,600 USD in today's dollars.

Naturally, you could begin to withdraw the principal amount as you near the expected end of retirement, but how do we model a way to do this while ensuring we don't running out of funds? And how can we reliably ensure a given standard of living throughout retirement?

**That's where this calculator comes in!**

The best part about this app is that it dynamically re-calculates retirement savings targets as you adjust these variables. So, if you find that the savings targets are too high then you may consider increasing your retirement age or decreasing your current COL (i.e., learn to live with less in retirement). On the other hand, if you've got retirement in the bag and you're saving way in excess of what this calculator is outputting, you can consider decreasing retirement age or increasing your current COL.

# How does this calculator work?
This calculator will consider inflation based on your estimated current COL to estimate monthly expenses up until the point at which you plan to exhaust your retirement savings. From there, I work backwards to calculate how much you need in order to retire at a given age.

Given the amount needed to retire, I calculate the current year level of monthly contribution necessary using the below formula:

 $curr.bal * ROI^{YTR} + \sum_{i = 0}^{i = MTR - 1}X * inflation^{Y}*monthly.ROI^{MTR-i} = ret.bal$

Where $Y = i / 12$

X represents monthly contribution in TODAY dollars (your contributions are assumed to track inflation).

$ROI$ and $monthly.ROI$ represent yearly and monthly expected return on investment. This should be lower than retirement ROI, given that retirement savings should be placed in a more conservative but safer investment vehicle.

$YTR$ and $MTR$ are Years and Months to retirement.

This formula assumes that your monthly contributions increase with inflation. However, this does not take into account major pay raises above inflation such as job changes or large events such as unemployment.

Solve for X

### Future features
- [ ] Add in the ability to model how the purchase of real estate, as a primary residence or as an investment, will impact retirement.
- [ ] Add ability to factor in social security or other pension benefits.
- [ ] Add ability to factor in leaving behind an inheritance.
- [ ] Allow user to calculate retirement age based on current level of saving and current COL.
