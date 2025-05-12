import struct
import csv
import os
from typing import List

class Field:
    def __init__(self, offset: int, size: int, ftype: int):
        self.offset = offset
        self.size = size
        self.ftype = ftype

def convert_to_utf8(raw: bytes) -> str:
    return raw.decode('iso-8859-1').strip()

def parse_header(dat_path: str):
    with open(dat_path, 'rb') as f:
        header = f.read(512)
        record_count = struct.unpack('<I', header[8:12])[0]
        record_size = struct.unpack('<H', header[78:80])[0]
        num_fields = header[89]

        fields: List[Field] = []
        for i in range(num_fields):
            base = 196 + (i * 8)
            offset = struct.unpack('<H', header[base:base+2])[0] - 1
            size = header[base+3]
            ftype = header[base+4]
            fields.append(Field(offset, size, ftype))

        return record_count, record_size, fields

def extrair_numero(raw: bytes) -> int:
    bytes_uteis = [b for b in raw if b != 0]
    if not bytes_uteis:
        return 0
    # Usa o maior byte útil e interpreta o valor hex como número
    hex_str = f"{max(bytes_uteis):02x}"
    return int(hex_str)


def parse_record(record: bytes, fields: List[Field], separator='|') -> str:
    row = []
    for field in fields:
        raw = record[field.offset:field.offset + field.size]
        if field.ftype == 0:  # String
            row.append(convert_to_utf8(raw))
        elif field.ftype == 1:  # Numérico            
            val = int.from_bytes(raw[1:], byteorder='little') if len(raw) > 1 else 0
            row.append(str(val))
        elif field.ftype == 2:  # Data
            jd = int.from_bytes(raw, byteorder='little')
            if jd > 100000:
                jd -= 465263
                row.append(str(jd))
            else:
                row.append("01/01/1000")
        else:
            row.append('UNKNOWN')
    return separator.join(row)

def read_tag_file(tag_path: str) -> List[str]:
    with open(tag_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    columns = [line.strip().strip('\x1a') for line in lines if line.strip() and ord(line[0]) != 26]
    return columns

def dat_to_csv(dat_path: str, csv_path: str, tag_path: str = None, separator='|'):
    record_count, record_size, fields = parse_header(dat_path)
    headers = [f"campo_{i+1}" for i in range(len(fields))]
    if tag_path and os.path.exists(tag_path):
        try:
            tag_headers = read_tag_file(tag_path)
            if len(tag_headers) == len(fields):
                headers = tag_headers
        except Exception:
            pass  # fallback para headers genéricos

    with open(dat_path, 'rb') as fin, open(csv_path, 'w', newline='', encoding='utf-8') as fout:
        fin.seek(512)
        writer = csv.writer(fout, lineterminator='\n')
        writer.writerow(headers)

        for _ in range(record_count):
            record = fin.read(record_size)
            if not record or len(record) < record_size:
                break
            if all(b == 0 for b in record):
                continue

            first_numeric_field = next((f for f in fields if f.ftype == 1), None)
            if first_numeric_field:
                raw = record[first_numeric_field.offset + 1:first_numeric_field.offset + first_numeric_field.size]
                val = int.from_bytes(raw, byteorder='little')
                if val == 0:
                    continue

            row = parse_record(record, fields, separator)
            writer.writerow([cell for cell in row.split(separator)])

def process_directory(directory: str, output: str, separator='|'):
    # List all .DAT files in the directory
    for filename in os.listdir(directory):
        if filename.upper().endswith('.DAT'):
            dat_path = os.path.join(directory, filename)
            
            # Find corresponding .TAG file
            base_name = os.path.splitext(filename)[0]
            tag_path = os.path.join(directory, f"{base_name}.TAG")
            if not os.path.exists(tag_path):
                tag_path = os.path.join(directory, f"{base_name}.tag")  # Try lowercase
                if not os.path.exists(tag_path):
                    tag_path = None
            
            # Generate output CSV path
            csv_path = os.path.join(output, f"{base_name}.csv")
            
            print(f"Processing {filename}...")
            try:
                dat_to_csv(dat_path, csv_path, tag_path, separator)
                print(f"Successfully created {csv_path}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
