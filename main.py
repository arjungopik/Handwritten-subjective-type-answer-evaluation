import subprocess

def execute_program1():
    subprocess.run(["venv38/Scripts/python.exe", "application.py"], check=True)

def execute_program2():
    subprocess.run(["venv312/Scripts/python.exe", "gemini.py"], check=True)
    subprocess.run(["venv312/Scripts/python.exe", "simcheck.py"], check=True)

if __name__ == "__main__":
    execute_program1()
    execute_program2()
