import collections
import numpy as np
import pandas as pd
import os

from argparse import Namespace

args = Namespace(
    base_dataset_dir="D:\\ml-datasets\\surnames-dataset\\",
    raw_dataset_csv="surnames.csv",
    train_proportion=0.7,
    val_proportion=0.15,
    test_proportion=0.15,
    output_munged_csv="surnames_with_splits.csv",
    seed=1337
)


if __name__ == '__main__':
    # Read raw data
    surnames = pd.read_csv(os.path.join(args.base_dataset_dir, args.raw_dataset_csv), header=0)

    # Splitting train by nationality
    by_nationality = collections.defaultdict(list)
    for _, row in surnames.iterrows():
        by_nationality[row.nationality].append(row.to_dict())

    # Create split data
    final_list = []
    np.random.seed(args.seed)
    for _, item_list in sorted(by_nationality.items()):
        np.random.shuffle(item_list)

        n = len(item_list)
        n_train = int(args.train_proportion * n)
        n_val = int(args.val_proportion * n)
        n_test = int(args.test_proportion * n)

        # Give data point a split attribute
        for item in item_list[:n_train]:
            item['split'] = 'train'
        for item in item_list[n_train:n_train + n_val]:
            item['split'] = 'val'
        for item in item_list[n_train + n_val:]:
            item['split'] = 'test'

            # Add to final list
        final_list.extend(item_list)

    # Write split data to file
    final_surnames = pd.DataFrame(final_list)
    print(final_surnames.split.value_counts())
    # Write munged data to CSV
    final_surnames.to_csv(os.path.join(args.base_dataset_dir, args.output_munged_csv), index=False)
    print("Output cvs file saved to ", os.path.join(args.base_dataset_dir, args.output_munged_csv))
