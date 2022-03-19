import inquirer
from inquirer.themes import GreenPassion

VALID_WEIGHT_SUM_ADVISE = "the sum of the weights must be 100"
INVALID_WEIGHT_SUM_ERROR = "Invalid weights," + VALID_WEIGHT_SUM_ADVISE

VALID_WEIGHT_ADVISE = "the weight must be between 0 and 100"
INVALID_WEIGHT_VALUE = "Invalid weight, " + VALID_WEIGHT_ADVISE

VALID_CHECKBOX_ERROR = "Select at least one Check-Box"


def define_weight(data_key, data_name):
    while True:
        weights = [
            inquirer.Text(
                data_key,
                message="Enter the weight of "
                + data_name
                + f" ({VALID_WEIGHT_SUM_ADVISE})",
            )
        ]
        defined_weight = inquirer.prompt(weights, theme=GreenPassion())
        if validate_weight_value(int(defined_weight[data_key])):
            break
        print(INVALID_WEIGHT_VALUE)

    return defined_weight


def validate_weight_sum(items):
    sum = 0
    for x in items:
        for k, v in x.items():
            sum += int(v)

    if sum != 100:
        return False
    else:
        return True


def validate_weight_value(weight):
    if weight > 100 or weight <= 0:
        return False
    else:
        return True


def validate_check_box_input(selected):
    if selected > 0:
        return True
    else:
        return False


def sublevel_cli(level_name, level_alias, sublevels, available_pre_config):
    reverse_sublevel = {v["name"]: k for k, v in available_pre_config.items()}

    sublevels_answer = [
        inquirer.Checkbox(
            "sublevels",
            message="Choose the " + level_alias + " for " + level_name,
            choices=[available_pre_config[x]["name"] for x in sublevels],
        )
    ]
    user_sublevels = inquirer.prompt(sublevels_answer, theme=GreenPassion())

    user_sublevels = [reverse_sublevel[x] for x in user_sublevels["sublevels"]]

    return user_sublevels


def define_characteristic(available_pre_config):
    characteristics = available_pre_config["characteristics"]

    if len(characteristics) == 1:
        user_characteristics = list(characteristics.keys())
        characteristics_weights = [{user_characteristics[0]: 100}]
        return user_characteristics, characteristics_weights

    reversed_characteristics = {v["name"]: k for k, v in characteristics.items()}
    while True:
        characteristics_answer = [
            inquirer.Checkbox(
                "characteristics",
                message="Choose the characteristics",
                choices=[x["name"] for _, x in characteristics.items()],
            )
        ]

        user_characteristics = inquirer.prompt(
            characteristics_answer, theme=GreenPassion()
        )

        if validate_check_box_input(len(user_characteristics["characteristics"])):
            break
        else:
            print(VALID_CHECKBOX_ERROR)

    user_characteristics = [
        reversed_characteristics[x] for x in user_characteristics["characteristics"]
    ]

    if len(user_characteristics) == 1:
        print("\nOnly one characteristic selected, no need to define weights")
        characteristics_weights = [{user_characteristics[0]: 100}]
        return user_characteristics, characteristics_weights

    characteristics_weights = []

    while True:
        for x in user_characteristics:
            characteristics_weights.append(define_weight(x, characteristics[x]["name"]))

        if validate_weight_sum(characteristics_weights):
            break
        else:
            print(INVALID_WEIGHT_SUM_ERROR)
            characteristics_weights = []

    return user_characteristics, characteristics_weights


def define_sublevel(user_levels, available_pre_config, level_key, sublevel_key):
    sublevels = available_pre_config[sublevel_key]

    if len(sublevels) == 1:
        user_sublevels = list(sublevels.keys())
        sublevels_weights = [{user_sublevels[0]: 100}]
        return user_sublevels, sublevels_weights

    selected_sublevels = []
    sublevels_weights = []

    for x in user_levels:
        if len(available_pre_config[level_key][x][sublevel_key]) == 1:
            local_selected_sublevels = available_pre_config[level_key][x][sublevel_key]
            local_selected_weights = [{local_selected_sublevels[0]: 100}]
            print(
                "\nOnly one %s (%s) available, no need to select or define weights\n"
                % (
                    sublevel_key,
                    available_pre_config[sublevel_key][local_selected_sublevels[0]][
                        "name"
                    ],
                )
            )

        else:
            while True:
                local_selected_sublevels = sublevel_cli(
                    available_pre_config[level_key][x]["name"],
                    sublevel_key,
                    available_pre_config[level_key][x][sublevel_key],
                    available_pre_config[sublevel_key],
                )

                if validate_check_box_input(len(local_selected_sublevels)):
                    break
                else:
                    print(VALID_CHECKBOX_ERROR)

            local_selected_weights = []

            while True:
                for y in local_selected_sublevels:
                    local_selected_weights.append(
                        define_weight(y, available_pre_config[sublevel_key][y]["name"])
                    )

                if validate_weight_sum(local_selected_weights):
                    break
                else:
                    print(INVALID_WEIGHT_SUM_ERROR)
                    local_selected_weights = []

        selected_sublevels.append(local_selected_sublevels)
        sublevels_weights.append(local_selected_weights)

    return selected_sublevels, sublevels_weights
