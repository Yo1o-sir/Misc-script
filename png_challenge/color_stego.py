from PIL import Image
import numpy as np

def binary_to_bits(data):
    """
    将字节数据转换为二进制字符串
    """
    return ''.join(format(byte, '08b') for byte in data)

def insert_lsb_hidden_data(image_path, output_path, data, channel_bit_pairs, is_file=False):
    """
    将数据（文本或文件）插入PNG图片的指定通道和位
    """
    try:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
    except Exception as e:
        print(f"错误: 无法打开图片 {image_path}: {str(e)}")
        return
    
    pixels = np.array(img, dtype=np.uint8)
    height, width, _ = pixels.shape
    
    
    if is_file:
        bits = binary_to_bits(data)
        print(f"文件大小: {len(data)} 字节 ({len(bits)} 位)")
    else:
        try:
            if data.startswith('b"') and data.endswith('"'):
                bytes_data = eval(data)
            else:
                bytes_data = data.encode('latin1')
            bits = binary_to_bits(bytes_data)
            print(f"消息长度: {len(bytes_data)} 字节 ({len(bits)} 位)")
        except Exception as e:
            print(f"错误: 无法解析文本消息: {str(e)}")
            return
    
    
    max_bits = height * width * len(channel_bit_pairs)
    if len(bits) > max_bits:
        print(f"错误: 数据太长（{len(bits)} 位），图片容量 {max_bits} 位")
        return
    
    print(f"图片容量: {max_bits} 位，通道/位组合: {channel_bit_pairs}")
    
    
    bit_index = 0
    for i in range(height):
        for j in range(width):
            pixel = pixels[i, j].copy().astype(np.uint8)
            for channel, bit in channel_bit_pairs:
                if bit_index >= len(bits):
                    break
                value = pixel[channel]
                
                pixel[channel] = np.uint8((value & (255 ^ (1 << bit))) | (int(bits[bit_index]) << bit))
                bit_index += 1
            pixels[i, j] = pixel
            if bit_index >= len(bits):
                break
        if bit_index >= len(bits):
            break
    
    
    try:
        Image.fromarray(pixels).save(output_path)
        print(f"已生成包含隐藏信息的图片: {output_path}")
    except Exception as e:
        print(f"错误: 保存图片失败: {str(e)}")

def main():
  
    image_path = input("请输入原始PNG图片路径: ")
    output_path = input("请输入输出PNG图片路径（包含隐藏信息）: ")
    input_type = input("输入类型（text/file）: ").lower()
    
    try:
        if input_type == 'file':
            file_path = input("请输入要隐藏的文件路径（例如 secret.zip）: ")
            with open(file_path, 'rb') as f:
                data = f.read()
            is_file = True
        else:
            data = input("请输入要隐藏的消息（例如 flag{test} 或 b\"PK\\x03\\x04\"）: ")
            is_file = False
        
        combo_input = input("请输入通道和位组合（格式：通道索引,位索引，例如 '0,0 2,1'，留空默认 '0,0 1,1 2,2'）: ")
        channel_bit_pairs = [(0,0), (1,1), (2,2)] if not combo_input.strip() else [tuple(map(int, pair.split(','))) for pair in combo_input.split()]
        
        for channel, bit in channel_bit_pairs:
            if channel not in [0, 1, 2] or bit not in range(8):
                print(f"错误: 无效的通道或位索引: ({channel},{bit})")
                return
        
        insert_lsb_hidden_data(image_path, output_path, data, channel_bit_pairs, is_file)
    except FileNotFoundError:
        print(f"错误: 文件未找到，请检查路径")
    except ValueError as e:
        print(f"错误: 无效输入: {str(e)}")
    except Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    main() Exception as e:
        print(f"错误: {str(e)}")

if __name__ == "__main__":
    main()
