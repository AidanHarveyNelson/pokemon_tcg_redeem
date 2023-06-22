## About the Project

If you are sick of having to enter the Pokemon TCG codes one by one or scanning the QR codes one by one this tool is for you. By providing it a list of codes or a file containing the codes it will automatically login to the Pokemon TCG website and redeem the codes for your account.

### Prerequisites

- Python v3.8
- Pipenv https://pypi.org/project/pipenv/
- Chrome Browser

### Setting up Environment

Assuming the above prerequisites have been installed already the following command will build a virtual environment. Run the below command from within this folder.

```
pipenv install 
```

### Running this Project

Currently this script supports either passing the codes in the command line with the `-c`/`--codes` or with the `-f`/`--file` parameters. I have included an example of both these commands below.

#### Running using a File

```
pipenv run main.py <username> <password> -f codes.txt
```

#### Running use Codes

```
pipenv run main.py <username> <password> -c 276-BLW2-ZVD-ZD6 2BH-L9RG-TGV-2G6 277-42NM-Y92-MCJ
```

### File Format

If using the File argument then save a txt file with the pokemon codes in the following structure. I have included a `codes.txt` file to provide an example of how the codes should be stored in the file.

```
276-BLW2-ZVD-ZD6
277-42NM-Y92-MCJ
2BH-L9RG-TGV-2G6
```
