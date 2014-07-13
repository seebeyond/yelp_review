
//    Copyright 2013 Petter Törnberg
//
//    This demo code has been kindly provided by Petter Törnberg <pettert@chalmers.se>
//    for the SentiWordNet website.
//
//    This program is free software: you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License
//    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.parser.common.ParserQuery;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import edu.stanford.nlp.parser.lexparser.Options;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.process.DocumentPreprocessor.DocType;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreebankLanguagePack;

public class SentimentScoreExtractor {

	private Map<String, Double> dictionary;
	String parserPath = null;
	LexicalizedParser lp = null;
	Options op = null;

	public SentimentScoreExtractor(String pathToSWN, String pPath) throws IOException {
		//parser path 
		parserPath=pPath;
		op = new Options();
		lp = LexicalizedParser.getParserFromFile(parserPath, op);
		op = lp.getOp();
		// This is our main dictionary representation
		dictionary = new HashMap<String, Double>();

		// From String to list of doubles.
		HashMap<String, HashMap<Integer, Double>> tempDictionary = new HashMap<String, HashMap<Integer, Double>>();

		BufferedReader csv = null;
		try {
			csv = new BufferedReader(new FileReader(pathToSWN));
			int lineNumber = 0;

			String line;
			while ((line = csv.readLine()) != null) {
				lineNumber++;

				// If it's a comment, skip this line.
				if (!line.trim().startsWith("#")) {
					// We use tab separation
					String[] data = line.split("\t");
					String wordTypeMarker = data[0];

					// Example line:
					// POS ID PosS NegS SynsetTerm#sensenumber Desc
					// a 00009618 0.5 0.25 spartan#4 austere#3 ascetical#2
					// ascetic#2 practicing great self-denial;...etc

					// Is it a valid line? Otherwise, through exception.
					if (data.length != 6) {
						throw new IllegalArgumentException(
								"Incorrect tabulation format in file, line: "
										+ lineNumber);
					}

					// Calculate synset score as score = PosS - NegS
					Double synsetScore = Double.parseDouble(data[2])
							- Double.parseDouble(data[3]);

					// Get all Synset terms
					String[] synTermsSplit = data[4].split(" ");

					// Go through all terms of current synset.
					for (String synTermSplit : synTermsSplit) {
						// Get synterm and synterm rank
						String[] synTermAndRank = synTermSplit.split("#");
						String synTerm = synTermAndRank[0] + "#"
								+ wordTypeMarker;

						int synTermRank = Integer.parseInt(synTermAndRank[1]);
						// What we get here is a map of the type:
						// term -> {score of synset#1, score of synset#2...}

						// Add map to term if it doesn't have one
						if (!tempDictionary.containsKey(synTerm)) {
							tempDictionary.put(synTerm,
									new HashMap<Integer, Double>());
						}

						// Add synset link to synterm
						tempDictionary.get(synTerm).put(synTermRank,
								synsetScore);
					}
				}
			}

			// Go through all the terms.
			for (Map.Entry<String, HashMap<Integer, Double>> entry : tempDictionary
					.entrySet()) {
				String word = entry.getKey();
				Map<Integer, Double> synSetScoreMap = entry.getValue();

				// Calculate weighted average. Weigh the synsets according to
				// their rank.
				// Score= 1/2*first + 1/3*second + 1/4*third ..... etc.
				// Sum = 1/1 + 1/2 + 1/3 ...
				double score = 0.0;
				double sum = 0.0;
				for (Map.Entry<Integer, Double> setScore : synSetScoreMap
						.entrySet()) {
					score += setScore.getValue() / (double) setScore.getKey();
					sum += 1.0 / (double) setScore.getKey();
				}
				score /= sum;

				dictionary.put(word, score);
			}
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			if (csv != null) {
				csv.close();
			}
		}
	}

	public double extract(String word) {
			//System.out.println(word);
			double score_a=0,score_n=0;
			if(dictionary.containsKey(word + "#" + "a")){
				score_a=dictionary.get(word + "#" + "a");
				//System.out.println("a-score: "+score_a);
			}
			if(dictionary.containsKey(word + "#" + "n")){
				score_n=dictionary.get(word + "#" + "n");
				//System.out.println("n-score: "+score_n);
			}
			
			if(score_a==0 && score_n==0){
				return 0;
			}
			else{
				score_a=Math.abs(score_a);
				score_n=Math.abs(score_n);
				if(Double.compare(score_a, score_n)<0){
					return score_n;
				}
				else{
					return score_a;
				}
			}
			
	}
	double processReviews(String reviewsFilePath){
		
		final DocType docType = DocType.Plain;
		double score = 0.0;
		DocumentPreprocessor documentPreprocessor = new DocumentPreprocessor(reviewsFilePath,docType,op.tlpParams.getInputEncoding());
		TreebankLanguagePack tlp = op.tlpParams.treebankLanguagePack();
		
		documentPreprocessor.setSentenceFinalPuncWords(tlp.sentenceFinalPunctuationWords());
	    documentPreprocessor.setEscaper(null);
	    documentPreprocessor.setSentenceDelimiter(null);
	    documentPreprocessor.setTagDelimiter(null);
	    documentPreprocessor.setElementDelimiter(null);
        documentPreprocessor.setTokenizerFactory(tlp.getTokenizerFactory());
        
        int num=0,numSents=0,numWords=0;
        for (List<HasWord> sentence : documentPreprocessor) {
          num++;
          numSents++;
         for(HasWord word : sentence){
        	  //System.out.println(word.toString());
        	  score+=extract(word.toString());
          }
        }
		return score;
	}
	void processData(String dataPath, String outputName){
		String line = "";
		String delimiter = "\t";
		
		BufferedReader br = null;
		BufferedWriter bw = null;
		BufferedWriter outWriter=null;
		
		//DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd-HH:mm:ss");
		//get current date time with Date()
		//Date date = new Date();
		String tmpfileName = new String("tmp-"+System.nanoTime()+".txt");
		File file = new File(tmpfileName);
		try {
			if (file.createNewFile()){
			        System.out.println("File is created!");
			  }else{
			        System.out.println("File already exists.");
			  }
		} catch (IOException e2) {
			// TODO Auto-generated catch block
			e2.printStackTrace();
		}
		
		
		try {
			File outfile =  new File(outputName);
				if (file.createNewFile()){
				        System.out.println("output File is created!");
				  }else{
				        System.out.println("File already exists.");
				  }
			outWriter = new BufferedWriter(new FileWriter(outputName));
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		
		double sentimentScore = 0.0;
	 
		try {
	 
			br = new BufferedReader(new FileReader(dataPath));
			
			while ((line = br.readLine()) != null) {
				bw = new BufferedWriter(new FileWriter(tmpfileName));
			        // use comma as separator
				String[] fields = line.split(delimiter);
				//System.out.println(fields[6]);
				//List<Double> scores = parseReview(fields[6]);
				//System.out.println(fields[0]);
				bw.write(fields[6]);
				bw.close();
				sentimentScore = processReviews(tmpfileName);
				String newRecord = new String(fields[0]+","+sentimentScore+"\n");
				outWriter.write(newRecord);
			
			}
	 
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
			if (br != null) {
				try {
					br.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
			if (outWriter != null) {
				try {
					outWriter.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
		System.out.println("Done");
	  }	
	public static void main(String [] args) throws IOException {
		if(args.length<1) {
			System.err.println("Usage: java SentimentScoreExtractor <pathToSentiWordNetFile> <parserPath> <training_data.tsv> <output.tsv>");
			return;
		}
		
		String pathToSWN = new String(args[0]);
		String parserPath = new String(args[1]);
		String trainDataPath = new String(args[2]);
		String outputPath = new String(args[3]);
		
		SentimentScoreExtractor sentiwordnet = new SentimentScoreExtractor(pathToSWN, parserPath);
		sentiwordnet.processData(trainDataPath, outputPath);

		
		//System.out.println(sentiwordnet.extract("sick", "a"));

	}
}