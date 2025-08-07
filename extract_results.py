import json

semantics = "dfquad"
threshold = 0.8
claim_strength_calculation_type = "estimated"

with open("results/full_results__1384111__dev.json", "r", encoding="utf-8") as f:
    data = json.load(f)

examples_for_checking_correctness_of_supporting_arguments_generated = []
examples_for_checking_correctness_of_attacking_arguments_generated = []
examples_for_checking_correct_weighing_of_arguments = []

for example in data["data"][semantics]:
    valid = example["valid"]

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

            examples_for_checking_correctness_of_supporting_arguments_generated.append(
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

            examples_for_checking_correctness_of_attacking_arguments_generated.append(
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

        examples_for_checking_correct_weighing_of_arguments.append(
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

with open("examples_for_checking_correctness_of_supporting_arguments_generated.json", 'w') as f:
    json.dump(examples_for_checking_correctness_of_supporting_arguments_generated, f)

with open("examples_for_checking_correctness_of_attacking_arguments_generated.json", 'w') as f:
    json.dump(examples_for_checking_correctness_of_attacking_arguments_generated, f)

with open("examples_for_checking_correct_weighing_of_arguments.json", 'w') as f:
    json.dump(examples_for_checking_correct_weighing_of_arguments, f)
