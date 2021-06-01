#!/usr/bin/env python3
"""
main.py, by John Webb, 2021-05-26
This program analyzes a csv file of business transactions.
"""

import sys
import csv
import os
import glob
import statistics
import shutil
from operator import getitem
from collections import OrderedDict
# import pandas as pd

def main():
    path = os.getcwd()
    input_dir = path + "/fraud_claims/*.csv"
    csv_files = glob.glob(input_dir)
    vendor_dict = {}
    # For each file input
    for file in csv_files:
        with open(file, encoding="utf-8") as csv_file:
            rows = csv.reader(csv_file, delimiter=',')
            for row in rows:
                # Read and format vendor name appropriately
                vendor = row[1]
                vendor = vendor.lower()
                vendor = vendor.replace('the', '')
                vendor = vendor.strip()
                # Continue if row is column header
                if vendor == 'vendor':
                    continue
                # Read and format Amount. Check if amount is there.
                amt_str = row[4]
                if not amt_str:
                    continue
                amt_str = amt_str.replace('$', '')
                amt_str = amt_str.replace(',', '')
                amt_str = amt_str.replace(' ', '')
                amount = float(amt_str)
                # Insert entry into dictionary.
                if vendor in vendor_dict:
                    vendor_dict[vendor]['count'] += 1
                    vendor_dict[vendor]['amounts'].append(amount)
                else:
                    vendor_dict[vendor] = {'count': 1,
                                        'amounts': [amount]
                                        }
    # Get output file and folder ready.
    output_dir = path+"/output/"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.mkdir(output_dir)
    output_file = output_dir+"/fraud_claim_summary.txt"
    outF = open(output_file, "w")
    sys.stdout = outF
    # Sort based on count. Calculate statistics and output for each vendor.
    sorted_vender_dict = sorted(vendor_dict.items(), key=lambda x: x[1]['count'], reverse=True)
    for vendor in sorted_vender_dict:
        count = vendor[1]['count']
        total = round(sum(vendor[1]["amounts"]),2)
        med = round(statistics.median(vendor[1]["amounts"]), 2)
        max_val = max(vendor[1]["amounts"])
        min_val = min(vendor[1]["amounts"])
        avg = total / count
        print("Vendor: ", vendor[0])
        print("\tNumber of occurrences: ", count)
        print("\tTotal Amount: ", total)
        print("\tAverage: ", avg)
        print("\tMin, Max, Median: {}, {}, {}".format(min_val, max_val, med))

if __name__ == "__main__":
    main()

        # col_list = ["Vendor", "Amount"]
        # dataframes = []
        # for file in csv_files:
        #     df = pd.read_csv(file, header=0, usecols=col_list)
        #     dataframes.append(df)
        # total_data = pd.concat(dataframes, ignore_index=True)
        # print(total_data.loc[2][1])
        # counts = total_data['Vendor'].value_counts()
        # sums = total_data.groupby('Vendor')['Amount'].sum()
        # print(counts)
        # print(sums)
