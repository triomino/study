[ImageFolder](https://pytorch.org/docs/stable/_modules/torchvision/datasets/folder.html#ImageFolder), [DatasetFolder](https://pytorch.org/docs/stable/_modules/torchvision/datasets/folder.html#DatasetFolder) torchvision 里的实现，class_to_idx 是从目录得到的，一个类一个目录。如果 train 和 test 的目录不一致，比如有时候部分类在 test 或者 train 中残缺，label 就会出问题。应该补上空文件夹以保证字典一致。

有一回 DataLoader 忘了传 num_workers 了，发现数据读取巨慢。因为默认是 0，在主进程里读取，开 1 都比它好得多。

写了个一开始就读入数据到内存的 Dataset [ImagenetteDataset](https://github.com/triomino/ModelParallel/blob/8a020696c14201b441f5b6c930945e8aa599a10e/pytorch/ResNet50/data/loader.py#L16L27)，开多进程的时候发现带 lambda 的函数签名不能序列化。把它改成了不传 loader 的版本 [loader.py#L24L48](https://github.com/triomino/ModelParallel/blob/c536d0706c9ea2ce352b3caf2d78190bc68d6248/pytorch/ResNet50/data/loader.py#L24L48)。不过 stackoverflow 有各种多进程不能 pickle 东西的 workaround, 有空看看，因为原来的做法挺方便的。

有人用 DALI 加速跟我有一样的[疑惑](https://github.com/NVIDIA/DALI/issues/1774), FileReader 传进去的 seed 不是用来 shuffle 的，shuffle 的是一个全局 seed，在所有进程所有机器上都一样。每次 epoch 结束后会改这个全局 seed. 那么 FileReader 传进去 seed 有啥用呢？