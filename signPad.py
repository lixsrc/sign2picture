import tkinter as tk
from PIL import Image, ImageDraw

class TransparentSignaturePad:
    def __init__(self, root, width=600, height=400, pen_size=4, pen_color='black'):
        self.root = root
        self.root.title("签名画板")
        self.width = width
        self.height = height
        self.pen_size = pen_size
        self.pen_color = pen_color

        # 创建Canvas
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='white')
        self.canvas.pack()

        # 初始化Pillow图像 (RGBA模式，透明背景)
        self.image = Image.new("RGBA", (self.width, self.height), (255, 255, 255, 0))
        self.draw = ImageDraw.Draw(self.image)

        # 绑定鼠标事件
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # 添加按钮
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(fill=tk.X)

        self.save_button = tk.Button(self.button_frame, text="保存签名", command=self.save_signature)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.clear_button = tk.Button(self.button_frame, text="清除画板", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=10, pady=10)

        # 初始化绘图状态
        self.last_x, self.last_y = None, None

    def on_button_press(self, event):
        self.last_x, self.last_y = event.x, event.y

    def on_move(self, event):
        x, y = event.x, event.y
        if self.last_x is not None and self.last_y is not None:
            # 在Canvas上绘制
            self.canvas.create_line(self.last_x, self.last_y, x, y,
                                    width=self.pen_size, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE, splinesteps=36)
            # 在Pillow图像上绘制
            self.draw.line([self.last_x, self.last_y, x, y],
                           fill=self.pen_color ,
                           width=self.pen_size)
            self.last_x, self.last_y = x, y

    def on_button_release(self, event):
        self.last_x, self.last_y = None, None

    def save_signature(self):
        # 保存Pillow图像为PNG，保留透明度
        self.image.save("./pics/signature.png", "PNG")
        print("签名已保存为 '/pics/signature.png'")

    def clear_canvas(self):
        self.canvas.delete("all")
        # 清空Pillow图像
        self.draw.rectangle([(0, 0), (self.width, self.height)], fill=(255, 255, 255, 0))
        self.get_position()
        print("画板已清空")


    def get_position(self):
        x_position = self.root.winfo_x()
        y_position = self.root.winfo_y()
        print(f"窗口的当前位置：X = {x_position}, Y = {y_position}")


if __name__ == "__main__":
    root = tk.Tk()
    pad = TransparentSignaturePad(root)
    # root.geometry("600x450+2700+100")

    root.mainloop()