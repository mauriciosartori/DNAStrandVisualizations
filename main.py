# DNA Stragit bnd Visualizations
# Scripts to Run
# python3 -m pip install numpy
# python3 -m pip install scipy


from nupack import *

def read_data(file_name):
    file = open("./assets/"+file_name, "r")
    return file.read()


# Main function
if __name__ == '__main__':
    print('DNA Strand Visualizations')

    # Parentheses, dot notation
    input_structure = read_data('dna_structure_1.txt')
    print(input_structure)

    # Paying around with Nupack
    # model1 = Model(material='rna', celsius=37)

    a = Domain('A4', 'Domain a')





