# Lec01-基础导论

[Lec01.pdf](PPT/Lec01(1).pdf)

  <iframe src="https://docs.google.com/viewer?url=https://github.com/Kinlauu/Kinlauu/raw/main/docs/Study/ISEE/信号与系统/PPT/Lec01(1).pdf&embedded=true" style="width:100%; height:200px;" frameborder="0"></iframe>

## 能力&功率


![image-20250220101628278](images\image-20250220101628278.png)

### 功能关系


<img src="images\image-20250220101820121.png" alt="image-20250220101820121" style="zoom:67%;" />

<img src="images\image-20250220101828863.png" alt="image-20250220101828863" style="zoom:50%;" />



<img src="images\image-20250220101850235.png" alt="image-20250220101850235" style="zoom:67%;" />

<img src="image-20250220101858718.png" alt="image-20250220101858718" style="zoom:50%;" />

<img src="images\image-20250220101906893.png" alt="image-20250220101906893" style="zoom:67%;" />

<img src="images\image-20250220101912845.png" alt="image-20250220101912845" style="zoom:50%;" />

# Building-Block Signals

# 冲激信号&阶跃信号

## 冲激信号-Unit-Impulse Signals 


<img src="images\image-20250220103222397.png" alt="image-20250220103222397" style="zoom:67%;" />

<img src="images\image-20250220103449511.png" alt="image-20250220103449511" style="zoom: 80%;" />

面积恒为1，当t -> 0 时

<img src="images\image-20250220103349732.png" alt="image-20250220103349732" style="zoom:67%;" />

单位脉冲信号为面积/重量为1


### 离散 DT

<img src="images\image-20250220102631384.png" alt="image-20250220102631384" style="zoom: 50%;" />

### 连续 CT

<img src="images\image-20250220102715551.png" alt="image-20250220102715551" style="zoom:50%;" />

!!!NOTE

    无法作为积木块信号，由于输入信号进入积分块出来都是0

----

## 阶跃信号-Unit-Step Signals 

<img src="images\image-20250220103627339.png" alt="image-20250220103627339" style="zoom:67%;" />

 单位冲激的不定积分就是单位阶跃

![image-20250220170817771](images\image-20250220170817771.png)

**单位冲激信号 -> 单位阶跃信号**

<img src="images\image-20250220103709044.png" alt="image-20250220103709044" style="zoom:67%;" />

<img src="images\image-20250220103718071.png" alt="image-20250220103718071" style="zoom:67%;" />



---


# Transformation of Time - 时间变换

## 1. Time shift 时移

![image-20250220103851222](images\image-20250220103851222.png)

 !!! note
    **t 减 右移 延迟**
    **t 加 左移 提前**


#### Sketch - 作图

![image-20250220104316692](images\image-20250220104316692.png)

## 2. Time reversal 翻转

![image-20250220104421282](images\image-20250220104421282.png)

![image-20250220104511319](images\image-20250220104511319.png)

![image-20250220104451287](images\image-20250220104451287.png)

## 3.Time scaling 缩放 - CT

<img src="images\image-20250220105341161.png" alt="image-20250220105341161" style="zoom:67%;" />

!!!note

    |a| < 1 拉伸
    
    |a| > 1 压缩

![image-20250220105506532](images\image-20250220105506532.png)

**Ex**.

![image-20250220105631893](images\image-20250220105631893.png)

![image-20250220110131535](images\image-20250220110131535.png)

![image-20250220110704883](images\image-20250220110704883.png)

!!!note

    1. 拉伸
    2. 翻转
    3. 时移 - 化简后**只跟x有关** 例题=-2（x+1），转完只用向**左移1，不是2**



---



# 系统

## 无记忆系统

在给定时间的**输出只依赖于同时的输入**

## 有记忆系统



## 因果系统

如果某一时刻的**输出仅依赖于某一时刻的输入**，则该系统是因果的，即系统不能预测输入。

**Same input => Same output**

<img src="images\image-20250220111341983.png" alt="image-20250220111341983" style="zoom:33%;" />

√××√√

!!!note

     只考虑x（t）内 t 是否会与未来相关（是不是输出在输入之后发生的），因果系统只依赖于当时刻，不能预测未来

 


## 稳定系统-BIBO

**定义1:** 稳定系统是指输入增量导致输出增量的系统。

**定义2:** 如果每个有界输入都导致有界输出，系统是BIBO稳定的。我们将使用这个定义



## 时不变系统 - TI

#### 定理：

![image-20250220161842565](images\image-20250220161842565.png)

#### 例题：

![image-20250220112118344](images\image-20250220112118344.png)

10100

 !!!note

    **系数与时间有关**or **t上有缩放**，就**非**时不变



## 线性系统

系统具有叠加性质，则该系统是线性的

**输入是线性组合=>输出线组合**



![image-20250220112503105](images\image-20250220112503105.png)

**例：判断**

![image-20250220112510149](images\image-20250220112510149.png)

非线性（平方项），时不变，因果

![image-20250220112516835](images\image-20250220112516835.png)

线性，非时不变，非因果

