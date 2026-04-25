# store variables
variables = {}

# open program file
with open("program.txt", "r") as file:
    lines = file.readlines()

# go through each line
for line in lines:
    line = line.strip()  # remove spaces

    if not line:
        continue  # skip empty lines

    parts = line.split()

    command = parts[0]

    # SHOUT command
    if command == "SHOUT":
        value = " ".join(parts[1:])

        # if it's a variable
        if value in variables:
            print(variables[value])
        else:
            # remove quotes if it's text
            print(value.strip('"'))

    # ASK command
    elif command == "ASK":
        var_name = parts[1]
        user_input = input()
        variables[var_name] = user_input

    # CONTROL command
    elif command == "CONTROL":
        var_name = parts[1]
        expression = " ".join(parts[3:])

        # simple eval (we improve later)
        try:
            value = eval(expression, {}, variables)
        except:
            value = expression.strip('"')

        variables[var_name] = value
