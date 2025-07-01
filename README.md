# Apollo

Apollo is a problem solver, tool tester, and study platform where I experiment with code and add tools that might help me on a daily basis.

---

> [!Warning]
> ***This is an experimental tool. Use at your own risk.***

## Installation
```sh
# Install apollo
pip install git+https://github.com/daniloptrial/apollo.git

# Try it out
apollo --version
```

## Help
```sh
# For more information run
apollo --help
```

## Configuration
The current configuration file only specifies the output path for downloaded files. To set it correctly, use:
```sh
apollo config --set download-output-path /your/path/here

# check if everything is ok with:
apollo config --show
```

## Try it out
```sh
# If you have an webcam, run:
apollo webcam --shade solid
```
```sh
# Want to watch an youtube video on your terminal?
apollo play https://www.youtube.com/watch?v=dQw4w9WgXcQ --shade solid -d
```
```sh
# Download an youtube video
apollo download https://www.youtube.com/watch?v=dQw4w9WgXcQ --res best -o
```
