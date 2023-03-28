import subprocess


def run_pylint(file_name):
    result = subprocess.run(["pylint", "--max-line-length=150","--disable=E0611,C0116", file_name], capture_output=True, text=True)
    print(result.stdout)


if __name__ == "__main__":
    run_pylint("C:\\Users\\henrychen\\Documents\\gitlab\\metis\\autoscript_kernel\\metis.py")