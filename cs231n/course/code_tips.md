# Vectorized Code
## Distance between vectors
(From assignment #1, KNN) $dist[i,j] = \|X[i]-X\_train[j]\|_2$.  
Following code is much faster than two nested loops.
```python
a = np.sum(np.square(X),axis=1).reshape(num_test,1)
b = np.sum(np.square(X_train),axis=1)
# (a+b): do broadcasting so expanded to a matrix of Na*Nb
dist = np.sqrt((a + b) - 2 * np.matmul(X, X_train.T))
```
## SVM
(From assignment #1, SVM Loss) 第$i$行整体减去这一行内第$y_i$个数。
```python
S = np.maximum(0, S - S[np.arange(num_train),y].reshape(num_train,1) + 1)
```
 * 用 array[lista, listb] 来检索出位置(lista_i, listb_i) 的元素
 * N\*M - N\*1 会自动对每行做 broadcast
 * np.maximum 做的是 broadcast，np.max 做的是 accumulation

(From assignment #1, SVM Gradient) 想到算 X_i 的系数矩阵就好做 vectorize 了。
```python
S[S > 0] = 0
```

(From assignment #1, Softmax Loss & Gradient) 用 keepdims 就不用 reshape 了。
```python
probs = exp_scores / np.sum(exp_scores, axis=1, keepdims=True)
```
Softmax 我实现的不干净，有重复运算。可以参考 https://cs231n.github.io/neural-networks-case-study/ probs 可以重复利用。

## NN
```python
# x[N, d1, d2, ..., dk] -> x[N, D]
x = x.reshape(x.shape[0], -1)
```

## CNN
做 spatial batchnorm 的时候，(N,C,H,W) 的数据要变成 (NxHxW,C)，用 transpose 做。
```python
# no transpose
x_row = np.zeros((N*H*W, C))
for i in range(C):
    x_row[:, i] = x[:, i, :, :].reshape(-1)
# transpose
x_row = x.transpose(0, 2, 3, 1).reshape(-1, C)
```
另外，gamma beta 的 shape 是 (1,C,1,1) 会方便，能直接乘、加 x(N,C,H,W)。

