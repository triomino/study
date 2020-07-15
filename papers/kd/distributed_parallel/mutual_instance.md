## 问题发现
Data Parallel 的时候想到一个很严重的问题。如果是样本之间的关系算 Loss，其实不好 backward. 初步想法是汇总各个 GPU 上的 sub-batch 得到 batch 然后 sub-batch x batch 是相似矩阵的一部分，一定要记得 no shuffle 来测试是不是和单卡行为一致。如果搞不出来或者效率很低去查查资料。

## 问题说明
假设我们一个 batch 的 loss 是这样的 $L(\mathcal X)=\frac{1}{n^2}\|
x_i-x_j\|_p$，forward 是照着公式这么写的。  
然后我们要把他送去 4 个 GPU 做 Data Parallel. 按照 torch.distributed 的逻辑，batch 分割成了 4 个 sub-batch，然后送到 4 个进程分别训练，forward 完成时同步一次，backward 完成时同步一次。  
这个逻辑对于一阶的 forward 过程是正确的。但是对于刚刚这个 loss 会出问题。  
不把 batch 分开时，整个 batch 算的距离和用下图整个大正方形面积表示：

![平方和损失函数图示](diag.png)  

但是按照分布式四个 GPU 自顾自算 $L(\mathcal X_i)(i=0,1,2,3)$ 算出来的结果是上图绿色部分。

## 如何解决
这个问题不难解决，[举例代码](instance_mutual.py)也已经写好了。其中 `MutualLossDistributed` 类就用来解决上面说明的问题。forward 的时候，我们额外传进去整个 batch，然后算一整行长方形的 Loss，如下图所示：  

![解决方法图示](row.png)

为了适应原来的框架，每个利用样本之间关系的方法需要另外写一个 Distributed 的类，它的 forward 接受 sub-batch 和整个 batch

## 可能存在的问题
1. 训练速度降低
2. 显存过大
