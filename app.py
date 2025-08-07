import streamlit as st
import random
import json
from google_sheets_writer import GoogleSheetsWriter

google_sheets_writer = GoogleSheetsWriter(
    spreadsheet_id="1x2yeFBQVQw8_mO6trYiT2qL3gNNXrfhFvJeshi6_Hzs"
)


def render_argument_section(example, argument_type, likert_options):
    """
    Renders an argument evaluation section for either supporting or attacking arguments.

    Args:
        example (dict): Dictionary containing 'claim' and 'argument' keys
        argument_type (str): Either "supporting" or "attacking" (will be capitalized automatically)
        likert_options (list): List of likert scale options

    Returns:
        dict: Dictionary containing all the user responses
    """
    import streamlit as st

    # Create unique keys and capitalize for display
    key_prefix = argument_type.lower()
    display_type = argument_type.capitalize()

    # Header section
    st.header(f"{display_type} Argument Question")
    st.subheader("Claim")
    st.text(example["claim"])
    st.subheader(f"{display_type} Argument")
    st.text(example["argument"])

    # Collect responses
    responses = {}

    # Correctness evaluation
    responses['correct'] = st.radio(
        f"Do you think the {key_prefix} argument is correct?",
        options=likert_options,
        key=f"{key_prefix}_correct"
    )

    # Optional explanation for incorrect arguments
    if responses['correct'] in ['Strongly Disagree', 'Disagree']:
        responses['explanation'] = st.text_area(
            f"Why do you think the {key_prefix} argument is incorrect?",
            key=f"{key_prefix}_explanation"
        )

    # Specific information evaluation
    responses['uses_specific_claim_information'] = st.radio(
        f"""Do you think the {key_prefix} argument uses SPECIFIC
        information from the claim?""",
        options=likert_options,
        key=f"{key_prefix}_uses_specific_claim_information"
    )

    # Relevant information evaluation  
    responses['uses_relevant_claim_information'] = st.radio(
        f"""Do you think the {key_prefix} argument uses RELEVANT
        information from the claim?""",
        options=likert_options,
        key=f"{key_prefix}_uses_relevant_claim_information"
    )

    return responses


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
    st.write(
        """
        Thank you for participating in this survey!

        This survey is part of an MSc individual project applying argumentation frameworks to Task 4 of the COLIEE competition.
        Task 4 involves using relevant statute articles to determine whether a specific legal conclusion is true or false.

        In this project, we frame the task as a **claim verification problem**. For each example:

        The **claim** being evaluated is:  
        **“This argument is valid, i.e. the premises entail the conclusion.”**

        The premises and conclusion in the argument are the following:.
        - **Premises**: A set of statute articles.
        - **Conclusion**: A proposed legal conclusion.

        For each claim, an LLM generates:

        - A **supporting argument** (that defends the claim). 
        - An **attacking argument** (that challenges the claim).

        You will be asked **three questions**, each based on a **different claim** and corresponding LLM-generated supporting and attacking arguments.

        The first 2 questions focus on assessing the quality of the supporting and attacking argument respectively.
        The third question focusses on assessing the relative strength of an attacking argument in
        comparison with a supporting argument. All 3 questions include the claim and arguments produced."""
             )
    st.title("Argument Validity Evaluation")

    likert_options = ['Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree']

    supporting_argument_responses = render_argument_section(
        example=supporting_example,
        argument_type="supporting",
        likert_options=likert_options
    )

    st.divider()

    attacking_argument_responses = render_argument_section(
        example=attacking_example,
        argument_type="attacking",
        likert_options=likert_options
    )

    st.divider()

    # Weighing Section
    st.header("Argument Weighing Question")
    st.subheader("Claim")
    st.text(weighing_example["claim"])

    st.subheader("Attacking Argument")
    st.text(weighing_example["attacking_argument"])
    st.subheader("Supporting Argument")
    st.text(weighing_example["supporting_argument"])

    which_argument = st.radio(
        """Out of the above attacking and supporting arguments, which is
        stronger? Or are they equally strong?""",
        ["Attacking Argument", "Supporting Argument", "Equally strong"],
        key="weighing_choice"
    )

    other_argument = 'Attacking Argument' if which_argument == 'Supporting Argument' else 'Supporting Argument'

    if which_argument == "Attacking Argument" or which_argument == "Supporting Argument":
        difference_in_strengths = st.radio(
            f"""How much stronger is the {which_argument} as compared with the {other_argument}?""",
            options=['Barely stronger', 'Slightly stronger', 'Moderately stronger',
                     'Much stronger', 'Extremely stronger'],
            key="difference_in_strengths"
        )

        weighing_explanation = st.text_area(
            f"""Why do you the {which_argument} is stronger than the {other_argument}?
            Possible reasons could be that the {which_argument} better makes use of
            information from the claim, or that all required premises are stated and
            referenced in the claim etc.""",
            key="weighing_explanation"
        )
    else:
        weighing_explanation = st.text_area(
            "Why do you think the arguments have equal strength?",
            key="weighing_explanation"
        )

    submitted = st.form_submit_button("Submit")

if submitted:
    st.success("Thanks! Your answers have been recorded.")

    google_sheets_writer.write_to_sheets(
        sheet_name="SupArg Eval",
        new_line_data=[
            supporting_argument_responses["correct"],
            supporting_argument_responses["explanation"] if supporting_argument_responses["explanation"] == "False" else "",
            supporting_argument_responses["uses_specific_claim_information"],
            supporting_argument_responses["uses_relevant_claim_information"],
            supporting_example["claim"],
            supporting_example["valid"],
            supporting_example["claim_initial_weight"],
            supporting_example["claim_strength"],
            supporting_example["threshold"],
            supporting_example["correct_prediction"],
            supporting_example["argument"],
            supporting_example["argument_strength"]
        ]
    )

    google_sheets_writer.write_to_sheets(
        sheet_name="AttArg Eval",
        new_line_data=[
            attacking_argument_responses["correct"],
            attacking_argument_responses["explanation"] if attacking_argument_responses["explanation"] == "False" else "",
            attacking_argument_responses["uses_specific_claim_information"],
            attacking_argument_responses["uses_relevant_claim_information"],
            attacking_example["claim"],
            attacking_example["valid"],
            attacking_example["claim_initial_weight"],
            attacking_example["claim_strength"],
            attacking_example["threshold"],
            attacking_example["correct_prediction"],
            attacking_example["argument"],
            attacking_example["argument_strength"]
        ]
    )

    google_sheets_writer.write_to_sheets(
        sheet_name="Arg Weigh Eval",
        new_line_data=[
            which_argument,
            difference_in_strengths,
            weighing_explanation,
            weighing_example["claim"],
            weighing_example["valid"],
            weighing_example["claim_initial_weight"],
            weighing_example["claim_strength"],
            weighing_example["threshold"],
            weighing_example["correct_prediction"],
            weighing_example["supporting_argument"],
            weighing_example["attacking_argument"],
            weighing_example["supporting_strength"],
            weighing_example["attacking_strength"],
            weighing_example["difference_in_strength"]
        ]
    )
