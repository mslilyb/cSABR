# cSABR
messing around with container implementations of common read alignment programs!

## Repo Map:
- `bakeoff`: unaltered SABR bakeoff script. WIP.
- `deffiles`: recipes for building Singularity Containers. See [Building a Singularity Image](#building-a-singularity-image)
- `input`: intermediate files captured from `bakeoff` script that are used as inputs in the pipeline for alignment programs. Obtained using the `-d` flag. Must be unzipped before usage.
- `src`: WIP sourcecode for `bakeoff`. Integrating containers is WIP. Most untouched.


## Building a Singularity Image from a Definition File

As a note, all `.def` files found in the `deffiles/` directory will require the end user to make edits according to their home system. Fields requiring user input are flanked/defined in the following format `<INSTRUCTIONS>`. Building an image will require either the source code or a binary of a desired alignment program.

Building a singularity image requires either `sudo` permissions or the usage of the `--fakeroot` flag. The command in general looks like this:

If `sudo`:
```bash
sudo singularity build desired_title_for_image.sif /path/to/definition/file.def
```

If not:
```bash
singularity build --fakeroot desired_title_for_image.sif /path/to/definition/file.def
```

For more details on definition files, including on how to make one, see the [official Singularity Documentation](https://docs.sylabs.io/guides/latest/user-guide/definition_files.html).

## Running a Singularity Image

Singularity containers can be run with `singularity run`, invoked on the command line almost the same as you would the program itself.

```bash
singularity [options] run your_container_image.sif <normal CLI for alignment program here>
```

As you can see, other than invoking the image, the rest of the command is the same, allowing all the same flags, arguments, and options as normal. However, there are a few important considerations to take when running a singularity container:

* Paths to files on the host system must be absolute (unknown if can be fixed? changed?)
* Singularity containers cannot write files on the host system by default. This behavior can be enabled by binding a directory. See below.

### Binding Host System Directories.

Binding a directory allows your singularity container to read and write in a specific directory, essentially treating it as part of the container. Binding is enabled using the `--bind` or `-B` flags. The format of the argument is `/host:/container`, where `/host` is the absolute path to the desired directory on the host system, and `/container` is some path in the container. This path doesn't need to exist already. Convention is to use `/mnt` as the container directory.

```bash
singularity run --bind /path/to/hostdir:/mnt your_container_image.sif <normal CLI for alignment program here>
```

Note: Fairly certain that your container will inherit read/write perms on all child directories to mount point. Use with care.

## Misc

- As of right now, I am working on being able to seamlessly incorporate container versions of aligners into the pipeline (hence copying over `src` from SABR)
- Still need to determine if best practice is to distribute recipes or full images (latter supported, is it tractable?)
	- Full containers are available on the ContainerLibrary, which is encouraging for the purposes of replication.

- python tool `spython`, developed by the SingularityCE devs, can be used to automatically convert a dockerfile into a Singularity Definiton File. 
```bash
pip install spython
```

- When comparing outputs between containers and SABR, try to ensure that your files are in the same format/orientation. There is an amount of beautification that occurs during the pipeline, which can make it seem like you're completely wrong.

- Containers hosted on repos like [Biocontainers](https://biocontainers.pro/) **can be run without downloading**, which while requiring a network connection is promising for the purposes of distribution. 

## Progress

- The `pblat` container works, and produces the same output as the SABR blat (i.e. conda pblat)!

## Next Steps

- Use `pblat` to begin exploring container performance compared to conda. Evaluate following cases:
	- Multiple threads, conda vs container
	- switch to Alpine Linux (needed?), conda vs. container
	- compile on ARM, conda vs. container vs. x86 etc etc.

- develop deffiles for all other alignment programs.
- `run-aligner.py` needs a way to pass in host bind directories if I'm automating containers. Add argparse? Alter bakeoff too? Could just bind `bakeoff` location, but not certain that's wise.