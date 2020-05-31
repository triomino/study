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
