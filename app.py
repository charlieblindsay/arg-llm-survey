import streamlit as st
import random
import json
from parts_of_form import (
    render_argument_section,
    render_comparison_of_arguments_section
)
from google_sheets_writer import GoogleSheetsWriter

google_sheets_writer = GoogleSheetsWriter(
    spreadsheet_id="1x2yeFBQVQw8_mO6trYiT2qL3gNNXrfhFvJeshi6_Hzs"
)

if "personal_info" not in st.session_state:
    st.session_state.personal_info = {
        "name": "",
        "job_title": "",
        "studying": ""
    }

if "rerun" not in st.session_state:
    st.session_state.rerun = 0

experiment_dict = {
    "qwen_14b": {
        "nR": "1411483",
        "uR": "1411484",
        "aR": "1406146",
        "uR_aR": "1411482"
        },
    "qwen_72b": {
        "nR": "196589",
        "uR": "196742",
        "aR": "196588",
        "uR_aR": "196746"
    }
}

with st.form("evaluation_form"):
    st.write("""
        Thank you for taking the time to complete this questionnaire!

        If you have any questions about the questionnaire, don't hesitate to
        contact Charlie Lindsay via email: cbl20@ic.ac.uk
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
        This questionnaire is part of an MSc individual project applying
        argumentation frameworks to Task 4 of the
        [COLIEE competition](https://coliee.org/overview).
        Task 4 involves using relevant statute articles to determine whether a
        specific legal conclusion is true or false.

        In this project, we frame the task as a **claim verification problem**.
        For each example:

        The **claim** being evaluated is:
        “This **argument** is valid, i.e. the **premises** entail the
        **conclusion**.”

        The **premises** and **conclusion** in the **argument** are the following:
        - **Premises**: A set of statute articles.
        - **Conclusion**: A proposed legal conclusion.

        For each claim, an LLM generates:

        - A **supporting argument** (that defends the claim).
        - An **attacking argument** (that challenges the claim).

        You will be asked **five questions**, each based on a **different
        claim** and the corresponding **supporting and/or attacking
        arguments**:
        - **Q1 and Q2** focus on assessing whether the arguments produced
        use information solely from the claim and whether the arguments are
        sound.
        - **Q3 and Q4** focus on comparing 2 arguments that take the
        same side, i.e. are either both attacking arguments or both supporting
        arguments.
        - **Q5** focusses on assessing the relative strength of an
        attacking argument in comparison with a supporting argument.

        All 5 questions include the claim and arguments produced. All questions
        **other than Q3** will state whether the claim is true or false.

        Your responses will help to provide qualitative assessments of:
        1. the LLM-generated arguments (Q1, Q2)
        2. whether different LLMs or different ArgLLM configurations
        improve argument quality (Q3, Q4)
        3. the means of assessing the strength of arguments (Q5)

        Thank you!
        """
        )

    st.divider()

    # ARGUMENTS GENERATED USING RANDOMLY CHOSEN MODEL AND SETTING
    main_model = random.choice(["qwen_14b", "qwen_72b"])
    main_setting = random.choice(["aR", "nR"])
    main_experiment_id = experiment_dict[main_model][main_setting]
    main_examples_folder = f"examples/{main_model}/{main_experiment_id}/"

    with open(f"{main_examples_folder}/attacking_arguments_examples.json", "r") as f:
        attacking_arguments = json.load(f)

    with open(f"{main_examples_folder}/supporting_arguments_examples.json", "r") as f:
        supporting_arguments = json.load(f)

    with open(f"{main_examples_folder}/weighing_examples.json", "r") as f:
        weighing_examples = json.load(f)

    supporting_example = random.choice(supporting_arguments)
    attacking_example = random.choice(attacking_arguments)
    weighing_example = random.choice(weighing_examples)

    likert_options = [
        'Strongly Disagree',
        'Disagree',
        'Neutral',
        'Agree',
        'Strongly Agree'
    ]

    st.title("Argument Soundness Questions")

    st.write("""Q1 and Q2 show a claim and one argument that takes the
             correct side, i.e. the argument supports the claim when
             the claim is true and attacks the claim when the claim is false.
             Your job is to decide whether the argument uses facts from the
             claim and whether the argument is sound.""")

    st.header("Q1: Supporting Argument Question")

    st.write("""NOTE: The following claim is true:""")

    supporting_argument_responses = render_argument_section(
        example=supporting_example,
        argument_type="supporting",
        likert_options=likert_options
    )

    st.divider()

    st.header("Q2: Attacking Argument Question")

    st.write("""NOTE: The following claim is false:""")

    attacking_argument_responses = render_argument_section(
        example=attacking_example,
        argument_type="attacking",
        likert_options=likert_options
    )

    st.divider()

    # Argument selection
    other_model = "qwen_72b" if main_model == "qwen_14b" else "qwen_14b"
    other_model_experiment_id = experiment_dict[other_model][main_setting]

    arg_type_for_model_comparison = random.choice(["supporting", "attacking"])

    st.title("Argument Comparison Section")

    st.write("""Q3 and Q4 show a claim, and then 2 arguments that take
             the same side, i.e. both attacking or both supporting the
             argument. Similar to Q1 and Q2, the arguments take the correct
             side, i.e. when the claim is true, the arguments will be
             supporting the claim, and when the claim is false, the arguments
             will be attacking the claim. For each question, your job
             is to decide which of the 2 arguments is clearer, and
             more persuasive.""")

    # MODEL COMPARISON SECTION

    st.header("Q3: Comparing Arguments 1")

    st.write(f'NOTE: The following claim is {"true" if arg_type_for_model_comparison == "supporting" else "false"}:')

    model_comparison_results = render_comparison_of_arguments_section(
        comparison_type='model',
        arg_type=arg_type_for_model_comparison,
        primary_attacking_arguments=attacking_arguments,
        primary_supporting_arguments=supporting_arguments,
        primary_experiment_id=main_experiment_id,
        secondary_experiment_id=other_model_experiment_id,
        primary_model=main_model,
        secondary_model=other_model,
        primary_settings=main_setting,
        secondary_settings=main_setting
    )

    st.divider()

    # ARGUMENT REASONING COMPARISON SECTION

    # Argument selection
    other_setting = "nR" if main_setting == "aR" else "aR"
    other_setting_experiment_id = experiment_dict[main_model][other_setting]
    other_setting_examples_folder = f"examples/{main_model}/{other_setting_experiment_id}/"

    arg_type_for_setting_comparison = "supporting" if arg_type_for_model_comparison == "attacking" else "attacking"

    st.header("Q4: Comparing Arguments 2")

    st.write(f'NOTE: The following claim is {"true" if arg_type_for_setting_comparison == "supporting" else "false"}:')

    settings_comparison_results = render_comparison_of_arguments_section(
        comparison_type='arguments_reasoning',
        arg_type=arg_type_for_setting_comparison,
        primary_attacking_arguments=attacking_arguments,
        primary_supporting_arguments=supporting_arguments,
        primary_experiment_id=main_experiment_id,
        secondary_experiment_id=other_setting_experiment_id,
        primary_model=main_model,
        secondary_model=main_model,
        primary_settings=main_setting,
        secondary_settings=other_setting
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
                st.session_state.personal_info["name"],
                st.session_state.personal_info["job_title"],
                st.session_state.personal_info["studying"],
                main_experiment_id,
                main_model,
                main_setting,
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
                st.session_state.personal_info["name"],
                st.session_state.personal_info["job_title"],
                st.session_state.personal_info["studying"],
                main_experiment_id,
                main_model,
                main_setting,
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
            sheet_name="Model Comparison",
            new_line_data=[
                st.session_state.personal_info["name"],
                st.session_state.personal_info["job_title"],
                st.session_state.personal_info["studying"],
                model_comparison_results["primary_experiment_id"],
                model_comparison_results["secondary_experiment_id"],
                model_comparison_results["primary_model"],
                model_comparison_results["secondary_model"],
                model_comparison_results["primary_settings"],
                model_comparison_results["secondary_settings"],
                model_comparison_results["arg_type"],
                model_comparison_results["primary_argument_has_correct_direction"],
                model_comparison_results["secondary_argument_has_correct_direction"],
                model_comparison_results["clarity_of_argument_comparison"],
                model_comparison_results["clarity_of_argument_comparison_score"],
                model_comparison_results["persuasiveness_comparison"],
                model_comparison_results["persuasiveness_comments"],
                model_comparison_results["persuasiveness_comparison_score"],
                model_comparison_results["claim"],
                model_comparison_results["primary_argument_text"],
                model_comparison_results["secondary_argument_text"],
                model_comparison_results["primary_argument_claim_initial_weight"],
                model_comparison_results["secondary_argument_claim_initial_weight"],
                model_comparison_results["primary_argument_claim_strength"],
                model_comparison_results["secondary_argument_claim_strength"],
                model_comparison_results["primary_argument_threshold"],
                model_comparison_results["secondary_argument_threshold"],
                model_comparison_results["primary_argument_correct_prediction"],
                model_comparison_results["secondary_argument_correct_prediction"],
                model_comparison_results["primary_argument_strength"],
                model_comparison_results["secondary_argument_strength"]
            ]
        )

        google_sheets_writer.write_to_sheets(
            sheet_name="Argument Reasoning Comparison",
            new_line_data=[
                st.session_state.personal_info["name"],
                st.session_state.personal_info["job_title"],
                st.session_state.personal_info["studying"],
                settings_comparison_results["primary_experiment_id"],
                settings_comparison_results["secondary_experiment_id"],
                settings_comparison_results["primary_model"],
                settings_comparison_results["secondary_model"],
                settings_comparison_results["primary_settings"],
                settings_comparison_results["secondary_settings"],
                settings_comparison_results["arg_type"],
                settings_comparison_results["primary_argument_has_correct_direction"],
                settings_comparison_results["secondary_argument_has_correct_direction"],
                settings_comparison_results["clarity_of_argument_comparison"],
                settings_comparison_results["clarity_of_argument_comparison_score"],
                settings_comparison_results["persuasiveness_comparison"],
                settings_comparison_results["persuasiveness_comments"],
                settings_comparison_results["persuasiveness_comparison_score"],
                settings_comparison_results["claim"],
                settings_comparison_results["primary_argument_text"],
                settings_comparison_results["secondary_argument_text"],
                settings_comparison_results["primary_argument_claim_initial_weight"],
                settings_comparison_results["secondary_argument_claim_initial_weight"],
                settings_comparison_results["primary_argument_claim_strength"],
                settings_comparison_results["secondary_argument_claim_strength"],
                settings_comparison_results["primary_argument_threshold"],
                settings_comparison_results["secondary_argument_threshold"],
                settings_comparison_results["primary_argument_correct_prediction"],
                settings_comparison_results["secondary_argument_correct_prediction"],
                settings_comparison_results["primary_argument_strength"],
                settings_comparison_results["secondary_argument_strength"],
            ]
        )

        if generate_new == "Submit answers, generate new questions":
            st.success(
                """Thank you for agreeing to answer more questions!
                The new questions have been generated.
                Please fill out your answers!"""
            )
            st.session_state.rerun += 1
            st.rerun()
        else:
            st.success("""Thank you! Your answers have been recorded.
                    Your time is greatly appreciated!""")
