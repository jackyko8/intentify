# This file contains the code to read from a text file and return a list of sentences as a list of strings

def get_sentences(file_path=None):
    if file_path is None:
        file_path = 'data/contact_data.txt'
    # print("file_path: {file_path}")
    lines = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        lines = [line.strip() for line in lines]
    except Exception as e:
        pass
    sentences = list(set(lines))
    return sentences, lines
