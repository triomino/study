## Distributed Training

### Load Data
#### Imagenet
[ImageFolder](https://pytorch.org/docs/stable/_modules/torchvision/datasets/folder.html#ImageFolder), [DatasetFolder](https://pytorch.org/docs/stable/_modules/torchvision/datasets/folder.html#DatasetFolder) torchvision 里的实现，class_to_idx 是从目录得到的，一个类一个目录。如果 train 和 test 的目录不一致，比如有时候部分类在 test 或者 train 中残缺，label 就会出问题。应该补上空文件夹以保证字典一致。

有一回 DataLoader 忘了传 num_workers 了，发现数据读取巨慢。因为默认是 0，在主进程里读取，开 1 都比它好得多。

写了个一开始就读入数据到内存的 Dataset [ImagenetteDataset](https://github.com/triomino/ModelParallel/blob/8a020696c14201b441f5b6c930945e8aa599a10e/pytorch/ResNet50/data/loader.py#L16L27)，开多进程的时候发现带 lambda 的函数签名不能序列化。把它改成了不传 loader 的版本 [loader.py#L24L48](https://github.com/triomino/ModelParallel/blob/c536d0706c9ea2ce352b3caf2d78190bc68d6248/pytorch/ResNet50/data/loader.py#L24L48)。不过 stackoverflow 有各种多进程不能 pickle 东西的 workaround, 有空看看，因为原来的做法挺方便的。

#### DALI
有人用 DALI 加速跟我有一样的[疑惑](https://github.com/NVIDIA/DALI/issues/1774), FileReader 传进去的 seed 不是用来 shuffle 的，shuffle 的是一个全局 seed，在所有进程所有机器上都一样。每次 epoch 结束后会改这个全局 seed. 那么 FileReader 传进去 seed 有啥用呢？

我没有设置 drop_last 发现还是每个 batch 都满了，而且是增加了，不是削掉了。  原因是 [DistributedSampler](https://pytorch.org/docs/stable/_modules/torch/utils/data/distributed.html#DistributedSampler) 内置的行为，摘取下面这段代码：
```python
# add extra samples to make it evenly divisible
indices += indices[:(self.total_size - len(indices))]
assert len(indices) == self.total_size
```
也就是 validation 的时候不可避免因为这个出现误差。我算是知道官方迟迟不用 DistributedSampler 做分布式的原因了。我也在官方 repo 里找到了这个 [issue](https://github.com/pytorch/pytorch/issues/25162)  
这一点 DALI 的 [DALIClassificationIterator](https://docs.nvidia.com/deeplearning/dali/user-guide/docs/plugins/paddle_plugin_api.html?highlight=daliclassificationiterator#nvidia.dali.plugin.paddle.DALIClassificationIterator) 就做的很透明了，用 fill_last_batch 和 last_batch_padded 两个参数控制，可以看看里面的 example，讲的很清楚。当然要记住 validate 的时候绝对要把两个都关了，这可能会造成 batch 残缺以及不同 GPU 上 batch_size 不一致，要在 all_reduce 的时候传递 size 保证合并结果的正确。

### Misc
用 nccl 做不同 GPU 的同步，用 gloo 做 CPU 不同进程的同步

## Pytorch Model
今天又碰到一个坑。在迭代的时候，如果 w=w+dw, 那么下一轮迭代 w.grad 会变成 None，即使你 w.requires_grad_()，也没用。这是因为 w=w+dw 做完 w 被视作中间变量(intermediate variable)，它再也不是 leaf 了。而 pytorch 为了省内存直接不保存中间变量的梯度。可以 w.detach_() 来让他脱离原图重新变成 leaf，这就是 [optimizer.zero_grad()](https://pytorch.org/docs/stable/_modules/torch/optim/optimizer.html#Optimizer.zero_grad) 的做法。也有人直接 w.data += ..., 可能挺省空间的. 如果不是迭代可以 retain_grad().

## Python
今天碰到的一个坑。[stackoverflow](https://stackoverflow.com/questions/29548587/import-fails-when-running-python-as-script-but-not-in-ipython) 有解答。直接 python 是能 import 当前目录下的东西，如果 python xxx.py 也能，这两个系统环境变量其实一样。但是 python aaa/xxx.py 就不对了，第一个环境变量会变成 aaa. 我真的搞不懂有些项目怎么弄的 path，直接 clone 下来都不能跑的。