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

有一些 TODO 记得做掉

### 效率记录
四卡 256 batch_size 16 worker: 0.15s/batch, 其中 0.023~0.035s 读数据。GPU全跑满。770s/epoch  
八卡 256 batch_size 16 worker: 0.161s/batch, 其中 0.020~0.057s 读数据。始终有 GPU 只有一半，偶尔多卡一起不满。805s/epoch  
八卡 512 batch_size 32 worker: 0.229s/batch, 其中 0.040~0.060s 读数据。经常有多卡不满(~70%)  570s/epoch  
六卡 384 batch_size 24 worker: 0.185s/batch, 其中 0.027~0.046s 读数据。经常有一张卡不满。630s/epoch  

八卡同 batch_size 甚至比四卡慢。原因可能是：卡同步耗时，数据读取更慢，观察到 data loading 比四卡耗时更多，明明单卡 batch 更小了。

Vanilla KD 570s 一个 epoch，GPU 没喂饱就算了，我已经很满意了，读取优化预处理优化内存缓冲什么的以后再说，都是蚊子腿。终于可以去玩 model parallel 了。希望 model parallel 能带来更惊人的加速。