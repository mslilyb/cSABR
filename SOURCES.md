# Links to all Alignment Program Source Code or Binaries

## Binaries:

* [bbmap](https://sourceforge.net/projects/bbmap/) (done with binary)
* [bowtie2](https://bowtie-bio.sourceforge.net/bowtie2/index.shtml) (also has src AND singularity containers)
* [bowtie2 containers](https://biocontainers.pro/tools/bowtie2)

## Source Code
* [bwa](https://github.com/lh3/bwa) (skip?)
* [gem3-mapper](https://github.com/smarco/gem3-mapper) (done)
* [gmap](http://research-pub.gene.com/gmap/src/gmap-gsnap-2024-11-20.tar.gz) (done)
* [hisat2](https://daehwankimlab.github.io/hisat2/download/) (done)
* [magicblast](https://ncbi.github.io/magicblast/doc/download.html) (has a docker image!) (done, but only on x86)
* [minimap2](https://github.com/lh3/minimap2) (done)
* [pblat](https://github.com/icebert/pblat) (done (i think))
* [segemehl](http://legacy.bioinf.uni-leipzig.de/Software/segemehl/) (check install notes) (done)
* [star](https://github.com/alexdobin/STAR) (also has binaries) (done)
* [subread](https://sourceforge.net/projects/subread/files/subread-2.0.8/) (installation guide is 404, will have to feel it out)
* [tophat](https://ccb.jhu.edu/software/tophat/index.shtml) (src and binaries)

### Install notes.
 
segemehl: has dependencies on `hstlib`, and may also require `hts-devel`. Also may need to export the `pkg-config` path manually:

```bash
export PKG_CONFIG_PATH=<path-to-pkg-config-configuration-files>
```
