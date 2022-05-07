def print_hi(name):
    print(f'DNA Strand Visualizations, {name}')  # Press ⌘F8 to toggle the breakpoint.

if __name__ == '__main__':
    lines = tuple(open('dnaStructure.txt', 'r'))
    for line in lines:
        print_hi('Line says ' + line)
    print_hi('PyCharm')

