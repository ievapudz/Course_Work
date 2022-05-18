#!/bin/sh

# Collecting results

echo -e "seq_id\tper_tok_averaged" > thermoclass/analysis/Cas12a_1022_splits_per_tok_averaged.tsv

cat thermoclass/predictions/FASTA/Cas12a_1022_splits.part-?.per_tok.fasta | grep '>' |\
	awk 'BEGIN{OFS="\t"}{ print $1, $4 }' | sed 's/>//g' | sed 's/mean=//g' |\
	sort >> thermoclass/analysis/Cas12a_1022_splits_per_tok_averaged.tsv

echo -e "seq_id\tper_tok_averaged" > thermoclass/analysis/Cas12b_1022_splits_per_tok_averaged.tsv

cat thermoclass/predictions/FASTA/Cas12b_1022_splits.part-?.per_tok.fasta | grep '>' |\
	awk 'BEGIN{OFS="\t"}{ print $1, $4 }' | sed 's/>//g' | sed 's/mean=//g' |\
	sort >> thermoclass/analysis/Cas12b_1022_splits_per_tok_averaged.tsv

# Merging analysis to one table (mean and per tok) and calucating deltas
echo -e "seq_id\tmean\taveraged_per_tok\tdelta" >\
	thermoclass/analysis/Cas12a_1022_splits_mean_vs_per_token_averaged.tsv

./scripts/misc/merge_mean_per_tok.py thermoclass/predictions/TSV/Cas12a_1022_splits.tsv \
	2 thermoclass/analysis/Cas12a_1022_splits_per_tok_averaged.tsv 1 >>\
	 thermoclass/analysis/Cas12a_1022_splits_mean_vs_per_token_averaged.tsv

echo -e "seq_id\tmean\taveraged_per_tok\tdelta" >\
	thermoclass/analysis/Cas12b_1022_splits_mean_vs_per_token_averaged.tsv

./scripts/misc/merge_mean_per_tok.py thermoclass/predictions/TSV/Cas12b_1022_splits.tsv \
	2 thermoclass/analysis/Cas12b_1022_splits_per_tok_averaged.tsv 1 >>\
	thermoclass/analysis/Cas12b_1022_splits_mean_vs_per_token_averaged.tsv

# Separating results for N and C terms
tail -n +2 thermoclass/analysis/Cas12a_1022_splits_mean_vs_per_token_averaged.tsv |\
	awk 'BEGIN{OFS="\t"; print "seq_id", "mean", "averaged_per_tok"}{ if(NR % 2 == 1) print $1, $2, $3}' |\
	sed 's/_1\t/\t/' > thermoclass/analysis/Cas12a_1022_splits_1_mean_vs_averaged_per_tok.tsv

tail -n +2 thermoclass/analysis/Cas12a_1022_splits_mean_vs_per_token_averaged.tsv |\
	awk 'BEGIN{OFS="\t"; print "seq_id", "mean", "averaged_per_tok"}{ if(NR % 2 == 0) print $1, $2, $3}' |\
	sed 's/_2\t/\t/' > thermoclass/analysis/Cas12a_1022_splits_2_mean_vs_averaged_per_tok.tsv

tail -n +2 thermoclass/analysis/Cas12b_1022_splits_mean_vs_per_token_averaged.tsv |\
	awk 'BEGIN{OFS="\t"; print "seq_id", "mean", "averaged_per_tok"}{ if(NR % 2 == 1) print $1, $2, $3}' |\
	sed 's/_1\t/\t/' > thermoclass/analysis/Cas12b_1022_splits_1_mean_vs_averaged_per_tok.tsv

tail -n +2 thermoclass/analysis/Cas12b_1022_splits_mean_vs_per_token_averaged.tsv |\
	awk 'BEGIN{OFS="\t"; print "seq_id", "mean", "averaged_per_tok"}{ if(NR % 2 == 0) print $1, $2, $3}' |\
	sed 's/_2\t/\t/' > thermoclass/analysis/Cas12b_1022_splits_2_mean_vs_averaged_per_tok.tsv

# Cas12a N

echo -e "seq_id\tN_mean\tsubseq_1_mean\tmean_delta" > thermoclass/analysis/Cas12a_N_vs_subseq_1_mean.tsv

./scripts/misc/merge_mean_per_tok.py thermoclass/predictions/TSV/Cas12a_N_mean.tsv 2\
	thermoclass/analysis/Cas12a_1022_splits_1_mean_vs_averaged_per_tok.tsv 1 >>\
	thermoclass/analysis/Cas12a_N_vs_subseq_1_mean.tsv

echo -e "seq_id\tN_averaged_per_tok\tsubseq_1_averaged_per_tok\tper_tok_delta" >\
	thermoclass/analysis/Cas12a_N_vs_subseq_1_per_tok.tsv

./scripts/misc/merge_mean_per_tok.py thermoclass/predictions/TSV/Cas12a_N_per_tok_averaged.tsv 1\
	thermoclass/analysis/Cas12a_1022_splits_1_mean_vs_averaged_per_tok.tsv 2 >>\
	thermoclass/analysis/Cas12a_N_vs_subseq_1_per_tok.tsv

paste thermoclass/analysis//Cas12a_N_vs_subseq_1_mean.tsv \
	thermoclass/analysis/Cas12a_N_vs_subseq_1_per_tok.tsv |\
	awk 'BEGIN{OFS="\t"}{print $1, $2, $3, $4, $6, $7, $8}' >\
	thermoclass/analysis/Cas12a_N_overlap_analysis.tsv

# Cas12a C

echo -e "seq_id\tC_mean\tsubseq_2_mean\tmean_delta" > thermoclass/analysis/Cas12a_C_vs_subseq_2_mean.tsv

./scripts/misc/merge_mean_per_tok.py thermoclass/predictions/TSV/Cas12a_C_mean.tsv 2\
	thermoclass/analysis/Cas12a_1022_splits_2_mean_vs_averaged_per_tok.tsv 1 >>\
	thermoclass/analysis/Cas12a_C_vs_subseq_2_mean.tsv

echo -e "seq_id\tC_averaged_per_tok\tsubseq_2_averaged_per_tok\tper_tok_delta" >\
	thermoclass/analysis/Cas12a_C_vs_subseq_2_per_tok.tsv

./scripts/misc/merge_mean_per_tok.py thermoclass/predictions/TSV/Cas12a_C_per_tok_averaged.tsv 1\
	thermoclass/analysis/Cas12a_1022_splits_2_mean_vs_averaged_per_tok.tsv 2 >>\
	thermoclass/analysis/Cas12a_C_vs_subseq_2_per_tok.tsv

paste thermoclass/analysis/Cas12a_C_vs_subseq_2_mean.tsv \
	thermoclass/analysis/Cas12a_C_vs_subseq_2_per_tok.tsv |\
	awk 'BEGIN{OFS="\t"}{print $1, $2, $3, $4, $6, $7, $8}' >\
	thermoclass/analysis/Cas12a_C_overlap_analysis.tsv

# Cas12b N

echo -e "seq_id\tN_mean\tsubseq_1_mean\tmean_delta" > thermoclass/analysis/Cas12b_N_vs_subseq_1_mean.tsv

./scripts/misc/merge_mean_per_tok.py thermoclass/predictions/TSV/Cas12b_N_mean.tsv 2\
	thermoclass/analysis/Cas12b_1022_splits_1_mean_vs_averaged_per_tok.tsv 1 >>\
	thermoclass/analysis/Cas12b_N_vs_subseq_1_mean.tsv

echo -e "seq_id\tN_averaged_per_tok\tsubseq_1_averaged_per_tok\tper_tok_delta" >\
	thermoclass/analysis/Cas12b_N_vs_subseq_1_per_tok.tsv

./scripts/misc/merge_mean_per_tok.py thermoclass/predictions/TSV/Cas12b_N_per_tok_averaged.tsv 1\
	thermoclass/analysis/Cas12b_1022_splits_1_mean_vs_averaged_per_tok.tsv 2 >>\
	thermoclass/analysis/Cas12b_N_vs_subseq_1_per_tok.tsv

paste thermoclass/analysis/Cas12b_N_vs_subseq_1_mean.tsv\
	thermoclass/analysis/Cas12b_N_vs_subseq_1_per_tok.tsv |\
	awk 'BEGIN{OFS="\t"}{print $1, $2, $3, $4, $6, $7, $8}' >\
	thermoclass/analysis/Cas12b_N_overlap_analysis.tsv

# Cas12b C

echo -e "seq_id\tC_mean\tsubseq_2_mean\tmean_delta" > thermoclass/analysis/Cas12b_C_vs_subseq_2_mean.tsv

./scripts/misc/merge_mean_per_tok.py thermoclass/predictions/TSV/Cas12b_C_mean.tsv 2\
	thermoclass/analysis/Cas12b_1022_splits_2_mean_vs_averaged_per_tok.tsv 1 >>\
	thermoclass/analysis/Cas12b_C_vs_subseq_2_mean.tsv

echo -e "seq_id\tC_averaged_per_tok\tsubseq_2_averaged_per_tok\tper_tok_delta" >\
	thermoclass/analysis/Cas12b_C_vs_subseq_2_per_tok.tsv

./scripts/misc/merge_mean_per_tok.py thermoclass/predictions/TSV/Cas12b_C_per_tok_averaged.tsv 1\
	thermoclass/analysis/Cas12b_1022_splits_2_mean_vs_averaged_per_tok.tsv 2 >>\
	thermoclass/analysis/Cas12b_C_vs_subseq_2_per_tok.tsv

paste thermoclass/analysis/Cas12b_C_vs_subseq_2_mean.tsv \
	thermoclass/analysis/Cas12b_C_vs_subseq_2_per_tok.tsv |\
	awk 'BEGIN{OFS="\t"}{print $1, $2, $3, $4, $6, $7, $8}' >\
	thermoclass/analysis/Cas12b_C_overlap_analysis.tsv

# Cleaning intermediary files

rm thermoclass/analysis/Cas12?_N_vs_*.tsv
rm thermoclass/analysis/Cas12?_C_vs_*.tsv
rm thermoclass/analysis/Cas12?_1022_splits_*.tsv
