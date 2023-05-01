import ctypes

gains = [0] * 10

payload = (ctypes.c_uint16 * (10 + 2))()
payload[0] = 0x4020
for i in range(1, 10 + 1):
  payload[i] = gains[i - 1]
check_sum = 0
for i in range (0, 10 + 1):
  check_sum += (payload[i] & 0x00ff) + ((payload[i] & 0xff00) >> 8)
payload[10 + 1] = 0xffff - check_sum

print(bytes(payload))