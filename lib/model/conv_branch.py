from .separable_conv import SeparableConv

from torch import nn


class ConvBranch(nn.Module):
    '''
    https://github.com/melodyguan/enas/blob/master/src/cifar10/general_child.py#L483
    '''
    def __init__(self,
                 in_planes,
                 out_planes,
                 kernel_size,
                 padding=0,
                 dilation=1,
                 stride=1,
                 separable=False,
                 Struct=nn.Conv2d):
        super(ConvBranch, self).__init__()

        self.in_planes = in_planes
        self.out_planes = out_planes
        self.kernel_size = kernel_size

        self.inp_conv1 = nn.Sequential(
            Struct(in_planes,
                   out_planes,
                   kernel_size=1,
                   bias=False,
                   dilation=dilation),
            nn.BatchNorm2d(out_planes, track_running_stats=False), nn.ReLU())

        conv = SeparableConv if separable else Struct
        self.out_conv = nn.Sequential(
            conv(in_planes,
                 out_planes,
                 kernel_size=kernel_size,
                 padding=padding,
                 dilation=dilation,
                 stride=stride,
                 bias=False),
            nn.BatchNorm2d(out_planes, track_running_stats=False), nn.ReLU())

    def forward(self, x):
        out = self.inp_conv1(x)
        out = self.out_conv(out)
        return out
