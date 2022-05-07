# DNA Strand Visualizations

def read_data(file_name):
    file = open("./assets/"+file_name, "r")
    return file.read()


# Main function.
if __name__ == '__main__':
    print('DNA Strand Visualizations')
    input_structure = read_data('dna_structure_1.txt')
    print(input_structure)
