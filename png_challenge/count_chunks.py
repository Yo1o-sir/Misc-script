import struct
from collections import Counter
import zlib

def check_png(file_path):
    correct_header = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
    try:
        with open(file_path, 'rb') as file:
            header = file.read(8)
            if len(header) != 8:
                return False, f"文件{file_path}太短，不是有效的PNG文件"
            if header != correct_header:
                return False, f"这文件不是png啊，这是正确的{correct_header}, 而你的这个文件是这个{header}"
            return True, f"文件{file_path}是一个有效的PNG文件"
    except FileNotFoundError:
        return False, f"文件{file_path}不存在"
    except Exception as e:
        return False, f"发生了一个错误: {e}"

def count_png_chunks(file_path):
 
    is_valid, message = check_png(file_path)
    if not is_valid:
        return 0, [], [], message

    chunk_count = 0
    chunk_types = []
    text_chunks = []
  
    text_chunk_types = {'zTXt', 'iTXt', 'tEXt'}
    
    try:
        with open(file_path, 'rb') as file:
   
            file.seek(8)
            
            while True:
     
                length_bytes = file.read(4)
                if len(length_bytes) != 4:
                    break  
                length = struct.unpack('>I', length_bytes)[0]
                
          
                type_bytes = file.read(4)
                if len(type_bytes) != 4:
                    return 0, [], [], f"文件{file_path}在读取块类型时出错"
                chunk_type = type_bytes.decode('ascii', errors='ignore')
                
        
                is_auxiliary = (len(chunk_type) == 4 and chunk_type[0].islower() and 
                              chunk_type[3].isupper())
                
                if chunk_type in text_chunk_types or is_auxiliary:
                    data = file.read(length)
                    try:
                        if chunk_type == 'zTXt':
                          
                            null_index = data.find(b'\0')
                            if null_index != -1:
                                keyword = data[:null_index].decode('ascii', errors='ignore')
                                compressed_data = data[null_index + 2:]  
                                try:
                                    content = zlib.decompress(compressed_data).decode('utf-8', errors='ignore')
                                    text_chunks.append(f"发现了zTXt块，关键字：{keyword}，内容：{content}")
                                except zlib.error:
                                    text_chunks.append(f"发现了zTXt块，关键字：{keyword}，内容：无法解压缩")
                        elif chunk_type == 'iTXt':
                            
                            null_index = data.find(b'\0')
                            if null_index != -1:
                                keyword = data[:null_index].decode('ascii', errors='ignore')
                                content = data[null_index + 5:].decode('utf-8', errors='ignore')  
                                text_chunks.append(f"发现了iTXt块，关键字：{keyword}，内容：{content}")
                        elif chunk_type == 'tEXt':
                          
                            null_index = data.find(b'\0')
                            if null_index != -1:
                                keyword = data[:null_index].decode('ascii', errors='ignore')
                                content = data[null_index + 1:].decode('ascii', errors='ignore')
                                text_chunks.append(f"发现了tEXt块，关键字：{keyword}，内容：{content}")
                        elif is_auxiliary:
                           
                            try:
                           
                                null_index = data.find(b'\0')
                                if null_index != -1:
                                    keyword = data[:null_index].decode('ascii', errors='ignore')
                                    content = data[null_index + 1:].decode('utf-8', errors='ignore')
                                    text_chunks.append(f"发现了自定义辅助块 {chunk_type}，关键字：{keyword}，内容：{content}")
                                else:
                                    
                                    content = data.decode('utf-8', errors='ignore')
                                    text_chunks.append(f"发现了自定义辅助块 {chunk_type}，内容：{content}")
                            except Exception as e:
                                text_chunks.append(f"解析自定义辅助块 {chunk_type} 时出错: {e}")
                    except Exception as e:
                        text_chunks.append(f"解析{chunk_type}块时出错: {e}")
                else:
            
                    file.seek(length, 1)
                
       
                crc_bytes = file.read(4)
                if len(crc_bytes) != 4:
                    return 0, [], [], f"文件{file_path}在读取CRC时出错"
                
             
                chunk_count += 1
                chunk_types.append(chunk_type)
                
             
                if chunk_type == 'IEND':
      
                    remaining_data = file.read()
                    if remaining_data:
                        try:
                      
                            content = remaining_data.decode('utf-8', errors='ignore')
                            if content.strip(): 
                                text_chunks.append(f"发现了IEND块后的额外内容，内容：{content}")
                        except Exception as e:
                            text_chunks.append(f"解析IEND块后内容时出错: {e}")
                    break  
                
    except Exception as e:
        return 0, [], [], f"解析{file_path}时发生错误: {e}"
    
    
    type_counts = Counter(chunk_types)
    type_summary = [f"{chunk_type}: {count} 次" for chunk_type, count in type_counts.items()]
    
    return chunk_count, type_summary, text_chunks, f"文件{file_path}包含 {chunk_count} 个数据块"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="检查PNG文件并统计其数据块")
    parser.add_argument("-f", "--files", nargs='+', required=True, help="指定要检查的PNG文件路径")
    args = parser.parse_args()

    for file_path in args.files:
     
        result, message = check_png(file_path)
        print(message)
        
        if result:
  
            count, types, text_chunks, summary = count_png_chunks(file_path)
            print(summary)
            if count > 0:
                print("数据块类型统计:")
                for type_info in types:
                    print(f"  {type_info}")
                if text_chunks:
                    print("\n文本块、自定义辅助块及IEND后内容:")
                    for text_info in text_chunks:
                        print(f"  {text_info}")
