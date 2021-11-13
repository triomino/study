## 矩阵
根据谱定理，实对称矩阵可以特征分解$A=U\Lambda U^{-1}$，普定理也指出$U$是正交阵。由于$U$是特征向量矩阵，直接缩放成单位正交矩阵，单位正交阵有$U^{-1}=U^T$，所以对称矩阵分解可以写成$A=U\Lambda U^{T}$  
对称矩阵特征值为实数证明：设有特征值不是实数，对应复特征向量拿出来，$Ax=\lambda x$，blabla 导致矛盾  
对称矩阵特征向量正交证明：$(\lambda_1,x),(\lambda_2,y)$,$\lambda_1x^Ty=(Ax)^Ty=x^TAy=\lambda_2x^Ty$所以要么$\lambda_1=\lambda_2$，要么$x^Ty=0$
单位正交阵必定对称证明：$Q^TQ=I$以及逆矩阵唯一。
## 图谱相关
### Kirchhoff's theorem
L=D-A 的n-1个非零特征值乘积乘n等于 spanning tree 个数(为什么L有n-1个非零特征值？显然取向量为1111可知必有一个是0)而这个值恰好等于L的任一个cofactor（为什么L所有cofactor相等，为什么恰好等于）   
### Laplacian 
normalized Laplacian$L^*=D^{-\frac{1}{2}}LD^{-\frac{1}{2}}$和$L$对称半正定（为何?$L$半正定拆开D配方就行了，$L^*$二次型和$L$一一对应）为什么还需要一个normalized，直接用$L$不好吗？  
$L^*$特征值[0,2]，为何？有什么用？  
$L^*$特征矩阵是不是单位正交阵？为啥用这个矩阵乘x就是图卷积？
### 图卷积
图信号傅里叶变换定义为$\mathscr{F}(x)=U^Tx$,其中$U$是 normalized Laplacian 的特征矩阵，逆变换则为$\mathscr{F}^{-1}(x)=Ux$。怎么理解？  
signal x 和 filter g 卷积定义为
$\mathscr{F}^{-1}(\mathscr{F}(x)\bigodot\mathscr{F}(g))=U(U^T(x)\bigodot U^T(g))$，$\bigodot$是对应位置向乘。为何如此定义？