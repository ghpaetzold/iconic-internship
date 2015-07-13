package main;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.apache.commons.cli.BasicParser;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Option;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import org.apache.commons.math3.stat.descriptive.moment.Mean;
import org.apache.commons.math3.stat.descriptive.moment.StandardDeviation;

public class EvaluateQualityEstimates {

    public static void main(String[] args) {
        //Get options:
        CommandLine cl = parseArguments(args);
        if (cl == null) {
            return;
        }

        //Get source, target and scores input files:
        String reference = cl.getOptionValue("ref");
        String estimates = cl.getOptionValue("est");
        
        //Evaluate estimated quality:
        Object[] qualityData = evaluateEstimates(reference, estimates);
        
        //Print quality data:
        int sum = (int) qualityData[0];
        double mean = (double) qualityData[1];
        double std = (double) qualityData[2];
        HashMap<Integer, Integer> gravityMap = (HashMap<Integer, Integer>) qualityData[3];
        System.out.println("Iconic QE Sum: " + sum);
        System.out.println("Iconic QE Mean: " + mean);
        System.out.println("Iconic QE Standard Deviation: " + std);
        System.out.println("Iconic QE Gravity Counts:");
        for(int i=0; i<=3; i++){
            System.out.println("\t" + i + ": " + gravityMap.get(i));
        }
    }

    private static CommandLine parseArguments(String[] args) {
        //Create options object:
        Options options = new Options();
        options.addOption("ref", true, "File containing gold-standard quality estimates.");
        options.addOption("est", true, "File containing predicted quality estimates.");

        //Get required options:
        HashSet<String> requiredOpts = new HashSet<>();
        Iterator iopt = options.getOptions().iterator();
        while (iopt.hasNext()) {
            Option o = (Option) iopt.next();
            requiredOpts.add(o.getOpt());
        }

        //Add additional options:
        options.addOption("help", false, "Prints a help message.");

        //Create help text:
        String header = "Evaluates the quality of predicted quality estimates.\n\n";
        String footer = "\nThis software is a property of Iconic Translation Machines Ltd.";
        HelpFormatter formatter = new HelpFormatter();

        //Create command line arguments:
        CommandLineParser parser = new BasicParser();
        try {
            CommandLine cmd = parser.parse(options, args);
            if (cmd.hasOption("help")) {
                formatter.printHelp("EvaluateQualityEstimates", header, options, footer, true);
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
            return cmd;
        } catch (ParseException ex) {
            Logger.getLogger(EstimateQuality.class.getName()).log(Level.SEVERE, null, ex);
            return null;
        }
    }

    private static Object[] evaluateEstimates(String reference, String estimates) {
        //Create the Iconic evaluation matrix:
        double[][] iconicMatrix = {
            {0,0,0,1,2,2},
            {0,0,0,1,2,2},
            {0,0,0,0,2,2},
            {1,1,0,0,0,2},
            {3,3,3,0,0,0},
            {3,3,3,3,0,0}
        };
        
        //Create statistics objects:
        Mean meanCalculator = new Mean();
        StandardDeviation stdCalculator = new StandardDeviation();
        HashMap<Integer, Integer> gravityMap = new HashMap<>();
        ArrayList<Double> gravityScores = new ArrayList<>();
        int sum = 0;
        
        //Initialize gravity map:
        for(int i=0; i<=3; i++){
            gravityMap.put(i, 0);
        }
        
        try {
            //Open estimates file:
            BufferedReader refB = new BufferedReader(new FileReader(reference));
            BufferedReader estB = new BufferedReader(new FileReader(estimates));
            
            //Read files and calculate scores:
            while(refB.ready()){
                int refScore = (int) Double.parseDouble(refB.readLine().trim());
                int estScore = (int) Double.parseDouble(estB.readLine().trim());
                
                double gravity = iconicMatrix[estScore][refScore];
                
                sum += gravity;
                gravityScores.add(gravity);
                gravityMap.put((int)gravity, gravityMap.get((int)gravity)+1);
            }
            
            //Calculate evaluation data:
            double[] gravities = new double[gravityScores.size()];
            for(int i=0; i<gravityScores.size(); i++){
                double score = gravityScores.get(i);
                gravities[i] = score;
            }
            double mean = meanCalculator.evaluate(gravities);
            double std = stdCalculator.evaluate(gravities);
            
            //Return evaluation data:
            Object[] result = new Object[4];
            result[0] = sum;
            result[1] = mean;
            result[2] = std;
            result[3] = gravityMap;
            return result;
            
        } catch (FileNotFoundException ex) {
            Logger.getLogger(EvaluateQualityEstimates.class.getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(EvaluateQualityEstimates.class.getName()).log(Level.SEVERE, null, ex);
        }
        return null;
    }

}
