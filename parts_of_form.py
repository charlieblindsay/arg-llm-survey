import streamlit as st
import html
import json
import random


def render_argument_section(example, argument_type, likert_options):
    key_prefix = argument_type.lower()
    verb = 'support' if key_prefix == 'supporting' else 'attack'
    opposite_verb = 'attack' if key_prefix == 'supporting' else 'support'
    display_type = argument_type.capitalize()
    name_of_argument = f'Argument {display_type} Claim'

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

    responses['facts_within_claim'] = st.radio(
        f"""Do all premises in the '{name_of_argument}' use facts only from the
        claim?""",
        options=['Yes', 'No'],
        key=f"{key_prefix}_facts_within_claim"
    )

    responses['facts_outside_claim_details'] = st.text_area(
        "If 'No', provide the premises that do not use facts in the claim:",
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

    responses['complete_premises'] = st.radio(
        f"""Does '{name_of_argument}' include all premises needed to make
        it a sound argument?""",
        options=['Yes', 'No'],
        key=f"{key_prefix}_complete_premises"
    )

    responses['uses_specific_claim_information'] = st.radio(
        f"Does '{name_of_argument}' use SPECIFIC information from the claim?",
        options=likert_options,
        key=f"{key_prefix}_uses_specific_claim_information"
    )

    return responses


def render_comparison_of_arguments_section(
        comparison_type,
        arg_type,
        primary_attacking_arguments,
        primary_supporting_arguments,
        primary_experiment_id,
        secondary_experiment_id,
        primary_model,
        secondary_model,
        primary_settings,
        secondary_settings,
):
    secondary_examples_folder = f"examples/{secondary_model}/{secondary_experiment_id}/"

    with open(f"{secondary_examples_folder}/{arg_type}_arguments_examples.json", "r") as f:
        secondary_arguments = json.load(f)

    arg_index = random.randint(
        0, len(secondary_arguments) - 1
    )
    secondary_argument = secondary_arguments[arg_index]

    if arg_type == 'attacking':
        primary_argument = primary_attacking_arguments[arg_index]
    elif arg_type == 'supporting':
        primary_argument = primary_supporting_arguments[arg_index]

    claim = primary_argument["claim"]
    primary_argument_text = primary_argument["argument"]
    secondary_argument_text = secondary_argument["argument"]

    st.markdown(
        '<p style="color: orange; font-size: 20px; font-weight: bold;">Claim</p>',
        unsafe_allow_html=True
    )
    claim_html = html.escape(claim).replace('\n', '<br>')
    st.markdown(
        f'<p style="color: orange;">{claim_html}</p>',
        unsafe_allow_html=True
    )

    arg_colour = "green" if arg_type == "supporting" else "red"

    st.markdown(
        f'<p style="color: {arg_colour}; font-size: 20px; font-weight: bold;">Argument {arg_type.capitalize()} Claim #1</p>',
        unsafe_allow_html=True
    )
    supporting_html = html.escape(
        primary_argument_text
        ).replace('\n', '<br>')
    st.markdown(
        f'<p style="color: {arg_colour};">{supporting_html}</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<p style="color: {arg_colour}; font-size: 20px; font-weight: bold;">Argument {arg_type.capitalize()} Claim #2</p>',
        unsafe_allow_html=True
    )
    supporting_html = html.escape(
        secondary_argument_text
        ).replace('\n', '<br>')
    st.markdown(
        f'<p style="color: {arg_colour};">{supporting_html}</p>',
        unsafe_allow_html=True
    )

    verb = 'support' if arg_type == 'supporting' else 'attack'

    primary_argument_has_correct_direction = st.radio(
        f"""Do the premises in the 'Argument {arg_type.capitalize()} Claim #1'
        intend to {verb} the claim?
        For now, ignore whether or not the argument is sound.""",
        options=['Yes', 'No'],
        key=f"{comparison_type}_comparison__direction_of_primary_arg"
    )

    secondary_argument_has_correct_direction = st.radio(
        f"""Do the premises in the 'Argument {arg_type.capitalize()} Claim #2'
        intend to {verb} the claim?
        For now, ignore whether or not the argument is sound.""",
        options=['Yes', 'No'],
        key=f"{comparison_type}_comparison__direction_of_secondary_arg"
    )

    clarity_of_argument_comparison = st.radio(
        "Which argument is clearer and easier to understand?",
        options=[f"Argument {arg_type.capitalize()} Claim #1",
                    f"Argument {arg_type.capitalize()} Claim #2",
                    "They are equally clear"],
        key=f"{comparison_type}_comparison__clarity_of_argument"
    )

    clarity_of_argument_comparison_score = st.radio(
        """If you said that an argument is easier to understand, how much
        easier is it to understand?""",
        options=["Slightly clearer", "Moderately clearer", "Much clearer"],
        key=f"{comparison_type}_comparison__clarity_of_argument_comparison_score"
    )

    persuasiveness_comparison = st.radio(
        "Which argument is more persuasive overall?",
        options=[f"Argument {arg_type.capitalize()} Claim #1",
                 f"Argument {arg_type.capitalize()} Claim #2",
                 "They are equally persuasive"],
        key=f"{comparison_type}_comparison__persuasiveness_comparison"
    )

    persuasiveness_comments = st.text_area(
        """If you said an argument was more persuasive, why is this
        argument more persuasive? Please mention details from both
        arguments.""",
        key=f"{comparison_type}_comparison__persuasiveness_comments"
    )

    persuasiveness_comparison_score = st.radio(
        """If you said an argument was more persuasive, how much more
        persuasive is the argument you selected?""",
        options=[
            "Slightly more persuasive",
            "Moderately more persuasive",
            "Much more persuasive"
        ],
        key=f"{comparison_type}_comparison__persuasiveness_comparison_score"
    )

    return {
        'arg_type': arg_type,
        'primary_experiment_id': primary_experiment_id,
        'secondary_experiment_id': secondary_experiment_id,
        'primary_model': primary_model,
        'secondary_model': secondary_model,
        'primary_settings': primary_settings,
        'secondary_settings': secondary_settings,
        'primary_argument_has_correct_direction': primary_argument_has_correct_direction,
        'secondary_argument_has_correct_direction': secondary_argument_has_correct_direction,
        'clarity_of_argument_comparison': clarity_of_argument_comparison,
        'clarity_of_argument_comparison_score': clarity_of_argument_comparison_score,
        'persuasiveness_comparison': persuasiveness_comparison,
        'persuasiveness_comments': persuasiveness_comments,
        'persuasiveness_comparison_score': persuasiveness_comparison_score,
        'claim': claim,
        'primary_argument_text': primary_argument_text,
        'secondary_argument_text': secondary_argument_text,
        'primary_argument_claim_initial_weight': primary_argument["claim_initial_weight"],
        'secondary_argument_claim_initial_weight': secondary_argument["claim_initial_weight"],
        'primary_argument_claim_strength': primary_argument["claim_strength"],
        'secondary_argument_claim_strength': secondary_argument["claim_strength"],
        'primary_argument_threshold': primary_argument["threshold"],
        'secondary_argument_threshold': secondary_argument["threshold"],
        'primary_argument_correct_prediction': primary_argument["correct_prediction"],
        'secondary_argument_correct_prediction': secondary_argument["correct_prediction"],
        'primary_argument_strength': primary_argument["argument_strength"],
        'secondary_argument_strength': secondary_argument["argument_strength"]
    }
