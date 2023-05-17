from pathlib import Path


def root_path(*paths) -> Path:
	return Path(__file__).parent.parent.joinpath(*paths)
