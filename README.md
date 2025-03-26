# mafMutationCounter
A python script that analyzes mutation counts in .maf files.

# Introduction
mafMutationCounter requires that the user has already used gdc-client to download the directories, and subsequently the files, from the Genome Data Commons manifest file. Only the directories are needed, this program moves and decompresses the .maf.gz files as necessary.

# Installation
```
git clone https://github.com/smoorsh/mafMutationCounter.git
```

# Run the Program
Change to the mafMutationCounter directory.
Replace 'PathToDirectoryWithDirectories' with the path to the directory containing all of the subdirectories with the .maf.gz files.
Replace 'GeneOfInterest' with the gene you are interested in collecting mutation data for.
```
cd mafMutationCounter
python maf-gdc.py PathToDirectoryWithDirectories GeneOfInterest
```
