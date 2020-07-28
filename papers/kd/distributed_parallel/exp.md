## teacher 调试过程
现在的 resnetv2.py 比 torchvision.py 的慢的多，而且显存占多一倍。但是代码逻辑都是一样的，需要寻找原因。  
原因是 resnetv2.py ResNet 的 forward 返回了中间层的问题。但是为什么返回中间层会降低效率？中间层并未接入 Loss?   
这是个乌龙，resnetv2 的 ResNet block 少了个 maxpool，不是中间层的问题。

4 卡 16 worker 256 batch_size 一个 epoch 约 800s，再增加 batch_size 时间节约幅度减小，到 512 才 770s。  
猜测原因
 * batch_size: 磁盘 io 达到瓶颈，从日志中可以看到，256 的时候总时间:数据读取约 4:1，数据读取时间方差小，范围 0.029~0.044s，
 512 的时候比值约 3:1，数据读取的时间在 batch 之间浮动较大，0.020s~0.109s 不等。
 * worker: 太少时，比如一卡一进程，GPU 很多时候在等 data. 如果太多，io 又会被卡，感觉是一个平衡的艺术。就实验结果和个人经验，一张卡配 4 个 worker 差不多了，再上去提升不多。
 * 卡：卡多起来也没什么用。应该要卡、batch_size、worker 一起大起来  

确认上面的原因需要进一步学习分布式多进程的原理。

使用 DALI，单个 epoch 中 batch_time 和 data_time 会同步增加，最后会变得很慢，GPU 各种跑不满，找个时间排除这个问题。[官方的例子](https://github.com/NVIDIA/DALI/blob/master/docs/examples/use_cases/pytorch/resnet50/main.py)也有这个问题，而且跑的比我还慢。目前最佳实践是分两组四卡，GPU 一直是满的，偶尔还是有跑不满的时候，不过我认为没办法再加速了。

## student 调试过程
当前问题是，train_student r=1, ab=0，按理来说和 train_teacher 差不多。但是准确率垃圾很多，load data 更慢，但是整体居然更快。说明 train_student 可能改的不对。  
10 epoch imagenette ResNet18  
teacher 和原来的 student 单个 ResNet18轻松上五十，改过只有 30+

先把 is_instance 去掉看看 load data 时间变化。很遗憾，不是它的问题。  
是 DDP 用在 module_list 上出问题了吗？  
是不是因为 optimizer 在套 DDP 前，这样参数还没送去 cuda？不是,train_teacher 就在前面不是问题。  
是不是因为 criterion_list 没有送去 cuda？好像也不是这个问题。  
是 model_s.eval() 的问题吗？也不是这个问题  
是 DDP 之后网络结构变了吗？  
是 max pooling 的原因吗？排除，因为 teacher 用的也是没有 maxpool  
找到原因了，是贪图方便，在 train 里写了 module_list=module_list.module，这样 DDP 直接被剥掉了，等于单卡在跑 1/num_gpu 的数据，效果不差才怪。这个失误太致命了。

为什么 load data 时间占比这么大？改好了就没这个问题了。batch:data 约 5:1 可以接受。

还会报警 /opt/anaconda3/lib/python3.7/site-packages/torch/nn/_reduction.py:43: UserWarning: size_average and reduce args will be deprecated, please use reduction='sum' instead. 找个时间去掉

关于最后一个 batch，如果舍掉会有问题，没有 validate 过程。测试是否是 dali 的问题。

有一些 TODO 记得做掉

突然遇到了 GPU0 显存巨大，其他卡几乎没有显存的问题。其实学习多进程的时候已经特别注意到了这个东西，甚至写了[笔记](https://github.com/triomino/study/blob/11811da6c44e2c61372d8fe607bdb5059d80da1d/pytorch/notes.md#ddp-%E5%92%8C-saveload)。原来我以前 teacher 都是全部 load 到 GPU0 上的？居然没有显存爆炸，真是奇迹。

tensorboard logger 会使得 GPU0 比别的都慢一拍，别人都要等一等它。目前尚未发现会有什么不良影响。

用 dali 第一个 epoch test 全是 0，查了大半天原来是 teacher validate 完没有 reset dataloader. DALI 为什么要 reset? 真是一言难尽。

### 效率记录
四卡 256 batch_size 16 worker: 0.15s/batch, 其中 0.023~0.035s 读数据。GPU全跑满。770s/epoch  
八卡 256 batch_size 16 worker: 0.161s/batch, 其中 0.020~0.057s 读数据。始终有 GPU 只有一半，偶尔多卡一起不满。805s/epoch  
八卡 512 batch_size 32 worker: 0.229s/batch, 其中 0.040~0.060s 读数据。经常有多卡不满(~70%)  570s/epoch  
六卡 384 batch_size 24 worker: 0.185s/batch, 其中 0.027~0.046s 读数据。经常有一张卡不满。630s/epoch  

八卡同 batch_size 甚至比四卡慢。原因可能是：卡同步耗时，数据读取更慢，观察到 data loading 比四卡耗时更多，明明单卡 batch 更小了。

Vanilla KD 570s 一个 epoch，GPU 没喂饱就算了，我已经很满意了，读取优化预处理优化内存缓冲什么的以后再说，都是蚊子腿。终于可以去玩 model parallel 了。希望 model parallel 能带来更惊人的加速。

Model Parallel 失败了，没有想的那么好。用上了 [DALI](https://github.com/NVIDIA/DALI/)，又快了几十秒。

用 DALI 失败了，不知道什么原因，从五六十个 epoch 起就减速了。减速之后并没有比之前快。十分难受，不管效率了，先把准确度做出来。

用 DALI 的时候又见到了 apex.amp 研究一下。

### 是否用 apex 的 DDP，是否用 DALI 的对比
均为 kd, 32x8 batsh_size ResNet34->ResNet18 32 workers，为了让各自方法不受之前缓存的影响，都训前两个 epoch，主要参考第二个。准确率有点不好对比，因为我没有 shuffle 的种子设成一样（懒）。格式 epoch_time(batch_time 变化)
pytorch.DDP  597s(11.37->0.119), 600s(11.41->0.120) acc 39~
pytorch.DDP+DALI.GPU epoch 531s(0.061->0.106), 487s(0.072->0.097) acc 39~
apex.DDP 
apex.DDP+DALI.GPU 516s(0.074->0.103), 506s(0.033->0.101) acc 38.97
并未感受到 apex.DDP 的优势。有空把 apex 的 amp 那一套都搬过来测一测时间，看整一套是不是更快。

### DALI 的精确度问题
从 torchvision 下载的 pretrained 模型直接 evaluate 发现和官方的 accuracy 不一样。这个 [issue](https://github.com/NVIDIA/DALI/issues/400) 里指出 DALI 预处理用 OpenCV/npp，和 pytorch 的 Pillow 不一样。resnet34 on imagenet 的准确度从 73.314% 变成 73.262%, 等于有 26 张图片因此被误分类。  
可以用 DALI 官方的程序运行 `python -m torch.distributed.launch --nproc_per_node=1 main.py --b 256 --pretrained --evaluate -a resnet34 PATH_TO_DATASET` 来证明并不是其他因素影响的。
用了 DALI 之后准确度:
resnet34: 73.262%
wrn_50_2: 78.472%
vgg13(without BN): 69.952%
vgg13(BN): 71.532%

### pytorch 的 deterministic 测试
主要基于 https://pytorch.org/docs/stable/notes/randomness.html  
又使用了 DALI，不过 DALI 分布式 shuffle 用了 hardcoded 的 seed, 所以不需要额外设 seed, 只要传进 dataloader/filereader 的 seed 是一样的就好了。  
做普通的 kd, resnet34->resnet18, bs=64x8  
没有 deterministic, 第一个 epoch: 608.12s, acc 26.462/51.816  
deterministic，前三个 epoch:   
620.16s, acc 26.006/51.386,   
502.22s, acc 38.498/65.230,  
497.58s, acc 44.028/70.656   
重复实验：  
498.05s, acc 26.006/51.386,  
489.69s, acc 38.498/65.230,  
495.23s, acc 44.028/70.656  