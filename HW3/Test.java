import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.StringTokenizer;
import java.util.Arrays;

public class Test {

    public static void main(String[] args) {
        String inputFilePath = "in/devdata/5722018235.txt";    // Input file path
        String outputFilePath = "test_output.txt";  // Output file path
        String[] bigrams = {"computer science", "information retrieval", "power politics", "los angeles", "bruce willis"};

        BufferedReader br = null;
        BufferedWriter bw = null;

        try {
            br = new BufferedReader(new FileReader(inputFilePath));
            bw = new BufferedWriter(new FileWriter(outputFilePath));
            String value;

            // Read each line in the file
            while ((value = br.readLine()) != null) {
                String[] parts = value.toLowerCase().split("\t", 2);

                // Check if split worked correctly
                if (parts.length < 2) {
                    bw.write("Input format error: Tab-separated value required.\n");
                    continue;
                }

                // Clean line to keep only lowercase letters, replace others with spaces
                String cleanedLine = parts[1].replaceAll("[^a-z]+", " ").trim();

                // Tokenize based on whitespace
                StringTokenizer itr = new StringTokenizer(cleanedLine, " ");

                while (itr.hasMoreTokens()) {
                    String word = itr.nextToken();
                    if (itr.hasMoreTokens()) {
                        String word2 = itr.nextToken();
                        String combine = word.trim() + " " + word2.trim();
                        bw.write(combine + "\n");

                        // Check if the combined bigram is in the array
                        if (Arrays.asList(bigrams).contains(combine)) {
                            // bw.write("Bigram found: " + combine + " with ID " + parts[0] + "\n");
                            // bw.write(combine + "\n");
                        }
                    }
                }
            }

            System.out.println("Processing complete. Check output.txt for results.");

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if (br != null) {
                    br.close();
                }
                if (bw != null) {
                    bw.close();
                }
            } catch (IOException ex) {
                ex.printStackTrace();
            }
        }
    }
}
