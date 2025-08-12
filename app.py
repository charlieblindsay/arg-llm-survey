import streamlit as st
import random
import json
from google_sheets_writer import GoogleSheetsWriter
import html

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

    # Red claim subheader and text
    st.markdown('<p style="color: orange; font-size: 20px; font-weight: bold;">Claim</p>', unsafe_allow_html=True)
    claim_html = html.escape(example["claim"]).replace('\n', '<br>')
    st.markdown(f'<p style="color: orange;">{claim_html}</p>', unsafe_allow_html=True)

    # Set argument color based on type
    if display_type.lower() == "supporting":
        argument_color = "green"
    elif display_type.lower() == "attacking":
        argument_color = "red"
    else:
        argument_color = "orange"  # fallback color

    # Argument subheader and text with conditional color
    st.markdown(f'<p style="color: {argument_color}; font-size: 20px; font-weight: bold;">Argument {display_type} Claim</p>', unsafe_allow_html=True)
    argument_html = html.escape(example["argument"]).replace('\n', '<br>')
    st.markdown(f'<p style="color: {argument_color};">{argument_html}</p>', unsafe_allow_html=True)

    # Collect responses
    responses = {}

    # Correctness evaluation
    responses['correct'] = st.radio(
        f"Given the claim provided above, do you agree that the argument {key_prefix} this claim is correct?",
        options=likert_options,
        key=f"{key_prefix}_correct"
    )

    # Optional explanation for incorrect arguments
    if responses['correct'] in ['Strongly Disagree', 'Disagree']:
        responses['explanation'] = st.text_area(
            f"If you answered 'Disagree' or 'Strongly Disagree', why do you think the {key_prefix} argument is incorrect?",
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
    st.write("""
        Thank you for taking the time to participate in this questionnaire!
    """)

    st.title("Personal Questions")

    name = st.text_input("What is your name?")

    job_title = st.text_input("What is your current job title?")

    studying = st.text_input(
        """If you answered 'Student' in the previous question,
        what are you studying?"""
    )

    st.divider()

    st.title("Questionnaire Description")

    st.write(
        """
        This questionnaire is part of an MSc individual project applying argumentation frameworks to Task 4 of the [COLIEE competition](https://coliee.org/overview).
        Task 4 involves using relevant statute articles to determine whether a specific legal conclusion (taken from the Japanese Bar exam) is true or false.

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
        comparison with a supporting argument. All 3 questions include the claim and arguments produced.

        Your responses will be very helpful as they will provide a qualitative assessment of the arguments
        produced by the LLM and the means by which the relative strength of arguments are assessed.
        """
             )

        # TODO: Decide whether to give option to refresh if question is too hard 

    st.divider()

    st.title("Argument Validity Questions")

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

    # Orange claim subheader and text
    st.markdown('<p style="color: orange; font-size: 20px; font-weight: bold;">Claim</p>', unsafe_allow_html=True)
    claim_html = html.escape(weighing_example["claim"]).replace('\n', '<br>')
    st.markdown(f'<p style="color: orange;">{claim_html}</p>', unsafe_allow_html=True)

    # Red attacking argument subheader and text
    st.markdown('<p style="color: red; font-size: 20px; font-weight: bold;">Attacking Argument</p>', unsafe_allow_html=True)
    attacking_html = html.escape(weighing_example["attacking_argument"]).replace('\n', '<br>')
    st.markdown(f'<p style="color: red;">{attacking_html}</p>', unsafe_allow_html=True)

    # Green supporting argument subheader and text
    st.markdown('<p style="color: green; font-size: 20px; font-weight: bold;">Supporting Argument</p>', unsafe_allow_html=True)
    supporting_html = html.escape(weighing_example["supporting_argument"]).replace('\n', '<br>')
    st.markdown(f'<p style="color: green;">{supporting_html}</p>', unsafe_allow_html=True)


    which_argument = st.radio(
    """Considering the claim above, please compare the attacking and supporting arguments.
    Which argument do you find stronger, or are they equally strong?""",
        ["Attacking Argument", "Supporting Argument", "Equally strong"],
        key="weighing_choice"
    )

    difference_in_strengths = st.radio(
        f"""How much stronger is this argument than the other?""",
        options=['Not stronger', 'Slightly stronger', 'Moderately stronger',
                 'Much stronger', 'Extremely stronger'],
        key="difference_in_strengths"
    )

    weighing_explanation = st.text_area(
        f"""Why do you think this argument is stronger than the other?
        Possible reasons could be that the stronger argument makes better use of
        information from the claim, or that all required premises are stated and
        referenced in the claim etc.""",
        key="weighing_explanation"
    )

    submitted = st.form_submit_button("Submit your responses")

if submitted:
    st.success("Thanks! Your answers have been recorded. Your time is greatly appreciated!")

    google_sheets_writer.write_to_sheets(
        sheet_name="SupArg Eval",
        new_line_data=[
            name,
            job_title,
            studying,
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
            name,
            job_title,
            studying,
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
            name,
            job_title,
            studying,
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
