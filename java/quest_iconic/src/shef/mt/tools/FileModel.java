/**
 *
 */
package shef.mt.tools;

import shef.mt.util.Logger;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.*;

import shef.mt.features.util.StringOperations;

/**
 * A FileModel contains information about the input text: the words contained
 * and their frequency in the reference corpus It registers 2 resources: "words"
 * and "freq", required by BB features 20-29
 *
 * @author Catalina Hallett
 *
 */
public class FileModel {

    private static HashMap<String, Integer> words;
    private static int wordCount;

    public FileModel(String sourceCorpus) {
        Logger.log("Building the word model for the input file");
        System.out.println("Building the input file model");
        long start = System.currentTimeMillis();
        //System.out.println(inFile+"  "+sourceCorpus);
        words = new HashMap<String, Integer>();

        try {
            String wordsSplit[];
            BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(sourceCorpus), "utf-8"));
            String line = br.readLine();
            while (line != null) {
                wordsSplit = line.split(" ");

                for (String word : wordsSplit) {
                    if (words.containsKey(word)) {
                        words.put(word, words.get(word) + 1);
                    }else{
                        words.put(word, 1);
                    }
                }
                line = br.readLine();
            }
            br.close();
            ResourceManager.registerResource("Freq");
        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println("Input file model built!");
    }

    public static Set getWords() {
        return words.keySet();
    }

    public static boolean containsWord(String word) {
        return words.containsKey(word);
    }

    public static int getFrequency(String word) {
        if (!words.containsKey(word)) {
            return -1;
        }
        return words.get(word);
    }

    public static void print() {
        Iterator<String> it = words.keySet().iterator();
        String word;
        while (it.hasNext()) {
            word = it.next();
            System.out.println(word + "\t" + words.get(word));
        }
    }
}