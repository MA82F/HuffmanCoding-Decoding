# libraries
import pickle
import os #handle remove or rename file
from collections import Counter
from tkinter import *
from tkinter import filedialog
#-------------------------------------------------------------------------------------------------------------Nodes---------

class Nodes:  
    def __init__(self, frequency, symbol, left = None, right = None):

        self.frequency = frequency
        self.symbol = symbol
        self.left = left 
        self.right = right
        self.code = ""
#-------------------------------------------------------------------------------------------------------------frequency_dictionary_creator---------

def frequency_dictionary_creator(filePath):                                  
    with open(filePath, 'r') as file:
        return Counter(file.read())
 # line 4 to 7 in another way:
 #                            def frequencyDictionaryCreator(filePath):
 #                                with open(file_path, 'r') as file:
 #                                    file_content = file.read()
 #                                    char_freq = {}
 #                                    for char in file_content:
 #                                        if char in char_freq:
 #                                            char_freq[char] += 1
 #                                        else:
 #                                            char_freq[char] = 1
 #                                    return char_freq
#-------------------------------------------------------------------------------------------------------------huffman_tree_creator---------

def huffman_tree_creator(frequency_dictionary):
    nodes=[]
    for symbol in frequency_dictionary.keys():  
        nodes.append(Nodes(frequency_dictionary[symbol], symbol))
    
    while len(nodes) > 1:  
        # sort increasing 
        nodes = sorted(nodes, key = lambda x: x.frequency)

        right = nodes[0]  
        left = nodes[1]  
      
        left.code = 0  
        right.code = 1  
      
        # combine the 2 smallest nodes 
        newNode = Nodes(left.frequency + right.frequency, left.symbol + right.symbol, left, right)  
      
        nodes.remove(left)  
        nodes.remove(right)  
        nodes.append(newNode)

    return nodes[0]
#-------------------------------------------------------------------------------------------------------------calculate_codes---------

the_codes = dict()
def calculate_codes(node, value = ''):  
    # a huffman code for current node  
    newValue = value + str(node.code)  
  
    if(node.left):  
        calculate_codes(node.left, newValue)  
    if(node.right):  
        calculate_codes(node.right, newValue)  
  
    if(not node.left and not node.right):  
        the_codes[node.symbol] = newValue  
           
    return the_codes
#--------------------------------------------------------------------------------------------------------------check_type_file--------

def check_type_file(file_path,format):
    file_extension = os.path.splitext(file_path)[1]
    if file_extension == format:
        return True
    else:
        return False

#--------------------------------------------------------------------------------------------------------------compress_file--------

def compress_file(file_path, code_dict):
    #another way to convert text by dict to 0&1:
                                                # compressed_data = ""
                                                # with open(file_path, 'r') as file:
                                                #     for char in file.read():
                                                #         compressed_data += code_dict[char]
    with open(file_path, "r") as f:
        text = f.read()
    compressed_text = "".join([code_dict[char] for char in text])
    pad_length = 8 - len(compressed_text) % 8
    padded_compressed_text = compressed_text + "0" * pad_length

    compressed_bytes = bytearray()
    for i in range(0, len(padded_compressed_text), 8):
        byte = padded_compressed_text[i:i+8]
        compressed_bytes.append(int(byte, 2))

    with open(file_path + ".cmp", "wb") as f:
        f.write(compressed_bytes)
#---------------------------------------------------------------------------------------------------------compress----------------

def compress():
    filePath = filepath_label.cget("text")

    if check_type_file(filePath,".txt"):
        frequency_dictionary = frequency_dictionary_creator(filePath)
        huffman_tree = huffman_tree_creator(frequency_dictionary)
        code_dict = calculate_codes(huffman_tree)
        compress_file(filePath, code_dict)
        with open("dictionary.bin","wb") as file:
            pickle.dump(code_dict, file)
        filepath_condition.config(text="the file compressed successfully")
        filepath_label.config(text= filePath + ".cmp")
    else:
        filepath_condition.config(text="the file format not supported")
#----------------------------------------------------------------------------------------------------------huffman_decoding--------

def huffman_decoding(file_path, codes):
    with open(file_path, 'rb') as file:
        encoded_data = file.read()

        # Build the Huffman tree:
                            # tree = {}
                            # for char, code in codes.items():
                            #     node = tree
                            #     for bit in code:
                            #         if bit not in node:
                            #             node[bit] = {}
                            #         node = node[bit]
                            #     node[None] = char
    
    padded_compressed_text = "".join(["{0:08b}".format(byte) for byte in encoded_data])
    compressed_text = padded_compressed_text.rstrip("0")
    print(padded_compressed_text)
    print("2\n")
    print(compressed_text)

    current_code = ""
    original_text = ""
    for char in compressed_text:
        current_code += char
        for key, value in codes.items():
            if current_code == value:
                original_text += key
                current_code = ""
                break
    
    return original_text
#----------------------------------------------------------------------------------------------------------deCompress-----

def deCompress():
    with open("dictionary.bin", 'rb') as file:
        codeDict = pickle.load(file)

    filePath = filepath_label.cget("text")

    if check_type_file(filePath,".cmp"):

        decodeData = huffman_decoding(filePath,codeDict)

        with open(filePath + ".txt","w") as file:
            file.write(decodeData)

        filepath_condition.config(text="the file deCompressed successfully")
        filepath_label.config(text= filePath + ".txt")
    else:
        filepath_condition.config(text="the file format not supported")
#----------------------------------------------------------------------------------------------------------browse------

def browse():
    filename = filedialog.askopenfilename()
    filepath_label.config(text=filename)
#----------------------------------------------------------------------------------------------------------gui---------

page = Tk()
page.geometry("300x200")
page.title("File Compression/Decompression(Huffman Coding)")

browse_button = Button(page, text="Browse", fg='black', bg='lightgray', command=browse,width=25, font = "helvetica 14")
browse_button.pack()

filepath_label = Label(page, text="No file selected.")
filepath_label.pack()

filepath_condition = Label(page, text="NULL")
filepath_condition.pack()

compress_button = Button(page, text="Compress", fg='black', bg='lightgray', command=compress,width=25, font = "helvetica 14")
compress_button.pack()

decompress_button = Button(page, text="Decompress" , fg='black', bg='lightgray', command=deCompress,width=25, font = "helvetica 14")
decompress_button.pack()

page.mainloop()

