import struct
import zlib
import argparse
from datetime import datetime

def calculate_crc(data):
    """计算 CRC32 校验值"""
    return zlib.crc32(data) & 0xffffffff

def create_png_chunk(chunk_type, data):
    """创建 PNG 数据块，包括长度、类型、数据和 CRC"""
    length = len(data)
    chunk_type_bytes = chunk_type.encode('ascii')
    chunk_data = chunk_type_bytes + data
    crc = calculate_crc(chunk_data)
    
    return (
        struct.pack('>I', length) +  
        chunk_data +                
        struct.pack('>I', crc)      
    )

def create_ihdr(width, height, bit_depth=8, color_type=2):
    """创建 IHDR 块（图像头部）"""
    ihdr_data = struct.pack(
        '>IIBBBBB',
        width,          
        height,         
        bit_depth,      
        color_type,    
        0,              
        0,              
        0               
    )
    return create_png_chunk('IHDR', ihdr_data)

def create_idat(width, height):
    """创建 IDAT 块（图像数据，简单示例使用纯色填充）"""
    
    scanline = b'\x00' + (b'\xFF\x00\x00' * width)  
    image_data = scanline * height
    compressed_data = zlib.compress(image_data)
    return create_png_chunk('IDAT', compressed_data)

def create_text_chunk(chunk_type, keyword, text):
    """创建文本块（tEXt, zTXt, iTXt）"""
    if chunk_type == 'tEXt':
        data = keyword.encode('ascii') + b'\x00' + text.encode('ascii')
    elif chunk_type == 'zTXt':
        compressed_text = zlib.compress(text.encode('utf-8'))
        data = keyword.encode('ascii') + b'\x00\x00' + compressed_text
    elif chunk_type == 'iTXt':
        data = (keyword.encode('ascii') + b'\x00' +  
                b'\x00\x00' +                       
                b'\x00\x00' +                       
                text.encode('utf-8'))               
    else:
        raise ValueError(f"不支持的文本块类型: {chunk_type}")
    return create_png_chunk(chunk_type, data)

def generate_png(filename, width=100, height=100, text_chunks=None):
    """生成 PNG 文件，并可插入指定的文本块"""
    
    png_signature = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
    
    
    chunks = [
        create_ihdr(width, height), 
        create_idat(width, height),  
    ]
    
  
    if text_chunks:
        for chunk_type, keyword, text in text_chunks:
            if chunk_type in ['tEXt', 'zTXt', 'iTXt']:
                chunks.insert(1, create_text_chunk(chunk_type, keyword, text))
    
  
    chunks.append(create_png_chunk('IEND', b''))
    
   
    try:
        with open(filename, 'wb') as f:
            f.write(png_signature)
            for chunk in chunks:
                f.write(chunk)
        return True, f"成功生成 PNG 文件: {filename}"
    except Exception as e:
        return False, f"生成 PNG 文件时出错: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成 PNG 文件并插入文本块")
    parser.add_argument("-o", "--output", default=f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                       help="输出 PNG 文件名")
    parser.add_argument("-W", "--width", type=int, default=100, help="图像宽度")
    parser.add_argument("-H", "--height", type=int, default=100, help="图像高度")
    parser.add_argument("-t", "--text", nargs=3, action='append',
                       metavar=('CHUNK_TYPE', 'KEYWORD', 'TEXT'),
                       help="添加文本块，格式：类型(tEXt/zTXt/iTXt) 关键字 文本内容")
    
    args = parser.parse_args()
    
 
    text_chunks = []
    if args.text:
        for chunk_type, keyword, text in args.text:
            if chunk_type not in ['tEXt', 'zTXt', 'iTXt']:
                print(f"错误：不支持的文本块类型 {chunk_type}")
                exit(1)
            text_chunks.append((chunk_type, keyword, text))
    

    success, message = generate_png(args.output, args.width, args.height, text_chunks)
    print(message)
