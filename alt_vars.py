#! /usr/bin/env python3
'''
alt_vars v1.0: Given a VCF, output a subset VCF containing only alternate variants with frequency >= threshold (default 0.5)
'''
import argparse
VARIANT_CALLERS = {'freebayes', 'ivar', 'lofreq'}

# main content
if __name__ == "__main__":
    # parse user args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input VCF File")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output VCF File")
    parser.add_argument('-v', '--variant_caller', required=True, type=str, help="Variant Caller (options: %s)" % ', '.join(sorted(VARIANT_CALLERS)))
    parser.add_argument('-m', '--min_alt_freq', required=False, type=float, default=0.5, help="Minimum Alt Allele Frequency")
    args = parser.parse_args()
    args.variant_caller = args.variant_caller.lower()
    assert args.variant_caller in VARIANT_CALLERS, "Invalid variant caller: %s (options: %s)" % (args.variant_caller, ', '.join(sorted(VARIANT_CALLERS)))
    assert args.min_alt_freq >= 0 and args.min_alt_freq <= 1, "Minimum Alt Allele Frequency must be between 0 and 1"

    # handle input
    if args.input.lower() == 'stdin':
        from sys import stdin as infile
    else:
        infile = open(args.input)

    # handle output
    if args.output.lower() == 'stdout':
        from sys import stdout as outfile
    else:
        outfile = open(args.output, 'w')

    # perform subsetting
    for line in infile:
        if line.startswith('#'):
            outfile.write(line)
        else:
            parts = line.strip().split('\t')
            if len(parts) == 1: # empty line
                continue
            if parts[6].upper() == 'FAIL': # FILTER column
                continue
            if args.variant_caller in {'freebayes', 'lofreq'}:
                alt_freq = parts[7].split('AF=')[1].split(';')[0]
            elif args.variant_caller == 'ivar':
                alt_freq = parts[-1].split(':')[-1]
            else:
                assert False, "Invalid variant caller: %s (options: %s)" % (args.variant_caller, ', '.join(sorted(VARIANT_CALLERS)))
            if ',' in alt_freq:
                alt_freq = max(float(v) for v in alt_freq.split(','))
            else:
                alt_freq = float(alt_freq)
            if alt_freq >= args.min_alt_freq:
                outfile.write(line)

    # finish up
    infile.close(); outfile.close()
