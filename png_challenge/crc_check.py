import zlib

ihdr=bytes.fromhex("49 48 44 52 00 00 05 DA 00 00 08 8D 08 02 00 00 00")
crc=zlib.crc32(ihdr)&0xFFFFFFFF #这里是确保CRC是无符号32位整数，这样才能与PNG文件的格式一致
print(f"计算的CRC:{hex(crc)}")

# tips:crc计算的只有块类型和数据，其他两个部分（长度和CRC）不参与计算