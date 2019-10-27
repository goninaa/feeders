#! /usr/local/bin/python3.6

# visualize coverage over region  (and then gene)

from sys import argv
import pysam
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
from os import listdir, getcwd
from os.path import join, isfile


REF = "/data3/Moran/Xenopus/genome/GCF_001663975.1_Xenopus_laevis_v2_genomic.fa"
GFF_FILE = "/data3/Moran/Xenopus/genome/GCF_001663975.1_Xenopus_laevis_v2_genomic.edited.gff"
FOLDER = ""  # TODO
GENE_LIST = ""


def find_exon_coordinates_by_gene_name_list(gene_list, gff_file=GFF_FILE):

	gene_exons_dict = defaultdict(list)
	
	with open(gff_file, 'r') as infile:
		split_lines = (line.split('\t') for line in infile if not line.startswith('#'))
		for split_line in split_lines:
			if split_line[2] == 'exon':
				exon_list_line = split_line[8].split(';')
				d = {x[0]: x[1] for x in (field.split('=') for field in exon_list_line)}
				try:
					if d['gene'] in gene_list:
						chr_name = split_line[0]
						strand = split_line[6]
						exon_pos = (int(split_line[3]), int(split_line[4]))
						gene_exons_dict[d['gene']].append((chr_name, exon_pos, strand))
						# ignoring strand
				except KeyError:
					try:
						if d['ID'] in gene_list:
							# print(f"{d['ID']},{d['product'].strip()}")
							chr_name = split_line[0]
							strand = split_line[6]
							exon_pos = (int(split_line[3]), int(split_line[4]))
							gene_exons_dict[d['ID']].append((chr_name, exon_pos, strand))
							# ignoring strand
					except KeyError:
						print(f"Something went wrong with this line: {d}")
	# by now we should have a dictionary with genes and a list of exons
	return gene_exons_dict

def gene_coverage_per_region(samfile, gene_value_list):              
	"""Recieves the samfile object and gene_value_list (the value of the dict)"""
	gene_chr = gene_value_list[0][0]  # saving chr
	gene_strand = gene_value_list[0][2]  # saving chr
	print(f"Gene is in chr {gene_chr} and strand {gene_strand}")
	if gene_strand == '+':
		pos_list = [x[1] for x in gene_value_list if x[0] == gene_chr]
	else:
		pos_list = list(reversed([x[1] for x in gene_value_list if x[0] == gene_chr]))
	# print(pos_list)
	start_end = (pos_list[0][0], pos_list[-1][1])  # start end of gene
	if start_end[0] > start_end[1]:  # replace positions
		start_end = (start_end[1], start_end[0])
	# print(start_end[0], start_end[1])
	gene_positions = []
	cov_per_pos = []
	try:
		for pileupcolumn in samfile.pileup(gene_chr, start_end[0], start_end[1]):
			# print(pileupcolumn.pos, pileupcolumn.n)
			gene_positions.append(pileupcolumn.pos)
			cov_per_pos.append(pileupcolumn.n)
	# except TypeError:
	except ValueError:
		print(f"Gene value list: {gene_value_list}")
		print(gene_chr, start_end[0], start_end[1])
		raise TypeError
	return gene_positions, cov_per_pos, pos_list



def load_gene_list(filename):
	"""loading a list file and returning the gene list as a list"""
	with open(filename, 'r') as infile:
		gene_list = [x.strip() for x in infile.readlines()]
	return gene_list


# load gene_list
gene_list_fname = argv[1]
gene_list = load_gene_list(gene_list_fname)
gene_exons_dict = find_exon_coordinates_by_gene_name_list(gene_list)


try:
    folder = argv[2]
except IndexError:
	folder = getcwd()
	print("No folder provided, using cwd")

suf = ".bam"
# bam_list = sorted([f for f in listdir(folder) if isfile(join(folder, f)) and f.endswith(suf)], key=lambda cell_num: int(cell_num.split('_')[0]))
bam_list = sorted([f for f in listdir(folder) if isfile(join(folder, f)) and f.endswith(suf)])

# for each bam create all figures
for bam_filename in bam_list:
	print(f"Working on bamfile: {bam_filename}")
	# loadsam
	with pysam.AlignmentFile(join(folder,bam_filename), "rb" ) as samfile:
		# indexed=pysam.IndexedReads(samfile)
	# TODO

		# doing for every one
		for gene,exons_pos in gene_exons_dict.items():
			print(f"Working on gene {gene}")

			gene_positions, cov_per_pos, exon_pos = gene_coverage_per_region(samfile, exons_pos)
			# now plot:
			try:
				max_y = max(cov_per_pos) + 1
				# st_point = min(gene_positions)
				# fixed_gene_positions = [x - st_point for x in gene_positions]
				# fixed_exon_pos = [(x[0] - st_point, x[1] - st_point) for x in exon_pos]
				# end_point = max(fixed_gene_positions)
			
				# print(gene_positions)
			except ValueError:
				if len(gene_positions) == 0:
					print("The gene is not covered, moving on.")
					continue
				# print(f"gene_positions {gene_positions}")
				# print(f"cov_per_pos {cov_per_pos}")
				# print(f"exon_pos {exon_pos}")
				# raise ValueError
			fig = plt.figure()
			# plt.plot(fixed_gene_positions, cov_per_pos, 'b-')
			# plt.plot(gene_positions, cov_per_pos, 'b-')
			plt.bar(gene_positions, cov_per_pos, width=1.0, facecolor='blue', edgecolor='blue')
			# for pos in fixed_exon_pos:
			exon_pos_flat = []
			# for x in exon_pos:
			# 	exon_pos_flat.append(x[0])
			# 	exon_pos_flat.append(x[1])
			for pos in exon_pos:
				plt.axvspan(pos[0], pos[1], alpha=0.2, color='r')
			# for pos in exon_pos_flat:
				# print(pos)
				# plt.fill_between(pos, max_y, alpha=0.2, color='r')

			plt.title(gene)  # the gene_name
			plt.ylim(0, max_y)
			# plt.xticks(range(len(gene_positions)))
			# plt.xlim(0, len(gene_positions))
			# plt.xlim(0, end_point)
			plt.savefig(f"{bam_filename}_{gene}.png")
			plt.close()

print("Done")
exit(0)
