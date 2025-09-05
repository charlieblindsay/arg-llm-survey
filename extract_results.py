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


def extract_experiment_hyperparameters(model_name, experiment_id):

    json_file_path = glob.glob(
        os.path.join(
            results_folder,
            model_name,
            f"{experiment_id}.json"
        )
    )

    with open(json_file_path[0], "r", encoding="utf-8") as f:
        data = json.load(f)

    hyperparameters_dict = {
        "semantics": data.get('arguments', {}).get('semantics'),
        "claim_strength_method": data.get(
            'arguments', {}
            ).get(
                'claim_strength_calc_method'
            ),
        "threshold": data.get('arguments', {}).get('threshold')
    }

    return hyperparameters_dict, data


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

    attacking_argument_dict = arguments.get('Adb0<-d1b1', {})
    supporting_argument_dict = arguments.get('Sdb0<-d1b1', {})

    return {
        "valid": valid,
        "arguments": arguments,
        "claim": claim,
        "claim_initial_weight": claim_initial_weight,
        "claim_strength": claim_strength,
        "predicted_label": predicted_label,
        "attacking_argument_dict": attacking_argument_dict,
        "supporting_argument_dict": supporting_argument_dict
    }


for model_name, experiment_dict in experiment_dict.items():
    for set_of_keys in [("nR", "uR"), ("aR", "uR_aR")]:
        no_uR_key = set_of_keys[0]
        uR_key = set_of_keys[1]

        experiment_id_no_uR = experiment_dict[no_uR_key]
        experiment_id_uR = experiment_dict[uR_key]

        hyperparameters_no_uR, data_no_uR = extract_experiment_hyperparameters(
            experiment_id=experiment_id_no_uR,
            model_name=model_name
        )
        hyperparameters_uR, data_uR = extract_experiment_hyperparameters(
            model_name=model_name,
            experiment_id=experiment_id_uR
        )

        supporting_arguments_examples = []
        attacking_arguments_examples = []
        weighing_examples = []

        for i in range(len(data_no_uR["data"][hyperparameters_no_uR["semantics"]])):
            example_dict_no_uR = get_example_dict(
                **hyperparameters_no_uR,
                data=data_no_uR,
                example_index=i
            )

            example_dict_uR = get_example_dict(
                **hyperparameters_uR,
                data=data_uR,
                example_index=i
            )

            if len(example_dict_no_uR["claim"]) < 1000 and 'Article 543' not in example_dict_no_uR["claim"]:
                if example_dict_no_uR["valid"]:

                    if example_dict_no_uR["supporting_argument_dict"] == {}:
                        continue

                    supporting_arguments_examples.append(
                        {
                            'claim': example_dict_no_uR["claim"],
                            'argument': example_dict_no_uR["supporting_argument_dict"]["argument"],
                            'argument_supports_claim': True,
                            'claim_strength': example_dict_no_uR["claim_strength"],
                            'claim_initial_weight': example_dict_no_uR["claim_initial_weight"],
                            'argument_strength': example_dict_no_uR["supporting_argument_dict"]["strength"],
                            'threshold': hyperparameters_no_uR["threshold"],
                            'valid': example_dict_no_uR["valid"],
                            'correct_prediction': example_dict_no_uR["predicted_label"] == example_dict_no_uR["valid"]
                        }
                    )

                else:

                    if example_dict_no_uR["attacking_argument_dict"] == {}:
                        continue

                    attacking_arguments_examples.append(
                        {
                            'claim': example_dict_no_uR["claim"],
                            'argument': example_dict_no_uR["attacking_argument_dict"]["argument"],
                            'argument_supports_claim': False,
                            'claim_strength': example_dict_no_uR["claim_strength"],
                            'claim_initial_weight': example_dict_no_uR["claim_initial_weight"],
                            'argument_strength': example_dict_no_uR["attacking_argument_dict"]["strength"],
                            'threshold': hyperparameters_no_uR["threshold"],
                            'valid': example_dict_no_uR["valid"],
                            'correct_prediction': example_dict_no_uR["predicted_label"] == example_dict_no_uR["valid"],
                        }
                    )

                weighing_examples.append(
                    {
                        'experiment_id_no_uR': experiment_id_no_uR,
                        'experiment_id_uR': experiment_id_uR,
                        'claim': example_dict_no_uR["claim"],
                        'valid': example_dict_no_uR["valid"],
                        'supporting_argument': example_dict_no_uR["supporting_argument_dict"]["argument"],
                        'attacking_argument': example_dict_no_uR["attacking_argument_dict"]["argument"],
                        'supporting_strength_no_uR': example_dict_no_uR["supporting_argument_dict"]["strength"],
                        'attacking_strength_no_uR': example_dict_no_uR["attacking_argument_dict"]["strength"],
                        'claim_initial_weight_no_uR': example_dict_no_uR["claim_initial_weight"],
                        'claim_strength_no_uR': example_dict_no_uR["claim_strength"],
                        'threshold_no_uR': hyperparameters_no_uR["threshold"],
                        'correct_prediction_no_uR': example_dict_no_uR["predicted_label"] == example_dict_no_uR["valid"],
                        'supporting_strength_uR': example_dict_uR["supporting_argument_dict"]["strength"],
                        'attacking_strength_uR': example_dict_uR["attacking_argument_dict"]["strength"],
                        'claim_initial_weight_uR': example_dict_uR["claim_initial_weight"],
                        'claim_strength_uR': example_dict_uR["claim_strength"],
                        'threshold_uR': hyperparameters_uR["threshold"],
                        'correct_prediction_uR': example_dict_uR["predicted_label"] == example_dict_uR["valid"],
                    }
                )

        folder_name = f"examples/{model_name}/{experiment_id_no_uR}"

        os.makedirs(folder_name, exist_ok=True)

        with open(f"{folder_name}/supporting_arguments_examples.json", 'w') as f:
            json.dump(supporting_arguments_examples, f)

        with open(f"{folder_name}/attacking_arguments_examples.json", 'w') as f:
            json.dump(attacking_arguments_examples, f)

        with open(f"{folder_name}/weighing_examples.json", 'w') as f:
            json.dump(weighing_examples, f)
