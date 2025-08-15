import json

semantics = "dfquad"
threshold = 0.8
claim_strength_calculation_type = "estimated"
job_id = 1384111
file_path = f"results/{job_id}.json"

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

supporting_arguments_examples = []
attacking_arguments_examples = []
weighing_examples = []

for example in data["data"][semantics]:
    valid = example["valid"] == 1

    arguments = example[claim_strength_calculation_type]['bag']['arguments']
    claim_dict = arguments['db0']
    claim = claim_dict["argument"]
    claim_initial_weight = claim_dict["initial_weight"]
    claim_strength = claim_dict["strength"]
    predicted_label = claim_strength > threshold

    if len(claim) < 1000:
        if example[claim_strength_calculation_type]['prediction'] > threshold:
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

with open(f"supporting_arguments_examples__{job_id}.json", 'w') as f:
    json.dump(supporting_arguments_examples, f)

with open(f"attacking_arguments_examples__{job_id}.json", 'w') as f:
    json.dump(attacking_arguments_examples, f)

with open(f"weighing_examples__{job_id}.json", 'w') as f:
    json.dump(weighing_examples, f)
