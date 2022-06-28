import re

# a = '采购人地址：吉林省长春市繁荣东路555号'
# c = 'tel：213312'
# # b = re.findall('[:： \n]+(.*?)[\n]+',a)
# b = re.findall('[:： ]+(.*)',a)
# c = re.findall('[:： ]+(.*)[ ]*',c)
# print(c)
# import re
#
from logging import exception

data = '''
Condition: Refurbished
Packaging: Brown/White Box
The warranty is through us for 90 Days.

display that makes each image and video appear sharp and crisp. The laptop has Intel Celeron N3060 Dual-Core 1.6 GHz processor with Intel HD graphics 400 and 4 GB RAM that gives lag free experience. The laptop has 16 GB - eMMC SSD which makes all essential data and entertainment files handy. The notebook has two USB 3.0 ports which enables faster file transfer and has IEEE 802.11a/b/g/n/ac wireless LAN for network communication. The laptop comes with 3 cell Li-Polymer battery which gives long run time upto 12.5 hours. It runs on chrome operating system.

Features:
- 11.6-inch (1366 x 768) LCD Display
- Intel Celeron N3060 Processor (Dual-Core, 2.48GHz, 0MB Cache)
- 4GB DDR3 System Memory
- 16GB SSD SATA Solid State Drive (SSD)
- Integrated Intel HD Graphics 2000
- 2 x USB 3.0, 1 x HDMI
- Standard Keyboard and Multi-touch Trackpad
- 1MP Webcam and Integrated Microphone
- No Ethernet, 802.11A and Bluetooth 4.2
- 3-cell Lithium-Polymer Battery
- Chrome OS  Operating System
- .8" x 8.1" x 11.8" (HxWxD); 2.7lbs
- Energy Star Compliant

Whats in the Box:
- HP Chromebook 11 G5 EE (4GB) Black
- AC Adapter

Specifications:

General Information:
- Energy Star Compliant: YES
- Model Number: 1FX82UT#ABA
- Release Year: 2016
- Lifestyle: Education
- Form Factor: Notebook
- Product Line (Notebook): Chromebook
- EPEAT Level: Not Applicable
Storage:
- Hard Drive Speed (RPM): 5400
- Hard Drive Type: Solid State Drive (SSD)
- Hard Drive Interface: SATA
- Hard Drive Size (GB)(0 if none): 16
Inputs/Outputs:
- Total USB-C Ports: 0
- Optical Drive Type: Not Applicable
- Integrated Microphone: YES
- Total DVI Outputs: 0
- Total USB 2.0 Ports: 0
- Total Headphone Outputs: 1
- Mouse Type: Multi-touch Trackpad
- Built-in Speakers: YES
- Total HDMI Outputs: 1
- Fingerprint Reader: NO
- Numeric Keypad: NO
- Backlit Keyboard: NO
- Keyboard Type: Standard
- Total USB 3.0 Ports: 2
- Total Ethernet Ports (RJ-45): 0
- Total DisplayPort Outputs: 0
- Webcam Megapixels (0 if none): 1
- Total VGA Outputs: 0
Processor:
- # of Processor Cores: 2
- Processor Speed (GHz): 2.48
- Processor Series: Intel Celeron
- Processor Model Number: Intel Celeron N3060
- Processor L3 Cache (MB): 0
RAM:
- Memory Type: DDR3
- Total RAM (GB): 4
- Maximum Memory Supported (GB): 4
- Total Memory Slots Available: 1
Graphics:
- Video Memory Available (MB): 0
- Graphics Type: Integrated
- Graphics Card Model Number: Intel HD Graphics 2000
Physical Features:
- Item Dimensions (H x W x D Inches): .8 x 8.1 x 11.8
- Item Weight (LBS): 2.71
- Color (Generic): Black
Display:
- Maximum Resolution (Width x Height): 1366 x 768
- Display Type: LCD
- Touch Screen: NO
- Screen Size (IN): 11.6
Battery:
- Battery Size (# of cells): 3
- Battery Life (HRS): 12.5
- Rechargeable Battery Type: Lithium-Polymer
Networking:
- Bluetooth Compatability: 4.2
- LAN Compatibility: No Wired Ethernet/LAN
- Wireless Network Compatibility: 802.11A
Operating System:
- Operating System Version: Not Applicable
- Desktop Operating System: Chrome OS
'''
# # print(data)
# print(re.findall('[\-\w \(\)]+: [\w \(\)]+',data))

# tel = '142733199801233015'
tel = '1198558613@qq.com'
b1 = re.findall('[0-9]{4}-[0-9]{7,9}|[a-zA-z0-9]{5,20}@[\w]{2,12}\.[a-z]{2,9}',tel)
print(b1)


isinstance(exception, TimeoutError)