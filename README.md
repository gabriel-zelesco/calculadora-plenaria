# calculadora-plenaria

This calculator determines the number of seats allocated in electoral processes using Largest Remainder Method as the distribution criterion and the D'Hondt Method to determine the order of calling.
This is the most commonly used model in electoral processes for workers' unions and student unions.

This calculator was developed using the Kivy framework and can be used on Android devices.

## Usage

The script is written in python 3.9. It uses the following external libraries:

- kivy
- buildozer

## Installation
For convenience, there is a environment file that can be used to create a conda environment with the required libraries. To use it, run the following command:
```bash
conda env create -f environment.yml
```
## Making an Android App from the script
We use Buildozer to compile the app. Unfortunately, this library only runs in a Linux environment. If you are a Windows user, you can use WSL (Windows Subsystem for Linux) to emulate Linux and run Buildozer.

## License
[MIT](https://choosealicense.com/licenses/mit/)
