## Distributed Training
一些个人工作汇总，防止忘记：  
1. 笔记 [Model Parallel and Data Parallel](../../pytorch/distributed_notes.md)  
2. 笔记 [A Problem of Data Parallel and Solution](../kd/distributed_parallel/mutual_instance.md)(内附代码链接)  
3. 笔记 [Some Code Notes](../../pytorch/code_notes.md)  
4. 代码 [Fork](https://github.com/triomino/examples) 了 pytorch 官方的 [example](https://github.com/pytorch/examples).改造了一下 imagenet 分布式的样例，使得能够分布式 validation.  
5. 代码 按照上面提到的第一个笔记，开了一个 [repo](https://github.com/triomino/ModelParallel) 来做 Model Parallel. 不过实验效果不如 Data Parallel. 缺少热情做下去。  
6. 代码 Fork 了 [Contrastive Representation Distillation(ICLR 2020)](https://github.com/HobbitLong/RepDistiller) 的代码，有一个公开的 [Fork](https://github.com/triomino/RepDistiller) 和另一个私人的 Fork. 公开的 Fork 只是加上了 IRG Loss，私人的加上了分布式和 [DALI](https://github.com/NVIDIA/DALI) DataLoader 加速，等做完一大堆实验开源。  
7. 实验记录 在上面这个私人 repo 的[凌乱的探索记录](../kd/distributed_parallel/exp.md)

## Papers
### Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour
 * Linear Scaling Rule: When the minibatch size is multiplied by k, multiply the learning rate by k. 一句话解释：loss 和梯度都对 batch size 做平均，这一条十分自然。例外：初始时网络剧烈变化，所以需要 warmup phase，以及 batch size 不能无限制扩大(~8k)。
 * 如果我对 2.3 没理解错，它是说 BN 层不需要考虑 GPU 之间同步 batch 的统计数据。很好，那[这篇笔记]((../kd/distributed_parallel/mutual_instance.md))提到的问题可能不是问题，但需要更多的证据支持。
 * 看到了很多 pytorch 集成的东西，比如梯度平均和 random shuffle，很开心我不用去操心这些。