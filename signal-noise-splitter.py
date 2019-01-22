#!/usr/bin/python
import h5py
import os

in_file_path = 'data/raw/scsn_p_2000_2017_6sec_0.5r_pick_train.hdf5'
mix_file_path = 'data/out/scsn_p_2000_2017_6sec_0.5r_pick_train_mix.hdf5'

print(f"Deleting old file...")
if os.path.exists(mix_file_path):
  os.remove(mix_file_path)
print(f"Deleted old file.")

print(f"Opening files for read/write...")
in_file = h5py.File(in_file_path, 'r', libver='latest')
mix_file = h5py.File(mix_file_path, 'x', libver='latest')
print(f"Opened files.")

# Common variables
target = 'X'
# datasets = in_file.keys()
datasets = [
  'evids',
  'sncls'
]
in_file_size = len(in_file[target])
# in_file_size = 

print(f"Initializing file...")
# 'X' has shape (size, 300), adding 'pwave' dataset
mix_file.create_dataset(target, (in_file_size * 2, 300), dtype=in_file[target].dtype)
mix_file.create_dataset("pwave", (in_file_size * 2,), dtype='uint8')
# Rest of the datasets (in datasets)
for dataset in datasets:
  print(f"Adding {dataset} to new file...")
  mix_file.create_dataset(dataset, (in_file_size * 2,), dtype=in_file[dataset].dtype)
print(f"Initialized file.")

print(f"Splitting time-series data...")
for x in range(in_file_size):
  index = x * 2
  # Match the other Datasets to the split waveforms
  common = {
    "evids": in_file["evids"][x],
    "sncls": in_file["sncls"][x]
  }
  # Noise
  mix_file[target][index] = in_file[target][x][:300]
  # PWave
  mix_file[target][index + 1] = in_file[target][x][300:]
  mix_file['pwave'][index + 1] = 1
  for dataset in common:
    mix_file[dataset][index] = common[dataset]
    mix_file[dataset][index + 1] = common[dataset]

  if x % 1000 == 0:
    print("{:3.2f}% completed...".format(x/in_file_size * 100))

print("Finished.")
