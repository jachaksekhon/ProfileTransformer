# ProfileTransformer

ProfileTransformer is a small CLI tool that helps users transfer profile information from one bot to another by converting profiles through a shared canonical format.

🛑 **Disclaimer:**  
This program may process sensitive data (such as addresses and payment information).

ProfileTransformer **_does not store any data_**, it only reads input files, transforms them in memory, and writes the converted output locally.

---

## Setup

### 1. Install Python

- Python **3.9 or higher** is required
- No external dependencies are needed

You can download any stable version here:

[Python For Windows](https://www.python.org/downloads/windows/)
[Python For Mac](https://www.python.org/downloads/macos/)

Verify your Python version:
```bash
python --version
```

### Navigate to the project directory (for CLI)

Before running the program, make sure you are inside the project folder.

Using your terminal or command prompt, navigate to the project root:

```bash
cd /your/path/here/ProfileTransformer
```

### 2. Prepare input file

Create an input file in the `project root`, depending on the source bot:

#### Converting from Stellar

Create a file named:
```text
stellarprofiles.json
```

#### Converting from Valor

Create a file named:
```text
valorprofiles.json
```

#### Converting from Cybersole

Create a file named:
```text
cybersoleprofiles.json
```

Paste your exported Stellar or Valor input into this file.

### 3. Run the program

You can run the ProfileTransfer using either the command line or a configuration file.

#### Option A: Using the command line


```bash
example:

python convert.py --from stellar --to valor
python convert.py --from valor --to cybersole
```

#### Option B: Without using the command line (Windows friendly)
1. Open the config.json file
2. Set the `from` and `to` fields to what you need
- Currently supporting: 
```
`Stellar -> Valor`
`Stellar -> Cybersole`,
`Valor -> Stellar`,
`Valor -> CyberSole`
`CyberSole -> Stellar`
`CyberSole -> Valor`
```
3. Double-click `convert.py`

Example:
```json
{
  "from": "stellar",
  "to": "valor"
}
```

### 4. Collect your results
An output file will be auto-generated and placed into the root of the project directory.

You can import this file directly into the bot it was made to be imported to!

---

## Feedback

If something doesn’t work as expected or you’d like to see support for another bot, feel free to open an issue or share your thoughts.

Suggestions and improvements are always welcome.
