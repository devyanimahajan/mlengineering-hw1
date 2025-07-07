# mlengineering-hw1

### Set up environment 
#### either use conda:
```bash
conda env create -f environment.yml
conda activate headline-env
```
#### or install with pip
```bash
pip install -r requirements.txt
```
in this case, make sure **rust is installed**

### Run Script
#### run as follows:
```bash
python score_headlines.py <input_file.txt> <source_name>
```
* <input_file.txt>: A text file containing one headline per line
* <source_name>: A short identifier like nyt or chicagotribune
#### example:
```bash
python score_headlines.py headlines_nyt_2024-12-02.txt nyt
```


