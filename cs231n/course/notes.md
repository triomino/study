# KNN
## Evaluate on the test set only a single time, at the very end.

Total data we have on hand = Train + Test  
Train = Train + Val, Val can be used multiple times.  
Test will only be used once at end.

# SVM, Softmax classifier
## Softmax Loss
$$\frac{e^{a_i}}{\sum_j{e^{a_j}}}=\frac{e^{a_i-p}}{\sum_j{e^{a_j-p}}}$$
Used to improve numeric stability.  
也就是说所有类分数加减一个数不改变 Loss。这和 Hinge Loss 是一样的。

# Optimization
## numerical gradient and analytic gradient
前者是在每一维取小的步长，按导数定义算出梯度。后者是按导数的解析式算，SVM里，
$$L_i=\sum_{j\ne y_i}{\max(0,w_j^Tx_i-w_{y_i}^Tx_{i}+\Delta)}\\
\nabla_{w_{y_i}} L_i=-x_i\times\sum_{j\ne y_i,w_j^Tx_i-w_{y_i}^Tx_i+\Delta>0}{1}\\
\nabla_{w_{j}} L_i=w_j^Tx_i-w_{y_i}^Tx_i+\Delta>0?x_i:0 (j\ne y_i)$$

numerical 简单，但是慢、不精确，anylytic 精确、快，但是需要推导。实际情况会 gradient check，比较两者来确认 anylytic 推导和实现正确。

## Mini-batch gradient descent
每次取一小批数据算梯度。Mini-batch size 如果变成 1，那么就是Stochastic Gradient Descent(sometimes on-line gradient descent)，有人也会把 Minibatch 叫做 SGD。

# Backpropagation / Chain rule
$$\sigma(x)=\frac{1}{1+e^{-x}},\frac{\text{d}\sigma(x)}{\text{d}x}=(1-\sigma(x))\sigma(x)$$
如果 $x$ 大，那么 bp 时 $\text{d}(Wx)/\text{d}W$ 会变大，learning rate 得变小

# Neural Networks
## Activation function
frequently used activation functions:sigmoid, tanh, ReLU, Leaky ReLU, Maxout.  
tanh compared to sigmoid: zero-centered.  
ReLU make network die easily, set small learning rate to avoid this problem, or use Leaky ReLU/Maxout. 
## Size of NN
一般而言， NN 三层以上，加层数优化效果不显著。CNN 不一样，深度对 performance 十分重要。  
尽量用大、深网络。有很多其他手段解决过拟合的问题，并非一定要缩小网络规模。另一个微小的原因是小网络 local minima 参差不齐，依赖随机初始化的 "luck"。
## Data processing
Whitening  
CNN 一般不用 normalization PCA 或者 Whitening, zero-centered 就够了。zero-center 只做在 train set 上，然后拿 train set 的平均去减 val/test 的向量。
## Weight Initialization
小但不为 0。有很多初始化建议，感觉都是玄学，ReLU 可以用这个 w = np.random.randn(n) * sqrt(2.0/n) (Delving Deep into Rectifiers:
Surpassing Human-Level Performance on ImageNet Classification)b 推荐设置为零  
Batch Normalization.

## Regularization
 * L2. 大的值造成的影响更大，优化这类 Loss 使得值分布更加 Diffuse
 * L1. 容易造成很多 0. 像 feature selection.
 * Dropout. 每个神经元有 p 概率失效，训练的时候只更新那些有效神经元，这里没讲清楚，是先固定多个部分网络最后聚合，还是每一次迭代步骤里这么做，我猜是后者。而且为啥这是个 Regularization?

## Loss
遇到 Regression 问题优先考虑能不能转化为 Classification

## Gradient Check
这一块有很多容易出问题的地方。
 * numerical 算法用 $\frac{f(x+h)-f(x-h)}{2h}$ 更好，误差是二阶的。比较 numerical and analytic 用相对误差。
 * [What Every Computer Scientist Should Know About Floating-Point Arithmetic](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html). 太小（1e-10以下）float 分布就不那么密集的，精度容易挂。可以缩放 Loss 使得 Gradient 保持在 1.0 这个级别。
 * 不光滑点。比如 max(0,-) 在 0 是不光滑的，Gradient Check 会出问题。减少数据点可以降低这种事情出现概率。
 * h 设置。太大太小都不好，1e-4 附近。[wiki](https://en.wikipedia.org/wiki/Numerical_differentiation)
 * Regularization Loss 占主导会掩盖错误的 analytic 实现。
## 开始训练前检查代码的小g巧
预估随机初始化的 Loss 并比较。改改几个超参看看 Loss 是不是符合预期变化。Overfit 一组小 sample 看看 Loss 能不能到 0.

## Learning
### update
除了直接减去 learning_rate*dx，也有 Momentum updat/Nesterov Momentum 这样的，dx 改变的是速度(前者在x点速度，后者在$x+\mu v$)。
### learning rate
可以是递减的，包括怎么减、什么时候减。
### 二阶迭代
直接牛顿 Hessian 计算 cost 太高。拟牛顿，Limited-memory BFGS。
### learning rate 适应性变化
Adagrad RMSprop Adam