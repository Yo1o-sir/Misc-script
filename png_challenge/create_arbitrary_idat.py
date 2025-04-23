import png  # 需要安装 pypng: pip install pypng
import zlib
import struct
import random
import sys

def generate_image_data(width, height, image_type='gradient'):
    """
    生成图像数据，控制数据量以生成适量IDAT块。

    参数:
        width, height: 图像尺寸
        image_type: 'random'（随机像素）, 'gradient'（渐变）, 'solid'（单色）

    返回:
        图像数据（RGB格式，列表形式）
    """
    image_data = []
    if image_type == 'random':
        for _ in range(height):
            row = [random.randint(0, 255) for _ in range(width * 3)]
            image_data.append(row)
    elif image_type == 'gradient':
        for y in range(height):
            row = []
            for x in range(width):
                r = (x * 255 // width) % 256
                g = (y * 255 // height) % 256
                b = ((x + y) * 255 // (width + height)) % 256
                row.extend([r, g, b])
            image_data.append(row)
    else:  # solid
        row = [255, 0, 0] * width  # 红色
        image_data = [row[:] for _ in range(height)]
    return image_data

def write_custom_png(filename, width, height, idat_chunk_limit=16000, image_type='gradient'):
    """
    生成PNG图片，严格控制IDAT块大小。

    参数:
        filename: 输出PNG文件名
        width, height: 图像宽高
        idat_chunk_limit: 每个IDAT块的最大数据大小（字节）
        image_type: 图像类型
    """
    # 生成图像数据
    image_data = generate_image_data(width, height, image_type)

    # 创建PNG写入器（不依赖chunk_limit）
    writer = png.Writer(
        width=width,
        height=height,
        greyscale=False,
        alpha=False,
        bitdepth=8,
        compression=0  # 无压缩，增加数据量，确保多块
    )

    # 获取压缩数据
    filter_type = 0  # 无滤波，简化处理
    raw_data = bytearray()
    for row in image_data:
        raw_data.append(filter_type)
        raw_data.extend(row)
    compressed_data = zlib.compress(raw_data, level=0)

    # 手动分割压缩数据为IDAT块
    with open(filename, 'wb') as f:
        # 写入PNG签名
        f.write(b'\x89PNG\r\n\x1a\n')

        # 写入IHDR
        ihdr_data = struct.pack(
            '>IIBBBBB',
            width, height, 8, 2, 0, 0, 0  # RGB, 无压缩，标准滤波，非隔行
        )
        write_chunk(f, b'IHDR', ihdr_data)

        # 写入IDAT块
        offset = 0
        idat_count = 0
        while offset < len(compressed_data):
            chunk_size = min(idat_chunk_limit, len(compressed_data) - offset)
            chunk_data = compressed_data[offset:offset + chunk_size]
            write_chunk(f, b'IDAT', chunk_data)
            idat_count += 1
            offset += chunk_size

        # 写入IEND
        write_chunk(f, b'IEND', b'')

    print(f"PNG文件已生成: {filename}")
    print(f"图像尺寸: {width}x{height}, 图像类型: {image_type}, IDAT块大小上限: {idat_chunk_limit}字节")

def write_chunk(file, chunk_type, data):
    """
    写入PNG数据块（长度 + 类型 + 数据 + CRC）。
    """
    file.write(struct.pack('>I', len(data)))
    file.write(chunk_type)
    file.write(data)
    crc = zlib.crc32(chunk_type + data)
    file.write(struct.pack('>I', crc))

def verify_idat_chunks(filename, expected_chunk_limit):
    """
    验证PNG文件中IDAT块的大小和数量。

    参数:
        filename: PNG文件名
        expected_chunk_limit: 期望的IDAT块大小上限
    """
    print(f"\n验证文件: {filename}")
    try:
        with open(filename, 'rb') as f:
            # 检查PNG签名
            signature = f.read(8)
            if signature != b'\x89PNG\r\n\x1a\n':
                print("错误: 不是有效的PNG文件")
                return

            idat_count = 0
            total_idat_size = 0
            chunk_sizes = []

            # 读取数据块
            while True:
                chunk_length_bytes = f.read(4)
                if not chunk_length_bytes:
                    break
                chunk_length = struct.unpack('>I', chunk_length_bytes)[0]
                chunk_type = f.read(4)

                if chunk_type == b'IDAT':
                    idat_count += 1
                    chunk_sizes.append(chunk_length)
                    total_idat_size += chunk_length

                f.seek(chunk_length, 1)  # 跳过数据
                f.seek(4, 1)  # 跳过CRC

            # 验证结果
            print(f"总计IDAT块数: {idat_count}")
            print(f"总IDAT数据大小: {total_idat_size}字节")
            for i, size in enumerate(chunk_sizes, 1):
                status = "符合预期"
                if size > expected_chunk_limit:
                    status = f"超出预期（{size - expected_chunk_limit}字节）"
                elif i < idat_count and size < expected_chunk_limit * 0.95:
                    status = "小于预期（可能数据不足）"
                elif i == idat_count and size < expected_chunk_limit:
                    status = "正常（最后一个块）"
                print(f"IDAT块 {i}: {size}字节 ({status})")

    except Exception as e:
        print(f"验证失败: {e}")

if __name__ == "__main__":
    # 配置参数
    output_file = "strict_idat.png"
    image_width = 1000
    image_height = 1000
    idat_size_limit = 70000
    image_type = 'gradient'  # 渐变图像，适中数据量

    # 生成和验证
    write_custom_png(
        filename=output_file,
        width=image_width,
        height=image_height,
        idat_chunk_limit=idat_size_limit,
        image_type=image_type
    )
    verify_idat_chunks(output_file, idat_size_limit)
