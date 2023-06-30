#!/usr/bin/env python

import sys
import argparse
import re


def parse_args():
    parser = argparse.ArgumentParser(description='Get coordinates from SAM file')
    parser.add_argument('SAM_files', metavar='SAM_file', nargs='+', help='SAM file(s) to extract coordinates')
    return parser.parse_args()


def process_sam_file(sam_file):
    coordinates_filename = 'coordinates.txt'
    coordinates_query_ref_filename = 'coordinates_query_ref.txt'

    with open(coordinates_filename, 'a') as coordinates_file, open(coordinates_query_ref_filename, 'w') as coordinates_query_ref_file:
        coordinates_query_ref_file.write('\t'.join(['query_name', 'query_start', 'query_end', 'query_length', 'chromosome', 'start', 'end', 'length']) + '\n')

        for line in open(sam_file, 'r'):
            fields = line.split('\t')
            if len(fields) < 10:
                continue
            query_name = fields[0]
            chromosome = fields[2]
            start = int(fields[3])
            cigar = fields[5]
            query_seq = fields[9]
            
            query_start_match = re.search(r'^(\d+)[SH]', cigar)
            query_start = int(query_start_match.group(1)) if query_start_match else 1

            query_length = sum(map(int, re.findall(r'(\d+)[M=XI]', cigar)))
            query_end = query_start + query_length - 1

            length = sum(map(int, re.findall(r'(\d+)[M=XDN]', cigar)))
            end = start + length - 1

            coordinates_query_ref_line = '\t'.join([query_name, str(query_start), str(query_end), str(query_length), chromosome, str(start), str(end), str(length)]) + '\n'
            coordinates_query_ref_file.write(coordinates_query_ref_line)

            coordinates_line = '\t'.join([chromosome, str(start), str(end)]) + '\n'
            coordinates_file.write(coordinates_line)


def main():
    args = parse_args()
    for sam_file in args.SAM_files:
        process_sam_file(sam_file)


if __name__ == '__main__':
    main()
