import torch
import triton
import triton.language as tl


@triton.jit
def add_k(x_ptr, y_ptr, o_ptr, n, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    offs = pid * BLOCK + tl.arange(0, BLOCK)
    m = offs < n
    tl.store(o_ptr + offs, tl.load(x_ptr + offs, mask=m) + tl.load(y_ptr + offs, mask=m), mask=m)


x = torch.randn(1024, device="cuda")
y = torch.randn(1024, device="cuda")
o = torch.empty_like(x)
add_k[(4,)](x, y, o, 1024, BLOCK=256)
torch.cuda.synchronize()
print("TRITON GPU KERNEL OK, max err =", (o - (x + y)).abs().max().item())
