# DNA Strand Visualizations

def read_data(file_name):
    file = open("./assets/"+file_name, "r")
    return file.read()


# Main function
if __name__ == '__main__':
    print('DNA Strand Visualizations')

    # Parentheses, dot notation
    input_structure = read_data('dnaParenDot_1.txt')
    print(input_structure)

    # DU+ notation
    lines = tuple(read_data('dnaDUPlus_1.txt'))
    for line in lines:
        print('Line says ' + line)

