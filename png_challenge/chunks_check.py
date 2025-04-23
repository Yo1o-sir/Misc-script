import struct
import argparse

def check_png(file_path):
    """检查文件是否为有效的 PNG 文件"""
    correct_header = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
    try:
        with open(file_path, 'rb') as file:
            header = file.read(8)
            if len(header) != 8:
                return False, f"文件{file_path}太短，不是有效的PNG文件"
            if header != correct_header:
                return False, f"文件{file_path}不是PNG文件，预期头{correct_header}，实际头{header}"
            return True, f"文件{file_path}是一个有效的PNG文件"
    except FileNotFoundError:
        return False, f"文件{file_path}不存在"
    except Exception as e:
        return False, f"发生错误: {e}"

def list_png_chunks(file_path):
    """逐个检测并输出 PNG 文件的数据块信息"""
    
    is_valid, message = check_png(file_path)
    if not is_valid:
        print(message)
        return

    print(message)
    print("数据块列表:")
    print("  序号  类型  大小（字节）")

    try:
        with open(file_path, 'rb') as file:
        
            file.seek(8)
            
            chunk_index = 0
            while True:
            
                length_bytes = file.read(4)
                if len(length_bytes) != 4:
                    if length_bytes:  
                        print(f"错误：第{chunk_index}个块长度数据不完整")
                    break  
                length = struct.unpack('>I', length_bytes)[0]
                
               
                type_bytes = file.read(4)
                if len(type_bytes) != 4:
                    print(f"错误：第{chunk_index}个块类型数据不完整")
                    break
                chunk_type = type_bytes.decode('ascii', errors='ignore')
                
          
                file.seek(length, 1)
                
               
                crc_bytes = file.read(4)
                if len(crc_bytes) != 4:
                    print(f"错误：第{chunk_index}个块CRC数据不完整")
                    break
                
            
                print(f"  {chunk_index:>4}  {chunk_type:<4}  {length:>12}")
                
                chunk_index += 1
                
             
                if chunk_type == 'IEND':
                    break
                
    except Exception as e:
        print(f"错误：解析{file_path}时发生异常: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="逐个列出PNG文件的数据块")
    parser.add_argument("-f", "--files", nargs='+', required=True, help="指定要检查的PNG文件路径")
    args = parser.parse_args()

    for file_path in args.files:
        list_png_chunks(file_path)

# 脚本使用方法：python3 chunks_check.py xxx.png
