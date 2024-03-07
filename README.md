# HDT-ViewMat

This is the official repository storing the implementation of the paper: "Efficient Privacy-Preserving Human Digital Twin Views Pre-Materialisation". (add doi to paper)

```
@inproceegings{conpref,
 title = {Efficient Privacy-Preserving Human Digital Twin Views Pre-Materialisation},
 author={Sirigu, Giorgia and Carminati, Barbara and Ferrari, Elena},
....
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
1. Unfold `bpel/Dataset/BPEL/Dataset178.zip`
2. Unfold `bpel/Dataset/BPEL/Realistic.zip`
3. Uncomment the lines in the `userSimulatorRandom.py` file from `408` to `1484` of the processes of interest to test.
4. Run file `userSimulatorRandom.py`

## Results
Results are organised in _.xlsx_ files generated in the main directory.
Results of the single processes are stored within `results` folder

[^1]: https://www.python.org/
