import sys
import zipfile
import os
from collections import defaultdict
import heapq

class HuffmanCompression:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_codes = {}
    
    def make_frequency_dict(self, text):
        frequency = defaultdict(int)
        for character in text:
            frequency[character] += 1
        return frequency
    
    def make_heap(self, frequency):
        for key in frequency:
            heapq.heappush(self.heap, [frequency[key], [key, ""]])
    
    def merge_nodes(self):
        while len(self.heap) > 1:
            lo = heapq.heappop(self.heap)
            hi = heapq.heappop(self.heap)
            
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
                
            heapq.heappush(self.heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
    def make_codes(self):
        self.codes = {code[0]: code[1] for code in self.heap[0][1:]}
        self.reverse_codes = {v: k for k, v in self.codes.items()}

def get_all_file_paths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

def main():
    paths = sys.argv[1:]
    
    for path in paths:
        try:
            if os.path.isfile(path):
                base_name = os.path.splitext(os.path.basename(path))[0]
                output_zip = f"_{base_name}.zip"
                files_to_compress = [path]
            else:
                base_name = os.path.basename(path)
                output_zip = f"_{base_name}.zip"
                files_to_compress = get_all_file_paths(path)
            
            with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in files_to_compress:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    huffman = HuffmanCompression()
                    freq = huffman.make_frequency_dict(content)
                    huffman.make_heap(freq)
                    huffman.merge_nodes()
                    huffman.make_codes()
                    
                    if os.path.isfile(path):
                        arcname = os.path.basename(file_path)
                    else:
                        arcname = os.path.relpath(file_path, path)
                    zipf.write(file_path, arcname)
                
        except Exception as e:
            print(f"Error processing {path}: {str(e)}")

if __name__ == "__main__":
    main()
