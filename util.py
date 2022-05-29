
# Read and return strand from a given file
def get_input_strand(file_name):
    file = open("./assets/" + file_name, "r")
    return file.read()
