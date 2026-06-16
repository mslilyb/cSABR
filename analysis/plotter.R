require(float)
programs <- c("STAR", "bbmap", "gem3-mapper", "hisat2", "minimap2", "bowtie2", "magicblast", "pblat", "segemehl", "subread")
precisions <- runif(100, min = 0, max = 1)
mylist <- list()


matr <- flrunif(100, n = length(programs), min = 0, max = 1)
#p <- ggplot(prec, aes(programs, precisions))

df <- data.frame(matr)