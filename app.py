import streamlit as st
import random
import json
from google_sheets_writer import GoogleSheetsWriter

google_sheets_writer = GoogleSheetsWriter(
    spreadsheet_id="1x2yeFBQVQw8_mO6trYiT2qL3gNNXrfhFvJeshi6_Hzs",
    sheet_name="Sheet1"
)

# Load JSON data
with open("examples_for_checking_correctness_of_attacking_arguments_generated.json", "r") as f:
    attacking_arguments = json.load(f)

with open("examples_for_checking_correctness_of_supporting_arguments_generated.json", "r") as f:
    supporting_arguments = json.load(f)

with open("examples_for_checking_correct_weighing_of_arguments.json", "r") as f:
    weighing_examples = json.load(f)

# pick one of each type up front so the form doesn't reshuffle on each widget-change
supporting_example = random.choice(supporting_arguments)
attacking_example = random.choice(attacking_arguments)
weighing_example = random.choice(weighing_examples)

with st.form("evaluation_form"):
    st.title("Argument Validity Evaluation")
    # Supporting Argument Section
    st.header("Supporting Argument Example")
    st.subheader("Claim")
    st.text(supporting_example["claim"])
    st.subheader("Supporting Argument")
    st.text(supporting_example["argument"])

    supporting_correct = st.radio(
        "Do you think the supporting argument is correct?",
        ["True", "False"],
        key="supporting_correct"
    )
    if supporting_correct == "False":
        supporting_explanation = st.text_area(
            "Please explain why you think the supporting argument is incorrect:",
            key="supporting_explanation"
        )

    # Attacking Argument Section
    st.header("Attacking Argument Example")
    st.subheader("Claim")
    st.text(attacking_example["claim"])
    st.subheader("Attacking Argument")
    st.text(attacking_example["argument"])

    attacking_correct = st.radio(
        "Do you think the attacking argument is correct?",
        ["True", "False"],
        key="attacking_correct"
    )
    if attacking_correct == "False":
        attacking_explanation = st.text_area(
            "Please explain why you think the attacking argument is incorrect:",
            key="attacking_explanation"
        )

    # Weighing Section
    st.header("Argument Weighing Evaluation")
    st.subheader("Claim")
    st.text(weighing_example["claim"])

    st.subheader("Attacking Argument")
    st.text(weighing_example["attacking_argument"])
    st.subheader("Supporting Argument")
    st.text(weighing_example["supporting_argument"])

    which_argument = st.radio(
        "Which argument do you think is more convincing?",
        ["Attacking Argument", "Supporting Argument"],
        key="weighing_choice"
    )
    weighing_explanation = st.text_area(
        "Please explain why you selected this argument:",
        key="weighing_explanation"
    )

    submitted = st.form_submit_button("Submit")

if submitted:
    st.success("Thanks! Your answers have been recorded.")

    new_line_data = [
        supporting_correct,
        supporting_explanation if supporting_correct == "False" else "",
        attacking_correct,
        attacking_explanation if attacking_correct == "False" else "",
        which_argument,
        weighing_explanation
    ]

    google_sheets_writer.write_to_sheets(
        new_line_data=new_line_data
    )

    st.json({
        "supporting_correct": supporting_correct,
        "supporting_explanation": supporting_explanation if supporting_correct == "False" else "",
        "attacking_correct": attacking_correct,
        "attacking_explanation": attacking_explanation if attacking_correct == "False" else "",
        "weighing_choice": which_argument,
        "weighing_explanation": weighing_explanation
    })
