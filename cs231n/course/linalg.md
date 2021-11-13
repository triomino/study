### 从损失函数理解矩阵对矩阵求导
假设对矩阵之间求导一无所知，尝试去理解 $\frac{\partial Y}{\partial W}$。$Y_{N*C}=X_{N*D}W_{D*C}$，损失函数$L=f(Y)$，$L$ 是一个数。从一维导数链式法则启发，矩阵求导应该有这样的形式：

$$\frac{\partial L}{\partial W}_{D*C} = X^T\frac{\partial L}{\partial Y}_{N*C}$$

$L$ 是数，所以 $\frac{\partial L}{\partial W}$和$\frac{\partial L}{\partial Y}$ 容易理解。从上式可以看出，$X^T$ 对 $\frac{\partial L}{\partial Y}$ 做了重新分布。$w_{i,j}$ 变化引起 $y_{j}$ 变化，从而引起 $L$ 变化，$X^T$ 规定了这些变化怎么转换。
