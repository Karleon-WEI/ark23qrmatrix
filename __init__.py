# must run in unix-like os
import sys
import os
from random import randint 
from random import sample
from PIL import Image
import qrcode

class QRMatrix:
    color_samples = ('red', 'blue', 'yellow')
    
    
    def __init__(self, 
                 color: str | None = None,
                 salt1: str | None = None,
                 salt2: str | None = None,
                 salt3: str | None = None): 
              
        self.salt1 = salt1
        self.salt2 = salt2
        self.salt3 = salt3
        
        if (color is None):
            self.true_color = None
            self.cipher = None
            self.subcipher = None
        else:
            self.set_true_color(color)

        self.true_salt = salt1
        from PIL import Image
        self.qrmat = Image.Image()
        self.uni_qrwidth = 0
        
    def set_true_color(self, color: str):
        self.true_color = color
        if not self.issalt(self.salt1):
            self.salt1 = str(randint(10, 99))
        self.true_salt = self.salt1
        import crypt
        self.cipher = crypt.crypt(self.true_color, self.true_salt)
        self.subcipher = self.cipher[2:]

    def gen(self):
        if (self.true_color is None):
            true_color = sample(QRMatrix.color_samples, 1)[0]
            self.set_true_color(true_color)
        elif not self.issalt(self.salt1):
            self.salt1 = str(randint(10, 99))       
        self.true_salt = self.salt1
        if not self.issalt(self.salt2):         
            self.salt2 = str(randint(10, 99))
        if not self.issalt(self.salt3):
            self.salt3 = str(randint(10, 99))        
        
    def gen_file_name(self):
        file_name = self.true_color + '-' + self.true_salt + '--' + self.subcipher + '-' + self.salt1 + '-' + self.salt2 + '-' + self.salt3
        self.file_name = file_name.replace(r"/", "~")
        return self.file_name 
        
    def createMatrixQRCode(self, 
                           word: str | None = None,
                           salt1: str | None = None,
                           salt2: str | None = None,
                           salt3: str | None = None,
                           save_to_png: bool = True,
                           dir_path: str = './qrs/',
                           show: bool = False):
        if self.issalt(salt1):         
            self.salt1 = salt1
        if self.issalt(salt2):         
            self.salt2 = salt2  
        if self.issalt(salt3):         
            self.salt3 = salt3
        if (word is not None):
            self.set_true_color(word)

        self.png_path = dir_path
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)
            
        self.gen()
        self.gen_file_name()
        self.img_save_path = os.path.join(self.png_path, self.file_name + '.png')
        
        self.qr0 = qrcode.make(self.subcipher)
        self.qr1 = qrcode.make(self.true_salt)
        self.qr2 = qrcode.make(self.salt2)
        self.qr3 = qrcode.make(self.salt3)
        
        self.uni_qrwidth = self.qr0.size[0]
        self.uni_qrheight = self.qr0.size[1]
        self.qrmat_size = (self.uni_qrwidth * 2, self.uni_qrheight * 2)
        
        
        self.qrmat = Image.new('RGB', self.qrmat_size)
        self.qrmat.paste(self.qr0, (0, 0, self.uni_qrwidth, self.uni_qrheight))  # 左上角
        self.qrmat.paste(self.qr1, (self.uni_qrwidth, 0, self.uni_qrwidth * 2, self.uni_qrheight))  # 右上角
        self.qrmat.paste(self.qr2, (0, self.uni_qrheight, self.uni_qrwidth, self.uni_qrheight * 2))  # 左下角
        self.qrmat.paste(self.qr3, (self.uni_qrwidth, self.uni_qrheight, self.uni_qrwidth * 2, self.uni_qrheight * 2))  # 右下角
        
        if save_to_png:
            self.qrmat.save(self.img_save_path)
            print(self.img_save_path, 'is done.')
        if show: self.qrmat.show()
        return self.qrmat
        
    def createTheAnswerPDF(self, save_to_path: str = './pdfs/'):
        if self.uni_qrwidth > 0:
            temp_image_path = "temp_image.png"
            asmat = Image.new('RGB', self.qrmat_size)
            src_str = self.file_name.replace("~", r"/")
            asqr = qrcode.make(src_str) 
            asqr.save(temp_image_path)
            
            if not os.path.isdir(save_to_path):
                os.makedirs(save_to_path)
            pdf_path = os.path.join(save_to_path, self.file_name + '.pdf')
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.units import mm
            from reportlab.pdfgen import canvas
            
            pdf = canvas.Canvas(pdf_path, pagesize=A4)
            pdf.drawImage(self.img_save_path, 0 * mm, 43 * mm, 210 * mm, 210 * mm)
            pdf.showPage()
            pdf.setFont("Helvetica", 8)
            pdf.drawString(15 * mm, 293 * mm, src_str)
            pdf.drawImage(temp_image_path, 0 * mm, 282 * mm, 15 * mm, 15 * mm)
            os.remove(temp_image_path)
            pdf.save()
            print(pdf_path, 'is done.')

    @staticmethod
    def issalt(salt: str) -> bool:
        return (salt is not None) and isinstance(salt, str) and len(salt) == 2 and salt.isdigit()

if __name__ == '__main__':
    
    for color in ['red', 'blue', 'yellow']:
        for _ in range(5):
            qrm = QRMatrix(color)
            qrm.createMatrixQRCode(dir_path='./case/PNG')
            qrm.createTheAnswerPDF(save_to_path='./case/PDF')
        