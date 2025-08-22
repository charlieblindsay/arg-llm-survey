import json
import os
import glob

results_folder = "results"

experiment_dict = {
    "qwen_14b": ["1406146", "1411483"],
    "qwen_72b": ["196588", "196589"]
}

for model_name, experiment_ids in experiment_dict.items():
    for experiment_id in experiment_ids:
        json_file_path = glob.glob(os.path.join(results_folder, model_name, f"{experiment_id}.json"))

        with open(json_file_path[0], "r", encoding="utf-8") as f:
            data = json.load(f)

        semantics = data.get('arguments', {}).get('semantics')
        claim_strength_method = data.get('arguments', {}).get('claim_strength_calc_method')
        threshold = data.get('arguments', {}).get('threshold')

        supporting_arguments_examples = []
        attacking_arguments_examples = []
        weighing_examples = []

        for example in data["data"][semantics]:
            valid = example["valid"] == 1

            arguments = example[claim_strength_method]['bag']['arguments']
            claim_dict = arguments['db0']
            claim = claim_dict["argument"]
            claim_initial_weight = claim_dict["initial_weight"]
            claim_strength = claim_dict["strength"]
            predicted_label = claim_strength > threshold

            if len(claim) < 1000:
                if valid:
                    argument_dict = arguments['Sdb0<-d1b1']
                    argument_text = argument_dict["argument"]
                    argument_strength = argument_dict["strength"]

                    supporting_arguments_examples.append(
                        {
                            'claim': claim,
                            'argument': argument_text,
                            'argument_supports_claim': True,
                            'claim_strength': claim_strength,
                            'claim_initial_weight': claim_initial_weight,
                            'argument_strength': argument_strength,
                            'threshold': threshold,
                            'valid': valid,
                            'correct_prediction': predicted_label == valid
                        }
                    )
                else:
                    argument_dict = arguments['Adb0<-d1b1']
                    argument_text = argument_dict["argument"]
                    argument_strength = argument_dict["strength"]

                    attacking_arguments_examples.append(
                        {
                            'claim': claim,
                            'argument': argument_text,
                            'argument_supports_claim': False,
                            'claim_strength': claim_strength,
                            'claim_initial_weight': claim_initial_weight,
                            'argument_strength': argument_strength,
                            'threshold': threshold,
                            'valid': valid,
                            'correct_prediction': predicted_label == valid
                        }
                    )

                weighing_examples.append(
                    {
                        'claim': claim,
                        'supporting_argument': arguments['Sdb0<-d1b1']["argument"],
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
