import streamlit as st
import random
import json
from google_sheets_writer import GoogleSheetsWriter
import html

google_sheets_writer = GoogleSheetsWriter(
    spreadsheet_id="1x2yeFBQVQw8_mO6trYiT2qL3gNNXrfhFvJeshi6_Hzs"
)


def render_argument_section(example, argument_type, likert_options):
    key_prefix = argument_type.lower()
    verb = 'support' if key_prefix == 'supporting' else 'attack'
    opposite_verb = 'attack' if key_prefix == 'supporting' else 'support'
    display_type = argument_type.capitalize()
    name_of_argument = f'Argument {display_type} Claim'

    st.header(f"{display_type} Argument Question")

    st.markdown(
        '<p style="color: orange; font-size: 20px; font-weight: bold;">Claim</p>',
        unsafe_allow_html=True
    )
    claim_html = html.escape(example["claim"]).replace('\n', '<br>')
    st.markdown(f'<p style="color: orange;">{claim_html}</p>', unsafe_allow_html=True)

    argument_color = "green" if key_prefix == "supporting" else "red"
    st.markdown(
        f'<p style="color: {argument_color}; font-size: 20px; font-weight: bold;">{name_of_argument}</p>',
        unsafe_allow_html=True
    )
    argument_html = html.escape(example["argument"]).replace('\n', '<br>')
    st.markdown(f'<p style="color: {argument_color};">{argument_html}</p>', unsafe_allow_html=True)

    responses = {}

    responses['correct_dialectical_relation'] = st.radio(
        f"""Do the premises in the '{name_of_argument}' intend to {verb} the claim
        rather than {opposite_verb} it?
        For now, ignore whether or not the '{name_of_argument}' is sound.""",
        options=['Yes', 'No'],
        key=f"{key_prefix}_correct_dialectical_relation"
    )

    responses['logically_valid'] = st.radio(
        f"Are any of the premises in the '{name_of_argument}' logically invalid?",
        options=['Yes', 'No'],
        key=f"{key_prefix}_logically_valid"
    )

    responses['logically_invalid_details'] = st.text_area(
        """If 'Yes', provide the premises that are logically invalid and
        explain why they are logically invalid.""",
        key=f"{key_prefix}_logically_invalid_details"
    )

    responses['facts_within_claim'] = st.radio(
        f"""Do all premises in the '{name_of_argument}' use facts only from the
        claim?""",
        options=['Yes', 'No'],
        key=f"{key_prefix}_facts_within_claim"
    )

    responses['facts_outside_claim_details'] = st.text_area(
        "If 'No', provide the premises using information outside the claim:",
        key=f"{key_prefix}_facts_outside_claim_details"
    )

    responses['relevant_premises'] = st.radio(
        f"""Are all premises in the '{name_of_argument}' relevant to the
        conclusion in the claim?""",
        options=['Yes', 'No'],
        key=f"{key_prefix}_relevant_premises"
    )

    responses['irrelevant_premises_details'] = st.text_area(
        "If 'No', provide the premises that are irrelevant:",
        key=f"{key_prefix}_irrelevant_premises_details"
    )

    responses['complete_premises'] = st.radio(
        f"""Does '{name_of_argument}' include all premises needed to be
        a sound argument?""",
        options=['Yes', 'No'],
        key=f"{key_prefix}_complete_premises"
    )

    responses['uses_specific_claim_information'] = st.radio(
        f"Does '{name_of_argument}' use SPECIFIC information from the claim?",
        options=likert_options,
        key=f"{key_prefix}_uses_specific_claim_information"
    )

    return responses


if "personal_info" not in st.session_state:
    st.session_state.personal_info = {"name": "", "job_title": "", "studying": ""}

if "rerun" not in st.session_state:
    st.session_state.rerun = 0

job_id = 1384111
date = '12-08-2025'

with open(f"examples/attacking_arguments_examples__{job_id}__{date}.json", "r") as f:
    attacking_arguments = json.load(f)

with open(f"examples/supporting_arguments_examples__{job_id}__{date}.json", "r") as f:
    supporting_arguments = json.load(f)

with open(f"examples/weighing_examples__{job_id}__{date}.json", "r") as f:
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

    st.session_state.personal_info["name"] = st.text_input(
        "What is your name?",
        st.session_state.personal_info["name"]
    )
    st.session_state.personal_info["job_title"] = st.text_input(
        "What is your job title?",
        st.session_state.personal_info["job_title"]
    )
    st.session_state.personal_info["studying"] = st.text_input(
        "If you answered 'Student', what are you studying?",
        st.session_state.personal_info["studying"]
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

        You will be asked **three questions**, each based on a **different
        claim** and corresponding LLM-generated supporting and attacking
        arguments.

        The first 2 questions focus on assessing the quality of the supporting
        and attacking arguments respectively.
        The third question focusses on assessing the relative strength of an
        attacking argument in comparison with a supporting argument. All 3
        questions include the claim and arguments produced.

        Your responses will be very helpful as they will provide a qualitative
        assessment of the arguments produced by the LLM and the means by which
        the relative strength of arguments are assessed.
        """
             )

    st.divider()

    st.title("Argument Validity Questions")

    likert_options = [
        'Strongly Disagree',
        'Disagree',
        'Neutral',
        'Agree',
        'Strongly Agree'
    ]

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
    st.markdown(
        '<p style="color: orange; font-size: 20px; font-weight: bold;">Claim</p>',
        unsafe_allow_html=True
    )
    claim_html = html.escape(weighing_example["claim"]).replace('\n', '<br>')
    st.markdown(
        f'<p style="color: orange;">{claim_html}</p>',
        unsafe_allow_html=True
    )

    # Green supporting argument subheader and text
    st.markdown(
        '<p style="color: green; font-size: 20px; font-weight: bold;">Argument Supporting Claim</p>',
        unsafe_allow_html=True
    )
    supporting_html = html.escape(
        weighing_example["supporting_argument"]
    ).replace('\n', '<br>')
    st.markdown(
        f'<p style="color: green;">{supporting_html}</p>',
        unsafe_allow_html=True
    )

    # Red attacking argument subheader and text
    st.markdown(
        '<p style="color: red; font-size: 20px; font-weight: bold;">Argument Attacking Claim</p>',
        unsafe_allow_html=True
    )
    attacking_html = html.escape(
        weighing_example["attacking_argument"]
    ).replace('\n', '<br>')
    st.markdown(
        f'<p style="color: red;">{attacking_html}</p>',
        unsafe_allow_html=True
    )

    supporting_argument_supports = st.radio(
        """Do the premises in the 'Argument Supporting Claim' intend to support the claim?
        For now, ignore whether or not the argument is sound.""",
        options=['Yes', 'No'],
        key="weighing_supporting_argument_supports"
    )

    attacking_argument_attacks = st.radio(
        """Do the premises in the 'Argument Attacking Claim' intend to attack the claim?
        For now, ignore whether or not the argument is sound.""",
        options=['Yes', 'No'],
        key="weighing_attacking_argument_attacks"
    )

    which_argument = st.radio(
        "Compare the attacking and supporting arguments. Which is stronger?",
        ["Argument Attacking Claim", "Argument Supporting Claim", "Equally strong"],
        key="weighing_which_argument"
    )

    difference_in_strengths = st.radio(
        "How much stronger is this argument than the other?",
        options=['Not stronger', 'Slightly stronger', 'Moderately stronger', 'Much stronger', 'Extremely stronger'],
        key="weighing_difference_in_strengths"
    )

    weighing_explanation = st.text_area(
        "Explain why this argument is stronger than the other:",
        key="weighing_explanation"
    )

    st.divider()

    generate_new = st.radio(
        """You can either submit your answers and generate new
                questions or submit your answers and finish the questionnaire.
                What would you like to do?""",
        options=["Submit answers, generate new questions", "Submit answers, end questionnaire"],
        key="weighing_generate_new"
    )

    submitted = st.form_submit_button("Submit")

    if submitted:
        google_sheets_writer.write_to_sheets(
            sheet_name="SupArg Eval",
            new_line_data=[
                date,
                job_id,
                st.session_state.personal_info["name"],
                st.session_state.personal_info["job_title"],
                st.session_state.personal_info["studying"],
                supporting_argument_responses["correct_dialectical_relation"],
                supporting_argument_responses["logically_valid"],
                supporting_argument_responses.get("logically_invalid_details", ""),
                supporting_argument_responses["facts_within_claim"],
                supporting_argument_responses.get("facts_outside_claim_details", ""),
                supporting_argument_responses["relevant_premises"],
                supporting_argument_responses.get("irrelevant_premises_details", ""),
                supporting_argument_responses["complete_premises"],
                supporting_argument_responses["uses_specific_claim_information"],
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
                date,
                job_id,
                st.session_state.personal_info["name"],
                st.session_state.personal_info["job_title"],
                st.session_state.personal_info["studying"],
                attacking_argument_responses["correct_dialectical_relation"],
                attacking_argument_responses["logically_valid"],
                attacking_argument_responses.get("logically_invalid_details", ""),
                attacking_argument_responses["facts_within_claim"],
                attacking_argument_responses.get("facts_outside_claim_details", ""),
                attacking_argument_responses["relevant_premises"],
                attacking_argument_responses.get("irrelevant_premises_details", ""),
                attacking_argument_responses["complete_premises"],
                attacking_argument_responses["uses_specific_claim_information"],
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
                date,
                job_id,
                st.session_state.personal_info["name"],
                st.session_state.personal_info["job_title"],
                st.session_state.personal_info["studying"],
                supporting_argument_supports,
                attacking_argument_attacks,
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

        if generate_new == "Submit answers, generate new questions":
            st.success(
                """Thank you for agreeing to answer more questions!
                The new questions have been generated.
                Please fill out your answers!"""
            )
            st.session_state.rerun += 1
            st.experimental_rerun()
        else:
            st.success("""Thank you! Your answers have been recorded.
                    Your time is greatly appreciated!""")
