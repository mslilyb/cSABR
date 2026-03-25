1. Sanity checks:
	- are the strands matching?
	- are the names right?
	- did it make up any transcripts?
	- did it managed ungapped alignments right?


2. Splice Detection (Gapped Alignmnents) (Case where coordinates are approx match, missing small overhang)
	- EX: alignment running from 100-200,240-300
		3' Overhang:
		- Gene: 5'~~~~~~~~[Exon]~~~~~~[Exon]~~~~~~~~~~~~~~~~~~~~~~~~~~~
			Tx: 5'        ------      --
		5' Overhang:
		- Gene: 5'~~~~~~~~[Exon]~~~~~~[Exon]~~~~~~~~~~~~~~~~~~~~~~~~~~~
			Tx: 5'             -      -----

	- DO WE DETECT SPLICES? (i.e., does the program make gapped alignments?)
		- What is the average amount of 'overhang'in a gapped alignment?
		- Does the program always detect the same splices given the same data?
		- Is there a strand or polarity bias?
		- First Graph: Accuracy Vs Overhang (Gapped Alignment Happened vs Amount of Overhang)
		- Very Qualitative: DID i make a gapped alignment
		- How much overhang do you allow before it's just WRONG?

3. Splice Accuracy
	- HOW far off is a program from the ground truth?
		- Second Graph: Hallucination vs Overhang (Quality of Alignment Vs Overhang)
		- Very Quantitative: WHAT does this gapped alignment look like and was it a good one
		- Some More Questions:
				- How much does a program need to make a gapped alignment?
				- How big can an internal exon be before its two alignments? Before it's detected?
				- Does NT comp affect splice detection?
				- For programs that usually miss, what causes a hit and vice versa?
				- Synthetic Genomes and how they affect results.
				- Is there strand or polarity bias

4. FTX handling overhaul
	- Refactor code and redesign output for long term useability
		- Namely: Separating FTX files to be single only means they are easier to handle long term (i.e.: instead of each `<progname>.ftx.gz` having two columns, one for the ground truth and one for the output, create a `groundtruth.ftx.gz` and `<progname>.ftx.gz`.)
			- This is for the sake of saving space by cutting redundant information, as well as allowing for a more modular and nimble analysis pipline down the road
