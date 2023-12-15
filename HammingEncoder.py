from typing import List
from bitarray import bitarray
import math

class HammingEncoder:
    def encode(self, data: bytes) -> bytes:
        bits = bitarray()
        bits.frombytes(data)

        encoded_bits = []

        for i in range(0, len(bits), 4):
            data_bits = [bits[i + j] if i + j < len(bits) else False for j in range(4)]

            p1 = data_bits[0] ^ data_bits[1] ^ data_bits[3]
            p2 = data_bits[0] ^ data_bits[2] ^ data_bits[3]
            p3 = data_bits[1] ^ data_bits[2] ^ data_bits[3]

            encoded_bits.extend([p1, p2, data_bits[0], p3, data_bits[1], data_bits[2], data_bits[3]])

        encoded_data = bitarray(encoded_bits)
        encoded_byte_array = bytearray(encoded_data.tobytes())

        return encoded_byte_array



import tkinter as tk
from tkinter import filedialog

class EncodingForm:
    def __init__(self, root):
        self.root = root
        root.title("EncodingForm")

        self.encoder = HammingEncoder()

        self.btn_browse = tk.Button(root, text="Browse", command=self.browse)
        self.btn_browse.pack(pady=10)

        self.btn_encode = tk.Button(root, text="Encode", command=self.encode)
        self.btn_encode.pack(pady=10)

        self.txt_file_name = tk.Entry(root)
        self.txt_file_name.pack(pady=10)

    def browse(self):
        file_path = filedialog.askopenfilename()
        self.txt_file_name.delete(0, tk.END)
        self.txt_file_name.insert(0, file_path)

    def encode(self):
        input_file_name = self.txt_file_name.get()
        output_file_name = input_file_name + ".encoded"

        try:
            with open(input_file_name, "rb") as file:
                file_data = bytearray(file.read())

            encoded_data = self.encoder.encode(file_data)

            with open(output_file_name, "wb") as output_file:
                output_file.write(encoded_data)

            tk.messagebox.showinfo("Success", f"File successfully encoded to {output_file_name}")
        except Exception as ex:
            tk.messagebox.showerror("Error", f"Error: {ex}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncodingForm(root)
    root.mainloop()
