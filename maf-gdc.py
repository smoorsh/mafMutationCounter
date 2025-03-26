### identifying gene mutations in cancer
import os
import gzip
import shutil
import glob
import pandas as pd
import numpy as np
import sys

### User defined input
parent_dir = sys.argv[1]
gene = sys.argv[2]
# input format: 'python maf-gdc.py PathToDirectory GeneOfInterest'

## move all of the .maf files up one directory and decompress them
subdirs = [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]

for subdir in subdirs:
    subdir_path = os.path.join(parent_dir, subdir)
        
    # Find all .maf.gz files in the subdirectory
    maf_files = glob.glob(os.path.join(subdir_path, "*.maf.gz"))
    #total_files += len(maf_files)
        
    for maf_file in maf_files:
        # Get just the filename without path
        filename = os.path.basename(maf_file)
            
        # Define the destination path (parent directory)
        dest_path = os.path.join(parent_dir, filename)
            
        # Move the file to parent directory
        shutil.move(maf_file, dest_path)
            
        # Decompress the file
        with gzip.open(dest_path, 'rb') as f_in:
            # Create the output filename by removing .gz extension
            out_filename = dest_path[:-3]  # Remove the .gz extension
                
            with open(out_filename, 'wb') as f_out:
                # Copy the decompressed content
                shutil.copyfileobj(f_in, f_out)
            
## count the number of instances of a specific gene name in column 1 in each file
files = glob.glob(os.path.join(parent_dir, "*.maf"))
results = {}
all_counts = []

for file in files:
    filename = os.path.basename(file)
    header_line = None
    
    ## remove commented header lines
    with open(file, 'r') as f:
        for i, line in enumerate(f):
            if not line.startswith('#'):
                header_line = i
                break
    
    if header_line is not None:
        maf_df = pd.read_csv(file, sep='\t', comment='#', skiprows=header_line, low_memory=False)
        
        ## count instances of gene of interest
        gene_count = maf_df[maf_df['Hugo_Symbol'] == gene].shape[0]
        # print(f"Found {gene_count} instances of {gene} in {filename}")
        results[filename] = gene_count
        all_counts.append(gene_count)

## average the numer of times the gene appears across all .maf files
print(f"Total occurrence count of {gene} across {len(all_counts)} files: {sum(all_counts)}")

if all_counts:
    average_count = sum(all_counts) / len(all_counts)
    print(f"\nAverage occurrence count of {gene} across {len(all_counts)} files: {average_count:.2f}")

## find the standard deviation
std_dev = np.std(all_counts)
print(f"Standard deviation: {std_dev:.2f}")