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