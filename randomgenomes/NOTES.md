# Notes on Random Builds

All builds completed with 10 chromosomes and the --double flag enabled.

## Fixed seed, variable length

Using seed = 1, genomes with internal exons that had a max length of 50, 100, 150, and 200.


## Fixed length, variable seedd

Using a fixed length of 50 for internal exons, tested effects of random genome on aligner performance

## Fixed length, fixed seed, noncanonical sites

Seed = 1, mexon_len = 50


```bash
# saving this for posterity
for dir in `ls -A .`; do mkdir -p `pwd`/$dir/reads/double `pwd`/$dir/reads/plus `pwd`/$dir/reads/minus; python3 ../../build_full/ftxparse.py ./$dir/build/ double; mv *.tsv ./$dir/reads/double/; python3 ../../build_full/ftxparse.py ./dir/$build/ +; mv *.tsv ./$dir/reads/plus; python3 ../../build_full/ftxparse.py ./$dir/build/ -; mv *.tsv ./$dir/reads/minus; done

# Lmao
```

```bash
#oh it got worse
for dir in `ls -A .`; do for sdir in `ls -A ./$dir/reads`; do mkdir -p ./$dir/reads/$sdir/results; for file in `find ./$dir/reads/$sdir -maxdepth 1 -type f`; do python3 ../../build_full/reads/accfinder.py $file ./$dir/reads/$sdir/ > ./$dir/reads/$sdir/results/`echo $file | cut -f1 -d '_'`.results ; done; done; done;
```
