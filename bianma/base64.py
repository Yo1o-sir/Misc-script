import base64
import random
import itertools
import uuid

# 标准 Base64 编码表
Standard_b64table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
Test_PlainText = """If you can keep your head when all about you

Are losing theirs and blaming it on you;

If you can trust yourself when all men doubt you,

But make allowance for their doubting too;

If you can wait and not be tired by waiting,

Or, being lied about, don't deal in lies,

Or, being hated, don't give way to hating,

And yet don't look too good, nor talk too wise;

If you can dream - and not make dreams your master;

If you can think - and not make thoughts your aim;

If you can meet with Triumph and Disaster

And treat those two impostors just the same;

If you can bear to hear the truth you've spoken

Twisted by knaves to make a trap for fools,

Or watch the things you gave your life to broken,

And stoop and build 'em up with worn-out tools;

If you can make one heap of all your winnings

And risk it on one turn of pitch-and-toss,

And lose, and start again at your beginnings

And never breathe a word about your loss;

If you can force your heart and nerve and sinew

To serve your turn long after they are gone,

And so hold on when there is nothing in you

Except the Will which says to them:"Hold on";

If you can talk with crowds and keep your virtue,

Or walk with kings - nor lose the common touch;

If neither foes nor loving friends can hurt you;

If all men count with you, but none too much;

If you can fill the unforgiving minute

With sixty seconds' worth of distance run

Yours is the Earth and everything that's in it,

And - which is more - you'll be a Man my son!"""


def random_b64table():
    """
    生成随机的 Base64 编码表
    """
    s_list = list(Standard_b64table)
    random.shuffle(s_list)
    b64table = "".join(s_list)
    return b64table


def random_bytes(length: int):
    """
    生成随机字节串
    """
    return random.randbytes(length)


def custom_b64encode(plaintext: str | bytes, b64table: str = Standard_b64table):
    """
    使用自定义编码表将给定的字符串编码为Base64格式。
    """
    if len(b64table) != 64:
        raise ValueError("base64编码表必须为64位")

    if isinstance(plaintext, str):
        byte_data = plaintext.encode("utf-8")
    else:
        byte_data = plaintext

    result = ""

    for i in range(0, len(byte_data), 3):
        chunk = byte_data[i : i + 3]
        binary_chunk = "".join(format(byte, "08b") for byte in chunk)
        binary_chunk += "0" * ((6 - len(binary_chunk)) % 6)

        for j in range(0, len(binary_chunk), 6):
            six_bit_group = binary_chunk[j : j + 6]
            index = int(six_bit_group, 2)
            result += b64table[index]
            # print(result)

    padding = "=" * ((4 - len(result)) % 4)
    result += padding

    return result


def custom_b64decode(enc: str, b64table: str = Standard_b64table):
    """
    使用自定义编码表将给定的Base64格式的字符串解码为原文。
    """
    if len(b64table) != 64:
        raise ValueError("base64编码表必须为64位")

    result = b""

    for i in range(0, len(enc), 4):
        chunk = enc[i : i + 4]
        binary_chunk = ""
        for c in chunk:
            if c == "=":
                break
            index = b64table.index(c)
            binary_chunk += format(index, "06b")
        binary_chunk += "0" * ((8 - len(binary_chunk)) % 8)

        for j in range(0, len(binary_chunk), 8):
            eight_bit_group = binary_chunk[j : j + 8]
            byte = int(eight_bit_group, 2)
            result += bytes([byte])

    return result


def build_custom_b64table(plaintext: str | bytes, wrong_b64: str, custom_b64table=None):
    """
    交互式构建错误的 Base64 编码表
    param:
        plaintext (str|bytes): 原始明文
        wrong_b64 (str): 错误的 Base64 编码
    return:
        str: 分析的 Base64 编码表
        bool: 编码表是否完整
    """

    # 初始化未知编码表
    if not custom_b64table:
        custom_b64table = ["?"] * 64

    # 计算正确的 Base64 编码
    if isinstance(plaintext, str):
        correct_b64 = base64.b64encode(plaintext.encode()).decode()
    else:
        correct_b64 = base64.b64encode(plaintext).decode()

    # 对比错误的编码和正确的编码，找出字符映射
    if not len(wrong_b64) == len(correct_b64):
        print("错误: 编码长度不匹配", len(wrong_b64), len(correct_b64))
        print(f"[正确编码] {correct_b64}")
        print(f"[错误编码] {wrong_b64}")
        return "", False
    for wrong_char, correct_char in zip(wrong_b64, correct_b64):
        if correct_char == "=":
            break
        idx = Standard_b64table.index(correct_char)
        char = wrong_char
        if custom_b64table[idx] == "?":
            custom_b64table[idx] = char

    custom_b64table = "".join(custom_b64table)

    return custom_b64table, False if "?" in custom_b64table else True


def burst_table(b64table: str, tips: str = Standard_b64table):
    """
    暴力破解 Base64 编码表
    """
    tables = []
    length = len(set(Standard_b64table) - set(b64table))
    elements = "".join(set(tips) - set(b64table) - set("="))
    permutations = list(itertools.permutations(range(length), len(elements)))
    print(f"b64table 缺少 {length} 个字符，需要爆破 {elements}")
    for perm in permutations:
        padding = ["!"] * length
        for i in range(len(elements)):
            padding[perm[i]] = elements[i]
        table_copy = b64table
        for i in range(length):
            table_copy = table_copy.replace("?", padding[i], 1)
        table_copy = table_copy.replace("!", "?")
        tables.append(table_copy)
    # print(tables)
    # print(tables)
    print(f"得到 {len(tables)} 个用来爆破指定密文的 Base64 编码表。")

    return tables


def chosen_plaintext_attack():
    """
    选择明文攻击
    """
    # 选择明文，编码后恰好覆盖64个字符
    plaintext = "zjR^':+I;8B=UT@/*9=4?0q]j;k6^*ZxuSvwl+>'0o`<||h.Gl0"
    print(f"选择明文 {plaintext}")

    # 模拟在服务器上的加密过程
    wrong_b64 = input("输入 Base64 编码结果: ").strip()

    # 模拟在本地的解密过程
    table, _ = build_custom_b64table(plaintext, wrong_b64)
    print(f"解得 Base64 编码表: {table}")


def test_chosen_plaintext_attack():
    # 选择明文，编码后恰好覆盖64个字符
    plaintext = "zjR^':+I;8B=UT@/*9=4?0q]j;k6^*ZxuSvwl+>'0o`<||h.Gl0"
    print(f"选择明文 {plaintext}")

    # 模拟在服务器上的加密过程
    table_0 = random_b64table()
    print(f"目标 Base64 编码表: {table_0}")
    wrong_b64 = custom_b64encode(plaintext, table_0)
    print(f"加密后的 Base64 编码: {wrong_b64}")

    # 模拟在本地的解密过程
    table, _ = build_custom_b64table(plaintext, wrong_b64)
    print(f"解得 Base64 编码表: {table}")
    if table == table_0:
        print("破解成功！")


def known_plaintext_attack():
    print("=== 已知明文攻击 ===")
    input_string = input("请输入要编码的字符串：")
    wrong_b64 = input("Base64 编码: ").strip()
    custom_alphabet = build_custom_b64table(input_string, wrong_b64)
    print("\n=== 计算得到的Base64 编码表 ===")
    print(custom_alphabet)


def test_known_plaintext_attack():
    print("=== 测试 已知明文攻击 在不同明文长度下的成功率 ===")
    for length in range(100, 601, 40):
        count_success = 0

        for _ in range(1000):
            plaintext = random_bytes(length)
            b64table = random_b64table()

            # 模拟解密错误的 Base64 编码
            encoded_string = custom_b64encode(plaintext, b64table)
            custom_alphabet, success = build_custom_b64table(plaintext, encoded_string)

            # print(success, custom_alphabet, b64table)
            if success and custom_alphabet == b64table:
                count_success += 1
        print(f"明文长度为 {length} Byte 时的成功率: {count_success / 1000:.2%}")


def known_plaintext_and_burst_attack():
    print("=== 已知明文攻击 + 暴力破解 ===")
    # 要求的 flag 和 table_0
    # flag = f"flag{{{uuid.uuid4()}}}"
    # table_0 = random_b64table()
    # print(f"目标 flag: {flag}")
    # print(f"目标 Base64 编码表: {table_0}")

    # 模拟在服务器上的加密过程
    # input_string = Test_PlainText[:106]
    # wrong_b64 = custom_b64encode(input_string, table_0)
    # enc_flag = custom_b64encode(flag, table_0)
    input_string = input("请输入已知明文：")
    wrong_b64 = input("明文对应的 Base64 编码: ").strip()
    enc_flag = input("请输入编码后的 flag: ").strip()
    print(f"加密后的明文: {input_string}")
    print(f"错误的 Base64 编码: {wrong_b64}")
    print(f"编码后的flag: {enc_flag}")

    custom_alphabet, success = build_custom_b64table(input_string, wrong_b64)
    print("\n=== 计算得到的Base64 编码表 ===")
    print(custom_alphabet)
    if success:
        print("=== Base64 编码表完整，破解成功！===")
        print(custom_b64decode(enc_flag, custom_alphabet))
        return

    print("Base64 编码表不完整！尝试暴力破解...")
    flags = set()
    for table in burst_table(custom_alphabet, enc_flag):
        # print(f"尝试破解后的 Base64 编码表: {table}")
        try:
            flag_dec = custom_b64decode(enc_flag, table).decode()
            if all(
                c
                in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-{}"
                for c in flag_dec
            ):
                print(f"可能的 base64 编码表: {table}")
                print(f"可能的 flag: {flag_dec}")
                flags.add(flag_dec)
        except:
            continue
    print("暴力破解结束。可能的 flag 如下：")
    for flag in flags:
        print(flag)


def test_known_plaintext_and_burst_attack():
    print("=== 测试 已知明文攻击 + 暴力破解 ===")
    # 要求的 flag 和 table_0
    flag = f"flag{{{uuid.uuid4()}}}"
    table_0 = random_b64table()
    print(f"目标 flag: {flag}")
    print(f"目标 Base64 编码表: {table_0}")

    # 模拟在服务器上的加密过程
    input_string = Test_PlainText[:106]
    wrong_b64 = custom_b64encode(input_string, table_0)
    enc_flag = custom_b64encode(flag, table_0)
    print(f"加密后的明文: {input_string}")
    print(f"错误的 Base64 编码: {wrong_b64}")
    print(f"编码后的flag: {enc_flag}")

    custom_alphabet, success = build_custom_b64table(input_string, wrong_b64)
    print("\n=== 计算得到的Base64 编码表 ===")
    print(custom_alphabet)
    if success:
        print("=== Base64 编码表完整，破解成功！===")
        print(custom_b64decode(enc_flag, custom_alphabet))
        return

    print("Base64 编码表不完整！尝试暴力破解...")
    flags = set()
    for table in burst_table(custom_alphabet, enc_flag):
        # print(f"尝试破解后的 Base64 编码表: {table}")
        try:
            flag_dec = custom_b64decode(enc_flag, table).decode()
            if all(
                c
                in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-{}"
                for c in flag_dec
            ):
                print(f"可能的 base64 编码表: {table}")
                print(f"可能的 flag: {flag_dec}")
                flags.add(flag_dec)
            if flag_dec == flag:
                print("破解成功！")
        except:
            continue
    print("暴力破解结束。可能的 flag 如下：")
    for flag in flags:
        print(flag)
    print("测试结果:")
    print(f"已知明文的字节长度为 {len(input_string.encode())} Byte。")
    print(f"flag数量: {len(flags)}")


def generate_question():
    """
    生成一个问题
    """
    # 生成待求的flag和table
    flag = f"flag{{{uuid.uuid4()}}}"
    b64table = random_b64table()
    print(f"目标 flag: {flag}")
    print(f"目标 Base64 编码表: {b64table}")

    # 加密
    input_string = Test_PlainText.replace("\n", " ")[:200]
    wrong_b64 = custom_b64encode(input_string, b64table)
    enc_flag = custom_b64encode(flag, b64table)
    print(f"加密后的明文: {input_string}")
    print(f"错误的 Base64 编码: {wrong_b64}")
    print(f"编码后的flag: {enc_flag}")


Menu = """
1. 选择明文攻击
2. 已知明文攻击
3. 已知明文攻击+爆破
4. 测试选择明文攻击
5. 测试已知明文攻击
6. 测试已知明文攻击+爆破
7. 生成一个问题
0. 退出
"""


def main():
    print("=== Base64 编码表 破解工具 ===")
    while True:
        print(Menu)
        choice = input("请输入选项：")
        if choice == "1":
            chosen_plaintext_attack()
        elif choice == "2":
            known_plaintext_attack()
        elif choice == "3":
            known_plaintext_and_burst_attack()
        elif choice == "4":
            test_chosen_plaintext_attack()
        elif choice == "5":
            test_known_plaintext_attack()
        elif choice == "6":
            test_known_plaintext_and_burst_attack()
        elif choice == "7":
            generate_question()
        elif choice == "0":
            break
        else:
            print("输入错误，请重新输入。")
            continue
        input("按任意键继续...")


if __name__ == "__main__":
    main()
    pass
