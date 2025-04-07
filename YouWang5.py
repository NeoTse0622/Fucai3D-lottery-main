'''修改组合杀号功能'''

import os
import csv
import random
import datetime
import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from itertools import permutations

# 生成一个随机的3D号码（3个数字）
def generate_number(index):
    return [int(digit) for digit in f"{index:03d}"]

# 判断大小组合
def size_combo(nums):
    return ''.join(['大' if n >= 5 else '小' for n in nums])

# 判断奇偶组合
def parity_combo(nums):
    return ''.join(['奇' if n % 2 != 0 else '偶' for n in nums])

# 判断012组合
def route_combo(nums):
    return ''.join([str(n % 3) for n in nums])

# 将数字组合转换为中文大小组合
def convert_to_size_combo(num_combo):
    return ''.join(['大' if digit == '1' else '小' for digit in num_combo])

# 将数字组合转换为中文奇偶组合
def convert_to_parity_combo(num_combo):
    return ''.join(['奇' if int(digit) % 2 != 0 else '偶' for digit in num_combo])

# 生成数据并存储到 csv 文件
def generate_and_store_csv(filename):
    data = []
    for i in range(1000):  # 从 0 到 999 生成 1000 个数据
        nums = generate_number(i)
        size = size_combo(nums)
        parity = parity_combo(nums)
        route = route_combo(nums)
        data.append([i + 1, ''.join(map(str, nums)), size, parity, route])

    # 将数据写入 CSV 文件
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['序号', '数据', '大小组合', '奇偶组合', '012组合'])  # 表头
        writer.writerows(data)
    print(f"数据已保存至 {filename}")

# 更新杀奇偶组合和杀大小组合的功能，支持数字输入
def kill_parity_combo(filename, kill_combo):
    try:
        kill_combo = convert_to_parity_combo(kill_combo)
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)
            rows = list(reader)

        remaining_rows = [row for row in rows if row[3] != kill_combo]
        killed_count = len(rows) - len(remaining_rows)

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(remaining_rows)

        messagebox.showinfo("提示", f"杀掉了 {killed_count} 条奇偶组合为 {kill_combo} 的数据")
    except Exception as e:
        messagebox.showerror("错误", f"发生错误：{e}")

def kill_size_combo(filename, kill_combo):
    try:
        kill_combo = convert_to_size_combo(kill_combo)
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)
            rows = list(reader)

        remaining_rows = [row for row in rows if row[2] != kill_combo]
        killed_count = len(rows) - len(remaining_rows)

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(remaining_rows)

        messagebox.showinfo("提示", f"杀掉了 {killed_count} 条大小组合为 {kill_combo} 的数据")
    except Exception as e:
        messagebox.showerror("错误", f"发生错误：{e}")

def kill_route_combo(filename, kill_combo):
    try:
        kill_combo = str(kill_combo)
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)
            rows = list(reader)

        remaining_rows = [row for row in rows if row[4] != kill_combo]
        killed_count = len(rows) - len(remaining_rows)

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(remaining_rows)

        messagebox.showinfo("提示", f"杀掉了 {killed_count} 条012路组合为 {kill_combo} 的数据")
    except Exception as e:
        messagebox.showerror("错误", f"发生错误：{e}")

def kill_containing_combo(filename, kill_combo):
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)
            rows = list(reader)

        remaining_rows = [row for row in rows if not any(kill_combo in col for col in row)]
        killed_count = len(rows) - len(remaining_rows)

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(remaining_rows)

        messagebox.showinfo("提示", f"杀掉了 {killed_count} 条包含 {kill_combo} 的数据")
    except Exception as e:
        messagebox.showerror("错误", f"发生错误：{e}")


def kill_number_group(filename, kill_numbers):
    try:
        # 将输入的字符串按空格分割成单个数字的列表
        kill_numbers = kill_numbers.strip().split()

        # 校验输入是否为有效的数字
        if not all(num.isdigit() and len(num) == 1 for num in kill_numbers):
            messagebox.showwarning("提醒", "请输入规范的数字（单个或多个，用空格隔开）！")
            return

        # 如果输入的数字少于 3 个，无法生成排列 Ax:3
        if len(kill_numbers) < 3:
            messagebox.showwarning("提醒", "至少需要输入 3 个数字以生成排列 Ax:3！")
            return

        # 生成排列 Ax:3
        kill_combinations = set([''.join(p) for p in permutations(kill_numbers, 3)])

        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)
            rows = list(reader)

        remaining_rows = []
        killed_count = 0
        for row in rows:
            data = row[1]  # 获取当前数据（号码）
            if data not in kill_combinations:
                remaining_rows.append(row)
            else:
                killed_count += 1

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(remaining_rows)

        messagebox.showinfo("提示", f"杀掉了 {killed_count} 条符合排列 A{len(kill_numbers)}:3 的数据")
    except Exception as e:
        messagebox.showerror("错误", f"发生错误：{e}")


# 新增保号组合功能
def preserve_number_group(filename, preserve_numbers):
    try:
        # 将输入的字符串按空格分割成单个数字的列表
        preserve_numbers = preserve_numbers.strip().split()

        # 校验输入是否为有效的数字
        if not all(num.isdigit() and len(num) == 1 for num in preserve_numbers):
            messagebox.showwarning("提醒", "请输入规范的数字（单个或多个，用空格隔开）！")
            return

        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)
            rows = list(reader)

        # 保留包含任意一个指定数字的号码组合
        preserved_rows = [row for row in rows if any(num in row[1] for num in preserve_numbers)]
        removed_count = len(rows) - len(preserved_rows)

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(preserved_rows)

        messagebox.showinfo("提示",
                            f"保号成功！保留了包含指定数字 {', '.join(preserve_numbers)} 的 {len(preserved_rows)} 条数据，移除了 {removed_count} 条数据")
    except Exception as e:
        messagebox.showerror("错误", f"发生错误：{e}")


# 更新实时数据显示到看板
def update_data_display(filename, listbox_widget, label_widget):
    try:
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)
            rows = list(reader)

        data_count = len(rows)
        label_widget.config(text=f"实时数据面板 ({data_count}条数据)")
        listbox_widget.delete(0, tk.END)
        listbox_widget.insert(tk.END, ", ".join(headers))
        for row in rows:
            listbox_widget.insert(tk.END, ", ".join(row))
    except Exception as e:
        messagebox.showerror("错误", f"发生错误：{e}")

# 爬取近期 400 期福彩 3D 开奖数据
def fetch_lottery_data():
    try:
        # 直接访问 iframe 的 URL
        url = "https://datachart.500.com/sd/history/inc/history.php?limit=400"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        print("响应状态码：", response.status_code)  # 调试信息
        soup = BeautifulSoup(response.text, 'html.parser')

        # 解析表格数据
        rows = soup.find_all('tr', class_='t_tr1')
        print("找到的行数：", len(rows))  # 调试信息
        lottery_data = []
        for row in rows:
            columns = row.find_all('td')
            if len(columns) > 1:
                lottery_data.append(columns[1].text.strip())  # 获取开奖号码
        print("爬取到的开奖数据：", lottery_data)  # 调试信息
        return lottery_data
    except Exception as e:
        messagebox.showerror("错误", f"爬取数据失败：{e}")
        return []


# 杀除爬取的数据
def kill_fetched_data(filename):
    try:
        lottery_data = fetch_lottery_data()
        if not lottery_data:
            messagebox.showwarning("警告", "未爬取到数据")
            return

        # 将爬取到的数据格式统一（去掉空格）
        lottery_data = [data.replace(" ", "") for data in lottery_data]

        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)
            rows = list(reader)

        remaining_rows = [row for row in rows if row[1] not in lottery_data]
        killed_count = len(rows) - len(remaining_rows)

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(remaining_rows)

        messagebox.showinfo("提示", f"杀掉了 {killed_count} 条近期开奖数据")
    except Exception as e:
        messagebox.showerror("错误", f"发生错误：{e}")


# 新增个十百杀号组合功能
def kill_position_combo(filename, kill_combo):
    try:
        # 将输入的字符串按空格分割成单个组合的列表
        kill_combos = kill_combo.strip().split()

        # 校验输入是否为有效的组合
        valid_positions = {'个', '十', '百'}
        for combo in kill_combos:
            if len(combo) != 2 or combo[0] not in valid_positions or not combo[1].isdigit():
                messagebox.showwarning("提醒", "请输入规范的组合（如 '个5 十6' 或 '个1 十5 百6'）！")
                return

        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)
            rows = list(reader)

        remaining_rows = []
        killed_count = 0
        for row in rows:
            data = row[1]  # 获取当前数据（号码）
            should_kill = False
            for combo in kill_combos:
                position = combo[0]  # 个、十、百
                digit = combo[1]  # 数字
                if position == '个' and data[2] == digit:
                    should_kill = True
                elif position == '十' and data[1] == digit:
                    should_kill = True
                elif position == '百' and data[0] == digit:
                    should_kill = True
            if should_kill:
                killed_count += 1
            else:
                remaining_rows.append(row)

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(remaining_rows)

        messagebox.showinfo("提示", f"杀掉了 {killed_count} 条符合 {kill_combo} 的数据")
    except Exception as e:
        messagebox.showerror("错误", f"发生错误：{e}")


# 在 create_gui 函数中新增个十百杀号组合模块
def create_gui():
    root = tk.Tk()
    root.title("友望3D")
    root.geometry("500x700")

    # 提示用户输入文件名
    tk.Label(root, text="请输入文件名（例如：data.csv）:").pack(pady=10)
    entry_filename = tk.Entry(root)
    entry_filename.pack(pady=5)

    # 生成数据按钮
    def on_generate():
        filename = entry_filename.get()
        if filename:
            generate_and_store_csv(filename)
            messagebox.showinfo("提示", "数据已生成并保存")
            update_data_display(filename, listbox_data_board, label_data_board)
        else:
            messagebox.showwarning("警告", "请输入文件名")

    tk.Button(root, text="生成数据", command=on_generate).pack(pady=10)

    # 爬取并杀除数据按钮
    def on_kill_fetched():
        filename = entry_filename.get()
        if filename:
            kill_fetched_data(filename)
            update_data_display(filename, listbox_data_board, label_data_board)
        else:
            messagebox.showwarning("警告", "请输入文件名")

    tk.Button(root, text="爬取并杀除近400期开奖数据", command=on_kill_fetched).pack(pady=10)

    # 新增保号组合模块
    def create_preserve_section():
        frame = tk.Frame(root)
        frame.pack(pady=15, padx=20, fill="x")

        tk.Label(frame, text="保号组合：").pack(side="left", padx=5)
        entry_preserve_number = tk.Entry(frame)
        entry_preserve_number.pack(side="left", padx=5, fill="x", expand=True)

        def on_preserve():
            filename = entry_filename.get()
            preserve_numbers = entry_preserve_number.get()
            if not filename:
                messagebox.showwarning("警告", "请输入文件名")
                return
            preserve_number_group(filename, preserve_numbers)
            update_data_display(filename, listbox_data_board, label_data_board)  # 刷新数据看板

        tk.Button(frame, text="确认保号", command=on_preserve).pack(side="right", padx=5)

    create_preserve_section()  # 添加保号组合模块

    # 新增个十百杀号组合模块
    def create_kill_position_section():
        frame = tk.Frame(root)
        frame.pack(pady=15, padx=20, fill="x")

        tk.Label(frame, text="个十百杀号组合：").pack(side="left", padx=5)
        entry_kill_position = tk.Entry(frame)
        entry_kill_position.pack(side="left", padx=5, fill="x", expand=True)

        def on_kill_position():
            filename = entry_filename.get()
            kill_combo = entry_kill_position.get()
            if not filename:
                messagebox.showwarning("警告", "请输入文件名")
                return
            kill_position_combo(filename, kill_combo)
            update_data_display(filename, listbox_data_board, label_data_board)  # 刷新数据看板

        tk.Button(frame, text="确认杀除", command=on_kill_position).pack(side="right", padx=5)

    create_kill_position_section()  # 添加个十百杀号组合模块

    # 创建杀奇偶、杀大小、杀012路等模块
    def create_kill_section(label, kill_func, placeholder):
        frame = tk.Frame(root)
        frame.pack(pady=15, padx=20, fill="x")

        tk.Label(frame, text=label).pack(side="left", padx=5)
        entry_kill_combo = tk.Entry(frame)
        entry_kill_combo.pack(side="left", padx=5, fill="x", expand=True)

        def on_kill():
            filename = entry_filename.get()
            kill_combo = entry_kill_combo.get()
            if not filename:
                messagebox.showwarning("警告", "请输入文件名")
                return
            if not kill_combo:
                messagebox.showwarning("警告", "请输入有效的组合")
                return
            kill_func(filename, kill_combo)
            update_data_display(filename, listbox_data_board, label_data_board)

        tk.Button(frame, text="确认杀除", command=on_kill).pack(side="right", padx=5)

    create_kill_section("杀奇偶组合：", kill_parity_combo, "输入奇偶组合（如 010）")
    create_kill_section("杀大小组合：", kill_size_combo, "输入大小组合（如 小小小）")
    create_kill_section("杀012路组合：", kill_route_combo, "输入012路组合（如 101）")
    create_kill_section("杀包含两字组合：", kill_containing_combo, "输入包含字（如 01）")
    create_kill_section("杀号码组合：", kill_number_group, "输入号码组合（如 1 4 6 7 9 8）")

    # 添加数据看板区域
    frame_data_board = tk.Frame(root)
    frame_data_board.pack(pady=15, padx=20, fill="both", expand=True)

    label_data_board = tk.Label(frame_data_board, text="实时数据面板 (0条数据)")
    label_data_board.pack()

    listbox_data_board = tk.Listbox(frame_data_board, height=10)
    listbox_data_board.pack(side="left", fill="both", expand=True)

    scroll_bar = tk.Scrollbar(frame_data_board, orient="vertical", command=listbox_data_board.yview)
    scroll_bar.pack(side="right", fill="y")

    listbox_data_board.config(yscrollcommand=scroll_bar.set)
    listbox_data_board.insert(tk.END, "请生成数据或执行操作以刷新数据看板。")

    root.mainloop()


if __name__ == "__main__":
    create_gui()
