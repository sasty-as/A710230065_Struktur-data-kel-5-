import pandas as pd
from collections import deque
import time

class LaptopNode:
    def __init__(self, laptop_id, data):
        self.laptop_id = laptop_id
        self.data = data
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, laptop_id, data):
        if self.root is None:
            self.root = LaptopNode(laptop_id, data)
        else:
            self._insert_iterative(laptop_id, data)

    def _insert_iterative(self, laptop_id, data):
        current = self.root
        while True:
            if laptop_id < current.laptop_id:
                if current.left is None:
                    current.left = LaptopNode(laptop_id, data)
                    break
                current = current.left
            elif laptop_id > current.laptop_id:
                if current.right is None:
                    current.right = LaptopNode(laptop_id, data)
                    break
                current = current.right
            else:
                current.data = data
                break

    def search(self, laptop_id):
        start_time = time.time()
        result = self._search_iterative(laptop_id)
        end_time = time.time()
        result['execution_time'] = end_time - start_time
        return result

    def _search_iterative(self, laptop_id):
        current = self.root
        operations = 0
        depth = 0
        while current is not None:
            operations += 1
            if laptop_id == current.laptop_id:
                return {"found": True, "operations": operations, "data": current.data, "depth": depth}
            elif laptop_id < current.laptop_id:
                current = current.left
            else:
                current = current.right
            depth += 1
        return {"found": False, "operations": operations, "data": None, "depth": depth}

def display_laptop_info(df, search_type):
    if search_type == 'company':
        search_value = input(f"Masukkan {search_type} laptop yang ingin anda cari: ")
        laptop_info = df[df['Company'].str.contains(search_value, case=False, regex=False)]
    elif search_type == 'product':
        search_value = input(f"Masukkan {search_type} laptop yang ingin anda cari: ")
        laptop_info = df[df['Product'].str.contains(search_value, case=False, regex=False)]
    elif search_type == 'harga':
        try:
            harga_min, harga_max = map(float, input("Masukkan rentang harga (contoh: 200 - 400): ").split('-'))
            laptop_info = df[(df['Price_in_euros'] >= harga_min) & (df['Price_in_euros'] <= harga_max)]
        except ValueError:
            print("Format harga tidak valid. Gunakan format: min - max")
            return None

    if laptop_info.empty:
        print(f"Tidak ada laptop yang sesuai dengan kriteria pencarian.")
    else:
        print("Informasi laptop:")
        pd.set_option('display.max_rows', None)  # Menampilkan semua baris
        print(laptop_info[['laptop_ID', 'Company', 'Product', 'TypeName', 'Inches', 'Price_in_euros']].sort_values('laptop_ID'))

    return laptop_info


def main():
    file_path = 'E:/A71_VScode/struktur data/laptop_price.csv'
    try:
        df = pd.read_csv(file_path, encoding='latin-1')
    except FileNotFoundError:
        print(f"File '{file_path}' tidak ditemukan.")
        return
    except UnicodeDecodeError:
        print(f"Tidak dapat membaca file '{file_path}' dengan encoding yang benar.")
        return
    
    print("Nama-nama kolom yang tersedia:")
    print(df.columns.tolist())
    
    search_type = input("Berdasarkan apa laptop yang anda cari? (company/product/harga): ").lower()
    while search_type not in ['company', 'product', 'harga']:
        print("Pilihan tidak valid. Silakan pilih 'company', 'product', atau 'harga'.")
        search_type = input("Berdasarkan apa laptop yang anda cari? (company/product/harga): ").lower()
    
    laptop_info = display_laptop_info(df, search_type)
    
    if laptop_info is not None and not laptop_info.empty:
        bst = BinarySearchTree()
        
        for _, row in laptop_info.iterrows():
            laptop_id = row['laptop_ID']
            data = row[['Company', 'Product', 'TypeName', 'Inches', 'Price_in_euros']].to_dict()
            bst.insert(laptop_id, data)

        search_again = input("Apakah anda ingin melakukan pencarian Binary Search berdasarkan laptop_ID? (y/n): ")
        if search_again.lower() == 'y':
            target_value = int(input("Masukkan laptop_ID yang ingin dicari: "))
            result = bst.search(target_value)
            
            print("Target Node Ditemukan:", result["found"])
            print("Jumlah Operasi:", result["operations"])
            print("Kedalaman Pencarian:", result["depth"])
            print("Waktu Eksekusi (detik):", result["execution_time"])

            if result["found"]:
                print("\nInformasi Laptop:")
                print(f"Laptop ID: {target_value}")
                print(f"Company: {result['data']['Company']}")
                print(f"Product: {result['data']['Product']}")
                print(f"Type: {result['data']['TypeName']}")
                print(f"Inches: {result['data']['Inches']}")
                print(f"Price in Euros: {result['data']['Price_in_euros']}")

if __name__ == "__main__":
    main()