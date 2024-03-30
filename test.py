import pymem
import re


def pattern_to_regex(pattern):
    """Convert a hexadecimal pattern with wildcards to a regex pattern."""
    regex_pattern = ""
    for char in pattern.split('x'):
        if char:  # If the segment is not empty, process as hexadecimal
            byte_str = bytes.fromhex(char)
            regex_pattern += ''.join(f'\\x{b:02x}' for b in byte_str)
        regex_pattern += '.'  # Add a dot for each wildcard 'x'
    regex_pattern = regex_pattern.rstrip('.')  # Remove the last dot added extra
    return regex_pattern


def find_pattern(process_name, pattern):
    pm = pymem.Pymem(process_name)
    regex_pattern = pattern_to_regex(pattern)
    regex = re.compile(regex_pattern.encode())

    # Iterate over all memory regions (simplified approach)
    for module in pm.list_modules():
        base = module.lpBaseOfDll
        size = module.SizeOfImage
        memory = pm.read_bytes(base, size)

        match = regex.search(memory)
        if match:
            print(f"Pattern found at address: {hex(base + match.start())}")
            return base + match.start()
    return None


# Example usage

pm = pymem.Pymem('HoloCure.exe')

# static address of global vars 7FF6AD13EBE8
# static address of the object array 7FF6AD147870 # player manager is in here somehwere
# process_name = 'HoloCure.exe'  # Replace with your actual process name
# pattern = '4C' + 'x' * 12 + '45' + 'x' * 4 + '49' + 'x' * 4 + '4C'
# obj_array_base = 0x7FF760E57870
# spacing = 16
# object_num = 12
# number_of_objects = pm.read_int(obj_array_base + 0x08 - 1)
# object_array_pointer_value = pm.read_int(1466889032016)
# print(object_array_pointer_value)

# object_array_address = 0x7ff75ffb1c4a
# print(hex(140700443941962))
# array_pointer_value = pm.read_int(object_array_address) + 3
# print(array_pointer_value)
# object_number_address = array_pointer_value + 12
# number_of_objects = pm.read_int(object_number_address) -1

#module_name = "HoloCure.exe"  # Change this to the actual module name
# try:
# module = pymem.process.module_from_name(pm.process_handle, module_name)
# print(module)
# base_address = module.lpBaseOfDll
# except :
#     print(f"Module {module_name} not found.")
#     base_address = None
#
# if base_address is not None:
#     symbol_offset = 140700443941965  # Example offset
#     symbol_address = base_address + symbol_offset
#
#     # Reading an integer as an example
#     try:
#         value = pm.read_int(symbol_address)
#         print(f"Value at {hex(symbol_address)}: {value}")
#     except Exception as e:
#         print(f"Failed to read memory at {hex(symbol_address)}: {str(e)}")
#

#------------------------------------------------------------------------------

array_pointer = pm.read_double(0x1CF51C12E70)
print(array_pointer)
# print(hex(array_base))
# print(number_of_objects)
# print(f"array_pointer is {array_pointer}")
#
# def read_name(adress):
#     attributes_pointer = adress + 24
#     attr_pointer_value = pm.read_longlong(attributes_pointer)
#     name_pointer = attr_pointer_value + 0x00
#     name_pointer_value = pm.read_longlong(name_pointer)
#     name_value = pm.read_string(name_pointer_value, 50)
#     return name_value
#
# print(f"Will iterate {number_of_objects} objects")
# for object_index in range(number_of_objects):
#     #print(f"object number: {object_index}")
#     object_address = pm.read_longlong(array_pointer + object_index * 16)
#     #print(f"reading name with adress: {object_address}")
#     object_name = read_name(object_address)
#
#     #print(object_address)
#     print(object_name)
