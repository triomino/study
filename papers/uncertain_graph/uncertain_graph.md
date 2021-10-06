
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
Read later

## Distance-Constraint Reachability Computation in Uncertain Graphs(VLDB-2011)
问题：distance-constraint reachability (DCR), 在不确定图里给定距离限制问 s-t 可达概率
贡献：提出这个问题，并给了一种方法

### 应用/起源
P2P 网络中，只寻找一定距离内的 peer，否则造成 congestion(拥塞)  
交通网络同理  
社交网络中更倾向于 trust hop 少的人（这一点我觉得他在扯淡，强行写进来当应用场景）
### Methods
Later

## Efficient Network Reliability Computation in Uncertain Graphs
