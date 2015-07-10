package main;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.logging.Level;
import java.util.logging.Logger;
import libsvm.svm_model;
import org.apache.commons.cli.BasicParser;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import quest.QuestProcessor;
import svm.SVMModelBuilderProcessor;

public class GetQualityModel {

    public static void main(String[] args) {
        //Get options:
        CommandLine cl = parseArguments(args);
        if(cl==null){
            return;
        }

        //Get source, target and scores input files:
        String sourceFile = cl.getOptionValue("source");
        String targetFile = cl.getOptionValue("target");
        String scoresFile = cl.getOptionValue("scores");
        String sourceLang = cl.getOptionValue("langsrc");
        String targetLang = cl.getOptionValue("langtrg");

        //Get resource paths:
        String gizaFile = cl.getOptionValue("giza");
        String ngramFile = cl.getOptionValue("ngramsrc");
        String corpusSrc = cl.getOptionValue("corpussrc");
        String corpusTrg = cl.getOptionValue("corpustrg");
        String lmSrc = cl.getOptionValue("lmsrc");
        String lmTrg = cl.getOptionValue("lmtrg");
        String srilmPath = cl.getOptionValue("srilm");

        //Get temporary folder:
        String tempFolder = cl.getOptionValue("temp");

        //Get features file:
        String featuresFile = cl.getOptionValue("features");

        //Get model file:
        String modelFile = cl.getOptionValue("model");

        //Get model parameters:
        String kernel = cl.getOptionValue("kernel");
        Integer samples = Integer.parseInt(cl.getOptionValue("samples"));
        Double C = null, gamma = null, epsilon = null;
        if (samples == 0) {
            C = Double.parseDouble(cl.getOptionValue("C"));
            gamma = Double.parseDouble(cl.getOptionValue("gamma"));
            epsilon = Double.parseDouble(cl.getOptionValue("epsilon"));
        }

        //Get output file:
        String outputFile = cl.getOptionValue("output");

        //Create QuestProcessor instance:
        QuestProcessor quest = new QuestProcessor(tempFolder, featuresFile, gizaFile,
                ngramFile, corpusSrc, corpusTrg, lmSrc, lmTrg, srilmPath, modelFile, sourceLang, targetLang);

        //Calculate features and get scores:
        ArrayList<ArrayList<Double>> features = quest.calculateFeatures(sourceFile, targetFile);
        ArrayList<Integer> scores = readScores(scoresFile);

        //Create model trainer:
        SVMModelBuilderProcessor svm = new SVMModelBuilderProcessor();

        //Train and save model:
        svm_model model = svm.buildModelFile(features, scores, modelFile, tempFolder, kernel, samples, C, gamma, epsilon);
    }

    private static CommandLine parseArguments(String[] args) {
        //Create options object:
        Options options = new Options();
        options.addOption("temp", true, "Folder for temporary files.");
        options.addOption("features", true, "XML features file.");
        options.addOption("giza", true, "Translation probabilities file.");
        options.addOption("ngramsrc", true, "Source n-gram counts file.");
        options.addOption("corpussrc", true, "Source corpus.");
        options.addOption("corpustrg", true, "Target corpus.");
        options.addOption("lmsrc", true, "Source language model.");
        options.addOption("lmtrg", true, "Target language model.");
        options.addOption("srilm", true, "SRILM binaries path.");
        options.addOption("langsrc", true, "Source language.");
        options.addOption("langtrg", true, "Target language.");
        options.addOption("source", true, "Source input file.");
        options.addOption("target", true, "Target input file.");
        options.addOption("scores", true, "Scores file.");
        options.addOption("model", true, "Path to save trained QE model.");
        options.addOption("kernel", true, "Kernel to be used.");
        options.addOption("samples", true, "Number of samples for cross-validation.");

        //Get required options:
        HashSet<String> requiredOpts = new HashSet<>();
        Iterator iopt = options.getOptions().iterator();
        while (iopt.hasNext()) {
            Option o = (Option) iopt.next();
            requiredOpts.add(o.getOpt());
        }

        //Add additional options:
        options.addOption("C", true, "Value for the C hyperparameter.");
        options.addOption("gamma", true, "Value for the gamma hyperparameter.");
        options.addOption("epsilon", true, "Value for the epsilon hyperparameter.");
        options.addOption("help", false, "Prints a help message.");

        //Create help text:
        String header = "Train a translation quality estimation model\n\n";
        String footer = "\nThis software is a property of Iconic Translation Machines Ltd.";
        HelpFormatter formatter = new HelpFormatter();

        //Create command line arguments:
        CommandLineParser parser = new BasicParser();
        try {
            CommandLine cmd = parser.parse(options, args);
            if (cmd.hasOption("help")) {
                formatter.printHelp("GetQualityModel", header, options, footer, true);
                return null;
            } else {
                for (String opt : requiredOpts) {
                    if (!cmd.hasOption(opt)) {
                        System.out.println("Missing argument: " + opt);
                        return null;
                    } else if (cmd.getOptionValue(opt) == null) {
                        System.out.println("Null option value: " + opt);
                        return null;
                    }
                }
            }

            Integer samples = Integer.parseInt(cmd.getOptionValue("samples"));
            if (samples == 0) {
                String[] requiredParams = {"C", "gamma", "epsilon"};
                for (String opt : requiredParams) {
                    if (!cmd.hasOption(opt)) {
                        System.out.println("Missing hyperparameter: " + opt);
                        return null;
                    } else if (cmd.getOptionValue(opt) == null) {
                        System.out.println("Null hyperparameter value: " + opt);
                        return null;
                    }
                }
            }
            return cmd;
        } catch (ParseException ex) {
            Logger.getLogger(EstimateQuality.class.getName()).log(Level.SEVERE, null, ex);
            return null;
        }
    }

    private static ArrayList<Integer> readScores(String scoresFile) {
        ArrayList<Integer> scores = new ArrayList<>();
        try {
            BufferedReader br = new BufferedReader(new FileReader(scoresFile));
            while (br.ready()) {
                Integer score = Integer.parseInt(br.readLine().trim());
                scores.add(score);
            }
        } catch (FileNotFoundException ex) {
            System.out.println("Error while opening scores file.");
        } catch (IOException ex) {
            System.out.println("Error while reading scores file.");
        }
        return scores;
    }

}
