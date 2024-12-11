import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import pandas as pd
from datetime import datetime

CSV_FILE = "nhan_vien.csv"
def save_to_csv(data):
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data)

def load_csv():
    try:
        with open(CSV_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            return list(reader)
    except FileNotFoundError:
        return []

def save_employee():
    data = [
        entry_ma.get(),
        entry_ten.get(),
        entry_don_vi.get(),
        entry_chuc_danh.get(),
        entry_ngay_sinh.get(),
        entry_gioi_tinh.get(),
        entry_cmnd.get(),
        entry_ngay_cap.get(),
    ]
    if all(data):
        save_to_csv(data)
        messagebox.showinfo("Thành công", "Đã lưu thông tin nhân viên!")
        clear_inputs()
    else:
        messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

def clear_inputs():
    for widget in entries:
        widget.delete(0, tk.END)

def show_birthday_today():
    data = load_csv()
    today = datetime.now().strftime("%d/%m/%Y")
    result = [row for row in data if row[4] == today]
    if result:
        result_str = "\n".join([f"Mã: {row[0]}, Tên: {row[1]}" for row in result])
        messagebox.showinfo("Sinh nhật hôm nay", result_str)
    else:
        messagebox.showinfo("Sinh nhật hôm nay", "Không có nhân viên nào sinh nhật hôm nay.")

def export_to_excel():
    data = load_csv()
    if data:
        df = pd.DataFrame(data, columns=["Mã", "Tên", "Đơn vị", "Chức danh", "Ngày sinh", "Giới tính", "Số CMND", "Ngày cấp"])
        df['Tuổi'] = df['Ngày sinh'].apply(lambda x: (datetime.now() - datetime.strptime(x, "%d/%m/%Y")).days // 365)
        df = df.sort_values(by="Tuổi", ascending=False)
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Thành công", f"Đã xuất danh sách ra {file_path}")
    else:
        messagebox.showwarning("Lỗi", "Danh sách nhân viên rỗng!")

root = tk.Tk()
root.title("Quản lý thông tin nhân viên")
root.geometry("600x400")

labels = ["Mã số", "Tên", "Đơn vị", "Chức danh", "Ngày sinh (DD/MM/YYYY)", "Giới tính", "Số CMND", "Ngày cấp (DD/MM/YYYY)"]
entries = []

for i, text in enumerate(labels):
    label = tk.Label(root, text=text)
    label.grid(row=i, column=0, padx=10, pady=5, sticky=tk.W)
    entry = tk.Entry(root, width=40)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries.append(entry)

entry_ma, entry_ten, entry_don_vi, entry_chuc_danh, entry_ngay_sinh, entry_gioi_tinh, entry_cmnd, entry_ngay_cap = entries

btn_save = tk.Button(root, text="Lưu thông tin", command=save_employee)
btn_save.grid(row=9, column=0, padx=10, pady=10)

btn_birthday = tk.Button(root, text="Sinh nhật hôm nay", command=show_birthday_today)
btn_birthday.grid(row=9, column=1, padx=10, pady=10)

btn_export = tk.Button(root, text="Xuất danh sách", command=export_to_excel)
btn_export.grid(row=10, column=0, padx=10, pady=10)

root.mainloop()