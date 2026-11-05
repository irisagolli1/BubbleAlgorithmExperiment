/* This class creates all data sets for the experiments and saves them into the data folder. */
package exp01;
import java.util.Random;

public final class DataGenerator {
    private DataGenerator() {}
    public static Integer[] generate(int size, String inputType, long seed) {
        Integer[] items = new Integer[size];
        Random random = new Random(seed);
        switch (inputType) {

            case "RANDOM": // CASE 1: Elements sorted in random order
                for (int i = 0; i < size; i++) {
                    items[i] = random.nextInt(100001);
                }
                break;

            case "SORTED": // CASE 2: Elements already in ascending order
                for (int i = 0; i < size; i++) {
                    items[i] = i;
                }
                break;

            case "REVERSE": // CASE 3: Elements already in descending order
                for (int i = 0; i < size; i++) {
                    items[i] = size - i;
                }
                break;

            case "NEARLY_SORTED": //CASE 4: Elements begin in ascending order, with a small number of randomly selected swaps / not propely sorted
                for (int i = 0; i < size; i++) {
                    items[i] = i;
                }
                int swaps = size / 100;
                if (size > 1 && swaps == 0) {
                    swaps = 1;
                }
                for (int i = 0; i < swaps; i++) {
                    int first = random.nextInt(size);
                    int second = random.nextInt(size);
                    Integer temp = items[first];
                    items[first] = items[second];
                    items[second] = temp;
                }
                break;

            default:
                throw new IllegalArgumentException("Input type: " + inputType + " is unknown.");
        }
        return items;
    }

    public static boolean isSorted(Integer[] items) { // Checking if the items in the array are sorted. If so -> true, otherwise false
        for (int i = 1; i < items.length; i++) {
            if (items[i - 1] > items[i]) {
                return false;
            }
        }
        return true;
    }
}
