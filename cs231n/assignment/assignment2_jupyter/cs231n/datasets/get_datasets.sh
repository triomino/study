if [ ! -d "cifar-10-batches-py" ]; then
  curl http://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz -O
  tar -xzvf cifar-10-python.tar.gz
  rm cifar-10-python.tar.gz
fi
