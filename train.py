from pymem import Pymem
from pymem.process import module_from_name

# Open the process
windows = Pymem("HoloCure.exe")
game_module = module_from_name(windows.process_handle, "HoloCure.exe").lpBaseOfDll

def calculate_address(address, offsets):
    addr = windows.read_longlong(address)
    for cnt, offset in enumerate(offsets):
        if cnt + 1 != len(offsets):
            addr = windows.read_longlong(addr + offset)
    return addr + offsets[-1]

hex_values_to_check = [hex(i) for i in range(10000)]

address = 0x0314EE60
offsets = [0x70, 0x28, 0x90, 0x18, 0x170, 0x98, 0x48, 0x10, 0x9C0, 0x0]
val_address = calculate_address(game_module + address, offsets)
value = windows.read_double(val_address)
print(f"This value is: {value}")

# tracked = [0x5b0]
# address_to_track = list()
# for hex_check in hex_values_to_check:
#     offsets = [0x0, 0x10F0, 0x18, 0x50, 0x10, 0x48, 0x10, 0x1FB0, 0x0, 0x48, 0x10, hex_check, 0x0]
#     addr = calculate_address(game_module + address, offsets)
#     try:
#         my_value = windows.read_double(addr)
#         print(f"Got: {my_value}")
#         if my_value >= 6.9 and my_value <= 1.1:
#             address_to_track.append(hex_check)
#     except:
#         continue

