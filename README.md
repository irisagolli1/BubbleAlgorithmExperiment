# Bubble Sort Experiment

## Project Objective
This project compares the execution time of three Bubble Sort implementations:
- BubbleSortPassPerItem
- BubbleSortUntilNoChange
- BubbleSortWhileNeeded

## Requirements
- Java JDK installed
- Terminal / Java-compatible IDE

## Project Structure
 `src/exp01/`  -    Java source files
 `results/`    -    Raw experimental data
 `report/`     -    Experimental design and report

## Compilation
From the project root directory, run: 
**javac -d out src/exp01/*.java**

## Execution
Run the benchmark using:
**java -cp out exp01.Benchmark**

## Results
The benchmark saves raw execution-time measurements to CSV file:
**results/raw-data.csv**

## Measurement Procedure
- Execution time is measured using `System.nanoTime()`.
- Array generation & copy happen outside of timed section.
- Each algorithm receives a copy of the same original input.
- The JVM is warmed up before measurements.
- Algorithm execution order is randomized.

The input generator uses fixed seeds from the array size, input type and repetition number. 