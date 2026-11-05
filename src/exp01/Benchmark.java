/* Benchmark.java:
1- runs all three given algorithms and generates equivalent inputs for each one
2- warms JVM up
3- randomizes order of algorithms
4- measures sorting operation
5- checks is output sorted?
6- save measurement into CSV file */

package exp01;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;
import java.util.function.Supplier;

public class Benchmark {
    private static final int[] ARRAY_SIZES = {100, 500, 1000, 2000, 5000};
    private static final String[] INPUT_TYPES = {"RANDOM", "SORTED", "REVERSE", "NEARLY_SORTED"};

    private static final int REPETITIONS = 30;
    private static final int WARMUP_ROUNDS = 10;
    private static final long BASE_SEED = 20261105L;

    private static class Algorithm {
        String name;
        Supplier<Sorter<Integer>> factory;

        Algorithm(String name, Supplier<Sorter<Integer>> factory) {
            this.name = name;
            this.factory = factory;
        }
    }

    private static final List<Algorithm> ALGORITHMS = new ArrayList<>();
    static {
        ALGORITHMS.add(new Algorithm("BubbleSortPassPerItem", BubbleSortPassPerItem::new));
        ALGORITHMS.add(new Algorithm("BubbleSortUntilNoChange", BubbleSortUntilNoChange::new));
        ALGORITHMS.add(new Algorithm("BubbleSortWhileNeeded", BubbleSortWhileNeeded::new));
    }

    public static void main(String[] args) throws IOException {
        File resultsFolder = new File("results");
        resultsFolder.mkdirs();
        File csvFile = new File(resultsFolder, "raw-data.csv");

        try (FileWriter writer = new FileWriter(csvFile)) {
            writer.write("Algorithm , Size of Array , Input Type , Repetition , Time in ns\n");
            warmUp();

            for (int size : ARRAY_SIZES) {
                for (String inputType : INPUT_TYPES) {
                    System.out.println("Running size=" + size + ", input=" + inputType);

                    for (int repetition = 1; repetition <= REPETITIONS; repetition++) {
                        long seed = BASE_SEED + size * 1000L + inputType.hashCode() * 10L + repetition;
                        Integer[] original = DataGenerator.generate(size, inputType, seed);
                        List<Algorithm> executionOrder = new ArrayList<>(ALGORITHMS);
                        Collections.shuffle(executionOrder, new Random(seed));

                        for (Algorithm algorithm : executionOrder) {
                            Integer[] items = original.clone();
                            Sorter<Integer> sorter = algorithm.factory.get();

                            // timing measures only sorter.sort(items)
                            long start = System.nanoTime();
                            sorter.sort(items);
                            long end = System.nanoTime();
                            long elapsed = end - start;

                            if (!DataGenerator.isSorted(items)) {
                                throw new IllegalStateException("Algorithm" + algorithm.name + " failed to sort given array");
                            }

                            writer.write(algorithm.name + "," + size + "," + inputType + "," + repetition + "," + elapsed + "\n");
                        }
                        writer.flush();
                    }
                }
            }
        }
        System.out.println("Benchmark completed");
        System.out.println("Results saved in results/raw-data.csv");
    }

    private static void warmUp() {
        System.out.println("Warming up JVM...");
        for (Algorithm algorithm : ALGORITHMS) {
            for (int i = 0; i < WARMUP_ROUNDS; i++) {
                Integer[] items = DataGenerator.generate(500, "RANDOM", BASE_SEED + i);
                Sorter<Integer> sorter = algorithm.factory.get();
                sorter.sort(items);

                if (!DataGenerator.isSorted(items)) {
                    throw new IllegalStateException("Warm up sorting failed: " + algorithm.name);
                }
            }
        }
        System.out.println("Warm up completed");
    }
}
