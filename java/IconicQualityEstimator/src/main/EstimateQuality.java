package main;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Iterator;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.apache.commons.cli.BasicParser;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import quest.QuestProcessor;

public class EstimateQuality {

    public static void main(String[] args) {
        //Get options:
        CommandLine cl = parseArguments(args);

        //Get source and target input files:
        String sourceFile = cl.getOptionValue("source");
        String targetFile = cl.getOptionValue("target");
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

        //Get output file:
        String outputFile = cl.getOptionValue("output");

        //Create QuestProcessor instance:
        long time = System.currentTimeMillis();
        QuestProcessor quest = new QuestProcessor(tempFolder, featuresFile, gizaFile,
                ngramFile, corpusSrc, corpusTrg, lmSrc, lmTrg, srilmPath, modelFile, sourceLang, targetLang);
        time = (System.currentTimeMillis()-time)/1000;
        System.out.println("Models loaded! Seconds taken: " + time);

        //Calculate features:
        time = System.currentTimeMillis();
        ArrayList<ArrayList<Double>> features = quest.calculateFeatures(sourceFile, targetFile);
        time = (System.currentTimeMillis()-time)/1000;
        System.out.println("Features calculated! Seconds taken: " + time);
        
        //Calculate scores:
        time = System.currentTimeMillis();
        ArrayList<Integer> scores = quest.estimateQuality(features);
        time = (System.currentTimeMillis()-time)/1000;
        System.out.println("Scores produced! Seconds taken: " + time);
        
        //Save scores:
        saveScores(scores, outputFile);
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
        options.addOption("model", true, "Path to QE model.");
        options.addOption("langsrc", true, "Source language.");
        options.addOption("langtrg", true, "Target language.");
        options.addOption("source", true, "Source input file.");
        options.addOption("target", true, "Target input file.");
        options.addOption("output", true, "Quality estimates output file.");

        //Get required options:
        HashSet<String> requiredOpts = new HashSet<>();
        Iterator iopt = options.getOptions().iterator();
        while (iopt.hasNext()) {
            Option o = (Option) iopt.next();
            requiredOpts.add(o.getOpt());
        }

        //Create command line arguments:
        CommandLineParser parser = new BasicParser();
        try {
            CommandLine cmd = parser.parse(options, args);
            for (String opt : requiredOpts) {
                if (!cmd.hasOption(opt)) {
                    System.out.println("Missing argument: " + opt);
                    return null;
                } else if (cmd.getOptionValue(opt) == null) {
                    System.out.println("Null option value: " + opt);
                    return null;
                }
            }
            return cmd;
        } catch (ParseException ex) {
            Logger.getLogger(EstimateQuality.class.getName()).log(Level.SEVERE, null, ex);
            return null;
        }
    }

    private static void saveScores(ArrayList<Integer> scores, String output) {
        try {
            BufferedWriter bw = new BufferedWriter(new FileWriter(output));
            for(Integer i: scores){
                bw.write(i + "");
                bw.newLine();
            }
            bw.close();
        } catch (IOException ex) {
            Logger.getLogger(EstimateQuality.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

}
