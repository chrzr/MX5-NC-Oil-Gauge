from machine import Pin,I2C,SPI,PWM,Timer
import framebuf
import time
import math
Vbat_Pin = 29

#Pin definition  引脚定义
I2C_SDA = 6
I2C_SDL = 7

DC = 8
CS = 9
SCK = 10
MOSI = 11
MISO = 12
RST = 13

BL = 25

###########################################################################################################
####################################### DRIVERS START #####################################################
###########################################################################################################

#LCD Driver  LCD驱动
class LCD_1inch28(framebuf.FrameBuffer):
    def __init__(self): #SPI initialization  SPI初始化
        self.width = 240
        self.height = 240
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1,100_000_000,polarity=0, phase=0,bits= 8,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        #Define color, Micropython fixed to BRG format  定义颜色，Micropython固定为BRG格式
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.black =   0x0000
        self.brown =   0X8430
        
        self.fill(self.white) #Clear screen  清屏
        self.show()#Show  显示

        self.pwm = PWM(Pin(BL))
        self.pwm.freq(5000) #Turn on the backlight  开背光
        
    def write_cmd(self, cmd): #Write command  写命令
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf): #Write data  写数据
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)
        
    def set_bl_pwm(self,duty): #Set screen brightness  设置屏幕亮度
        self.pwm.duty_u16(duty)#max 65535
        
    def init_display(self): #LCD initialization  LCD初始化
        """Initialize dispaly"""  
        self.rst(1)
        time.sleep(0.01)
        self.rst(0)
        time.sleep(0.01)
        self.rst(1)
        time.sleep(0.05)
        
        self.write_cmd(0xEF)
        self.write_cmd(0xEB)
        self.write_data(0x14) 
        
        self.write_cmd(0xFE) 
        self.write_cmd(0xEF) 

        self.write_cmd(0xEB)
        self.write_data(0x14) 

        self.write_cmd(0x84)
        self.write_data(0x40) 

        self.write_cmd(0x85)
        self.write_data(0xFF) 

        self.write_cmd(0x86)
        self.write_data(0xFF) 

        self.write_cmd(0x87)
        self.write_data(0xFF)

        self.write_cmd(0x88)
        self.write_data(0x0A)

        self.write_cmd(0x89)
        self.write_data(0x21) 

        self.write_cmd(0x8A)
        self.write_data(0x00) 

        self.write_cmd(0x8B)
        self.write_data(0x80) 

        self.write_cmd(0x8C)
        self.write_data(0x01) 

        self.write_cmd(0x8D)
        self.write_data(0x01) 

        self.write_cmd(0x8E)
        self.write_data(0xFF) 

        self.write_cmd(0x8F)
        self.write_data(0xFF) 


        self.write_cmd(0xB6)
        self.write_data(0x00)
        self.write_data(0x20)

        self.write_cmd(0x36)
        self.write_data(0x98)

        self.write_cmd(0x3A)
        self.write_data(0x05) 


        self.write_cmd(0x90)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x08) 

        self.write_cmd(0xBD)
        self.write_data(0x06)
        
        self.write_cmd(0xBC)
        self.write_data(0x00)

        self.write_cmd(0xFF)
        self.write_data(0x60)
        self.write_data(0x01)
        self.write_data(0x04)

        self.write_cmd(0xC3)
        self.write_data(0x13)
        self.write_cmd(0xC4)
        self.write_data(0x13)

        self.write_cmd(0xC9)
        self.write_data(0x22)

        self.write_cmd(0xBE)
        self.write_data(0x11) 

        self.write_cmd(0xE1)
        self.write_data(0x10)
        self.write_data(0x0E)

        self.write_cmd(0xDF)
        self.write_data(0x21)
        self.write_data(0x0c)
        self.write_data(0x02)

        self.write_cmd(0xF0)   
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        self.write_cmd(0xF1)    
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37)  
        self.write_data(0x6F)


        self.write_cmd(0xF2)   
        self.write_data(0x45)
        self.write_data(0x09)
        self.write_data(0x08)
        self.write_data(0x08)
        self.write_data(0x26)
        self.write_data(0x2A)

        self.write_cmd(0xF3)   
        self.write_data(0x43)
        self.write_data(0x70)
        self.write_data(0x72)
        self.write_data(0x36)
        self.write_data(0x37) 
        self.write_data(0x6F)

        self.write_cmd(0xED)
        self.write_data(0x1B) 
        self.write_data(0x0B) 

        self.write_cmd(0xAE)
        self.write_data(0x77)
        
        self.write_cmd(0xCD)
        self.write_data(0x63)


        self.write_cmd(0x70)
        self.write_data(0x07)
        self.write_data(0x07)
        self.write_data(0x04)
        self.write_data(0x0E) 
        self.write_data(0x0F) 
        self.write_data(0x09)
        self.write_data(0x07)
        self.write_data(0x08)
        self.write_data(0x03)

        self.write_cmd(0xE8)
        self.write_data(0x34)

        self.write_cmd(0x62)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x71)
        self.write_data(0xED)
        self.write_data(0x70) 
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x0F)
        self.write_data(0x71)
        self.write_data(0xEF)
        self.write_data(0x70) 
        self.write_data(0x70)

        self.write_cmd(0x63)
        self.write_data(0x18)
        self.write_data(0x11)
        self.write_data(0x71)
        self.write_data(0xF1)
        self.write_data(0x70) 
        self.write_data(0x70)
        self.write_data(0x18)
        self.write_data(0x13)
        self.write_data(0x71)
        self.write_data(0xF3)
        self.write_data(0x70) 
        self.write_data(0x70)

        self.write_cmd(0x64)
        self.write_data(0x28)
        self.write_data(0x29)
        self.write_data(0xF1)
        self.write_data(0x01)
        self.write_data(0xF1)
        self.write_data(0x00)
        self.write_data(0x07)

        self.write_cmd(0x66)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0xCD)
        self.write_data(0x67)
        self.write_data(0x45)
        self.write_data(0x45)
        self.write_data(0x10)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)

        self.write_cmd(0x67)
        self.write_data(0x00)
        self.write_data(0x3C)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x54)
        self.write_data(0x10)
        self.write_data(0x32)
        self.write_data(0x98)

        self.write_cmd(0x74)
        self.write_data(0x10)
        self.write_data(0x85)
        self.write_data(0x80)
        self.write_data(0x00) 
        self.write_data(0x00) 
        self.write_data(0x4E)
        self.write_data(0x00)
        
        self.write_cmd(0x98)
        self.write_data(0x3e)
        self.write_data(0x07)

        self.write_cmd(0x35)
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)
    
    #设置窗口    
    def setWindows(self,Xstart,Ystart,Xend,Yend): 
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(Xstart)
        self.write_data(0x00)
        self.write_data(Xend-1)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(Ystart)
        self.write_data(0x00)
        self.write_data(Yend-1)
        
        self.write_cmd(0x2C)
     
    #Show  显示   
    def show(self): 
        self.setWindows(0,0,self.width,self.height)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
        
    '''
        Partial display, the starting point of the local
        display here is reduced by 10, and the end point
        is increased by 10
    '''
    #Partial display, the starting point of the local display here is reduced by 10, and the end point is increased by 10
    #局部显示，这里的局部显示起点减少10，终点增加10
    def Windows_show(self,Xstart,Ystart,Xend,Yend):
        if Xstart > Xend:
            data = Xstart
            Xstart = Xend
            Xend = data
            
        if (Ystart > Yend):        
            data = Ystart
            Ystart = Yend
            Yend = data
            
        if Xstart <= 10:
            Xstart = 10
        if Ystart <= 10:
            Ystart = 10
            
        Xstart -= 10;Xend += 10
        Ystart -= 10;Yend += 10
        
        self.setWindows(Xstart,Ystart,Xend,Yend)      
        self.cs(1)
        self.dc(1)
        self.cs(0)
        for i in range (Ystart,Yend-1):             
            Addr = (Xstart * 2) + (i * 240 * 2)                
            self.spi.write(self.buffer[Addr : Addr+((Xend-Xstart)*2)])
        self.cs(1)
        
    #Write characters, size is the font size, the minimum is 1  
    #写字符，size为字体大小,最小为1
    def write_text(self,text,x,y,size,color):
        ''' Method to write Text on OLED/LCD Displays
            with a variable font size

            Args:
                text: the string of chars to be displayed
                x: x co-ordinate of starting position
                y: y co-ordinate of starting position
                size: font size of text
                color: color of text to be displayed
        '''
        background = self.pixel(x,y)
        info = []
        # Creating reference charaters to read their values
        self.text(text,x,y,color)
        for i in range(x,x+(8*len(text))):
            for j in range(y,y+8):
                # Fetching amd saving details of pixels, such as
                # x co-ordinate, y co-ordinate, and color of the pixel
                px_color = self.pixel(i,j)
                info.append((i,j,px_color)) if px_color == color else None
        # Clearing the reference characters from the screen
        self.text(text,x,y,background)
        # Writing the custom-sized font characters on screen
        for px_info in info:
            self.fill_rect(size*px_info[0] - (size-1)*x , size*px_info[1] - (size-1)*y, size, size, px_info[2]) 
    
        
#Touch drive  触摸驱动
class Touch_CST816T(object):
    #Initialize the touch chip  初始化触摸芯片
    def __init__(self,address=0x15,mode=0,i2c_num=1,i2c_sda=6,i2c_scl=7,int_pin=21,rst_pin=22,LCD=None):
        self._bus = I2C(id=i2c_num,scl=Pin(i2c_scl),sda=Pin(i2c_sda),freq=400_000) #Initialize I2C 初始化I2C
        self._address = address #Set slave address  设置从机地址
        self.int=Pin(int_pin,Pin.IN, Pin.PULL_UP)     
        self.tim = Timer()     
        self.rst=Pin(rst_pin,Pin.OUT)
        self.Reset()
        bRet=self.WhoAmI()
        if bRet :
            print("Success:Detected CST816T.")
            Rev= self.Read_Revision()
            print("CST816T Revision = {}".format(Rev))
            self.Stop_Sleep()
        else    :
            print("Error: Not Detected CST816T.")
            return None
        self.Mode = mode
        self.Gestures="None"
        self.Flag = self.Flgh =self.l = 0
        self.X_point = self.Y_point = 0
        self.int.irq(handler=self.Int_Callback,trigger=Pin.IRQ_FALLING)
      
    def _read_byte(self,cmd):
        rec=self._bus.readfrom_mem(int(self._address),int(cmd),1)
        return rec[0]
    
    def _read_block(self, reg, length=1):
        rec=self._bus.readfrom_mem(int(self._address),int(reg),length)
        return rec
    
    def _write_byte(self,cmd,val):
        self._bus.writeto_mem(int(self._address),int(cmd),bytes([int(val)]))

    def WhoAmI(self):
        if (0xB5) != self._read_byte(0xA7):
            return False
        return True
    
    def Read_Revision(self):
        return self._read_byte(0xA9)
      
    #Stop sleeping  停止睡眠
    def Stop_Sleep(self):
        self._write_byte(0xFE,0x01)
    
    #Reset  复位    
    def Reset(self):
        self.rst(0)
        time.sleep_ms(1)
        self.rst(1)
        time.sleep_ms(50)
    
    #Set mode  设置模式   
    def Set_Mode(self,mode,callback_time=10,rest_time=5): 
        # mode = 0 gestures mode 
        # mode = 1 point mode 
        # mode = 2 mixed mode 
        if (mode == 1):      
            self._write_byte(0xFA,0X41)
            
        elif (mode == 2) :
            self._write_byte(0xFA,0X71)
            
        else:
            self._write_byte(0xFA,0X11)
            self._write_byte(0xEC,0X01)
     
    #Get the coordinates of the touch  获取触摸的坐标
    def get_point(self):
        xy_point = self._read_block(0x03,4)
        
        x_point= ((xy_point[0]&0x0f)<<8)+xy_point[1]
        y_point= ((xy_point[2]&0x0f)<<8)+xy_point[3]
        
        self.X_point=x_point
        self.Y_point=y_point
        
    def Int_Callback(self,pin):
        if self.Mode == 0 :
            self.Gestures = self._read_byte(0x01)

        elif self.Mode == 1:           
            self.Flag = 1
            self.get_point()

    def Timer_callback(self,t):
        self.l += 1
        if self.l > 100:
            self.l = 50

class QMI8658(object):
    def __init__(self,address=0X6B):
        self._address = address
        self._bus = I2C(id=1,scl=Pin(I2C_SDL),sda=Pin(I2C_SDA),freq=100_000)
        bRet=self.WhoAmI()
        if bRet :
            self.Read_Revision()
        else    :
            return NULL
        self.Config_apply()

    def _read_byte(self,cmd):
        rec=self._bus.readfrom_mem(int(self._address),int(cmd),1)
        return rec[0]
    def _read_block(self, reg, length=1):
        rec=self._bus.readfrom_mem(int(self._address),int(reg),length)
        return rec
    def _read_u16(self,cmd):
        LSB = self._bus.readfrom_mem(int(self._address),int(cmd),1)
        MSB = self._bus.readfrom_mem(int(self._address),int(cmd)+1,1)
        return (MSB[0] << 8) + LSB[0]
    def _write_byte(self,cmd,val):
        self._bus.writeto_mem(int(self._address),int(cmd),bytes([int(val)]))
        
    def WhoAmI(self):
        bRet=False
        if (0x05) == self._read_byte(0x00):
            bRet = True
        return bRet
    def Read_Revision(self):
        return self._read_byte(0x01)
    def Config_apply(self):
        # REG CTRL1
        self._write_byte(0x02,0x60)
        # REG CTRL2 : QMI8658AccRange_8g  and QMI8658AccOdr_1000Hz
        self._write_byte(0x03,0x23)
        # REG CTRL3 : QMI8658GyrRange_512dps and QMI8658GyrOdr_1000Hz
        self._write_byte(0x04,0x53)
        # REG CTRL4 : No
        self._write_byte(0x05,0x00)
        # REG CTRL5 : Enable Gyroscope And Accelerometer Low-Pass Filter 
        self._write_byte(0x06,0x11)
        # REG CTRL6 : Disables Motion on Demand.
        self._write_byte(0x07,0x00)
        # REG CTRL7 : Enable Gyroscope And Accelerometer
        self._write_byte(0x08,0x03)

    def Read_Raw_XYZ(self):
        xyz=[0,0,0,0,0,0]
        raw_timestamp = self._read_block(0x30,3)
        raw_acc_xyz=self._read_block(0x35,6)
        raw_gyro_xyz=self._read_block(0x3b,6)
        raw_xyz=self._read_block(0x35,12)
        timestamp = (raw_timestamp[2]<<16)|(raw_timestamp[1]<<8)|(raw_timestamp[0])
        for i in range(6):
            # xyz[i]=(raw_acc_xyz[(i*2)+1]<<8)|(raw_acc_xyz[i*2])
            # xyz[i+3]=(raw_gyro_xyz[((i+3)*2)+1]<<8)|(raw_gyro_xyz[(i+3)*2])
            xyz[i] = (raw_xyz[(i*2)+1]<<8)|(raw_xyz[i*2])
            if xyz[i] >= 32767:
                xyz[i] = xyz[i]-65535
        return xyz
    def Read_XYZ(self):
        xyz=[0,0,0,0,0,0]
        raw_xyz=self.Read_Raw_XYZ()  
        #QMI8658AccRange_8g
        acc_lsb_div=(1<<12)
        #QMI8658GyrRange_512dps
        gyro_lsb_div = 64
        for i in range(3):
            xyz[i]=raw_xyz[i]/acc_lsb_div#(acc_lsb_div/1000.0)
            xyz[i+3]=raw_xyz[i+3]*1.0/gyro_lsb_div
        return xyz

#########################################################################################################
####################################### I2C DRIVERS #####################################################
#########################################################################################################
    
    
# The MIT License (MIT)
#
# Copyright (c) 2016 Radomir Dopieralski (@deshipu),
#               2017 Robert Hammelrath (@robert-hh)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
import utime as time

_REGISTER_MASK = const(0x03)
_REGISTER_CONVERT = const(0x00)
_REGISTER_CONFIG = const(0x01)
_REGISTER_LOWTHRESH = const(0x02)
_REGISTER_HITHRESH = const(0x03)

_OS_MASK = const(0x8000)
_OS_SINGLE = const(0x8000)  # Write: Set to start a single-conversion
_OS_BUSY = const(0x0000)  # Read: Bit=0 when conversion is in progress
_OS_NOTBUSY = const(0x8000)  # Read: Bit=1 when no conversion is in progress

_MUX_MASK = const(0x7000)
_MUX_DIFF_0_1 = const(0x0000)  # Differential P  =  AIN0, N  =  AIN1 (default)
_MUX_DIFF_0_3 = const(0x1000)  # Differential P  =  AIN0, N  =  AIN3
_MUX_DIFF_1_3 = const(0x2000)  # Differential P  =  AIN1, N  =  AIN3
_MUX_DIFF_2_3 = const(0x3000)  # Differential P  =  AIN2, N  =  AIN3
_MUX_SINGLE_0 = const(0x4000)  # Single-ended AIN0
_MUX_SINGLE_1 = const(0x5000)  # Single-ended AIN1
_MUX_SINGLE_2 = const(0x6000)  # Single-ended AIN2
_MUX_SINGLE_3 = const(0x7000)  # Single-ended AIN3

_PGA_MASK = const(0x0E00)
_PGA_6_144V = const(0x0000)  # +/-6.144V range  =  Gain 2/3
_PGA_4_096V = const(0x0200)  # +/-4.096V range  =  Gain 1
_PGA_2_048V = const(0x0400)  # +/-2.048V range  =  Gain 2 (default)
_PGA_1_024V = const(0x0600)  # +/-1.024V range  =  Gain 4
_PGA_0_512V = const(0x0800)  # +/-0.512V range  =  Gain 8
_PGA_0_256V = const(0x0A00)  # +/-0.256V range  =  Gain 16

_MODE_MASK = const(0x0100)
_MODE_CONTIN = const(0x0000)  # Continuous conversion mode
_MODE_SINGLE = const(0x0100)  # Power-down single-shot mode (default)

_DR_MASK = const(0x00E0)     # Values ADS1015/ADS1115
_DR_128SPS = const(0x0000)   # 128 /8 samples per second
_DR_250SPS = const(0x0020)   # 250 /16 samples per second
_DR_490SPS = const(0x0040)   # 490 /32 samples per second
_DR_920SPS = const(0x0060)   # 920 /64 samples per second
_DR_1600SPS = const(0x0080)  # 1600/128 samples per second (default)
_DR_2400SPS = const(0x00A0)  # 2400/250 samples per second
_DR_3300SPS = const(0x00C0)  # 3300/475 samples per second
_DR_860SPS = const(0x00E0)  # -   /860 samples per Second

_CMODE_MASK = const(0x0010)
_CMODE_TRAD = const(0x0000)  # Traditional comparator with hysteresis (default)
_CMODE_WINDOW = const(0x0010)  # Window comparator

_CPOL_MASK = const(0x0008)
_CPOL_ACTVLOW = const(0x0000)  # ALERT/RDY pin is low when active (default)
_CPOL_ACTVHI = const(0x0008)  # ALERT/RDY pin is high when active

_CLAT_MASK = const(0x0004)  # Determines if ALERT/RDY pin latches once asserted
_CLAT_NONLAT = const(0x0000)  # Non-latching comparator (default)
_CLAT_LATCH = const(0x0004)  # Latching comparator

_CQUE_MASK = const(0x0003)
_CQUE_1CONV = const(0x0000)  # Assert ALERT/RDY after one conversions
_CQUE_2CONV = const(0x0001)  # Assert ALERT/RDY after two conversions
_CQUE_4CONV = const(0x0002)  # Assert ALERT/RDY after four conversions
# Disable the comparator and put ALERT/RDY in high state (default)
_CQUE_NONE = const(0x0003)

_GAINS = (
    _PGA_6_144V,  # 2/3x
    _PGA_4_096V,  # 1x
    _PGA_2_048V,  # 2x
    _PGA_1_024V,  # 4x
    _PGA_0_512V,  # 8x
    _PGA_0_256V   # 16x
)

_GAINS_V = (
    6.144,  # 2/3x
    4.096,  # 1x
    2.048,  # 2x
    1.024,  # 4x
    0.512,  # 8x
    0.256  # 16x
)

_CHANNELS = {
    (0, None): _MUX_SINGLE_0,
    (1, None): _MUX_SINGLE_1,
    (2, None): _MUX_SINGLE_2,
    (3, None): _MUX_SINGLE_3,
    (0, 1): _MUX_DIFF_0_1,
    (0, 3): _MUX_DIFF_0_3,
    (1, 3): _MUX_DIFF_1_3,
    (2, 3): _MUX_DIFF_2_3,
}

_RATES = (
    _DR_128SPS,   # 128/8 samples per second
    _DR_250SPS,   # 250/16 samples per second
    _DR_490SPS,   # 490/32 samples per second
    _DR_920SPS,   # 920/64 samples per second
    _DR_1600SPS,  # 1600/128 samples per second (default)
    _DR_2400SPS,  # 2400/250 samples per second
    _DR_3300SPS,  # 3300/475 samples per second
    _DR_860SPS    # - /860 samples per Second
)


class ADS1115:
    def __init__(self, i2c, address=0x48, gain=1):
        self.i2c = i2c
        self.address = address
        self.gain = gain
        self.temp2 = bytearray(2)

    def _write_register(self, register, value):
        self.temp2[0] = value >> 8
        self.temp2[1] = value & 0xff
        self.i2c.writeto_mem(self.address, register, self.temp2)

    def _read_register(self, register):
        self.i2c.readfrom_mem_into(self.address, register, self.temp2)
        return (self.temp2[0] << 8) | self.temp2[1]

    def raw_to_v(self, raw):
        v_p_b = _GAINS_V[self.gain] / 32768
        return raw * v_p_b

    def set_conv(self, rate=4, channel1=0, channel2=None):
        """Set mode for read_rev"""
        self.mode = (_CQUE_NONE | _CLAT_NONLAT |
                     _CPOL_ACTVLOW | _CMODE_TRAD | _RATES[rate] |
                     _MODE_SINGLE | _OS_SINGLE | _GAINS[self.gain] |
                     _CHANNELS[(channel1, channel2)])

    def read(self, rate=4, channel1=0, channel2=None):
        """Read voltage between a channel and GND.
           Time depends on conversion rate."""
        self._write_register(_REGISTER_CONFIG, (_CQUE_NONE | _CLAT_NONLAT |
                             _CPOL_ACTVLOW | _CMODE_TRAD | _RATES[rate] |
                             _MODE_SINGLE | _OS_SINGLE | _GAINS[self.gain] |
                             _CHANNELS[(channel1, channel2)]))
        while not self._read_register(_REGISTER_CONFIG) & _OS_NOTBUSY:
            time.sleep_ms(1)
        res = self._read_register(_REGISTER_CONVERT)
        return res if res < 32768 else res - 65536

    def read_rev(self):
        """Read voltage between a channel and GND. and then start
           the next conversion."""
        res = self._read_register(_REGISTER_CONVERT)
        self._write_register(_REGISTER_CONFIG, self.mode)
        return res if res < 32768 else res - 65536

    def alert_start(self, rate=4, channel1=0, channel2=None,
                    threshold_high=0x4000, threshold_low=0, latched=False) :
        """Start continuous measurement, set ALERT pin on threshold."""
        self._write_register(_REGISTER_LOWTHRESH, threshold_low)
        self._write_register(_REGISTER_HITHRESH, threshold_high)
        self._write_register(_REGISTER_CONFIG, _CQUE_1CONV |
                             _CLAT_LATCH if latched else _CLAT_NONLAT |
                             _CPOL_ACTVLOW | _CMODE_TRAD | _RATES[rate] |
                             _MODE_CONTIN | _GAINS[self.gain] |
                             _CHANNELS[(channel1, channel2)])

    def conversion_start(self, rate=4, channel1=0, channel2=None):
        """Start continuous measurement, trigger on ALERT/RDY pin."""
        self._write_register(_REGISTER_LOWTHRESH, 0)
        self._write_register(_REGISTER_HITHRESH, 0x8000)
        self._write_register(_REGISTER_CONFIG, _CQUE_1CONV | _CLAT_NONLAT |
                             _CPOL_ACTVLOW | _CMODE_TRAD | _RATES[rate] |
                             _MODE_CONTIN | _GAINS[self.gain] |
                             _CHANNELS[(channel1, channel2)])

    def alert_read(self):
        """Get the last reading from the continuous measurement."""
        res = self._read_register(_REGISTER_CONVERT)
        return res if res < 32768 else res - 65536


class ADS1113(ADS1115):
    def __init__(self, i2c, address=0x48):
        super().__init__(i2c, address, 1)

    def raw_to_v(self, raw):
        return super().raw_to_v(raw)

    def read(self, rate=4):
        return super().read(rate, 0, 1)

    def alert_start(self, rate=4, threshold_high=0x4000, threshold_low=0, latched=False):
        return super().alert_start(rate, 0, 1, threshold_high, threshold_low, latched)

    def alert_read(self):
        return super().alert_read()


class ADS1114(ADS1115):
    def __init__(self, i2c, address=0x48, gain=1):
        super().__init__(i2c, address, gain)

    def raw_to_v(self, raw):
        return super().raw_to_v(raw)

    def read(self, rate=4):
        return super().read(rate, 0, 1)

    def alert_start(self, rate=4, threshold_high=0x4000, threshold_low=0, latched=False):
        return super().alert_start(rate, 0, 1, threshold_high,
            threshold_low, latched)

    def alert_read(self):
        return super().alert_read()


class ADS1015(ADS1115):
    def __init__(self, i2c, address=0x48, gain=1):
        super().__init__(i2c, address, gain)

    def raw_to_v(self, raw):
        return super().raw_to_v(raw << 4)

    def read(self, rate=4, channel1=0, channel2=None):
        return super().read(rate, channel1, channel2) >> 4

    def alert_start(self, rate=4, channel1=0, channel2=None, threshold_high=0x400,
        threshold_low=0, latched=False):
        return super().alert_start(rate, channel1, channel2, threshold_high << 4,
            threshold_low << 4, latched)

    def alert_read(self):
        return super().alert_read() >> 4

    
#########################################################################################################
####################################### DRIVERS END #####################################################
#########################################################################################################

# ========== Main starts here ============

# Set up colours

def colour(R,G,B): # Convert RGB888 to RGB565
    return (((G&0b00011100)<<3) +((B&0b11111000)>>3)<<8) + (R&0b11111000)+((G&0b11100000)>>5)

w = colour(255,255,255)
r = colour(255,0,0)
g = colour(0,255,0)
b = colour(0,0,255)
y = colour(255,255,0)
c = colour(0,255,255)
m = colour(255,0,255)
g = colour(100,100,100)
o = colour(255,65,51)
bl = colour(0,0,0)

colours = [o,r,y,g,c,b,m,w,g,bl] # List of colours, 0 to 9

# Set up LCD display screen and Touch sensor
LCD = LCD_1inch28()
LCD.set_bl_pwm(65535)

Touch=Touch_CST816T(mode=0,LCD=LCD) # Touch ON - mode 1

mode = 0
Touch.Set_Mode(mode)

# ========== Config starts here ==========

# Define I2C Pins
i2c=I2C(0, freq=400000, sda=machine.Pin(16), scl=machine.Pin(17))
adc = ADS1115(i2c, address=0x48, gain=0)

oil_temp_upper = 110.0
oil_press_lower = 1.0

default_color = 0
cp = default_color
default_background_color = 9

contrast_color = 0
center_text = "chrzr"
center_color = 0
sync_color = True

alert_color = 9
alert_contrast_color = 9
alert_background_color = 1
alert_center_color = 9

precision = 1

# ========== Config ends here ==========

def scale_value(value, in_min, in_max, out_min, out_max):
  scaled_value = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
  return scaled_value

def get_sensor_values(precision):
  # Get Pressure Value from Sensor
  sensor1_reading = adc.read(1, 0)
  PressureBar = scale_value(sensor1_reading, 100, 1100, 500, 4000) / 10000
  
  if precision == 0:
      PressureBar = int(PressureBar)
  else:
      PressureBar = round(float(PressureBar), precision)
  
  time.sleep_ms(1)
  # Get NTC Voltage from Sensor
  sensor2_adc = adc.read(1, 1)
  sensor2_voltage = adc.raw_to_v(adc.read(1, 1))
  
  print("V2: " + str(sensor2_voltage))
   
  Rt = (5 / sensor2_voltage  - 1)
  Rt = 1050 / Rt 
   
  print("NTC: " + str(Rt))
        
  A = 0.001290549975
  B = 0.0002613150625
  C = 0.0000001623214479
        
  TempK = 1 / (A + (B * math.log(Rt)) + C * math.pow(math.log(Rt), 3))
      
  TempC = TempK - 273.15
  TempC = int(TempC)
  
  return PressureBar, TempC

def compare_values(val, val_compare, comparator):
    
    if (comparator == "<=" and (float(val) <= val_compare)) or (comparator == ">=" and (float(val) >= val_compare)):
        return True
    else:
        return False

def draw_oil_temp(val, cp, alert):

    if len(val) <= 2 :
        val = " " + val
        
    if alert == True:
        val_color = alert_color
        cp = alert_contrast_color
        local_contrast_color = alert_contrast_color
        LCD.rect(0,0,250,100,colours[alert_background_color],True)
    else:
        val_color = cp
        
        if sync_color == False:
            local_contrast_color = contrast_color
        else:
            local_contrast_color = cp
            
        LCD.rect(0,0,250,100,colours[default_background_color],True)

    LCD.write_text("OIL TEMP",55,65,2,colours[local_contrast_color])
    LCD.write_text(val,58,20,4,colours[val_color])
    LCD.write_text("C",155,33,2,colours[val_color])
    LCD.hline(0, 95,250,colours[local_contrast_color])
    LCD.hline(0, 96,250,colours[local_contrast_color])
    LCD.hline(0, 97,250,colours[local_contrast_color])
    
def draw_oil_pressure(val, cp, alert):
    
    if len(val) == 1 :
        val = "  " + val
    elif len(val) == 3:
        val = " " + val
    
    if alert == True:
        val_color = alert_color
        cp = alert_contrast_color
        local_contrast_color = alert_contrast_color
        LCD.rect(0,131,250,139,colours[alert_background_color],True)
    else:
        val_color = cp
        
        if sync_color == False:
            local_contrast_color = contrast_color
        else:
            local_contrast_color = cp
            
        LCD.rect(0,131,250,139,colours[default_background_color],True)
    
    LCD.hline(0, 134,250,colours[local_contrast_color])
    LCD.hline(0, 135,250,colours[local_contrast_color])
    LCD.hline(0, 136,250,colours[local_contrast_color])
    LCD.write_text("OIL PRESS",50,150,2,colours[local_contrast_color])
    LCD.write_text(val,45,180,4,colours[val_color])
    LCD.write_text("bar",100,215,2,colours[val_color])

def draw_center(val, cp, alert):
    
    if alert == True:
        local_center_color = alert_center_color    
    else:
        if sync_color == False:
            local_center_color = center_color
        else:
            local_center_color = cp
        
    LCD.write_text(val,60,105,3,colours[local_center_color])

def draw_screen(cp, oil_temp, oil_press):
    
    LCD.fill(0)
    
    draw_oil_temp(oil_temp, cp, compare_values(oil_temp, oil_temp_upper, ">="))
    draw_oil_pressure(oil_press, cp, compare_values(oil_press, oil_press_lower, "<="))
    draw_center(center_text, cp, False)
    
    LCD.show()

running = True
try:
    while running:
    
        if Touch.Gestures == 0x01: # UP
            Touch.Gestures = 0  # Clear the current gesture
            print(precision)
            precision = precision + 1
            if precision > 3: precision = 0
            
        elif Touch.Gestures == 0x02: # Down
            Touch.Gestures = 0  # Clear the current gesture
            print(precision)
            precision = precision - 1
            if precision < 0: precision = 3
            
        elif Touch.Gestures == 0x04: # Right
            Touch.Gestures = 0  # Clear the current gesture
            cp = cp + 1
            if cp > 9: cp = 0
            
        elif Touch.Gestures == 0x03: # Left
            Touch.Gestures = 0  # Clear the current gesture
            cp = cp - 1
            if cp < 0: cp = 9
            
        # Double tap or Long Press to HALT
        #elif (Touch.Gestures == 0x0C) or (Touch.Gestures == 0x0B):
        #    running = False
        #    break
        
        sensor_values = get_sensor_values(precision)
        
        PressureBar = sensor_values[0]
        TempC = sensor_values[1]
        
        draw_screen(cp, str(TempC), str(PressureBar))
        
        time.sleep(0.1) # Delay to untouch - Debounce

except KeyboardInterrupt:
    pass

# Tidy up after CTRL-C / KeyboardInterrupt or HALT Gesture
LCD.fill(0)
LCD.show()
