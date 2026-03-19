import torch
import torchvision
import torch.nn as nn
from torch.nn import init
from torch.autograd import Variable
from attention import DualCrossModalAttention
import warnings

warnings.filterwarnings("ignore")


def weights_init_kaiming(m):
    classname = m.__class__.__name__
    # print(classname)
    if classname.find('Conv') != -1:
        init.kaiming_normal_(m.weight.data, a=0, mode='fan_in')  # For old pytorch, you may use kaiming_normal.
    elif classname.find('Linear') != -1:
        init.kaiming_normal_(m.weight.data, a=0, mode='fan_out')
        init.constant_(m.bias.data, 0.0)
    elif classname.find('BatchNorm1d') != -1:
        init.normal_(m.weight.data, 1.0, 0.02)
        init.constant_(m.bias.data, 0.0)


def weights_init_classifier(m):
    classname = m.__class__.__name__
    if classname.find('Linear') != -1:
        init.normal_(m.weight.data, std=0.001)
        init.constant_(m.bias.data, 0.0)


class ClassBlock(nn.Module):
    def __init__(self, input_dim, class_num, droprate, relu=False, bnorm=True,
                 num_bottleneck=512, linear=True, return_f=False):
        super(ClassBlock, self).__init__()
        self.return_f = return_f
        add_block = []
        if linear:
            add_block += [nn.Linear(input_dim, num_bottleneck)]
        else:
            num_bottleneck = input_dim
        if bnorm:
            add_block += [nn.BatchNorm1d(num_bottleneck)]
        if relu:
            add_block += [nn.LeakyReLU(0.1)]
        if droprate > 0:
            add_block += [nn.Dropout(p=droprate)]
        add_block = nn.Sequential(*add_block)
        add_block.apply(weights_init_kaiming)

        classifier = []
        classifier += [nn.Linear(num_bottleneck, class_num)]
        classifier = nn.Sequential(*classifier)
        classifier.apply(weights_init_classifier)

        self.add_block = add_block
        self.classifier = classifier

    def forward(self, x):
        x = self.add_block(x)
        if self.return_f:
            f = x
            x = self.classifier(x)
            return x, f
        else:
            x = self.classifier(x)
            return x


class SCSEBlock(nn.Module):
    def __init__(self, channel, reduction=16):
        super(SCSEBlock, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)

        self.channel_excitation = nn.Sequential(nn.Linear(channel, int(channel // reduction)),
                                                nn.ReLU(inplace=True),
                                                nn.Linear(int(channel // reduction), channel),
                                                nn.Sigmoid())

        self.spatial_se = nn.Sequential(nn.Conv2d(channel, 1, kernel_size=1,
                                                  stride=1, padding=0, bias=False),
                                        nn.Sigmoid())

    def forward(self, x):
        bahs, chs, _, _ = x.size()

        # Returns a new tensor with the same data as the self tensor but of a different size.
        chn_se = self.avg_pool(x).view(bahs, chs)
        chn_se = self.channel_excitation(chn_se).view(bahs, chs, 1, 1)
        chn_se = torch.mul(x, chn_se)

        spa_se = self.spatial_se(x)
        spa_se = torch.mul(x, spa_se)
        return torch.add(chn_se, 1, spa_se)


class Decoder(nn.Module):
    def __init__(self, in_channels, channels, out_channels):
        super(Decoder, self).__init__()
        self.conv1 = nn.Sequential(nn.Conv2d(in_channels, channels, kernel_size=3, padding=1),
                                   nn.BatchNorm2d(channels),
                                   nn.ReLU(inplace=True))
        self.conv2 = nn.Sequential(nn.Conv2d(channels, out_channels, kernel_size=3, padding=1),
                                   nn.BatchNorm2d(out_channels),
                                   nn.ReLU(inplace=True))
        self.drop = torch.nn.Dropout2d(p=0.50)
        self.SCSE = SCSEBlock(out_channels)

    def forward(self, x, e=None):
        x = torch.nn.functional.upsample(x, scale_factor=2, mode='bilinear')
        if e is not None:
            x = torch.cat([x, e], 1)
            x = self.drop(x)

        x = self.conv1(x)
        x = self.conv2(x)
        x = self.SCSE(x)
        return x


class STFL_Net(nn.Module):
    def __init__(self, n_classes=1, activation=nn.Sigmoid()):
        super(STFL_Net, self).__init__()
        self.n_classes = n_classes
        self.resnet_full = torchvision.models.resnet50(pretrained=True)
        self.resnet_word = torchvision.models.resnet50(pretrained=True)

        self.dual_cma = DualCrossModalAttention(in_dim=2048, size=16, ratio=8, ret_att=False)

        self.decoder4 = Decoder(4096 + 2048, 2048, 2048)
        self.decoder3 = Decoder(2048 + 1024, 1024, 1024)
        self.decoder2 = Decoder(1024 + 512, 512, 512)
        self.decoder1 = Decoder(512 + 128, 256, 256)
        self.decoder0 = Decoder(256, 128, 128)

        self.final_conv = nn.Sequential(nn.Conv2d(128, self.n_classes, kernel_size=1, padding=0))
        self.final_activation = activation

    def forward(self, image_full, image_word):
        x1_full = self.resnet_full.conv1(image_full)
        x1_full = self.resnet_full.bn1(x1_full)
        x1_full = self.resnet_full.relu(x1_full)
        x2_full = self.resnet_full.maxpool(x1_full)

        x2_full = self.resnet_full.layer1(x2_full)
        x3_full = self.resnet_full.layer2(x2_full)
        x4_full = self.resnet_full.layer3(x3_full)
        fea_full = self.resnet_full.layer4(x4_full)

        x1_word = self.resnet_word.conv1(image_word)
        x1_word = self.resnet_word.bn1(x1_word)
        x1_word = self.resnet_word.relu(x1_word)
        x2_word = self.resnet_word.maxpool(x1_word)

        x2_word = self.resnet_word.layer1(x2_word)
        x3_word = self.resnet_word.layer2(x2_word)
        x4_word = self.resnet_word.layer3(x3_word)
        fea_word = self.resnet_word.layer4(x4_word)

        fea_full, fea_word = self.dual_cma(fea_full, fea_word)

        fea = torch.cat((fea_full, fea_word), dim=1)
        x4 = torch.cat((x4_full, x4_word), dim=1)
        d4 = self.decoder4(fea, x4)

        x3 = torch.cat((x3_full, x3_word), dim=1)
        d3 = self.decoder3(d4, x3)

        x2 = torch.cat((x2_full, x2_word), dim=1)
        d2 = self.decoder2(d3, x2)

        x1 = torch.cat((x1_full, x1_word), dim=1)
        d1 = self.decoder1(d2, x1)

        d0 = self.decoder0(d1)
        mask = self.final_conv(d0)
        mask = self.final_activation(mask)

        return mask


if __name__ == '__main__':
    input_full = torch.randn(2, 3, 512, 512)
    input_word = torch.randn(2, 3, 512, 512)

    model = STFL_Net()
    out = model(dummy_input_fullinput, input_word)
    print(out.shape)
