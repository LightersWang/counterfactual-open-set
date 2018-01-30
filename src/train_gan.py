#!/usr/bin/env python
import argparse
import os
import sys

parser = argparse.ArgumentParser()
# The result_dir must always be specified
parser.add_argument('--result_dir', required=True, help='Output directory for images and model checkpoints')
# Other options have default values
parser.add_argument('--beta1', type=float, default=0.5, help='beta1 for adam. [default: 0.5]')
parser.add_argument('--weight_decay', type=float, default=.0, help='Optimizer L2 weight decay [default: .0]')
parser.add_argument('--pt_loss', type=float, default=1.0, help='Multiplier for pull-away term loss [default: 1.0]')
parser.add_argument('--fm_loss', type=float, default=1.0, help='Multiplier for feature-matching loss [default: 1.0]')
parser.add_argument('--generator_weight', type=float, default=0.1, help='Multiplier for generator adversarial loss [default: 0.1]')
parser.add_argument('--epochs', type=int, default=10, help='number of epochs to train for [default: 10]')

options = vars(parser.parse_args())

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from dataloader import FlexibleCustomDataloader
from training import train_gan
from networks import build_networks, save_networks, get_optimizers
from options import load_options, get_current_epoch
from locking import acquire_lock, release_lock

options = load_options(options)
dataloader = FlexibleCustomDataloader(fold='train', **options)
networks = build_networks(dataloader.num_classes, **options)
optimizers = get_optimizers(networks, **options)

start_epoch = get_current_epoch(options['result_dir']) + 1
for epoch in range(start_epoch, start_epoch + options['epochs']):
    train_gan(networks, optimizers, dataloader, epoch=epoch, **options)
    save_networks(networks, epoch, options['result_dir'])