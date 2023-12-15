import os
from typing import Tuple, List
from bitarray import bitarray
import math

class HammingDecoder:
    def decode(self, encoded_data: bytes) -> Tuple[bytes, List[int]]:
        bits = bitarray()
        bits.frombytes(encoded_data)

        decoded_bits = []
        error_positions = []

        for i in range(0, len(bits), 7):
            code_bits = [bits[i + j] if i + j < len(bits) else False for j in range(7)]

            p1 = code_bits[0] ^ code_bits[2] ^ code_bits[4] ^ code_bits[6]
            p2 = code_bits[1] ^ code_bits[2] ^ code_bits[5] ^ code_bits[6]
            p3 = code_bits[3] ^ code_bits[4] ^ code_bits[5] ^ code_bits[6]

            error_position = (p1 << 0) | (p2 << 1) | (p3 << 2)

            if error_position != 0:
                error_positions.append(i + error_position - 1)
                code_bits[error_position - 1] = not code_bits[error_position - 1]

            if i // 7 * 4 < (len(bits) + 3) // 7 * 4:
                decoded_bits.extend([code_bits[2], code_bits[4], code_bits[5], code_bits[6]])

        decoded_data = bitarray(decoded_bits)
        decoded_byte_array = bytearray(decoded_data.tobytes())

        return decoded_byte_array, error_positions


import tkinter as tk
from tkinter import filedialog

class DecodingForm:
    def __init__(self, root):
        self.root = root
        root.title("DecodingForm")

        self.decoder = HammingDecoder()

        self.btn_browse = tk.Button(root, text="Browse", command=self.browse)
        self.btn_browse.pack(pady=10)

        self.btn_decode = tk.Button(root, text="Decode", command=self.decode)
        self.btn_decode.pack(pady=10)

        self.txt_file_name = tk.Entry(root)
        self.txt_file_name.pack(pady=10)

    def browse(self):
        file_path = filedialog.askopenfilename()
        self.txt_file_name.delete(0, tk.END)
        self.txt_file_name.insert(0, file_path)

    def decode(self):
        input_file_name = self.txt_file_name.get()
        output_file_name = self.get_decoded_file_name(input_file_name)

        try:
            with open(input_file_name, "rb") as file:
                file_data = bytearray(file.read())

            decoded_data, error_positions = self.decoder.decode(file_data)

            with open(output_file_name, "wb") as output_file:
                output_file.write(decoded_data)

            message = f"File successfully decoded to {output_file_name}\n"
            if error_positions:
                message += "Errors corrected at positions: " + ", ".join(map(str, error_positions))
            else:
                message += "No errors detected."

            tk.messagebox.showinfo("Success", message)
        except Exception as ex:
            tk.messagebox.showerror("Error", f"Error: {ex}")

    def get_decoded_file_name(self, encoded_file_name):
        without_encoded_extension = (
            encoded_file_name[:-8] if encoded_file_name.endswith(".encoded") else encoded_file_name
        )

        directory = os.path.dirname(without_encoded_extension)
        file_name_without_ext = os.path.splitext(os.path.basename(without_encoded_extension))[0]
        extension = os.path.splitext(without_encoded_extension)[1]

        new_file_name = os.path.join(directory, f"{file_name_without_ext}_decoded{extension}")
        return new_file_name

if __name__ == "__main__":
    root = tk.Tk()
    app = DecodingForm(root)
    root.mainloop()
