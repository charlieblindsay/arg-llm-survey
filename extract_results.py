import json
import os
import glob

results_folder = "results"

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


def get_example_dict(
        data, semantics, claim_strength_method, threshold, example_index
):
    example = data["data"][semantics][example_index]
    valid = example["valid"] == 1

    arguments = example[claim_strength_method]['bag']['arguments']
    claim_dict = arguments['db0']
    claim = claim_dict["argument"]
    claim_initial_weight = claim_dict["initial_weight"]
    claim_strength = claim_dict["strength"]
    predicted_label = claim_strength > threshold

    return {
        "valid": valid,
        "arguments": arguments,
        "claim": claim,
        "claim_initial_weight": claim_initial_weight,
        "claim_strength": claim_strength,
        "predicted_label": predicted_label
    }


for model_name, experiment_dict in experiment_dict.items():
    for set_of_keys in [("nR", "uR"), ("aR", "uR_aR")]:
        no_uR_key = set_of_keys[0]
        uR_key = set_of_keys[1]

        experiment_id_no_uR = experiment_dict[no_uR_key]
        experiment_id_uR = experiment_dict[uR_key]

        json_file_path_no_uR = glob.glob(
            os.path.join(
                results_folder,
                model_name,
                f"{experiment_id_no_uR}.json"
            )
        )

        json_file_path_uR = glob.glob(
            os.path.join(
                results_folder,
                model_name,
                f"{experiment_id_uR}.json"
            )
        )

        with open(json_file_path_no_uR[0], "r", encoding="utf-8") as f:
            data_no_uR = json.load(f)

        with open(json_file_path_uR[0], "r", encoding="utf-8") as f:
            data_uR = json.load(f)

        semantics_no_uR = data_no_uR.get('arguments', {}).get('semantics')
        claim_strength_method_no_uR = data_no_uR.get('arguments', {}).get('claim_strength_calc_method')
        threshold_no_uR = data_no_uR.get('arguments', {}).get('threshold')

        semantics_uR = data_uR.get('arguments', {}).get('semantics')
        claim_strength_method_uR = data_uR.get('arguments', {}).get('claim_strength_calc_method')
        threshold_uR = data_uR.get('arguments', {}).get('threshold')

        supporting_arguments_examples = []
        attacking_arguments_examples = []
        weighing_examples = []

        for i in range(len(data_no_uR["data"][semantics_no_uR])):
            example_dict_no_uR = get_example_dict(
                data=data_no_uR,
                semantics=semantics_no_uR,
                claim_strength_method=claim_strength_method_no_uR,
                threshold=threshold_no_uR,
                example_index=i
            )

            example_dict_uR = get_example_dict(
                data=data_uR,
                semantics=semantics_uR,
                claim_strength_method=claim_strength_method_uR,
                threshold=threshold_uR,
                example_index=i
            )

            attacking_argument_dict_no_uR = example_dict_no_uR["arguments"]['Adb0<-d1b1']
            argument_text_no_uR = attacking_argument_dict_no_uR["argument"]
            argument_strength_no_uR = attacking_argument_dict_no_uR["strength"]

            supporting_argument_dict_no_uR = example_dict_no_uR["arguments"]['Sdb0<-d1b1']
            argument_text_no_uR = supporting_argument_dict_no_uR["argument"]
            argument_strength_no_uR = supporting_argument_dict_no_uR["strength"]

            if len(example_dict_no_uR["claim"]) < 1000:
                if example_dict_no_uR["valid"]:

                    supporting_arguments_examples.append(
                        {
                            'claim': example_dict_no_uR["claim"],
                            'argument': argument_text_no_uR,
                            'argument_supports_claim': True,
                            'claim_strength': example_dict_no_uR["claim_strength"],
                            'claim_initial_weight': example_dict_no_uR["claim_initial_weight"],
                            'argument_strength': argument_strength_no_uR,
                            'threshold': example_dict_no_uR["threshold"],
                            'valid': example_dict_no_uR["valid"],
                            'correct_prediction': example_dict_no_uR["predicted_label"] == example_dict_no_uR["valid"]
                        }
                    )

                else:
                    argument_dict_no_uR = example_dict_no_uR["arguments"]['Adb0<-d1b1']
                    argument_text_no_uR = argument_dict_no_uR["argument"]
                    argument_strength_no_uR = argument_dict_no_uR["strength"]

                    attacking_arguments_examples.append(
                        {
                            'claim': example_dict_no_uR["claim"],
                            'argument': argument_text_no_uR,
                            'argument_supports_claim': False,
                            'claim_strength': example_dict_no_uR["claim_strength"],
                            'claim_initial_weight': example_dict_no_uR["claim_initial_weight"],
                            'argument_strength': argument_strength_no_uR,
                            'threshold': threshold_no_uR,
                            'valid': example_dict_no_uR["valid"],
                            'correct_prediction': example_dict_no_uR["predicted_label"] == example_dict_no_uR["valid"],
                        }
                    )

                attacking_argument_dict_no_Ur = example_dict_no_Ur["arguments"]['Adb0<-d1b1']
                argument_text_no_Ur = argument_dict_no_Ur["argument"]
                argument_strength_no_Ur = argument_dict_no_Ur["strength"]

                weighing_examples.append(
                    {
                        'claim': example_dict_no_uR["claim"],
                        'supporting_argument': example_dict_no_uR["arguments"]['Sdb0<-d1b1']["argument"],
                        'attacking_argument': arguments['Adb0<-d1b1']["argument"],
                        'supporting_strength': arguments["Sdb0<-d1b1"]["strength"],
                        'attacking_strength': arguments["Adb0<-d1b1"]["strength"],
                        'support_is_stronger_than_attack': arguments["Sdb0<-d1b1"]["strength"] > arguments["Adb0<-d1b1"]["strength"],
                        'support_is_equal_to_attack': arguments["Sdb0<-d1b1"]["strength"] == arguments["Adb0<-d1b1"]["strength"],
                        'claim_initial_weight': claim_initial_weight,
                        'claim_strength': claim_strength,
                        'threshold': threshold,
                        'valid': valid,
                        'correct_prediction': predicted_label == valid,
                        'difference_in_strength': arguments["Sdb0<-d1b1"]["strength"] - arguments["Adb0<-d1b1"]["strength"]
                    }
                )

        folder_name = f"examples/{model_name}/{experiment_id}"

        os.makedirs(folder_name, exist_ok=True)

        with open(f"{folder_name}/supporting_arguments_examples.json", 'w') as f:
            json.dump(supporting_arguments_examples, f)

        with open(f"{folder_name}/attacking_arguments_examples.json", 'w') as f:
            json.dump(attacking_arguments_examples, f)

        with open(f"{folder_name}/weighing_examples.json", 'w') as f:
            json.dump(weighing_examples, f)
