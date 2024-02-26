import upnpclient
import qrcode
import os
import wx
import http.server
import socketserver
import socket
import threading
import time

app = wx.App()

# 使用wxPython渲染二维码
class QRCodeFrame(wx.Frame):
    def __init__(self, url):
        wx.Frame.__init__(self, None, title="请使用手机扫描二维码", size=(300, 300))
        panel = wx.Panel(self, -1, style=wx.BORDER_SUNKEN)
        self.qrcode_bitmap = self.create_qrcode_bitmap(url)
        self.imgBitmap = wx.StaticBitmap(panel, -1, self.qrcode_bitmap, style=wx.ALIGN_CENTER)
        self.imgBitmap.SetSize((300, 300))
        # 自适应窗口大小，水平居中, 垂直居中
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.imgBitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        panel.SetSizer(sizer)
        sizer.Fit(self)
        sizer.SetSizeHints(self)
        self.Centre()

    def create_qrcode_bitmap(self, url):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img = img.convert("RGB")
        width, height = img.size
        img = wx.Bitmap.FromBuffer(width, height, img.tobytes())

        return img

    def update_qrcode(self, new_url):
        print("更新二维码->>>", new_url)
        self.qrcode_bitmap.Destroy()  # Destroy the old bitmap
        self.qrcode_bitmap = self.create_qrcode_bitmap(new_url)
        self.imgBitmap.SetBitmap(self.qrcode_bitmap)
        # imgBitmap 左右居中 并将大小设置为300x300
        self.imgBitmap.SetSize((300, 300))
        self.Refresh()

def get_local_ip():
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip
  except Exception as e:
    print("获取本地ip失败：{}".format(e))
    return None


class HttpHandler(http.server.SimpleHTTPRequestHandler):
  # 返回页面文件
  def do_GET(self):
    self.send_response(200)
    self.send_header("Content-type", "text/html")
    self.end_headers()

    # 返回本地的index.html文件
    with open("src/html/index.html", "rb") as f:
      self.wfile.write(f.read())
  # 测试是否可以连接的接口, 返回json数据
  def do_POST(self):
    self.send_response(200)
    self.send_header("Content-type", "application/json")
    self.end_headers()
    self.wfile.write(b'{"status": "ok"}')


def start_web_server(port = 9790, frame = None):
    # 检测端口是否被占用, 并启动web服务，然后返回端口号
    while True:
        try:
            with socketserver.TCPServer(("", port), HttpHandler) as httpd:
                if frame:
                    frame.update_qrcode("http://{}:{}".format(get_local_ip(), port))
                    # 十秒后更新二维码
                    threading.Timer(3, frame.update_qrcode, ["    Lorem ipsum dolor sit amet consectetur adipisicing elit. Odio tempore magni numquam, atque magnam reprehenderit hic! Deserunt quaerat harum quas alias maxime. Officia nulla voluptate voluptas quos totam exercitationem distinctio aspernatur consequatur expedita ipsam consectetur non dignissimos error sit quaerat enim, hic harum minus minima soluta odit provident molestiae commodi nihil. Culpa, quidem rem voluptate sed a odit reprehenderit. Asperiores voluptatem maiores repellat reprehenderit! Porro reprehenderit beatae, blanditiis aut nemo itaque qui natus quasi eligendi excepturi eaque iure tenetur modi illum odit sunt cupiditate est in sequi rem delectus. Ad nostrum doloribus aliquid. Sapiente odit suscipit blanditiis repellendus commodi. Deleniti!  ????????"]).start()
                httpd.serve_forever()

        except Exception as e:
            print("启动服务失败：{}".format(e))
            # 代码暂停
            print("端口 {} 被占用，尝试使用其他端口".format(port))
            port += 1
            continue
        break
    return port


def render(boolean, ip, port = 9790):
    if boolean:
        frame = QRCodeFrame("http://{}:{}".format(ip, port))
        server_thread = threading.Thread(target=start_web_server, args=(port, frame,))
        server_thread.daemon = True
        server_thread.start()
        frame.Show()

    else:
        wx.StaticText(frm, -1, "启动服务失败", style=wx.ALIGN_CENTER)
    app.MainLoop()



def search_upnp_devices():
    devices = upnpclient.discover()
    print("查找到 {} 个 UPnP 设备：".format(len(devices)))
    for i, device in enumerate(devices):
        print("设备 {} ：{}".format(i + 1, device.friendly_name))
        for service in device.services:
            print(service)
        print("\n")

def start():
    ip = get_local_ip()
    port = 9790
    if ip:
        render(True, ip, port)
    else:
        render(False)

start()
