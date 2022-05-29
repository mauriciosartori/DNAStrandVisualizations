
# Read and return strand from a given file
def get_input_strand(file_name):
    file = open("./assets/" + file_name, "r")
    return file.read()


# Parse the given string in Run-length encoded dot-parens-plus notation
# into a list with the frequency of each char
# (5.6)5 -> [('(', 5), ('.', 6), (')', 5)]
def parse_dot_parens_plus(string):
    items = []
    expanded_string = ""
    for n, char in enumerate(string):
        if char.isdigit():
            items.append((string[n - 1], int(char)))
        elif n >= 1 and not string[n - 1].isdigit() and char != string[n - 1]:
            items.append((string[n - 1], 1))
    for char, num in items:
        expanded_string += char * num
    return (items, expanded_string)
