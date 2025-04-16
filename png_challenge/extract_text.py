import argparse
import struct
import zlib

def is_png(file_path):
    png_signature=bytes([0x89,0x50,0x4E,0x47,0x0D,0x0A,0x1A,0x0A])
    try:
        f=open(file_path,'rb')
        header=f.read(8)
        if header !=png_signature:
            f.close()
            return None,False
        return f,True
    except FileNotFoundError:
        print(f"文件{file_path}不存在")
        return None,False

def read_chunk(f):
    try:
        length_data=f.read(4)
        if len(length_data)!=4:
            return None
        length=struct.unpack('>I',length_data)[0]

        chunk_type=f.read(4)
        if len(chunk_type)!=4:
            return None
        data=f.read(length)
        if len(data)!=length:
            return None
        
        crc_data=f.read(4)
        if len(crc_data)!=4:
            return None
        crc=struct.unpack('>I',crc_data)[0]

        calculated_crc=zlib.crc32(chunk_type+data)&0xffffffff
        if calculated_crc !=crc:
            print(f"CRC check failed for chunk {chunk_type.decode('ascii',errors='ignore')},计算值{calculated_crc:08x},文件值{crc:08x}")
            
            return None
        return length,chunk_type,data,crc
    except Exception as e:
        print(f"read chunk error:{e}")
        return None
    
def analyze_png_chunks(file_path):
    f,is_valid=is_png(file_path)
    if not is_valid:
        print(f"{file_path}不是一个PNG文件")
        return
    
    chunk_count=0
    chunk_types={}
    try:
        while True:
            chunk=read_chunk(f)
            if chunk is None:
                print("数据块解析结束或出错")
                break
            length,chunk_type,data,crc=chunk
            chunk_type_str=chunk_type.decode('ascii',errors='ignore')
            chunk_count +=1
            chunk_types[chunk_type_str]=chunk_types.get(chunk_type_str,0)+1

            print(f"数据块{chunk_count}:")
            print(f"类型：{chunk_type_str}")
            print(f"长度：{length}字节")
            print(f"CRC:{crc:08x}")
            if chunk_type_str=='IEND':
                print("find IEND chunk,结束解析")
                break
        print("\n数据块统计:")
        print(f"总数据块数：{chunk_count}")
        print("数据块类型统计:")
        for chunk_type,count in chunk_types.items():
            print(f"{chunk_type}:{count}")
    finally:
        f.close()

if __name__=="__main__":
    parser=argparse.ArgumentParser(description="check if a file is a PNG")
    parser.add_argument("-f","--file",required=True,help="path to the file to check")
    args=parser.parse_args()
    file_path=args.file

    analyze_png_chunks(file_path)