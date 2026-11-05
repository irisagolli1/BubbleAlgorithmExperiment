# Experimental Design

## 1. Research Objective
Our objective for this experiment is comparing the execution time of three different implementations of the Bubble Sort algorithm:
- BubbleSortUntilNoChange
- BubbleSortWhileNeeded
- BubbleSortPassPerItem
This experiment will determine if these algorithms execution times differ under the experimental conditions (defined below).

## 2. Research Question
How does the choice of Bubble Sort implementation affect execution time for different input sizes and initial input arrangements?

## 3. Hypothesis
Hypothesis are predictions -> the final result may or may not support them. They will be evaluated using measurements that are collected in the experiment.

- **H1:** Under the same conditions, the three Bubble sort algorithms will have different execution times  
- **H2:** BubbleSortPassPerItem will be slower because it performs a specific number of passes, even if array is sorted.  
- **H3:** BuubleSortUntilNoChange and BubbleSortWhileNeeded will perform better on sorted and nearly sorted arrays compared to the others because they can stop when they see that there is a need for more swaps.  
- **H4:** Execution time will increase as input size decreases.

## 4. Variables
Variables are categorized in: Independent, Dependent and Controlled Variables.

### a. Independent Variables
1. **Algorithm:** the given Bubble Sort implementations (BubbleSortUntilNoChange, BubbleSortWhileNeeded and BubbleSortPassPerItem)
2. **Input size:** number of elements in the array
3. **Initial input arrangement:** order of elements before sorting

### b. Dependent Variable
Execution time that is measured in nanoseconds (ns)

### c. Controlled Variables
These conditions will be kept consistent:
- Programming language and Java version
- Data type and value range
- JVM configuration
- Timing method
- Input arrays supplied to each algorithm
- Warm-up and measurement procedure

## 5. Experimental Conditions
Input sizes: 100, 500, 1000, 2000 and 5000 elements

Input Arrangements:
- **Random:** elements generated in random order
- **Sorted:** elements already in ascending order (from lowest to highest value element)
- **Reverse sorted:** elements in descending order (from highest to lowest value element)
- **Nearly sorted:** start with a sorted array and perform a certain number of random swaps

Algorithms will get equivalent copies of the same original input for each experimental repetition.

## 6. Repetitions
Plan is to perform 30 timed repetitions for each combination of algorithm, input size and input arrangement.
We will use a preliminary pilot experiment, to check if the proposed settings produce reliable and practical measurements.

## 7. Measurement Procedure
Execution time is measured using the Java's System.nanoTime() method.
Outside the timed section: array generation, copying, correctness checks, console output and file writing.
JVM will be warmed up before collection of measurements.
The order in which algorithms are measured will vary to reduce systematic ordering effects.

## 8. Correctness
Before performance measurements, we will test each algorithm to verify that it correctly sorts the input.

## 9. Data Collection
All timing measurements will be stored in a CSV file, together with other details such as: the algorithm name, input size, input type, repetition number and time (in ns).

The experiment will document: computer specifications, Java version, JVM settings, random seeds, input-generation procedure and measurement procedure.