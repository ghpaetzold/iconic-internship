package svm;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;
import java.util.StringTokenizer;
import java.util.Vector;

import libsvm.svm;
import libsvm.svm_model;
import libsvm.svm_node;
import libsvm.svm_parameter;
import libsvm.svm_problem;

/**
 * Class responsible for creating an SVM for the SVM Model Builder step.
 *
 * @author GustavoH
 *
 */
public class SVMModelBuilderProcessor {

    /**
     * Builds a text file model based on a given file of training data.
     *
     * @param inputPath path for text file containing training data.
     * @param modelPath path for output text file containing the final model.
     * @param n number of samples for cross-validation.
     */
    public svm_model buildModelFile(ArrayList<ArrayList<Double>> features, ArrayList<Integer> scores, String modelPath, String temp, String kernel, int n) {
        svm_parameter param = new svm_parameter();
        param.shrinking = 1;
        param.svm_type = svm_parameter.C_SVC;
        switch (kernel) {
            case "linear":
                param.kernel_type = svm_parameter.LINEAR;
                break;
            case "rbf":
                param.kernel_type = svm_parameter.RBF;
                break;
            case "poly":
                param.kernel_type = svm_parameter.POLY;
                break;
            case "sigmoid":
                param.kernel_type = svm_parameter.SIGMOID;
                break;
            default:
                param.kernel_type = svm_parameter.LINEAR;
                break;
        }
        
        param.cache_size = 64;
        param.degree = 2;
        param.gamma = 0;
        param.coef0 = 0;
        param.nu = 0.5;
        param.cache_size = 100;
        param.C = 1;
        param.eps = 1e-3;
        param.p = 0.1;
        param.shrinking = 1;
        param.probability = 0;
        param.nr_weight = 0;
        param.weight_label = new int[0];
        param.weight = new double[0];
        svm_model predictionModel = buildTrainingModel(features, scores, temp, param, n);
        try {
            svm.svm_save_model(modelPath, predictionModel);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return predictionModel;
    }

    /**
     * Builds an svm_model object based on training data.
     *
     * @param modelPath text file containing training data.
     * @param inputPath folder to save temporary cross-validation samples.
     * @param param parameters object for the SVM.
     * @param n number of samples of the cross-validation
     * @return an svm_model object trained with the best combination of
     * parameters.
     */
    private svm_model buildTrainingModel(ArrayList<ArrayList<Double>> features, ArrayList<Integer> scores, String temp,
            svm_parameter param, int n) {
        double threshold = 0.2;
        Random r = new Random();
        HashMap<Integer, ArrayList<String>> valuesMap = new HashMap<>();

        //Create string representation of features and scores:
        ArrayList<String> featuresString = new ArrayList<>();
        for (int i = 0; i < features.size(); i++) {
            ArrayList<Double> values = features.get(i);
            Integer score = scores.get(i);
            String line = score + " ";
            for (int j=0; j<values.size(); j++) {
                Double d = values.get(j);
                line += (j+1) + ":" + d + " ";
            }
            featuresString.add(line.trim());
        }

        //Produce cross-validation temporary files.
        for (int i = 0; i < n; i++) {
            BufferedWriter mbTrain = null;
            BufferedWriter mbTest = null;
            try {
                mbTrain = new BufferedWriter(new FileWriter(new File(temp + File.separator + "temp.train." + i + ".txt")));
                mbTest = new BufferedWriter(new FileWriter(new File(temp + File.separator + "temp.test." + i + ".txt")));
                ArrayList<String> testValues = new ArrayList<>();

                for (int j = 0; j < features.size(); j++) {
                    String entry = featuresString.get(j);
                    double aux = r.nextDouble();
                    if (aux <= threshold) {
                        mbTest.write(entry);
                        mbTest.newLine();
                        testValues.add(entry.split(" ")[0].trim());
                    } else {
                        mbTrain.write(entry);
                        mbTrain.newLine();
                    }
                }

                mbTrain.close();
                mbTest.close();
                valuesMap.put(i, testValues);
            } catch (FileNotFoundException e) {
                System.out.println("Problem while producing cross-validation files.");
                System.out.println(e.getLocalizedMessage());
            } catch (IOException e) {
                System.out.println("Problem while producing cross-validation files.");
                System.out.println(e.getLocalizedMessage());
            } finally {
                if (mbTrain != null) {
                    try {
                        mbTrain.close();
                    } catch (IOException e) {
                        System.out.println(e.getLocalizedMessage());
                    }
                }
                if (mbTest != null) {
                    try {
                        mbTest.close();
                    } catch (IOException e) {
                        System.out.println(e.getLocalizedMessage());
                    }
                }
            }
        }

        //Create lists of possible parameters values for SVM.
        double[] Gammas = {0.0001, 0.0305344, 0.00122137};
        double[] Cs = {1, 5, 10};
        double[] Epsilons = {0.1, 0.2};
        double minRMSE = 9999;
        double bestGamma = 0;
        double bestC = 0;
        double bestEpsilon = 0;

        //Estimate error for each combination of parameters and select the best one.
        for (double Gamma : Gammas) {
            for (double C : Cs) {
                for (double Epsilon : Epsilons) {
                    double totalRMSE = 0;
                    param.gamma = Gamma;
                    param.C = C;
                    param.eps = Epsilon;
                    for (int i = 0; i < n; i++) {
                        svm_problem problem = this.buildProblem(temp
                                + File.separator + "temp.train." + i + ".txt");
                        svm_model tempModel = svm.svm_train(problem, param);
                        double partialRMSE = calculateRSME(temp
                                + File.separator + "temp.test." + i + ".txt",
                                valuesMap.get(i), tempModel);
                        totalRMSE += partialRMSE;
                    }
                    if (totalRMSE < minRMSE) {
                        minRMSE = totalRMSE;
                        bestGamma = Gamma;
                        bestC = C;
                        bestEpsilon = Epsilon;
                    }
                }
            }
        }

        //Modify parameters object with best values for parameters.
        param.gamma = bestGamma;
        param.C = bestC;
        param.eps = bestEpsilon;
        svm_problem final_problem = buildProblem(featuresString);

        //Delete temporary cross-validation input files.
        for (int i = 0; i < n; i++) {
            File train = new File(temp + File.separator + "temp.train."
                    + i + ".txt");
            File test = new File(temp + File.separator + "temp.test." + i
                    + ".txt");
            train.delete();
            test.delete();
        }

        //Return an SVM object.
        return svm.svm_train(final_problem, param);

    }

    /**
     * Calculate error for a give cross-validation step.
     *
     * @param testPath text file with reference feature values of translations.
     * @param values list of reference ideal scores for the translations.
     * @param model SVM trained with a given set of parameters.
     * @return total difference between ideal scores and predicted scores.
     */
    private double calculateRSME(String testPath, ArrayList<String> values,
            svm_model model) {
        double result = 0;

        BufferedReader br = null;
        try {
            br = new BufferedReader(new FileReader(new File(testPath)));
            int n = 0;
            while (br.ready()) {
                String entry = br.readLine().trim();
                if (!entry.isEmpty()) {
                    double score = svm.svm_predict(model, buildSvm_Node(entry));
                    result += Math.pow(
                            score - Double.parseDouble(values.get(n)), 2);
                    n++;
                }
            }
            result = result / (double) n;
            result = Math.sqrt(result);
            br.close();
            return result;
        } catch (FileNotFoundException e) {
            System.out.println("Error while calculating RMSE: File not found.");
            System.out.println(e.getLocalizedMessage());
            return -1;
        } catch (IOException e) {
            System.out.println("Error while calculating RMSE: Input/Output exception.");
            System.out.println(e.getLocalizedMessage());
            return -1;
        } finally {
            if (br != null) {
                try {
                    br.close();
                } catch (IOException e) {
                    System.out.println(e.getLocalizedMessage());
                }
            }
        }
    }

    /**
     * Creates an svm_node vector for a given string of feature values.
     *
     * @param s string containing all feature values of a translation.
     * @return an svm_node vector equivalent to the feature values of the input
     * string.
     */
    private static svm_node[] buildSvm_Node(String s) {
        String[] features = s.trim().split(" ");
        int size = features.length;
        if (!features[0].contains(":")) {
            String[] aux = new String[size - 1];
            for (int i = 0; i < size - 1; i++) {
                aux[i] = features[i + 1];
            }
            features = aux;
            size = size - 1;
        }
        svm_node[] result = new svm_node[size];
        for (int i = 0; i < size; i++) {
            String feature = features[i];
            String[] data = feature.split(":");
            String index = data[0];
            String value = data[1];
            svm_node aux = new svm_node();
            aux.index = Integer.valueOf(index);
            aux.value = Double.valueOf(value);
            result[i] = aux;
        }
        return result;
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
            System.err.print("NaN or Infinity in input\n");
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
        svm_problem prob = new svm_problem();
        BufferedReader fp = null;
        try {
            fp = new BufferedReader(new FileReader(input_file_name));
        } catch (FileNotFoundException e) {
            System.out.println("Failed to open model file.");
            System.out.println(e.getLocalizedMessage());
            return null;
        }
        Vector<Double> vy = new Vector<Double>();
        Vector<svm_node[]> vx = new Vector<svm_node[]>();
        int max_index = 0;

        while (true) {
            String line;
            try {
                line = fp.readLine();
            } catch (IOException e) {
                System.out.println("Failed to read model file.");
                System.out.println(e.getLocalizedMessage());
                if (fp != null) {
                    try {
                        fp.close();
                    } catch (IOException ioe) {
                        System.out.println(ioe.getLocalizedMessage());
                    }
                }
                return null;
            }
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

        try {
            fp.close();
        } catch (IOException e) {
            System.out.println(e.getLocalizedMessage());
        }

        return prob;
    }

    private svm_problem buildProblem(ArrayList<String> input) {
        svm_problem prob;

        Vector<Double> vy = new Vector<>();
        Vector<svm_node[]> vx = new Vector<>();
        int max_index = 0;

        for (int i = 0; i < input.size(); i++) {
            String line = input.get(i);

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

        return prob;
    }

}
