# HDT-ViewMat

This is the official repository storing the implementation of the paper: "Efficient Privacy-Preserving Human Digital Twin Views Pre-Materialisation".

```
@inproceedings{sirigu2024human,
  title={Human Digital Twins: Efficient Privacy-Preserving Access Control Through Views Pre-materialisation},
  author={Sirigu, Giorgia and Carminati, Barbara and Ferrari, Elena},
  booktitle={IFIP Annual Conference on Data and Applications Security and Privacy},
  pages={24--43},
  year={2024},
  organization={Springer}
}
}
```

## Requirements
- Python 3.10+[^1]
- Python libraries:
  - treelib
  - lxml
  - termcolor
  - nompy
  - xlexwriter

## Run the System
1. Uncomment the lines in the `userSimulatorRandom.py` file from `408` to `1484` of the processes of interest to test.
2. Run file `userSimulatorRandom.py`

## Results
Results are organised in _.xlsx_ files generated in the main directory.
Results of the single processes are stored within the `results` folder

[^1]: https://www.python.org/
