## 推导Ax求导
$A=(\alpha_1,\alpha_2,...,\alpha_n),Ax=\begin{matrix}\sum{a_{1,j}x_j}\\\sum{a_{2,j}x_j}\\...\\\sum{a_{n,j}x_j}\end{matrix}$  
$\frac{\partial(Ax)}{\partial x_j}=\begin{matrix}a_{1,j}\\a_{2,j}\\...\\a_{n,j}\end{matrix}=\alpha_j$，所以$\frac{\partial(Ax)}{\partial x}=(\alpha_1,...,\alpha_n)=A$
## 推导二次型求导
$y=x^TAx=\sum_{i,j}a_{i,j}x_ix_j$  
### 一阶
与$x_i$相关的项$\sum_{j\ne i}a_{i,j}x_ix_j+\sum_{k\ne i}a_{k,i}x_kx_i+a_{i,i}x_i^2$  
$\frac{\partial y}{\partial x_i}=\sum_{i\ne j}(a_{i,j}+a_{j,i})x_j+2a_{i,i}x_i$  
所以，$\frac{\mathrm dy}{\mathrm dx}=Ax+A^Tx$($\frac{\mathrm{d}y}{\mathrm{d}x}$就是$\nabla y$)   
### 二阶
$\frac{\partial (A+A^T)x}{\partial x_j}=\begin{matrix}a_{1,j}+a_{j,1}\\ a_{2,j}+a_{j,2} \\ ... \\a_{n,j}+a_{j,n}\end{matrix}=col_j+row_j$  
$\nabla^2y=\nabla((A+A^T)x)=(\frac{\partial (A+A^T)x}{\partial x_1},\frac{\partial (A+A^T)x}{\partial x_2},...,
\frac{\partial (A+A^T)x}{\partial x_n})=(col_1+row_1,col_2+row_2,...,col_n+row_n)=A+A^T$。事实上不用这么来一遍，直接用$Ax$求导的结论。
### A对称
当$A$对称时，有$\frac{\mathrm dy}{\mathrm dx}=2Ax,\nabla^2y=2A$   
## Dual Norm
$\|z\|_*=\textrm{sup}_x{z^Tx|\|x\|\le 1}$  
和$\|z\|$不一定相等，因为$\|x\|$不一定是$2-norm$  
当$\|x\|$是$1-norm$时，其实$\|z\|_*$是$\infty-norm$，这两个互为对偶范数。
$2-norm$的对偶恰好是它自己，$\frac{1}{p}+\frac{1}{q}=1$的$p,q$对偶
### Subgradient(single)/Subdifferential(set of subgradient)
取到对偶的集合，即$\partial\|z\|_*=\{x|<x,z>=\|z\|_*,\|x\|\le 1\}$，它可能有多个位置，比如$\infty-norm$的$(1，1)$，$1-norm$的一条线段。

## 半连续(Semi-continuity)、上境图(epigraph)
上半连续：$\forall \epsilon$存在开邻域$U$使得$f(x)<f(x_0)+\epsilon$  
连续=上半+下半，上境图闭合=下半连续=凸函数闭合。  
普通函数上境图可能不闭合。把$x^2$右半部分上移1个单位，$f(0)=1$，这样它上半连续但不下半连续，是开的。如果$f(0)=0$则是闭合的。主要区别在于$(0,0～1)$这条线段是不是在epigraph里。  
凸函数也可能不闭合。比如$f(x,y)$只在单位圆上非负，圆内$0$，那么不闭合。  
因此，闭合的凸函数，任一个层级要么空，要么闭合。层级是$f(x)\le \beta$的$x$范围。  
$\frac{1}{x},e^{x}$凸闭，值域和定义域都开。  
幸运的是，凸函数只在边界上可能不连续，内点必然连续。普通函数不一定了（上面的例子）

## 次梯度/次微分
$f(x)\ge f(x_0)+<g,x-x_0>$  
### 与凸函数
定义域每个点可次微分非空->凸  
凸函数定义域内点->次微分非空  
闭凸函数的边界点仍可能无次梯度，所以上面定理条件不可松弛。  
可微的，每个点次梯度唯一，就是梯度；否则可能不唯一。  
一个凸集的”支撑“向量其实就是凸集在这个向量切平面的另一边。  
显然最低点到$x_0$和$x_0$的次梯度点积$\ge 0$(和梯度类似，次梯度是远离最低点的方向)
### 与凸函数的方向导数
因为不光滑，所以我们要研究次梯度。为了算次梯度，引入方向导数作为计算次梯度的桥梁。内点虽然不一定光滑（不一定有梯度），但是连续，连续凸就一定有方向导数。    

想象凸函数$z=f(x,y)$,在最低点$(x_0,y_0)$有一个方向向量$p$，在这个方向上长度从0不断增加，$p$延展的平面$y=p^T(x-x_0)+y_0$不断在$p$方向上陡峭起来,直到卡住凸面(x,y,f(x,y))，它就是在这个方向的最大次梯度。$(x_0,y_0)$在$p$方向的导数就是它的长度。而且，任何其他方向的次梯度在$p$上的投影小于这个值。

把上面情形中的最低点换成另一个点，是两个面的交线上一点，$p$方向上是两条折线的交点。那么你$p$在不断变长的过程中，平面会和凸壳先相交后不交，再相交，不交的$[a,b](0<a\le b)$乘以单位化$p$就是次梯度，而$p$方向导数等于$b$，$-p$方像导数是$-a$。光滑凸表面上$a=b$因为正负方向导数是相反的。
### 支撑函数
$\psi_Q(g)=sup\{<g,x>|x\in Q\}$ 考虑闭集Q，如果g方向射线和Q有交那x就是最远点，无交是-g方向最近点，用sup无非就是Q可能是开的，边缘没法取，所以不是max。

如果两个闭凸集支撑函数一样，那么他们也相等。

## 记号
$\psi_Q(g)=sup\{<g,x>|x\in Q\}$  
$Conv\{a,b,c\}=\{\lambda_1a+\lambda_2b+\lambda_3c,0\le\lambda_i\le 1,\sum\lambda_i=1\}$

## 一些结论
### there is no $x$ s.t. $Ax=b$ => $\exist z$ s.t. $A^Tz=0,b^Tz\ne 0$
Proof. $\forall z,A^Tz=0\rightarrow b^Tz=0$，then for such $z$,$\alpha_1\perp z,\alpha_2\perp z,...,$，$b\perp z$ means $b$ can be expanded with $\alpha_{1\text{ to }n}$
反过来怎么证明？由于$b$不在$\alpha_i$张成的空间，$b$的分量一定有不在$\alpha$空间的并且和$\alpha$垂直的正交基，那个基作为$z$即可