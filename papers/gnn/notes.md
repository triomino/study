## Semi-spuervised classification with GCN（ICLR2017）
### 模型思路
1. 从$g_\theta\ast x=Ug_\theta U^Tx$开始，$g_\theta$用$g_{\theta'}\approx \sum\limits_{k=0}^K\theta_k'T_k(\widetilde \Lambda)$（$T_k$是 Chebyshev 多项式，$\widetilde \Lambda=\frac{2}{\lambda_{max}}\Lambda-I_N$）逼近，好处是直接变成Laplacian参与计算不用分解啥的，$O(|E|)$复杂度。  
2. 现在只用一阶逼近，$\theta_0'$和$\theta_1'$直接合成一个参数（令$\theta_0'=-\theta_1'=\theta$），得到$g_\theta\approx\theta(I_N+D^{-\frac{1}{2}}AD^{-\frac{1}{2}})x$
3. 上式特征值[0,2]，多层会造成 gradient exploding/vanishing，用Renormalization trick $Z=\widetilde D^{-\frac{1}{2}}\widetilde A\widetilde D^{-\frac{1}{2}}X\Theta$，其中$\widetilde{A}=A+I_N,\widetilde{D}_{i,i}=\sum_j{\widetilde{A}_{i,j}}$

一些说明：
 * $\Theta$ 每层的列数可能不一样，设它的 size 是$C\times F$，$C$是输入维数，第一层就等于特征维数，$F$是输出维数，最后卷出来的维数。这一层的$C$等于上一层的$F$，而本层内可能$F<C$
### 疑问
2.2小节 最后的renormalization trick 为何有效？希望搞懂等价性和如何防止 gradient exploding/vanishing  
3.1 Loss 里为什么Y是个矩阵？难道不是个向量吗  
3.1 batch gradient descent 是什么技术

## CNN
CNN 可以看作全连接的 regularization，因为全链接参数那么多，容易过拟合

## Jumping Knowledge Networks
现代图神经网络的本质是邻近节点的信息传播。GCN 的 spectral 和 spatial 做法，GAT 对邻节点分布求权重（这个其实是传播方向），skip connection 等等，都没有超出邻近节点 aggration 的 schema. 

### 固定层数的 GCN
本文认为固定层数的 GCN 是不好的，严谨的证明通过和随机游走对比。这里只总结精神：在高密度的核心区域节点表征收敛很快，每个点趋于整个核心图的 representation，丢失了各自local的特征，而在稀疏的边缘区域（比如树形），收敛很慢，这个时候却需要足够多的迭代次数。GAT 和本文工作是同时且正交的，因为 GAT 关注传播方向的改进，而本文关注局部信息的保留。本文工作和上述所有内容都可以结合。

### Jumping
所以本文提出 Jumping，对所有迭代过程中的representation，做连接/取Max/LSTM-attention,后两者可以结合，复杂度高，小图过拟合，如果做连接可能要一层线性transformation，这个是所有节点共享，不是nodewise，所以适合小图防过拟合，但其实舍弃了一定的locality。

### 疑问
LSTM + attension 不会引入过多参数吗？因为 nodewise,O(N)个参数？

# TO LEARN
 * Max-pooling
 * LSTM
 * residual connections/skip connectsion