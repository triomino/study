## Introduction
There is no algorithm that decides whether an alleged algorithm for computing f(x) is indeed such an algorithm.  
从一个经典的自我指涉悖论开始。
简述：
1. 排列所有算法 $E_1,...,E_n,...$, 设每个算法对应函数 $f_1(x),...,f_n(x),...$，令 $g(x)=f_x(x)+1$  
2. 没有一个 i 使得 $f_i(x)=g(x)$，即没有算法能算它。
3. 1 和 2 矛盾，2 说 g(x) 没有算法能算，但是 1 的算法“列举 $E_i$ 然后模拟”明明能算出任意 $g(x_0)$ 的值。到底哪里除了问题呢？这是一个很隐蔽的错误，我们无意中假设了给一个算法和一个函数，存在一个通用算法能判断给定算法是否计算了给定函数 f(x). g(x) 是不可计算的，我们在 1 中用通俗语言说的“算法”不能被形式化地确定表示。（存疑）

### predicate and it extension
Extension(P) = $\{x_1, x_2, ..., x_n|P(x_1,...,x_n)\}$

## Chap 1
Formally represent an algorithm/computing process  
### Related to definition
internal configurations, alphabet, instantaneous description,   
Z is simple,   
$\alpha$ is an instantaneous description of Z,   
tape expression,   
internal configuration of Z at $\alpha$, scanned symbol of Z at $\alpha$, tape expression of Z at $\alpha$  
$q_iS_jS_kq_l$, $q_iS_jLq_l$, $q_iS_jRq_l$, $q_iS_jq_kq_l$
### Related to computing
$\alpha\rightarrow\beta$  
terminal with respect to Z  
computation of a Turing machine Z
$\alpha_p=Res_Z(\alpha_1)$  
$\bar n=1^{n+1}, (\overline{n_1,n_2,..n_k})=\overline{n_1}B\overline{n_2}B...B\bar{n_k}$,$\langle M\rangle$ number of 1 in M  
$\Psi_Z^{(n)}(x_1,...,x_n)=\begin{cases}\langle Res_Z(q_1(\overline{x_1,...,x_n}))\rangle\\ undefined \end{cases}$  
f(x_1,...,x_n) is partially computable, Z computes f. if f is total -> computable  
$x-y$ 在 <0 时无定义，即不停机，proper subtraction $<0$ 时令 $x-y=0$  
There exists a partially computable function f(m) whose completion g(m) is not computable.  
### Relative computation
$\alpha \xrightarrow[A]{} \beta(Z)$, $q_iS_jq_kq_l$, choose $q_k$ if $\langle\alpha\rangle\in A$ otherwise $q_l$  
$\alpha$ is final w.r.t Z, simple -> final = terminal  
A-computation, $\alpha_p=Res_Z^A(\alpha_1)$, $\alpha_p$ is A-resultant of $\alpha_1$ w.r.t Z  
$\Psi_{Z;A}^{(n)}(x_1,...,x_n)=\begin{cases}\langle Res_Z^A(q_1(\overline{x_1,...,x_n}))\rangle\\ undefined \end{cases}$  
f(x_1,...,x_n) is <b>partially</b> A-computable, Z A-computes f. if f is total -> A-computable  
(partially) computable -> (partially) A-computable  
(partially )$\empty$-computable ~ (partially) computable  
set S is (A-)computable ~ $C_S(x)$ is (A-)computable  
A is A-computable. Proof $q_1 B q_2 q_3$, $q_2$ 清除所有 1，$q_3$ 清除完再写一个 1, this TM A-computes $C_A(x)$  
## Chap 2
$\theta(Z)$ = max i of $q_i$ in Z  
n-regular(n>0): $Res_Z^A[q_1(\overline{m_1,...,m_n})]=q_{\theta(Z)}(\overline{r_1,...,r_s})$(if defined), no quadruaple start with $q_\theta(Z)$  
$Z^{(n)}$: all $q_i\rightarrow q_{n+i}$