## (14NIPSworkshop) Distilling the Knowledge in a Neural Network
一些直觉：
 * 复杂模型很多多出来的信息，比如远远低于标签分数的类分数。这些信息被浪费了。
 * 从复杂模型学过来的简单模型是对直接学做 regularization，效果会好于直接训练简单模型。

### Temperature
$q_j=\frac{e^{z_j/T}}{\sum_i{e^{z_i/T}}}$
训 Teacher 的时候 $T=T_0$ 设的很大。训 student 时，目标函数分两部分：在 $T=T_0$ 下 teacher 和 student 的 soft targets 交叉熵，和在 $T=1$ 下 student 和标签的交叉熵。因为产生的梯度是 $1/T$ 规模，后面一部分分配 $1/T_0^2$ 的权重。

Temperature 让 Loss 增加对那些负例的关注，所以高 Temperature 是在尽可能保留 T=1 时丢失的那些信息。但是 student 非常简单的时候 Temperature 得降低，以减少这些负例的信息比例。

### ensumble of specialists
specialist: 专门在难以分辨的类（用聚类之类的手段决定哪些类很接近）之间做分类，其他类归为一个 dustbin class 为了防止过拟合，用原来模型的参数初始化，并调节 dustbin 样例比例。预测的时候，先用原模型得到最可能的k类，和这些类有交的 specialists 被拿来和原模型一起算 Loss。显然 specialists 可以并行蒸馏。

### soft targets as regularization
teacher 算出来的 probability distribution, hard targets 指 label distribution. hard targets 更容易过拟合，soft targets 中负例信息更丰富，所以可以看作一种 regularization 手段。

## review
关键是用 soft target 算 loss，这是一种 regularization，文章也解释了为什么，是更好地利用了负例隐藏的信息。specialists 是一个很有意思的想法。
