from argparse import ArgumentParser
import pandas as pd
import os

# Takes one or two csv files and deduplicates based on the values of one or two columns.
# Outputs a new csv file with non-duplicated rows.
def main():
    # Read csv input into Pandas dataframes
    df_1 = pd.read_csv(args.input[0])
    if len(args.input) == 2:
        df_2 = pd.read_csv(args.input[1])
        merged_df = pd.concat([df_1, df_2])
        if len(args.columns) == 2:
            merged_df.drop_duplicates(subset=[args.columns[0], args.columns[1]], keep='first', inplace=True)
        else:
            merged_df.drop_duplicates(subset=args.columns[0], keep='first', inplace=True)
        merged_df.to_csv('/Users/jtim/Dropbox/DLSS/research-intelligence/research-intelligence-reports/general/output/no_dupes.csv', index=False)
    else:
        if len(args.columns) == 2:
            df_1.drop_duplicates(subset=[args.columns[0], args.columns[1]], keep='first', inplace=True)
        else:
            df_1.drop_duplicates(subset=args.columns[0], keep='first', inplace=True)
        df_1.to_csv('/Users/jtim/Dropbox/DLSS/research-intelligence/research-intelligence-reports/general/output/no_dupes.csv', index=False)

if __name__ == "__main__":
    # CLI client options.
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        action='store',
        nargs="+",
        help="Which csv file/s do you want to input?")
    parser.add_argument(
        "-c",
        "--columns",
        action='store',
        nargs="+",
        help="Which column/s should be used for deduplication?")
    args = parser.parse_args()
    main()
