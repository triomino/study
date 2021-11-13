from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    S = X.dot(W)
    num_train = S.shape[0]
    S -= np.max(S, axis=1).reshape(num_train, 1)
    for i in range(num_train):
        p = np.exp(S[i]) / np.sum(np.exp(S[i]))
        loss -= np.log(p[y[i]])
        dW[:,y[i]] -= X[i]
        for j in range(W.shape[1]):
           dW[:, j] += p[j] * X[i]
    loss /= num_train
    loss += reg * np.sum(W * W)
    dW /= num_train
    dW += 2.0 * reg * W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    S = X.dot(W)
    num_train = S.shape[0]
    # Use keepdims = True is better here
    S -= np.max(S, axis=1).reshape(num_train, 1)
    loss = (-np.sum(S[np.arange(num_train),y]) + np.sum(np.log(np.sum(np.exp(S),axis=1))))/num_train + reg * np.sum(W*W)
    S = np.exp(S)
    # Use keepdims = True is better here
    S = S / np.sum(S, axis=1).reshape(num_train, 1)
    S[np.arange(num_train), y] -= 1
    dW = X.T.dot(S) / num_train + 2.0 * reg * W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
