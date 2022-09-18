import struct
import json

formats = {703808: 'cf1', 703809: 'cf2'}
third_octave = [25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 320, 400, 500, 640, 800, 1000, 1250, 1600, 2000,
                2500, 3200, 4000, 5000, 6400, 8000, 10000, 12500, 16000, 20000]
octave = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
license_type = ["None", "Manufacturer", "ThirdParty", "Research", "ResandDev", "CLFDev"]
balloon_reference = ["Absolute", "Relative", "Arbitrary"]
radiation_type = ["HalfSphere", "FullSphere"]
lsp_type = ["Passive", "Active", "Powered"]
symmetry_type = ["Full", "Vertical", "Horizontal", "None", "Rotational", "Polar"]
total_max_input_type = ["Power", "Voltage"]
total_max_input_method = ["AES2_1984", "IEC_268_1", "EIA_426_B", "CUSTOM"]
dxf_units = ["MM", "CM", "DM", "M", "IN", "FT"]
dxf_direction = ["XNEG", "XPOS", "YNEG", "YPOS", "ZNEG", "ZPOS"]

def read_uint32(fstream):
    return struct.unpack('I', fstream.read(4))[0]


def read_float(fstream):
    return struct.unpack('f', fstream.read(4))[0]


def read_chars(fstream, length):
    return fstream.read(length).replace(b'\x00', b'').decode()


class ClfReader:
    def __init__(self):
        self.file_data = {}

    def parse_file(self, fstream):
        self.file_data = {}
        file_header = {}
        header_file_info = {}
        try:
            header_file_info["id"] = formats[read_uint32(fstream)]
        except KeyError:
            raise IOError("Unidentified CLF file type")
        header_file_info["version"] = read_uint32(fstream)
        header_file_info["draft"] = read_uint32(fstream)
        header_file_info["bin_version"] = read_uint32(fstream)
        header_file_info["reader"] = read_uint32(fstream)
        header_file_info["reader_version"] = read_chars(fstream, 8)
        header_file_info["checksum"] = read_uint32(fstream)
        header_file_info["magic"] = read_uint32(fstream)
        header_file_info["header_extra"] = [read_uint32(fstream) for _ in range(4)]
        file_header["header"] = header_file_info
        file_header["hdr_license"] = read_chars(fstream, 256)
        file_header["hdr_license_type"] = read_uint32(fstream)
        file_header["hdr_license_type_name"] = license_type[file_header["hdr_license_type"]]
        file_header["hdr_model_name"] = read_chars(fstream, 256)
        file_header["hdr_model_manufacturer"] = read_chars(fstream, 256)
        file_header["hdr_description"] = read_chars(fstream, 256)
        file_header["hdr_given_flags"] = read_uint32(fstream)
        file_header["hdr_has_colors"] = bool(file_header["hdr_given_flags"] & 1)
        file_header["hdr_has_mounting"] = bool(file_header["hdr_given_flags"] & 2)
        file_header["hdr_has_measurement_note"] = bool(file_header["hdr_given_flags"] & 4)
        file_header["hdr_has_measurement_environment"] = bool(file_header["hdr_given_flags"] & 8)
        file_header["hdr_has_measurement_distance"] = bool(file_header["hdr_given_flags"] & 16)
        file_header["hdr_has_sensitivity_info"] = bool(file_header["hdr_given_flags"] & 128)
        file_header["hdr_has_impedance_info"] = bool(file_header["hdr_given_flags"] & 256)
        file_header["hdr_has_axial_spectrum"] = bool(file_header["hdr_given_flags"] & 1024)
        file_header["hdr_has_axial_spectrum_info"] = bool(file_header["hdr_given_flags"] & 2048)
        file_header["hdr_has_cabinet_system"] = bool(file_header["hdr_given_flags"] & 4096)
        file_header["hdr_colors"] = read_chars(fstream, 256)
        file_header["hdr_mounting"] = read_chars(fstream, 256)
        file_header["hdr_weight"] = read_float(fstream)
        file_header["hdr_website"] = read_chars(fstream, 256)
        file_header["hdr_measure_contact"] = read_chars(fstream, 256)
        file_header["hdr_measure_email"] = read_chars(fstream, 256)
        file_header["hdr_measure_date"] = read_chars(fstream, 16)
        file_header["hdr_text_file_date"] = read_chars(fstream, 16)
        file_header["hdr_bin_file_date"] = read_chars(fstream, 16)
        file_header["hdr_measure_note"] = read_chars(fstream, 256)
        file_header["hdr_measure_environment"] = read_chars(fstream, 256)
        file_header["hdr_measure_distance"] = read_float(fstream)
        file_header["hdr_lsp_type"] = read_uint32(fstream)
        file_header["hdr_lsp_type_name"] = lsp_type[file_header["hdr_lsp_type"]]
        file_header["hdr_type_info"] = read_chars(fstream, 256)
        file_header["hdr_sensitivity_info"] = read_chars(fstream, 256)
        file_header["hdr_impedance_info"] = read_chars(fstream, 256)
        file_header["hdr_total_maximum_in_type"] = read_uint32(fstream)
        file_header["hdr_total_maximum_in_type_name"] = total_max_input_type[file_header["hdr_total_maximum_in_type"]]
        file_header["hdr_total_maximum_in"] = read_float(fstream)
        file_header["hdr_total_maximum_in_method"] = read_uint32(fstream)
        file_header["hdr_total_maximum_in_method_name"] = total_max_input_method[
            file_header["hdr_total_maximum_in_method"]]
        file_header["hdr_total_maximum_in_info"] = read_chars(fstream, 256)
        file_header["hdr_total_maximum_in_custom_spectrum"] = [read_float(fstream) for _ in range(30)]
        file_header["hdr_avg_impedance"] = read_float(fstream)
        file_header["hdr_total_axial_spectrum"] = [read_float(fstream) for _ in range(30)]
        file_header["hdr_total_axial_spectrum_info"] = read_chars(fstream, 256)
        file_header["hdr_radiation"] = read_uint32(fstream)
        file_header["hdr_radiation_name"] = radiation_type[file_header["hdr_radiation"]]
        file_header["hdr_symmetry"] = read_uint32(fstream)
        file_header["hdr_symmetry_name"] = symmetry_type[file_header["hdr_symmetry"]]
        file_header["hdr_balloon_reference"] = read_uint32(fstream)
        file_header["hdr_balloon_reference_name"] = balloon_reference[file_header["hdr_balloon_reference"]]
        file_header["hdr_cab_flags"] = read_uint32(fstream)
        file_header["hdr_cab_has_rect"] = bool(file_header["hdr_cab_flags"] & 1)
        file_header["hdr_cab_has_trap"] = bool(file_header["hdr_cab_flags"] & 2)
        file_header["hdr_cab_has_edges"] = bool(file_header["hdr_cab_flags"] & 4)
        file_header["hdr_cab_has_face_edges"] = bool(file_header["hdr_cab_flags"] & 8)
        file_header["hdr_cab_has_dxf"] = bool(file_header["hdr_cab_flags"] & 16)
        file_header["hdr_cab_rect_min"] = [read_float(fstream) for _ in range(3)]
        file_header["hdr_cab_rect_max"] = [read_float(fstream) for _ in range(3)]
        file_header["hdr_cab_trap"] = {"xmin": read_float(fstream), "xmax": read_float(fstream),
                                       "yminr": read_float(fstream), "xmaxr": read_float(fstream),
                                       "yminf": read_float(fstream), "ymaxf": read_float(fstream),
                                       "zminr": read_float(fstream), "zmaxr": read_float(fstream),
                                       "zminf": read_float(fstream), "zmaxf": read_float(fstream)}
        file_header["hdr_dxf_unit"] = read_uint32(fstream)
        file_header["hdr_dxf_unit_name"] = dxf_units[file_header["hdr_dxf_unit"]]
        file_header["hdr_dxf_origin"] = [read_float(fstream) for _ in range(3)]
        file_header["hdr_dxf_axis"] = read_uint32(fstream)
        file_header["hdr_dxf_axis_name"] = dxf_direction[file_header["hdr_dxf_axis"]]
        file_header["hdr_dxf_up"] = read_uint32(fstream)
        file_header["hdr_dxf_up_name"] = dxf_direction[file_header["hdr_dxf_up"]]
        file_header["hdr_reserved_1"] = read_chars(fstream, 48)
        self.file_data["header"] = file_header
        file_balloon_data = {}
        if header_file_info["id"] == "cf1":
            file_balloon_data["size"] = 29168
            file_balloon_data["n_bands"] = 10
            file_balloon_data["n_rot"] = 36
            file_balloon_data["n_arc"] = 19
            file_balloon_data["frequencies"] = octave
            file_balloon_data["accuracy_angle"] = 10
        else:
            file_balloon_data["size"] = 329408
            file_balloon_data["n_bands"] = 30
            file_balloon_data["n_rot"] = 72
            file_balloon_data["n_arc"] = 37
            file_balloon_data["accuracy_angle"] = 5
            file_balloon_data["frequencies"] = third_octave
        file_balloon_data["rotation_angle"] = [i*file_balloon_data["accuracy_angle"]
                                               for i in range(file_balloon_data["n_rot"])]
        file_balloon_data["arc_angle"] = [90 - i * file_balloon_data["accuracy_angle"]
                                          for i in range(file_balloon_data["n_arc"])]
        file_balloon_data["min_band"] = read_uint32(fstream)
        file_balloon_data["max_band"] = read_uint32(fstream)
        file_balloon_data["measure_voltage"] = [read_float(fstream) for _ in range(file_balloon_data["n_bands"])]
        file_balloon_data["sensitivity"] = [read_float(fstream) for _ in range(file_balloon_data["n_bands"])]
        file_balloon_data["impedance"] = [read_float(fstream) for _ in range(file_balloon_data["n_bands"])]
        file_balloon_data["6db_hor_left"] = [read_float(fstream) for _ in range(file_balloon_data["n_bands"])]
        file_balloon_data["6db_hor_right"] = [read_float(fstream) for _ in range(file_balloon_data["n_bands"])]
        file_balloon_data["6db_ver_upper"] = [read_float(fstream) for _ in range(file_balloon_data["n_bands"])]
        file_balloon_data["6db_ver_lower"] = [read_float(fstream) for _ in range(file_balloon_data["n_bands"])]
        file_balloon_data["axial_q"] = [read_float(fstream) for _ in range(file_balloon_data["n_bands"])]
        file_balloon_data["on_axis"] = [[read_float(fstream) for _ in range(file_balloon_data["n_rot"])] for _ in
                                        range(file_balloon_data["n_bands"])]
        file_balloon_data["balloon"] = [[[read_float(fstream) for _ in range(file_balloon_data["n_arc"])] for _ in
                                         range(file_balloon_data["n_rot"])] for _ in
                                        range(file_balloon_data["n_bands"])]
        file_balloon_data["reserved"] = [read_float(fstream) for _ in range(file_balloon_data["n_bands"])]
        self.file_data["balloon"] = file_balloon_data


file_to_process = "IF2108"
with open("resources/" + file_to_process + ".CF2", 'rb') as stream:
    data = ClfReader()
    data.parse_file(stream)
    # export to JSON
    with open(file_to_process + ".json", 'w') as out_file:
        json.dump(data.file_data, out_file, indent=2)
    # export directivity to csv
    with open(file_to_process + ".csv", 'w') as out_file:
        out_file.write("frequency, rotation, arc, attenuation\n")
        for frequency, frequency_data in \
                zip(data.file_data["balloon"]["frequencies"], data.file_data["balloon"]["balloon"]):
            for rotation_angle, rotation_data in zip(data.file_data["balloon"]["rotation_angle"], frequency_data):
                for arc_angle, arc_data in zip(data.file_data["balloon"]["arc_angle"], rotation_data):
                    out_file.write("%g,%d,%d,%.2f\n" % (frequency, rotation_angle, arc_angle, arc_data))
