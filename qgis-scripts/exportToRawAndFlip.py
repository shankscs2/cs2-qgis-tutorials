import subprocess

params = {
    'utility' : 'gdal_translate',
    'out_type': '-ot UInt16',
    'out_file_type' : '-of ENVI',
    'scale': '-scale 0 2047 0 65535',
    'outsize' : '-outsize 4096 4096',
    'source' : '[source_path]',
    'destination': '[destination_path].raw'
}

def read_raw_file(input_path):
    with open(input_path, 'rb') as file:
        raw_data = file.read()
    return raw_data

def write_raw_file(output_path, raw_data):
    with open(output_path, 'wb') as file:
        file.write(raw_data)

def flip_horizontal(raw_data, width, height):
    # Assuming each pixel is represented by 2 bytes (16 bits)
    pixel_size = 2
    flipped_data = bytearray()

    for y in range(height):
        for x in range(width - 1, -1, -1):
            start_index = (y * width + x) * pixel_size
            end_index = start_index + pixel_size
            flipped_data.extend(raw_data[start_index:end_index])

    return bytes(flipped_data)

def generate_output_file_path(input_path):
    no_ext = input_path.split(".raw")[0]
    return no_ext + "-flipped.raw"


def export(params):
    subprocess.run([x for x in params.split(" ") if x != ""])


def main(params):
    params_str = " ".join(params.values())
    export(params_str)
    raw_data = read_raw_file(params['source'])
    flipped_data = flip_horizontal(raw_data, 4096, 4096)
    write_raw_file(generate_output_file_path(params['destination']), flipped_data)

main(params)