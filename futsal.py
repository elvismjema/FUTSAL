import sys


# store variables
variables = {}
functions = {}


def evaluate(expression):
    builtins = {
        "ARSENAL": lambda text: text[::-1],
        "LENGTH": lambda text: len(text),
        "INT": lambda value: int(value),
        "STR": lambda value: str(value),
    }

    try:
        return eval(expression, builtins, variables)
    except:
        return expression.strip('"')


def execute_lines(lines, variables, functions=functions):
    skip_block = False
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        i += 1

        if not line:
            continue  # skip empty lines

        parts = line.split()
        command = parts[0]

        if skip_block:
            if command == "FULLTIME":
                skip_block = False
            elif command == "SUB":
                skip_block = False
            continue

        # SHOUT command
        if command == "SHOUT":
            value = " ".join(parts[1:])

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

            value = evaluate(expression)

            variables[var_name] = value

        # CHECKIN command
        elif command == "CHECKIN":
            condition = " ".join(parts[1:])
            try:
                result = eval(condition, {}, variables)
            except:
                result = False

            if not result:
                skip_block = True

        # SUB command
        elif command == "SUB":
            skip_block = True

        # REPEAT command
        elif command == "REPEAT":
            condition = " ".join(parts[1:])
            body = []
            while i < len(lines):
                bline = lines[i].strip()
                i += 1
                bparts = bline.split() if bline else []
                if bparts and bparts[0] == "FULLTIME":
                    break
                body.append(bline)
            while True:
                try:
                    if not eval(condition, {}, variables):
                        break
                except:
                    break
                execute_lines(body, variables, functions)

        # PLAY command
        elif command == "PLAY":
            func_name = parts[1]
            body = []
            while i < len(lines):
                bline = lines[i].strip()
                i += 1
                bparts = bline.split() if bline else []
                if bparts and bparts[0] == "FULLTIME":
                    break
                body.append(bline)
            functions[func_name] = body

        # RUN command
        elif command == "RUN":
            func_name = parts[1]
            if func_name in functions:
                execute_lines(functions[func_name], variables, functions)
            else:
                print(f"Error: function '{func_name}' not defined")

        # FULLTIME command
        elif command == "FULLTIME":
            pass

if len(sys.argv) < 2:
    print("Usage: python3 futsal.py <file>")
    exit()

filename = sys.argv[1]

with open(filename, "r") as file:
    lines = file.readlines()

execute_lines(lines, variables)
