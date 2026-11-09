import streamlit as st

# -----------------------------------------
# 1. Set up the webpage
# -----------------------------------------

st.set_page_config(
    page_title="NPV Calculator",
    page_icon="💰",
    layout="centered"
)

# Display the title and introduction
st.title("💰 Net Present Value (NPV) Calculator")

st.write(
    "Use this calculator to determine the Net Present Value "
    "of an investment based on its initial cost, discount rate, "
    "and expected future cash flows."
)

st.divider()

# -----------------------------------------
# 2. Collect information from the user
# -----------------------------------------

st.subheader("Enter Investment Information")

# Ask the user for the initial investment
initial_investment = st.number_input(
    "Initial Investment ($)",
    min_value=0.0,
    value=10000.0,
    step=500.0,
    help="Enter the amount of money invested today."
)

# Ask the user for the discount rate
discount_rate = st.number_input(
    "Discount Rate (%)",
    min_value=0.0,
    value=10.0,
    step=0.5,
    help="Enter the required rate of return as a percentage."
)

# Ask the user for future cash flows
st.write("**Future Cash Flows ($)**")

st.write(
    "Enter one cash flow for each year. "
    "Separate the numbers with commas or put each number on a new line."
)

cash_flow_input = st.text_area(
    "Enter Cash Flows",
    value="4000, 4000, 4000, 4000",
    height=120,
    help="Example: 4000, 5000, 6000, 7000"
)

# -----------------------------------------
# 3. Calculate the NPV
# -----------------------------------------

if st.button("Calculate NPV", type="primary"):

    try:
        # Convert the user's cash flows into a list of numbers
        cash_flows = [
            float(value.strip())
            for value in cash_flow_input.replace("\n", ",").split(",")
        ]

        # Check that cash flows were entered
        if not cash_flow_input.strip():
            st.warning("Please enter at least one cash flow.")

        # Check for invalid or empty entries
        elif not all(value.strip() for value in
                     cash_flow_input.replace("\n", ",").split(",")):
            st.error("Please enter a valid number for every cash flow.")

        else:
            # Convert the discount rate from a percentage to a decimal
            rate = discount_rate / 100

            # Create a list to store present values
            present_values = []

            # Calculate the present value of each year's cash flow
            for year, cash_flow in enumerate(cash_flows, start=1):

                present_value = cash_flow / ((1 + rate) ** year)

                present_values.append(present_value)

            # Add all present values together
            total_present_value = sum(present_values)

            # Subtract the initial investment to calculate NPV
            npv = total_present_value - initial_investment

            # -----------------------------------------
            # 4. Display the results
            # -----------------------------------------

            st.divider()
            st.subheader("NPV Results")

            # Display the final NPV
            st.metric(
                label="Net Present Value",
                value=f"${npv:,.2f}"
            )

            # Display the investment information
            st.write(f"**Initial Investment:** ${initial_investment:,.2f}")
            st.write(f"**Discount Rate:** {discount_rate:.2f}%")
            st.write(f"**Number of Years:** {len(cash_flows)}")

            st.write(
                f"**Total Present Value of Cash Flows:** "
                f"${total_present_value:,.2f}"
            )

            # -----------------------------------------
            # 5. Display each year's cash flow
            # -----------------------------------------

            st.subheader("Cash Flow Breakdown")

            # Create a table showing each year's information
            results = []

            for year, (cash_flow, pv) in enumerate(
                zip(cash_flows, present_values), start=1
            ):
                results.append({
                    "Year": year,
                    "Cash Flow": f"${cash_flow:,.2f}",
                    "Present Value": f"${pv:,.2f}"
                })

            # Display the table
            st.table(results)

            # -----------------------------------------
            # 6. Explain what the NPV means
            # -----------------------------------------

            st.subheader("Investment Evaluation")

            if npv > 0:
                st.success(
                    "Positive NPV: This investment is expected "
                    "to create value based on the discount rate."
                )

            elif npv < 0:
                st.error(
                    "Negative NPV: This investment is expected "
                    "to lose value based on the discount rate."
                )

            else:
                st.info(
                    "NPV is zero: This investment is expected "
                    "to earn exactly the required rate of return."
                )

    except ValueError:
        # Display an error if the user enters invalid information
        st.error(
            "Invalid input. Please enter numbers only for your cash flows."
        )

# -----------------------------------------
# 7. Display instructions
# -----------------------------------------

st.divider()

st.subheader("How to Use This Calculator")

st.write("""
1. Enter the initial investment amount.
2. Enter the discount rate as a percentage.
3. Enter the expected cash flow for each year.
4. Separate cash flows with commas or new lines.
5. Click the Calculate NPV button.
6. Review your NPV and the cash flow breakdown.

Remember: Enter the initial investment as a positive number.
Future cash flows can be positive or negative.
Use the same currency for all amounts.
""")

st.caption("NPV Calculator built with Python and Streamlit.")
