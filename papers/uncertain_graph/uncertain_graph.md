
## An In-Depth Comparison of s-t Reliability Algorithms over Uncertain Graphs(2019)
问题：在 uncertain graph 里估计 s-t 的可达概率，本文模型是每条边有互相独立的表示是否连接的概率。  
贡献：总结 6 个 SOA 方法，放在同样的条件下对比，基于 accuracy/varience/memory cost/time cost 对它们做出充分全面的对比。  
拓展：分布式方法、其他形式的 s-t 可达概率、reduction of uncertainty before estimating s-t reliability、top-k query...
![](images/s-t.png)  
### 应用/起源
quality of connections between devices in device network  
social/biological network  
predict probability of protein-protein interaction  
discover reliable peers in P2P transfer  
infomation diffusion in social network(estimate number of infected people)
### Methods
**直接蒙特卡洛**。每次询问采样 k 个图，不用完全采样，直接从 s 开始一边 BFS 一边确定边。（应该可以提前采样 k 个图，查询时用各种手段加速计算可达）

**蒙特卡洛加索引**。提前采样 k 个图，每条边村 k-bit 表示在 k 个图里是否连接。这样 BFS 时节点要反复入队，其实没快多少，甚至因为要跑完全图慢了不少。改进思路：可以参考最短路那篇文章里的 bit parallel 思想，说不定能一次跑完/一次64轮。

**RSS**. Recursive Stratified Sampling. 后面有。

**Lazy Propagation Sampling**. 给蒙特卡洛优化常数，尽量不接触未激活边。一条边在激活之后，取一个几何分布随机变量计算下次取到的轮数，从而可以在中间这几轮采样中直接跳过对该边的采样。具体实现的时候每个节点维护一个比较轮次的最小堆就行了。我有一个巨大的疑惑，它不是全局的轮数，是每个点单独计算轮数（这个点被访问第几轮了），这样和直接蒙特卡洛还一样吗？
这里有一个问题，就是几何随机变量取的复杂度要加速到 O(1), 不然是没有意义的，只是变成提前采样边了。

## Distance-Constraint Reachability Computation in Uncertain Graphs(VLDB-2011)
问题：distance-constraint reachability (DCR), 在不确定图里给定距离限制问 s-t 可达概率
贡献：提出这个问题，并给了一种方法

### 应用/起源
P2P 网络中，只寻找一定距离内的 peer，否则造成 congestion(拥塞)  
交通网络同理  
社交网络中更倾向于 trust hop 少的人（这一点我觉得他在扯淡，强行写进来当应用场景）
### Methods
Later

## Efficient Network Reliability Computation in Uncertain Graphs(2019)
问题：s-t 的可达概率
贡献：用分层抽样减少采样数量，给了更紧的上下界？our approach is the first solution to achieve both high efficiency and accuracy to compute the network reliability

文章把方法叫做 $S^2BDD$ scalable and sampling binary decision diagram

### Methods
Later

## Recursive Stratified Sampling: A New Framework for Query Evaluation on Uncertain Graphs(TKDE-2015)
问题：s-t 可达概率/影响力最大化/DCR 等等
贡献：RSS(Recursive Stratified Sampling),RCSS,主要是降低 variance

这篇文章提出的核心内容**并非**一个 s-t 可达概率方法，而是采样框架(RSS-Ⅰ RSS-Ⅱ)。这个框架基于这样两类问题：
 * 由查询 q 所决定的函数 $\phi_q(G)$，求所有可能 G 上 $\phi_q(G)$ 的期望；
 * 求所有 G 中 $\phi_q(G)$ 大于或小于某个阈值的概率。(这其实是和第一个一样的问题，把函数变成比较函数就行了)

这两个采样框架不考虑图特性和查询函数的特征，因此又提出了 cut-set based 分层采样方法 BCSS 和 RCSS。

一个技巧。
### Methods
**BSS-Ⅰ (Basic Stratified Sampling)**
选取 $r$ 条边，在分出的 $2^r$ 子空间中分别蒙特卡罗。边的选择策略视问题而定，如果查询是影响力最大化，那应该在 seed 集连通分量里选。  
即使子空间采样数量不平衡，仍然是 unbias 的(这有点反直觉啊。是因为它先在子空间做了平均再乘以每个子空间的概率吗？)，不过 variance 会受到每个子空间采样数量的影响。最优的采样数量依赖于每个空间的 variance，这不可知，因此直接设置成 $\pi_iN$，$\pi_i$就是那 $r$ 条边的概率。可以证明这样 variance 比直接整个蒙特卡洛小。  
注意到在子空间里很多边固定了，那么可以进一步剪枝，比如在影响力最大化问题里，BFS 不到的边就不考虑了，文章 Section 6 会讲更多剪枝策略。

**RSS-Ⅰ (Recursive Stratified Sampling)**
多级 BSS-Ⅰ, 我认为，如果没有特殊选边策略（直接随机选）和剪枝技巧，那么 RSS-Ⅰ 和直接改 $r$ 的 BSS-Ⅰ 是一样的。所以对于 RSS-Ⅰ 而言，剪枝技巧是很重要的创新，没有加这个不能算新方法。
个人疑惑：实际采样数量乘以概率会有四舍五入，分层多的时候舍入误差造成采样数量偏差，这怎么处理的？

**BSS-Ⅱ**
选 r 条边，分 r+1 层，第 i 层是前 i-1 条边不连接，i 边连接的子空间，0 层是全不连。比 Ⅰ 优点：容易控制分层数量，容易运用剪枝技巧。

**BCSS(Basic Cut-Set Stratified Sampling)**
和 BSS-Ⅱ 一样。先求 cut set(集合里所有边 fail 的时候，无论其他边怎么样，$\phi_q$是同一个值)，BCSS 就是对这 cut set 做 BSS-Ⅱ  
并未说明 cut set 怎么求。

**剪枝技巧**  
给定 seed set 求影响节点数期望。分层是根据一部分边的确定来分的，通过确定连接的边不能 BFS 到的点直接剪掉不考虑。对不同方法，可以减少 BFS 的次数。  
RSS-Ⅰ: 直接 BFS 需要 $2^r$ 次。事实上，每条边 BFS 一次得到需要考虑的点，其他边集合就是这些点集的合并。只需要 $r+1$ 次 BFS. 由于 RSS-Ⅰ r 小，递归多，只在根分层 BFS  
RSS-Ⅱ: 易得第 i+1 层 BFS 的点是第 i 层的子集(除了 i=0)，因此不停加边 BFS，每条边只被访问一次。此外，分层抽样树里，同一深度的分层，也只要一次。**我觉得不对，同一深度不是跨层增加的**，虽然没有剪掉不该剪的，但这样没有达到最优剪枝。很遗憾，这一点文章根本没有给出证明，文章中只说了子树加边最后和节点一样，但是子树初始状态根本不可以从左边继承过来。其实严格按照根节点散发的话，这个结论是对的，但实际并非如此，常常是固定选 r 条。  
RCSS：和 RSS-Ⅱ 一样，只是不用做空层抽样（因为这一层结果是已知的）。边取 seed set 的所有出边。**问题是递归，后面的边怎么取**  
我觉得这个剪枝部分太拉跨了，描述得很随意，前面的部分很简单，废话写一大堆。



## Scalable Influence Maximization for Prevalent Viral Marketing in Large-Scale Social Networks(SIGKDD-2010)
问题：影响力最大化
贡献：又快又好

### Methods
每个点搞个最大概率路径树，边是从叶子指向根的，概率大于阈值的不考虑。递归可算 $S$ 对根 $v$ 的影响概率（里面有容斥）。把所有 $v$ 的概率加起来就能算 $S$ 的影响期望。  
加速：树上某个点加到 $S$ 的时候，求新集合激活根的概率，只要走一遍树就能全部求出每个点的影响。具体之后再说


## Maximizing the Spread of Influence through a Social Network(2003)
问题：影响力最大化
正式形式化。$O(k|V|N|E|)$, $k$ 是目标集合大小，$N$ 是每次估计时蒙特卡洛次数，显然这个复杂度不可接受。

## Cost Effective Lazy Forward (CELF) Algorithm
在文章 Cost-effective Outbreak Detection in Networks(KDD-07) 提出。就是朴素方法加剪枝，由子模性质，新加入的点在这一轮的增量不会大于上一轮时的增量，弄个堆维护一下增量就行了，甚至没有删除，~~用肥波拿起堆直接 O(1)~~。夷，不对，这里用的是大根堆，减小增量并不是小根堆里的 decrease key，还是要 log(n)。复杂度是 $O(k|V|\log |V|N|E|)$，但是实际跑要快很多。不过第一轮的 $O(|V|N|E|)$ 是硬伤。

## Erdős–Rényi
随机图，小数据可以用。