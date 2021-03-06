/*===========================================================================
 Copyright (C) 2014 by the Okapi Framework contributors
 -----------------------------------------------------------------------------
 This library is free software; you can redistribute it and/or modify it 
 under the terms of the GNU Lesser General Public License as published by 
 the Free Software Foundation; either version 2.1 of the License, or (at 
 your option) any later version.

 This library is distributed in the hope that it will be useful, but 
 WITHOUT ANY WARRANTY; without even the implied warranty of 
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser 
 General Public License for more details.

 You should have received a copy of the GNU Lesser General Public License 
 along with this library; if not, write to the Free Software Foundation, 
 Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

 See also the full LGPL text here: http://www.gnu.org/copyleft/lesser.html
 ===========================================================================*/
package quest;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.StringTokenizer;
import java.util.Vector;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import libsvm.svm;
import libsvm.svm_model;
import libsvm.svm_node;
import libsvm.svm_problem;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;
import routines.svm_scale;
import shef.mt.features.util.FeatureManager;
import shef.mt.features.util.Sentence;
import shef.mt.tools.FileModelOriginal;
import shef.mt.tools.Giza;
import shef.mt.tools.LanguageModel;
import shef.mt.tools.NGramProcessor;
import shef.mt.tools.ResourceManager;
import shef.mt.util.PropertiesManager;

public class QuestProcessor {

    private String input;
    private String output;
    private String sourceFile;
    private String targetFile;
    private String sourceLang;
    private String targetLang;
    private NodeList featureList;
    private Document xmlReader;
    private PropertiesManager resourceManager;
    private FeatureManager featureManager;
    private svm_model predictionModel;
    private double minScore;
    private double maxScore;

    /**
     * Creates a QuEstProcessor instance.
     *
     * @param tempFolder Folder in which to save temporary files.
     * @param featuresFile XML file with the features to be calculated.
     * @param gizaFile Translation probabilities file.
     * @param sourceNGram N-gram counts file.
     * @param sourceCorpus Source language corpus.
     * @param targetCorpus Target language corpus.
     * @param modelPath Path in which to save the trained model.
     * @param sourceLanguage Source language.
     * @param targetLanguage Target language.
     */
    public QuestProcessor(String tempFolder, String featuresFile, String gizaFile,
            String sourceNGram, String sourceCorpus, String targetCorpus, String modelPath, String sourceLanguage, String targetLanguage) {

        sourceLang = sourceLanguage;
        targetLang = targetLanguage;

        // Make sure the temporary input folder exists.
        File tmpDir = new File(tempFolder);
        tmpDir.mkdirs();

        //Read parameters adequatly.
        parseArguments(tempFolder, featuresFile, gizaFile, sourceNGram, sourceCorpus, targetCorpus, modelPath);
        input = resourceManager.getString("input");

        //Read features' XML file.
        featureList = null;
        try {
            xmlReader = DocumentBuilderFactory.newInstance()
                    .newDocumentBuilder().parse(featuresFile);
            featureList = xmlReader.getElementsByTagName("feature");
        } catch (SAXException | IOException | ParserConfigurationException e) {
            e.printStackTrace();
        }

        //Load model:
        try {
            predictionModel = svm.svm_load_model(modelPath);
        } catch (IOException ex) {
            System.out.println(ex.getMessage());
        }

        //Load resources:
        FileModelOriginal fm = new FileModelOriginal(resourceManager.getString(sourceLang + ".corpus"));
        loadGiza();
        processNGrams();
    }

    /**
     * Creates a QuEstProcessor instance.
     *
     * @param modelPath Path in which to load the trained model.
     */
    public QuestProcessor(String modelPath) {
        //Load model:
        try {
            predictionModel = svm.svm_load_model(modelPath);
        } catch (IOException ex) {
            System.out.println(ex.getMessage());
        }
    }

    /**
     * Adds all parameters values to the featureManager class attribute.
     *
     * @param tempFolder Folder in which to save temporary files.
     * @param featuresFile XML file with the features to be calculated.
     * @param gizaFile Translation probabilities file.
     * @param sourceNGram N-gram counts file.
     * @param sourceCorpus Source language corpus.
     * @param targetCorpus Target language corpus.
     * @param srilmPath Path to the binaries folder of SRILM.
     * @param modelPath Path in which to save the trained model.
     */
    private void parseArguments(String tempFolder,
            String featuresFile, String gizaFile,
            String sourceNgram, String sourceCorpus, String targetCorpus, String modelPath) {
        featureManager = new FeatureManager(featuresFile);
        featureManager.setFeatureList("all");
        resourceManager = new PropertiesManager();
        resourceManager.setProperty("logger.on", "false");
        resourceManager.setProperty("shef.mt.copyright",
                "(c) University of Sheffield, 2012");
        resourceManager.setProperty("input", tempFolder);
        resourceManager.setProperty(sourceLang + ".corpus", sourceCorpus);
        resourceManager.setProperty(targetLang + ".corpus", targetCorpus);
        resourceManager.setProperty(sourceLang + ".ngram", sourceNgram);
        resourceManager.setProperty("pair." + sourceLang + targetLang + ".giza.path", gizaFile);
        resourceManager.setProperty("tools.ngram.output.ext", ".ppl");
        resourceManager.setProperty("ngramsize", "3");
    }

    /**
     * Returns the integer value of a string.
     *
     * @param s string to be parsed.
     * @return equivalent integer value.
     */
    private static int atoi(String s) {
        return Integer.parseInt(s);
    }

    /**
     * Returns the double value of a string.
     *
     * @param s string to be parsed.
     * @return equivalent double value.
     */
    private static double atof(String s) {
        double d = Double.valueOf(s).doubleValue();
        if (Double.isNaN(d) || Double.isInfinite(d)) {
            System.out.println("NaN or Infinity in input.");
            System.exit(1);
        }
        return (d);
    }

    /**
     * Builds an svm_problem object based on a given input file.
     *
     * @param input_file_name file containing the data to be built the
     * svm_problem of.
     * @return an svm_problem object representing the input data.
     */
    private svm_problem buildProblem(String input_file_name) {
        BufferedReader fp = null;
        svm_problem prob = new svm_problem();
        try {
            fp = new BufferedReader(new FileReader(input_file_name));
            Vector<Double> vy = new Vector<Double>();
            Vector<svm_node[]> vx = new Vector<svm_node[]>();
            int max_index = 0;

            while (true) {
                String line = fp.readLine();
                if (line == null) {
                    break;
                }
                StringTokenizer st = new StringTokenizer(line, " \t\n\r\f:");

                vy.addElement(atof(st.nextToken()));
                int m = st.countTokens() / 2;
                svm_node[] x = new svm_node[m];
                for (int j = 0; j < m; j++) {
                    x[j] = new svm_node();
                    x[j].index = atoi(st.nextToken());
                    x[j].value = atof(st.nextToken());
                }
                if (m > 0) {
                    max_index = Math.max(max_index, x[m - 1].index);
                }
                vx.addElement(x);
            }

            prob = new svm_problem();
            prob.l = vy.size();
            prob.x = new svm_node[prob.l][];
            for (int i = 0; i < prob.l; i++) {
                prob.x[i] = vx.elementAt(i);
            }
            prob.y = new double[prob.l];
            for (int i = 0; i < prob.l; i++) {
                prob.y[i] = vy.elementAt(i);
            }
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        } finally {
            if (fp != null) {
                try {
                    fp.close();
                } catch (IOException e) {
                    return null;
                }
            }
        }
        return prob;
    }

    public String getSourceFile() {
        return sourceFile;
    }

    public void setSourceFile(String sourceFile) {
        this.sourceFile = sourceFile;
    }

    public String getTargetFile() {
        return targetFile;
    }

    public void setTargetFile(String targetFile) {
        this.targetFile = targetFile;
    }

    /**
     * Extracts the feature values from a given SVM training file.
     *
     * @param path text file containing the training data.
     * @return an array containing the feature values extracted.
     */
    private ArrayList<ArrayList<Double>> extractFeatureValuesFromSVMFile(String path) {
        ArrayList<ArrayList<Double>> result = new ArrayList<>();

        BufferedReader br = null;
        try {
            br = new BufferedReader(new FileReader(new File(path)));
            while (br.ready()) {
                String line = br.readLine().trim();
                if (!line.trim().isEmpty()) {
                    String[] data = line.split(" ");

                    ArrayList<Double> featvalues = new ArrayList<>();
                    for (int i = 1; i < data.length; i++) {
                        String[] featureData = data[i].split(":");
                        featvalues.add(Double.parseDouble(featureData[1].trim()));
                    }
                    result.add(featvalues);
                }
            }
            br.close();
        } catch (FileNotFoundException e) {
            System.out.println(e.getLocalizedMessage());
        } catch (IOException e) {
            System.out.println(e.getLocalizedMessage());
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (Exception e) {
                    System.out.println("Failed to close buffered stream.");
                }
            }
        }
        return result;
    }

    /**
     * Creates an svm_node vector for a given string of feature values.
     *
     * @param s string containing all feature values of a translation.
     * @return an svm_node vector equivalent to the feature values of the input
     * string.
     */
    private static svm_node[] buildSvm_Node(ArrayList<Double> values) {
        svm_node[] result = new svm_node[values.size()];
        for (int i = 0; i < values.size(); i++) {
            svm_node aux = new svm_node();
            aux.index = i + 1;
            aux.value = values.get(i);
            result[i] = aux;
        }
        return result;
    }

    /**
     * Adequate format of feature values.
     *
     * @param values array list of feature values
     * @return formatted string of values
     */
    private String formatFeatureValues(ArrayList<Double> values) {
        String result = "";
        for (int i = 1; i <= values.size(); i++) {
            result += i + ":" + values.get(i - 1) + " ";
        }
        result = result.trim();
        return result;
    }

    /**
     * Adequate format of feature values.
     *
     * @param values unformatted string of values
     * @return formatted string of values
     */
    private String formatFeatureValues(String values) {
        String[] splitValues = values.trim().split("\t");
        String result = "";
        for (int i = 1; i <= splitValues.length; i++) {
            result += i + ":" + splitValues[i - 1] + " ";
        }
        result = result.trim();
        return result;
    }

    /**
     * Produces a language model object based on an n-gram counts file.
     *
     * @return language model object.
     */
    private LanguageModel processNGrams() {
        NGramProcessor ngp = new NGramProcessor(
                resourceManager.getString(sourceLang + ".ngram"));
        return ngp.run();
    }

    /**
     * Obsolete function that loads a Giza object onto memory.
     */
    private void loadGiza() {
        String gizaPath = resourceManager.getString("pair." + sourceLang + targetLang + ".giza.path");
        Giza giza = new Giza(gizaPath);
    }

    public PropertiesManager getResourceManager() {
        return resourceManager;
    }

    /**
     * Calculates feature values for all sentence pairs in a set of files.
     *
     * @param sourceFile Source language sentences file.
     * @param targetFile Target language sentences file.
     * @return A matrix with the feature values of all sentence pairs.
     */
    public ArrayList<ArrayList<Double>> calculateFeatures(String sourceFile, String targetFile) {
        this.sourceFile = sourceFile;
        this.targetFile = targetFile;

        ArrayList<ArrayList<Double>> result = null;

        File f = new File(sourceFile);
        String sourceFileName = f.getName();
        f = new File(targetFile);
        String targetFileName = f.getName();

        BufferedReader brSource = null;
        BufferedReader brTarget = null;
        BufferedWriter tempNorm = null;
        try {
            brSource = new BufferedReader(new FileReader(sourceFile));
            brTarget = new BufferedReader(new FileReader(targetFile));

            ResourceManager.printResources();
            Sentence sourceSent;
            Sentence targetSent;
            int sentCount = 0;

            String lineSource = brSource.readLine();
            String lineTarget = brTarget.readLine();

            // Lists to store source and target sentences in sequence
            ArrayList<Sentence> sourceSentences = new ArrayList<>();
            ArrayList<Sentence> targetSentences = new ArrayList<>();

            // File to store temporarily non-normalized feature values
            File nonNorm = new File(resourceManager.getString("input")
                    + File.separator + "temp_non_normalized.txt");
            tempNorm = new BufferedWriter(new FileWriter(nonNorm));

            while ((lineSource != null) && (lineTarget != null)) {

                sourceSent = new Sentence(lineSource, sentCount);
                targetSent = new Sentence(lineTarget, sentCount);

                sourceSent.computeNGrams(3);
                targetSent.computeNGrams(3);

                ++sentCount;
                String featureValues = featureManager.runFeatures(sourceSent,
                        targetSent);

                // Save source and target sentences in lists
                sourceSentences.add(sourceSent);
                targetSentences.add(targetSent);

                // Write SVM formatted feature values onto temporary
                // non-normalized features file
                String formattedFeatureValues = formatFeatureValues(featureValues);
                tempNorm.write("0.0 " + formattedFeatureValues);
                tempNorm.newLine();

                lineSource = brSource.readLine();
                lineTarget = brTarget.readLine();
            }
            tempNorm.close();

            // Normalize the non-normalized temporary file feature values
            svm_scale scaler = new svm_scale();
            String[] params_svm = new String[7];
            params_svm[0] = "-o";
            params_svm[1] = resourceManager.getString("input")
                    + File.separator + "temp_normalized.txt";
            params_svm[2] = "-l";
            params_svm[3] = "-1";
            params_svm[4] = "-u";
            params_svm[5] = "1";
            params_svm[6] = resourceManager.getString("input")
                    + File.separator + "temp_non_normalized.txt";
            scaler.run(params_svm);

            // Read the normalized feature values
            result = extractFeatureValuesFromSVMFile(resourceManager
                    .getString("input")
                    + File.separator
                    + "temp_normalized.txt");

            File deleter = new File(resourceManager.getString("input")
                    + File.separator + "temp_non_normalized.txt");
            deleter.delete();

            deleter = new File(resourceManager.getString("input")
                    + File.separator + "temp_normalized.txt");
            deleter.delete();

            brSource.close();
            brTarget.close();
        } catch (IOException e) {
            System.out.println("ERROR: " + e.getLocalizedMessage());
        } finally {
            if (brSource != null) {
                try {
                    brSource.close();
                } catch (Exception e) {
                    System.out.println("Failed to close buffered stream.");
                }
            }
            if (brTarget != null) {
                try {
                    brTarget.close();
                } catch (Exception e) {
                    System.out.println("Failed to close buffered stream.");
                }
            }
            if (tempNorm != null) {
                try {
                    tempNorm.close();
                } catch (Exception e) {
                    System.out.println("Failed to close buffered stream.");
                }
            }
        }
        return result;
    }

    /**
     * Calculates feature values for an individual pair of sentences.
     *
     * @param sourceSentence Source language sentence.
     * @param targetSentence Target language sentence.
     * @return A matrix with the feature values of the sentence pair.
     */
    public ArrayList<ArrayList<Double>> calculateFeaturesForPair(String sourceSentence, String targetSentence) {
        ArrayList<ArrayList<Double>> result = null;

        BufferedWriter tempNorm = null;
        try {
            ResourceManager.printResources();
            Sentence sourceSent;
            Sentence targetSent;
            int sentCount = 0;

            String lineSource = sourceSentence;
            String lineTarget = targetSentence;

            // Lists to store source and target sentences in sequence
            ArrayList<Sentence> sourceSentences = new ArrayList<>();
            ArrayList<Sentence> targetSentences = new ArrayList<>();

            // File to store temporarily non-normalized feature values
            File nonNorm = new File(resourceManager.getString("input")
                    + File.separator + "temp_non_normalized.txt");
            tempNorm = new BufferedWriter(new FileWriter(nonNorm));

            sourceSent = new Sentence(lineSource, sentCount);
            targetSent = new Sentence(lineTarget, sentCount);

            sourceSent.computeNGrams(3);
            targetSent.computeNGrams(3);

            ++sentCount;
            String featureValues = featureManager.runFeatures(sourceSent,
                    targetSent);

            // Save source and target sentences in lists
            sourceSentences.add(sourceSent);
            targetSentences.add(targetSent);

            // Write SVM formatted feature values onto temporary non-normalized features file
            String formattedFeatureValues = formatFeatureValues(featureValues);
            tempNorm.write("0.0 " + formattedFeatureValues);
            tempNorm.newLine();
            tempNorm.close();

            // Normalize the non-normalized temporary file feature values
            svm_scale scaler = new svm_scale();
            String[] params_svm = new String[7];
            params_svm[0] = "-o";
            params_svm[1] = resourceManager.getString("input")
                    + File.separator + "temp_normalized.txt";
            params_svm[2] = "-l";
            params_svm[3] = "-1";
            params_svm[4] = "-u";
            params_svm[5] = "1";
            params_svm[6] = resourceManager.getString("input")
                    + File.separator + "temp_non_normalized.txt";
            scaler.run(params_svm);

            // Read the normalized feature values
            result = extractFeatureValuesFromSVMFile(resourceManager
                    .getString("input")
                    + File.separator
                    + "temp_normalized.txt");

            File deleter = new File(resourceManager.getString("input")
                    + File.separator + "temp_non_normalized.txt");
            deleter.delete();

            deleter = new File(resourceManager.getString("input")
                    + File.separator + "temp_normalized.txt");
            deleter.delete();
        } catch (IOException e) {
            System.out.println("ERROR: " + e.getLocalizedMessage());
        } finally {
            if (tempNorm != null) {
                try {
                    tempNorm.close();
                } catch (Exception e) {
                    System.out.println("Failed to close buffered stream.");
                }
            }
        }
        return result;
    }

    
    /**
     * Estimates the quality of a translation.
     *
     * @param features Matrix with the features of the translations to be scored.
     * @return An integer array with the scores predicted.
     */
    public ArrayList<Integer> estimateQuality(ArrayList<ArrayList<Double>> features) {
        ArrayList<Integer> scores = new ArrayList<>();
        for (int i = 0; i < features.size(); i++) {
            ArrayList<Double> values = features.get(i);

            svm_node[] finalFeatureValues = buildSvm_Node(values);
            double score = svm.svm_predict(predictionModel, finalFeatureValues);
            scores.add(Math.toIntExact(Math.round(score)));
        }
        return scores;
    }

}
