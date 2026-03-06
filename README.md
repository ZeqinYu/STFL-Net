# STFL-Net and STFD

---

Official implementation of **STFL-Net** and the **STFD** dataset from our ICASSP 2023 paper “Learning to Locate the Text Forgery in Smartphone Screenshots”. <br>
[![github](https://img.shields.io/badge/-Github-black?logo=github)](https://github.com/ZeqinYu/STFL-Net) [![Paper](https://img.shields.io/badge/Paper-PDF-informational)](https://ieeexplore.ieee.org/abstract/document/10095070/) <br> 
Zeqin Yu, Bin Li, Yuzhen Lin, Jinhua Zeng, Jishen Zeng  

(_In collaboration with **Alibaba Security**_)

> - Parts of **STFD** were adopted in the <br>
>   □ ["2022 Real-World Image Forgery Detection Challenge" (真实场景篡改图像检测挑战赛)](https://tianchi.aliyun.com/competition/entrance/531945/introduction?spm=5176.12281949.1003.1.c90d2448TlNT6k).  
> - 🧐 *Funny story*: We discovered that another subset of **STFD** resurfaced in the ICDAR 2023 competitions under a different partnership, although the organizers have not publicly disclosed the source: <br>
>   □ ["DTT in Images 1: Text Manipulation Classification"](https://tianchi.aliyun.com/competition/entrance/532048/rankingList) and ["DTT in Images 2: Text Manipulation Detection"](https://tianchi.aliyun.com/competition/entrance/532052/introduction?spm=5176.12281957.0.0.4c885d9bYCL71E).  
> - **If you use data from any of these challenges, please cite our paper.**

---
## 📰 News
* **[2026.03.06]** 🔥🔥 The **STFD dataset** has been publicly released ([Google Drive](https://drive.google.com/drive/folders/1Ta5CO6XZslDXyj2i621mezVrwq8Arm9s?dmr=1&ec=wgc-drive-%5Bmodule%5D-goto) / [Baidu Netdisk]()).
  Please send an email to **[kimjyu@foxmail.com](mailto:kimjyu@foxmail.com)** using your **academic or institutional email address** to request access.

  The email should include:

  * Your **name, affiliation, and homepage (if available)**
  * Your **supervisor's name, affiliation, and homepage (if available)**
  * A **brief description of your research purpose**
* **[2026.02.09]** 🔥 We have updated the dataset details and added example samples.

> **TODO (coming soon!)** 
> - [ ] 📦 **Release STFL-Net code & checkpoints**
> - [x] 🔗 **Publish full STFD dataset download links**

## Overview

### Screenshot Sources
The screenshots were captured from real devices to reflect realistic usage scenarios.

| Category | Description |
|----------|-------------|
| Systems | Android, HarmonyOS, iOS, Windows |
| Scenes  | Chat, Social Media, Mobile Payment, E-commerce, Online Banking, Maps & Transportation, Web Browsing, System Interfaces, Documents|
| Devices | Realme Q3 Pro, Oppo Reno1, Honor 9, Honor V30, Vivo X21s, Samsung Note20 Ultra, Vivo X60, Honor 30-1, Xiaomi 9, Honor V20, Nova 8, OnePlus 9, Huawei Mate30, Honor 30-2, Honor 20 Pro, iPhone 7, iPad Air 3, iPad 2020, iPhone 12, iPhone XS, iPhone 11, iPhone SE2, iPhone 14 Pro, MacBook Air 2015, MacBook Pro 2017, Win10 Dell Optiplex 7080, Win11 Xiaomi Air14, Win10 Xiaomi Air14 |
| Format  | PNG / JPEG |

### Tampering Examples
#### Copy-Move
Copy a text region and paste it to another location within the same image.
<p align="center">
  <img src="imgs/com/0ba51385ddc8ade89a53f4b5881abf9b.png" width="45.6%" style="margin-right:30px;"/>
  <img src="imgs/fe591d44ebe6f6fb7d5558cd2b655e49.png" width="45%"/>
</p>

#### Splicing
Paste text regions from another image into the target image.
<p align="center">
  <img src="imgs/fcb556cba9a4ca85ed41a96ded1fa198.png" width="45%" style="margin-right:30px;"/>
  <img src="imgs/c67e92a92e8bb4aa95541d6359f5e18e.png" width="45%"/>
</p>

#### Removal
Remove existing text and fill the region using inpainting.
<p align="center">
  <img src="imgs/e8439b9e91077c3e2a1a549dd0fdaa07.png" width="45.6%" style="margin-right:30px;"/>
  <img src="imgs/fc539af84b2ff19904f18b457c6856e6.png" width="45%"/>
</p>

#### Insertion
Insert new text content into blank regions.
<p align="center">
  <img src="imgs/b9e25cfd9889269c1d60e10dda4539df.png" width="45%" style="margin-right:30px;"/>
  <img src="imgs/e871a802328f0bbbf445fab592a319b1.png" width="45%"/>
</p>

#### Replacement
Replace original text with newly generated text.
<p align="center">
  <img src="imgs/a0f61f66a5ebe69526b79f6f2b6879ed.png" width="45%" style="margin-right:30px;"/>
  <img src="imgs/1d7b444730be83cb2f0c2aae0a78c315.png" width="45.55%"/>
</p>

### Dataset Structure
```text
STFD/
├── 1_Copy-move/
│   ├── tamper/ # tampered screenshots (copy-move)
│   │   ├── 0a31c69e308a843cee5f0ad08799b61b.png
│   │   ├── 0ba9fbaa8f4918ac92aa2e14f578a3a1.png
│   │   └── ...
│   └── masks/ # binary masks (same filename as tamper)
│       ├── 0a31c69e308a843cee5f0ad08799b61b.png
│       ├── 0ba9fbaa8f4918ac92aa2e14f578a3a1.png
│       └── ...
├── 2_Splicing/
│   ├── tamper/
│   └── masks/
├── 3_Removal/
│   ├── tamper/
│   └── masks/
├── 4_Insertion/
│   ├── tamper/
│   └── masks/
└── 5_Replacement/
    ├── tamper/
    └── masks/
```
---


## ✍️ Citation
```bibtex
@inproceedings{yu2023learning,
  title        = {Learning to Locate the Text Forgery in Smartphone Screenshots},
  author       = {Yu, Zeqin and Li, Bin and Lin, Yuzhen and Zeng, Jinhua and Zeng, Jishen},
  booktitle    = {ICASSP 2023–2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  pages        = {1--5},
  year         = {2023},
  organization = {IEEE}
}

