# 这里主要是见多了，有些出题人会将图片或其他文件进行倒置或按照几个字节进行转置
with open("./task_flag.jpg","rb") as f1:
    f=f1.read()
    with open("./flag.jpg","ab") as f2:
        len=len(f)
        i=0
        while i<len:
            hex=f[i:i+4][::-1]
            f2.write(hex)
            i+=4
            