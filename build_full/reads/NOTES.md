# Notes for SABR analysis.

## 1. Raw Accuracy
Reads were aligned and generated using the following command:

```bash
./pb2 data.ln/ce01.f* build_full -fs1
```

Results:
|-------------------|--------------|
| Program | Accuracy |
| hisat2_reads | 0.9377315223 |
|STAR_reads | 0.9192120582 |
| segemehl_reads | 0.9082359276 |
| pblat_reads | 0.8765980262 |
| minimap2_reads | 0.8599562719 |
| magicblast_reads | 0.8526891404 |
| bowtie2_reads | 0.6378457168 |
| bbmap_reads | 0.6378178645 |
| gem3-mapper_reads | 0.6378178645 |
| subread_reads | 0.6377691229 |
|-------------------|--------------|
