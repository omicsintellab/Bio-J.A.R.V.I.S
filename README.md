# BIO - J.A.R.V.I.S 

BIO - J.A.R.V.I.S (Just an Artificial Reasoning and Very Interpretative System) is a tool to generate clinical records as simple as breath.

***Main Script***:
___
**```bio_jarvis.py```** - Run all the script.

## Reference and citation
> In Progress

## Change Log
**BIO - J.A.R.V.I.S version 1.0 - December 2025**

- Bugs ou others suggestions for improvement, just let me know: deyvid.amgarten@usp.br

## Dependecies
All scripts from this project were coded in [Python 3](https://www.python.org/downloads/). So, first of all, make sure you have it installed and updated.

**Theses Python libraries are required:**
- [ETE4 Toolkit](https://jorgebotas.github.io/ete4-documentation/)
- [Bio Python (Entrez module)](https://biopython.org/docs/1.76/api/Bio.Entrez.html)
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Python-dotenv](https://pypi.org/project/python-dotenv/)
- [Pandas](https://pandas.pydata.org/)

### Before intalling anything

Since this project uses AWS API to conncet to Bedrocks services, It's necessary to start a **virtual enviroment (venv)** to avoid any problems.
After cloning this repository, open the directory and run:

```
python3 -m venv venv # This will create virtual enviroment
```

Then, start the venv:
```
source venv/bin/activate
```

Since venv is active, It should show something like this in terminal:
```
(venv) your@user Bio-J.A.R.V.I.S % 
```

Now, to install all the required libraries, run:

```
pip3 install -r requirements.txt
```

> 💡 BIO-J.A.R.V.I.S requires an unix O.S (any Linux distro or MacOs) to run some libraries and modules, make sure You're using one.

### AWS Settings
To finally run **BIO-J.A.R.V.I.S**, You must creat a file called **.env** and the paste Your AWS credentials:

```
AWS_ACCESS_KEY_ID="..."
AWS_SECRET_ACCESS_KEY="..."
AWS_SESSION_TOKEN="..."
```
If **there's not an** **AWS_SESSION_TOKEN="..."**, You must paste only what It shows to and comment **line 18** from **aws_handler.py** 
```            
aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
```

## Quick Start
Inside the directory where BIO-J.A.R.V.I.S was extracted (or cloned), You're gonna need to start the virtual enviroment:

```
python3 venv/bin/activate
```

Now, just start having fun:
```
python3 bio_jarvis.py -tx 2697049
```
To run using TaxID, use -tx param and type (or paste) after. But, if You want to run using organim name, use this:

```
python3 bio_jarvis.py -n "Severe acute respiratory syndrome coronavirus 2"
```
> ⚠️ Make sure the name You did type (or paste) is correct.

## Author
[Gustavo Bezerra](https://github.com/BizerraGuU)

This tool was developed as part of my undergraduate research project conducted at the Albert Einstein Israelite Faculty of Health Sciences, São Paulo, Brazil.

## License
> In Progress