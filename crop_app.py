import cv2
import tkinter as tk
from tkinter import filedialog
img=None
clone=None
cropped_img=None
drawing=False
ix,iy=-1,-1
def draw_rectangle(event,x,y,flags,param):
    global ix,iy,drawing,img,cropped_img
    if event==cv2.EVENT_LBUTTONDOWN:
        drawing=True
        ix,iy=x,y
    elif event==cv2.EVENT_MOUSEMOVE and drawing:
        temp=img.copy()
        cv2.rectangle(temp,(ix,iy),(x,y),(0,255,0),2)
        cv2.imshow("Image",temp)
    elif event==cv2.EVENT_LBUTTONUP:
        drawing=False
        x1,y1=min(ix,x),min(iy,y)
        x2,y2=max(ix,x),max(iy,y)
        cropped_img=img[y1:y2,x1:x2]
        if cropped_img.size!=0:
            img=cropped_img.copy()  
            cv2.imshow("Image",img)
def select_image():
    global img,clone
    path=filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files","*.jpg *.jpeg *.png *.bmp")]
    )
    if not path:
        return
    img=cv2.imread(path)
    clone=img.copy()  
    root.destroy()  
    start_opencv()
def start_opencv():
    global img,clone,cropped_img
    cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
    cv2.imshow("Image",img)
    cv2.setMouseCallback("Image",draw_rectangle)
    while True:
        cv2.imshow("Image",img)
        key=cv2.waitKey(1) & 0xFF
        if key==ord('s') and cropped_img is not None:
            save_path=filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG","*.jpg"), ("PNG","*.png")]
            )
            if save_path:
                cv2.imwrite(save_path, img)
                print(f"Image Saved: {save_path}")
        elif key==ord('r'):
            img=clone.copy()
            cropped_img=None
            cv2.imshow("Image",img)
        elif key==27:
            break

    cv2.destroyAllWindows()
root=tk.Tk()
root.title("Image Crop Instructions")
root.geometry("350x200")
root.resizable(False, False)
tk.Label(
    root,
    text="Image Crop Tool",
    font=("Arial",14,"bold")
).pack(pady=10)
tk.Label(
    root,
    text="Instructions:\n\n"
         "S  → Save cropped image\n"
         "R  → Re-crop selection\n"
         "ESC → Exit application",
    font=("Arial", 10),
    justify="left"
).pack(pady=5)
tk.Button(
    root,
    text="Select Image",
    width=20,
    command=select_image
).pack(pady=15)
root.mainloop()