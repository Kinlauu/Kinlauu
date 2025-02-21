---
title : Lec02-DT&CT
---


[Lec02.pdf](PPT/Lec02.pdf)

  <iframe src="https://docs.google.com/viewer?url=https://github.com/Kinlauu/Kinlauu/raw/main/docs/Study/ISEE/信号与系统/PPT/Lec02.pdf&embedded=true" style="width:100%; height:200px;" frameborder="0"></iframe>

## DT Discrete-Time System

### 多重表征

#### 1. 描述

为了减少存储一系列几乎相等的大数所需的比特数，记录第一个数字，然后记录连续的差异。

#### 2. 差分方程

![image-20250220113408756](images\image-20250220113408756.png)

![image-20250220114904737](images\image-20250220114904737.png)

#### 3. 框图

![image-20250220113422954](images\image-20250220113422954.png)

​	

!!!note
     **取反=>延迟=>相加**

![image-20250220114550233](images\image-20250220114550233.png)

!!!caution

     **0状态输入**

<img src="images\image-20250220114619582.png" alt="image-20250220114619582" style="zoom:50%;" />

<img src="images\image-20250220114639856.png" alt="image-20250220114639856" style="zoom:50%;" />

<img src="images\image-20250220114650635.png" alt="image-20250220114650635" style="zoom:50%;" />

####  运算 （方程<=>框图）

![image-20250220115424413](images\image-20250220115424413.png)



##### 替代：

![image-20250220115451115](images\image-20250220115451115.png)

![image-20250220115523816](images\image-20250220115523816.png)

把Delay 替换为 R 

可得到运算方程：

![image-20250220115530435](images\image-20250220115530435.png)

##### 原方程转换：

![image-20250220120004248](images\image-20250220120004248.png)

##### 例：

1. 

![image-20250220120348703](images\image-20250220120348703.png)

1. 

![image-20250220120607243](images\image-20250220120607243.png)

![image-20250220121055445](images\image-20250220121055445.png)

#### 累加器

![image-20250220121759799](images\image-20250220121759799.png)

![image-20250220121812961](images\image-20250220121812961.png)

---



## CT Discrete-Time System



### 多重表征

#### 1. 描述

![image-20250220122058667](images\image-20250220122058667.png)

#### 2. 差分方程

![image-20250220122011132](images\image-20250220122011132.png)

#### 3.框图

![image-20250220122022401](images\image-20250220122022401.png)

#### 运算

![image-20250220122044279](images\image-20250220122044279.png)

##### 例题：

![image-20250220122441292](images\image-20250220122441292.png)
