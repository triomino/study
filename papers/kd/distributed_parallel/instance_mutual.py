import torch
import torch.distributed as dist
import torch.multiprocessing as mp
import torch.nn as nn
import torch.optim as optim
from torch.nn.parallel import DistributedDataParallel as DDP


d_in = 64
d_out = 32


class MutualLoss(nn.Module):
    def __init__(self):
        super(MutualLoss, self).__init__()
        self.fc = nn.Linear(d_in, d_out)

    def forward(self, x, eps=1e-12):
        N = x.shape[0]
        x = x.view(N, -1)
        x = self.fc(x)
        x_square = x.pow(2).sum(dim=1)
        prod = x @ x.t()
        res = (x_square.unsqueeze(1) + x_square.unsqueeze(0) -
               2 * prod).clamp(min=eps)

        res = res.clone()
        res[range(len(x)), range(len(x))] = 0

        return res.sum() / (1.0 * N * N)


class MutualLossDistributed(nn.Module):
    def __init__(self):
        super(MutualLossDistributed, self).__init__()
        self.fc = nn.Linear(d_in, d_out)

    def forward(self, x, y, eps=1e-12):
        Nx = x.shape[0]
        Ny = y.shape[0]
        x = x.view(Nx, -1)
        y = y.view(Ny, -1)
        x = self.fc(x)
        y = self.fc(y)
        x_square = x.pow(2).sum(dim=1)
        y_square = y.pow(2).sum(dim=1)
        prod = x @ y.t()
        res = (x_square.unsqueeze(1) + y_square.unsqueeze(0) -
               2 * prod).clamp(min=eps)

        return res.sum() / (1.0 * Nx * Ny)


def worker(rank, world_size, start_model, input_batch, true_grad,
           true_loss, cross_batch=False):
    dist.init_process_group("nccl", rank=rank, world_size=world_size,
                            init_method='tcp://127.0.0.1:23456')
    input_batch = input_batch.to(rank)
    input_div = torch.split(input_batch, input_batch.shape[0]
                            // world_size)[rank]

    model = MutualLossDistributed() if cross_batch else MutualLoss()
    model.load_state_dict(start_model.state_dict())
    model = model.to(rank)
    model = DDP(model, device_ids=[rank])

    optimizer = optim.SGD(model.parameters(), lr=0.1)

    loss = model(input_div, input_batch) if cross_batch else model(input_div)
    loss.backward()
    optimizer.step()

    module = model.module
    loss = collect_avg(loss.item(), rank=rank, world_size=world_size)
    true_grad = true_grad.to(rank)
    grad_diff = module.fc.weight.grad.detach() - true_grad

    if rank == 0:
        if cross_batch:
            print('sub batch x batch')
        else:
            print('sub batch x sub batch')
        print('loss diff ', abs(loss - true_loss).item())
        print('grad diff  ', torch.sum(grad_diff * grad_diff).item())


def single(start_model, input_batch):
    print('Single Process')
    model = MutualLoss()
    model.load_state_dict(start_model.state_dict())

    optimizer = optim.SGD(model.parameters(), lr=0.1)

    loss = model(input_batch)
    loss.backward()
    optimizer.step()

    return loss, model


def main():
    world_size = 8
    start_model = MutualLoss()
    input_batch = torch.randn(512, d_in)

    loss, model = single(start_model, input_batch)
    grad = model.fc.weight.grad.detach()
    loss = loss.detach()
    mp.spawn(worker, args=(world_size, start_model, input_batch, grad,
                           loss, True), nprocs=world_size, join=True)

    mp.spawn(worker, args=(world_size, start_model, input_batch, grad,
                           loss, False), nprocs=world_size, join=True)


if __name__ == "__main__":
    main()


def collect_avg(x, rank=0, world_size=1):
    x = torch.tensor(x).cuda(rank)
    dist.all_reduce(x, dist.ReduceOp.SUM)
    return x / (1.0 * world_size)
