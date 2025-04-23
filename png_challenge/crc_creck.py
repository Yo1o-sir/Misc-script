import zlib
import struct
import argparse
import itertools
from pathlib import Path

def check_png(bin_data, file_path):
    """检查 PNG 文件头和 IHDR 块完整性"""
    correct_header = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
    if len(bin_data) < 33:
        return False, f"文件{file_path}太短，不是有效的PNG文件"
    if bin_data[:8] != correct_header:
        return False, f"文件{file_path}不是PNG文件，预期头{correct_header}，实际头{bin_data[:8]}"
    length = struct.unpack('>I', bin_data[8:12])[0]
    chunk_type = bin_data[12:16].decode('ascii', errors='ignore')
    if length != 13 or chunk_type != 'IHDR':
        return False, f"文件{file_path}的IHDR块无效，长度应为13，类型应为IHDR，实际长度{length}，类型{chunk_type}"
    return True, f"文件{file_path}是一个有效的PNG文件"

def repair_png(file_path, bin_data, width, height):
    """生成修复后的 PNG 文件"""
    output_path = str(Path(file_path).with_stem(Path(file_path).stem + '_fixed'))
    try:
        new_data = (
            bin_data[:16] +
            struct.pack('>I', width) +
            struct.pack('>I', height) +
            bin_data[24:]
        )
        with open(output_path, 'wb') as f:
            f.write(new_data)
        return True, f"修复成功，保存为 {output_path}"
    except Exception as e:
        return False, f"保存修复文件失败: {e}"

def main():
    parser = argparse.ArgumentParser(description="通过CRC爆破PNG文件的IHDR宽高并修复")
    parser.add_argument("-f", type=str, default=None, required=True,
                        help="输入同级目录下图片的名称")
    args = parser.parse_args()

    try:
        bin_data = open(args.f, 'rb').read()
    except FileNotFoundError:
        print(f"文件{args.f}不存在")
        return

 
    is_valid, message = check_png(bin_data, args.f)
    print(message)
    if not is_valid:
        return


    ihdr_data = bin_data[12:29]
    original_crc32 = struct.unpack('>I', bin_data[29:33])[0]
    crc32key = zlib.crc32(ihdr_data)
    width, height = struct.unpack('>II', bin_data[16:24])

    print(f"原始宽度: {width}, hex: {hex(width)}")
    print(f"原始高度: {height}, hex: {hex(height)}")
    print(f"CRC 校验: {'通过' if crc32key == original_crc32 else '失败'}")

    if crc32key == original_crc32:
        print("宽高没有问题!")
        return

  
    input_ = input("宽高被改了，是否CRC爆破宽高? (Y/n): ")
    if input_.lower() not in ["y", ""]:
        print("退出爆破")
        return

    common_resolutions = [
        (300, 200), (1920, 1080), (1280, 720), (1024, 768), (800, 600),
        (2560, 1440), (3840, 2160), (512, 512), (640, 480)
    ]

    print("\n开始 CRC 宽高爆破：")
   
    for i, j in common_resolutions:
        data = (
            bin_data[12:16] +
            struct.pack('>I', i) +
            struct.pack('>I', j) +
            bin_data[24:29]
        )
        crc32 = zlib.crc32(data)
        if crc32 == original_crc32:
            print(f"\n找到匹配的宽高！")
            print(f"CRC32: {hex(original_crc32)}")
            print(f"宽度: {i}, hex: {hex(i)}")
            print(f"高度: {j}, hex: {hex(j)}")
            
           
            success, repair_message = repair_png(args.f, bin_data, i, j)
            print(repair_message)
            return

 
    print("常见分辨率未找到匹配，尝试穷举 1 到 4095...")
    for i, j in itertools.product(range(1, 4096), range(1, 4096)):
        data = (
            bin_data[12:16] +
            struct.pack('>I', i) +
            struct.pack('>I', j) +
            bin_data[24:29]
        )
        crc32 = zlib.crc32(data)
        if crc32 == original_crc32:
            print(f"\n找到匹配的宽高！")
            print(f"CRC32: {hex(original_crc32)}")
            print(f"宽度: {i}, hex: {hex(i)}")
            print(f"高度: {j}, hex: {hex(j)}")
            
            
            success, repair_message = repair_png(args.f, bin_data, i, j)
            print(repair_message)
            return

    print("\n爆破失败，未找到匹配CRC的宽高")

if __name__ == "__main__":
    main() 
