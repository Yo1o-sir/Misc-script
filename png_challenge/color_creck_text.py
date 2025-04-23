from PIL import Image
import numpy as np
import itertools
import re

def load_markers(dict_file):
    """
    从字典文件加载标志列表，支持正则表达式
    """
    try:
        with open(dict_file, 'r', encoding='utf-8') as f:
            markers = [line.strip() for line in f if line.strip()]
        
        regex_markers = []
        string_markers = []
        for marker in markers:
            if marker.startswith('r"') and marker.endswith('"'):
                try:
                  
                    pattern = marker[2:-1]
                    regex_markers.append(re.compile(pattern, re.IGNORECASE))
                except re.error as e:
                    print(f"无效正则表达式 {marker}: {str(e)}")
            else:
                string_markers.append(marker)
        return string_markers, regex_markers
    except Exception as e:
        print(f"无法读取字典文件 {dict_file}: {str(e)}")
        return ['flag'], []

def extract_message_from_combination(pixels, height, width, channel_bit_pairs, string_markers, regex_markers, binary_mode=False):
    """
    从指定的通道和位组合中提取隐藏信息，支持正则表达式
    """
    if not channel_bit_pairs:
        return None, channel_bit_pairs
    
    binary_message = ""
    max_bits = 1024 if binary_mode else 1024 * 8  
    for i in range(height):
        for j in range(width):
            pixel = pixels[i, j]
            if len(pixel) != 3:
                return None, channel_bit_pairs
            
            for channel, bit in channel_bit_pairs:
                if channel not in [0, 1, 2] or bit not in range(8):
                    return None, channel_bit_pairs
                value = pixel[channel]
                binary_message += str((value >> bit) & 1)
                
                if len(binary_message) >= max_bits:
                    break
            
            if not binary_mode and len(binary_message) >= 8:
                byte = binary_message[-8:]
                try:
                    char = chr(int(byte, 2))
                    if char == '\0':
                        binary_message = binary_message[:-8]
                        break
                except ValueError:
                    continue
        if not binary_mode and len(binary_message) >= 8 and char == '\0':
            break
        if len(binary_message) >= max_bits:
            break
    
    if binary_mode:
        
        temp_message = ""
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if len(byte) == 8:
                try:
                    temp_message += chr(int(byte, 2))
                except ValueError:
                    break
        for marker in string_markers:
            if marker.lower() in temp_message.lower():
                return binary_message, channel_bit_pairs
        for regex in regex_markers:
            if regex.search(temp_message):
                return binary_message, channel_bit_pairs
        return None, channel_bit_pairs
    
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) == 8:
            try:
                message += chr(int(byte, 2))
            except ValueError:
                break
    
    for marker in string_markers:
        if marker.lower() in message.lower():
            return message, channel_bit_pairs
    for regex in regex_markers:
        if regex.search(message):
            return message, channel_bit_pairs
    return None, channel_bit_pairs

def extract_lsb_message(image_path, dict_file="markers.txt", output_file="extracted_message.txt", binary_output="extracted_binary.bin"):
    
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
    except Exception as e:
        print(f"错误: 无法打开图片 {image_path}: {str(e)}")
        return None, None
    
 
    try:
        pixels = np.array(img, dtype=np.uint8)
        height, width, _ = pixels.shape
        print(f"图片尺寸: {width}x{height}")
    except Exception as e:
        print(f"错误: 无法加载像素数据: {str(e)}")
        return None, None
    
   
    string_markers, regex_markers = load_markers(dict_file)
    print(f"已加载标志: {string_markers + [m.pattern for m in regex_markers]}")
    
    
    channels = [0, 1, 2]
    bits = list(range(8))  
    
   
    print("开始提取，请等待...")
    for r in range(1, 4):
        for channel_combo in itertools.permutations(channels, r):
            for bit_combo in itertools.product(bits, repeat=len(channel_combo)):
                channel_bit_pairs = [(channel_combo[i], bit_combo[i]) for i in range(len(channel_combo))]
                
             
                message, combo = extract_message_from_combination(pixels, height, width, channel_bit_pairs, string_markers, regex_markers, binary_mode=False)
                if message:
                    try:
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write(message)
                        print(f"找到包含标志的文本消息！使用的通道和位组合: {combo}")
                        print(f"文本消息已保存到 {output_file}")
                        return message, combo
                    except Exception as e:
                        print(f"错误: 保存文本消息出错: {str(e)}")
                
               
                binary_message, combo = extract_message_from_combination(pixels, height, width, channel_bit_pairs, string_markers, regex_markers, binary_mode=True)
                if binary_message:
                    try:
                        binary_bytes = bytes(int(binary_message[i:i+8], 2) for i in range(0, len(binary_message) - len(binary_message) % 8, 8))
                        with open(binary_output, 'wb') as f:
                            f.write(binary_bytes)
                        print(f"找到包含标志的二进制数据！使用的通道和位组合: {combo}")
                        print(f"二进制数据已保存到 {binary_output}")
                        return binary_message, combo
                    except Exception as e:
                        print(f"错误: 保存二进制数据出错: {str(e)}")
    
    print("未找到包含任何标志的消息")
    return None, None

def main():
  
    image_path = input("请输入包含隐藏信息的PNG图片路径: ")
    dict_file = input("请输入标志字典文件路径（默认 'markers.txt'）: ") or "markers.txt"
    
    try:
        result, combo = extract_lsb_message(image_path, dict_file)
        if result:
            if isinstance(result, str):
                print("提取的内容预览:", result[:100], "..." if len(result) > 100 else "")
            else:
                print("提取的内容预览:", result[:100], "..." if len(result) > 100 else "")
            print(f"使用的通道和位组合: {combo}")
        else:
            print("提取失败，请检查图片或字典文件")
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    main()
