import sys

HEADER_FILE = "header.txt"
MULTIPLICATIVE_FACTOR = "multiplicative_factor.txt"
POWER = "power.txt"

header = """

 _______   ________  __       __   ______            _____   ______   _______
/       \ /        |/  \     /  | /      \          /     | /      \ /       \\
$$$$$$$  |$$$$$$$$/ $$  \   /$$ |/$$$$$$  |         $$$$$ |/$$$$$$  |$$$$$$$  |
$$ |  $$ |$$ |__    $$$  \ /$$$ |$$ |  $$ |            $$ |$$ |  $$ |$$ |__$$ |
$$ |  $$ |$$    |   $$$$  /$$$$ |$$ |  $$ |       __   $$ |$$ |  $$ |$$    $$<
$$ |  $$ |$$$$$/    $$ $$ $$/$$ |$$ |  $$ |      /  |  $$ |$$ |  $$ |$$$$$$$  |
$$ |__$$ |$$ |_____ $$ |$$$/ $$ |$$ \__$$ |      $$ \__$$ |$$ \__$$ |$$ |__$$ |
$$    $$/ $$       |$$ | $/  $$ |$$    $$/       $$    $$/ $$    $$/ $$    $$/
$$$$$$$/  $$$$$$$$/ $$/      $$/  $$$$$$/         $$$$$$/   $$$$$$/  $$$$$$$/


"""

def read_values(filename, conversion):
    """
    Reads space-separated values from a file, row by row,
    and applies a conversion function to each.
    The conversion function must accept exactly one string parameter.
    """
    with open(filename, "r") as file_handle:
        lines = file_handle.readlines()
        return [[conversion(val) for val in line.split()] for line in lines]

data_filename = sys.argv[1]
data = read_values(data_filename, float)

print(header)

with open(HEADER_FILE, "r") as constants_file_header_handler:
    const_data = constants_file_header_handler.read()
    print(f"{const_data} \n")
print("Parameters from constant files: ")
with open(MULTIPLICATIVE_FACTOR, "r") as constants_file_factor_handler:
    multiplicative_factor = int(constants_file_factor_handler.read())
    print(f"multiplicative factor : {multiplicative_factor}")
with open(POWER, "r") as constants_file_power_handler:
    power = int(constants_file_power_handler.read())
    print(f"power: {power}")
    print(f"\nResults of {data_filename}:")

for row in data:
    output = []
    for column in row:
        output.append((column * multiplicative_factor) ** power)

    print(output)

