import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringReader;

import edu.stanford.nlp.process.Tokenizer;
import edu.stanford.nlp.process.TokenizerFactory;
import edu.stanford.nlp.process.CoreLabelTokenFactory;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.process.PTBTokenizer;
import edu.stanford.nlp.process.DocumentPreprocessor.DocType;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.Label;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.trees.*;
import edu.stanford.nlp.util.TypesafeMap.Key;
import edu.stanford.nlp.parser.common.ParserQuery;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import edu.stanford.nlp.parser.lexparser.Options;

public class YelpReviewParser {

	MemoryTreebank trainingData=null;
	
	public LexicalizedParser lp = null;
	public Options op = null;
	
	//aux items
	int sentenceCounter = 0;
	int wordCounter = 0;
	Set<String> nounTags;
	Set<String> verbTags;
	Set<String> adjTags;
	Set<String> advTags;
	Set<String> conjTags;
	Set<String> prepTags;
	Set<String> pronounTags;
	Set<String> modalTags;
	Set<String> articleTags;
	String countStr;
	String swStr;
	String sfStr; //min,max, average sentence length, ratio of max to min sen len
	
	YelpReviewParser(String cmd, String arg){
		if(cmd.equals("train")){
			System.out.println("creating training data treebank");
			
			op = setParserOptions();
			
			if(arg != null){
				trainingData=makeTreebank(arg);
			}	
			
			System.out.println("training parser");
			lp = LexicalizedParser.trainFromTreebank(trainingData, op);
		}
		else if(cmd.equals("parse")){
			//load parser
			lp = LexicalizedParser.getParserFromFile(arg, op);
			op = lp.getOp();
			
			//tag counting aux
			nounTags=new HashSet<String>();
			verbTags=new HashSet<String>();
			adjTags=new HashSet<String>();
			advTags=new HashSet<String>();
			conjTags=new HashSet<String>();
			prepTags=new HashSet<String>();
			pronounTags=new HashSet<String>();
			modalTags=new HashSet<String>();
			articleTags=new HashSet<String>();
			
			nounTags.add("NN");
			nounTags.add("NNP");
			nounTags.add("NNS");
			nounTags.add("NNPS");
			
			pronounTags.add("PRP");
			pronounTags.add("PRP$");
			pronounTags.add("WP");
			pronounTags.add("WP$");
			
			verbTags.add("VB");
			verbTags.add("VBD");
			verbTags.add("VBG");
			verbTags.add("VBN");
			verbTags.add("VBP");
			verbTags.add("VBZ");
			
			adjTags.add("JJ");
			adjTags.add("JJR");
			adjTags.add("JJS");
			
			advTags.add("RB");
			advTags.add("RBR");
			advTags.add("RBS");
			advTags.add("WRB");
			
			conjTags.add("CC");
			
			prepTags.add("IN");
			
			modalTags.add("MD");
			
			articleTags.add("DT");
			
		}
		
		
	}
	Options setParserOptions(){
		 Options op = new Options();
		 op.doDep = false;
		 op.doPCFG = true;
		 op.setOptions("-goodPCFG", "-evals", "tsv");
		 
		 return op;
	}
	
	void setTestingOptions(String prefix, String ext){
		//op.testOptions.writeOutputFiles = true;
		op.testOptions.outputFilesPrefix = new String(prefix);
		op.testOptions.outputFilesExtension = new String(ext);
		op.testOptions.verbose = false;
		//op.testOptions.testingThreads = 10;
	}
	
	MemoryTreebank makeTreebank(String path) {
	    System.err.println("Creating treebank dir: " + path);
	    Treebank tTreebank = op.tlpParams.diskTreebank();
	    System.err.print("Reading trees...");	    
	    
		tTreebank.loadPath(path);
		
		System.out.println("done [read " + tTreebank.size() + " trees].");
	    return convertToMembank(tTreebank);
	  }
	
	MemoryTreebank convertToMembank(Treebank tBank) {
		MemoryTreebank newTreebank = new MemoryTreebank();
		for(Tree treeInstance : tBank){
			
				newTreebank.add(treeInstance);				
			
	
		}
		return newTreebank;
		
	}

	List<Double> processReviews(String reviewsFilePath){
		
		final DocType docType = DocType.Plain;
		List<Double> scores = new ArrayList<Double>();
		DocumentPreprocessor documentPreprocessor = new DocumentPreprocessor(reviewsFilePath,docType,op.tlpParams.getInputEncoding());
		TreebankLanguagePack tlp = op.tlpParams.treebankLanguagePack();
		
		documentPreprocessor.setSentenceFinalPuncWords(tlp.sentenceFinalPunctuationWords());
	    documentPreprocessor.setEscaper(null);
	    documentPreprocessor.setSentenceDelimiter(null);
	    documentPreprocessor.setTagDelimiter(null);
	    documentPreprocessor.setElementDelimiter(null);
        documentPreprocessor.setTokenizerFactory(tlp.getTokenizerFactory());
		
        ParserQuery pq = lp.parserQuery();
        int num=0,numSents=0,numWords=0;
        HashMap<String, Double> posCounter;

        posCounter=new HashMap<String,Double>();
        posCounter.put("PRONOUN", 0.0);
        posCounter.put("NOUN",0.0);
        posCounter.put("MODALVERB", 0.0);
        posCounter.put("VERB", 0.0);
        posCounter.put("ADJECTIVE", 0.0);
        posCounter.put("ADVERB", 0.0);
        posCounter.put("CONJUNCTION", 0.0);
        posCounter.put("PREPOSITION", 0.0);
        posCounter.put("ARTICLE", 0.0);
        
        HashMap<String, Double> startsWithCounter;

        startsWithCounter=new HashMap<String,Double>();
        startsWithCounter.put("PRONOUN", 0.0);
        startsWithCounter.put("NOUN", 0.0);
        startsWithCounter.put("MODALVERB", 0.0);
        startsWithCounter.put("VERB", 0.0);
        startsWithCounter.put("ADJECTIVE", 0.0);
        startsWithCounter.put("ADVERB", 0.0);
        startsWithCounter.put("CONJUNCTION", 0.0);
        startsWithCounter.put("PREPOSITION", 0.0);
        startsWithCounter.put("ARTICLE", 0.0);
        
        List<Integer> senLen = new ArrayList<Integer>();
        for (List<HasWord> sentence : documentPreprocessor) {
          num++;
          numSents++;
          int len = sentence.size();
          senLen.add(len);
          numWords += len;
          System.out.println("Parsing [sent. " + num + " len. " + len + "]: " + Sentence.listToString(sentence, true));
          Tree parseOutput = lp.apply(sentence);
          scores.add(parseOutput.score());
          
         
          /*POS tags count code*/          
          int preterminal_count=0;
          for(Tree n : parseOutput){
        	  if(n.isPreTerminal()){
        		  
        		  String posTag=n.label().toString();
        		  if(nounTags.contains(posTag)){
        			  posCounter.put("NOUN", posCounter.get("NOUN")+1);
        			  if(preterminal_count==0)
        			  {
        				  startsWithCounter.put("NOUN", startsWithCounter.get("NOUN")+1);
        				  preterminal_count++;
        			  }
        		  }
        		  else if(verbTags.contains(posTag)){
        			  posCounter.put("VERB", posCounter.get("VERB")+1);
        			  if(preterminal_count==0)
        			  {
        				  startsWithCounter.put("VERB", startsWithCounter.get("VERB")+1);
        				  preterminal_count++;
        			  }
        		  }
        		  else if(adjTags.contains(posTag)){
        			  posCounter.put("ADJECTIVE", posCounter.get("ADJECTIVE")+1);
        			  if(preterminal_count==0)
        			  {
        				  startsWithCounter.put("ADJECTIVE", startsWithCounter.get("ADJECTIVE")+1);
        				  preterminal_count++;
        			  }
        		  }
        		  else if(advTags.contains(posTag)){
        			  posCounter.put("ADVERB", posCounter.get("ADVERB")+1);
        			  if(preterminal_count==0)
        			  {
        				  startsWithCounter.put("ADVERB", startsWithCounter.get("ADVERB")+1);
        				  preterminal_count++;
        			  }
        		  }
        		  else if(conjTags.contains(posTag)){
        			  posCounter.put("CONJUNCTION", posCounter.get("CONJUNCTION")+1);
        			  if(preterminal_count==0)
        			  {
        				  startsWithCounter.put("CONJUNCTION", startsWithCounter.get("CONJUNCTION")+1);
        				  preterminal_count++;
        			  }
        		  }
        		  else if(prepTags.contains(posTag)){
        			  posCounter.put("PREPOSITION", posCounter.get("PREPOSITION")+1);
        			  if(preterminal_count==0)
        			  {
        				  startsWithCounter.put("PREPOSITION", startsWithCounter.get("PREPOSITION")+1);
        				  preterminal_count++;
        			  }
        		  }
        		  else if(modalTags.contains(posTag)){
        			  posCounter.put("MODALVERB", posCounter.get("MODALVERB")+1);
        			  if(preterminal_count==0)
        			  {
        				  startsWithCounter.put("MODALVERB", startsWithCounter.get("MODALVERB")+1);
        				  preterminal_count++;
        			  }
        		  }
        		  else if(pronounTags.contains(posTag)){
        			  posCounter.put("PRONOUN", posCounter.get("PRONOUN")+1);
        			  if(preterminal_count==0)
        			  {
        				  startsWithCounter.put("PRONOUN", startsWithCounter.get("PRONOUN")+1);
        				  preterminal_count++;
        			  }
        		  }
        		  else if(articleTags.contains(posTag)){
        			  posCounter.put("ARTICLE", posCounter.get("ARTICLE")+1);
        			  if(preterminal_count==0)
        			  {
        				  startsWithCounter.put("ARTICLE", startsWithCounter.get("ARTICLE")+1);
        				  preterminal_count++;
        			  }
        		  }
        		  else{
        			 // System.out.println("tag dint match "+n.label());
        			  if(preterminal_count==0)
        			  {
        				  //starts with some other tag
        				  preterminal_count++;
        			  }
        		  }
        	  }
          }        
          //processResults(pq, numProcessed++, pwo);
        }
        
        //convert counts to string
        sentenceCounter=numSents;
        wordCounter=numWords;
        
        //changing to relative frequency
        countStr=new String("");
        if(wordCounter==0 || sentenceCounter==0){
        	countStr+=posCounter.get("NOUN")+"\t";
            countStr+=posCounter.get("VERB")+"\t";
            countStr+=posCounter.get("ADVERB")+"\t";
            countStr+=posCounter.get("ADJECTIVE")+"\t";
            countStr+=posCounter.get("PREPOSITION")+"\t";
            countStr+=posCounter.get("CONJUNCTION")+"\t";
            countStr+=posCounter.get("PRONOUN")+"\t";
            countStr+=posCounter.get("MODALVERB")+"\t";
            countStr+=posCounter.get("ARTICLE");
        }
        else{
        	countStr+=posCounter.get("NOUN")/wordCounter+"\t";
            countStr+=posCounter.get("VERB")/wordCounter+"\t";
            countStr+=posCounter.get("ADVERB")/wordCounter+"\t";
            countStr+=posCounter.get("ADJECTIVE")/wordCounter+"\t";
            countStr+=posCounter.get("PREPOSITION")/wordCounter+"\t";
            countStr+=posCounter.get("CONJUNCTION")/wordCounter+"\t";
            countStr+=posCounter.get("PRONOUN")/wordCounter+"\t";
            countStr+=posCounter.get("MODALVERB")/wordCounter+"\t";
            countStr+=posCounter.get("ARTICLE")/wordCounter;
        }
        swStr=new String("");
        if(wordCounter==0 || sentenceCounter==0){
        	 
             swStr+=startsWithCounter.get("NOUN")+"\t";
             swStr+=startsWithCounter.get("VERB")+"\t";
             swStr+=startsWithCounter.get("ADVERB")+"\t";
             swStr+=startsWithCounter.get("ADJECTIVE")+"\t";
             swStr+=startsWithCounter.get("PREPOSITION")+"\t";
             swStr+=startsWithCounter.get("CONJUNCTION")+"\t";
             swStr+=startsWithCounter.get("PRONOUN")+"\t";
             swStr+=startsWithCounter.get("MODALVERB")+"\t";
             swStr+=startsWithCounter.get("ARTICLE");
        }
        else{
        	 
             swStr+=startsWithCounter.get("NOUN")/sentenceCounter+"\t";
             swStr+=startsWithCounter.get("VERB")/sentenceCounter+"\t";
             swStr+=startsWithCounter.get("ADVERB")/sentenceCounter+"\t";
             swStr+=startsWithCounter.get("ADJECTIVE")/sentenceCounter+"\t";
             swStr+=startsWithCounter.get("PREPOSITION")/sentenceCounter+"\t";
             swStr+=startsWithCounter.get("CONJUNCTION")/sentenceCounter+"\t";
             swStr+=startsWithCounter.get("PRONOUN")/sentenceCounter+"\t";
             swStr+=startsWithCounter.get("MODALVERB")/sentenceCounter+"\t";
             swStr+=startsWithCounter.get("ARTICLE")/sentenceCounter;
        }
        
       
        
        //generate sentence features
        
        double minl=9999999,maxl=0;
        double avgl=0;double rtlen=0;
        if(sentenceCounter==0 || wordCounter==0){
        	avgl=0;
        	minl=0;maxl=0;
        	rtlen=0;
        }
        else{
        	avgl=wordCounter/sentenceCounter;
           	for(int len : senLen){
        		if(len<minl){
        			minl=len;
        		}
        		if(len>maxl){
        			maxl=len;
        		}
        	}
           	rtlen=maxl/minl;
        }
        
        sfStr=new String("");
        sfStr+=minl+"\t";
        sfStr+=maxl+"\t";
        sfStr+=avgl+"\t";
        sfStr+=rtlen;
		return scores;
	}
	void processData(String dataPath, String outputName){
		String line = "";
		String delimiter = "\t";
		
		BufferedReader br = null;
		BufferedWriter bw = null;
		BufferedWriter outWriter=null;
		
	//	DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd-HH:mm:ss");
		//get current date time with Date()
	//	Date date = new Date();
		String tmpfileName = new String("tmp-"+System.nanoTime()+".txt");
		//System.out.println(System.currentTimeMillis());
		//System.out.println(System.nanoTime());
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
			outWriter = new BufferedWriter(new FileWriter(outputName));
			String header=new String("");
			header+="id"+"\t"+"name"+"\t"+"review_count"+"\t"+"review_id"+"\t"+"review_date"+"\t"+"stars"+"\t"+"text"+"\t";
			header+="uname"+"\t"+"avg_stars"+"\t"+"user_cool"+"\t"+"user_funny"+"\t"+"user_useful"+"\t";
			header+="fans"+"\t"+"friend_count"+"\t"+"user_reviewcount"+"\t"+"yelp_startdate"+"\t"+"review_cool"+"\t"+"review_funny"+"\t"+"review_useful"+"\t";
			header+="parse_scores"+"\t"+"sentence_count"+"\t"+"word_count"+"\t"+"Num_nouns"+"\t"+"Num_verbs"+"\t"+"Num_advs"+"\t"+"Num_adjs"+"\t"+"Num_prep"+"\t"+"Num_conj"+"\t";
			header+="Num_pronouns"+"\t"+"Num_modals"+"\t"+"Num_articles"+"\t";
			header+="SW_nouns"+"\t"+"SW_verbs"+"\t"+"SW_advs"+"\t"+"SW_adjs"+"\t"+"SW_prep"+"\t"+"SW_conj"+"\t";
			header+="SW_pronouns"+"\t"+"SW_modals"+"\t"+"SW_articles"+"\t";
			header+="Min_sent_len"+"\t"+"Max_sent_len"+"\t"+"Avg_sent_len"+"\t"+"Ratio of max to min"+"\n";
			outWriter.write(header);
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		
		List<Double> scores = new ArrayList<Double>();
	 
		try {
	 
			br = new BufferedReader(new FileReader(dataPath));
			
			while ((line = br.readLine()) != null) {
				bw = new BufferedWriter(new FileWriter(tmpfileName));
			        // use comma as separator
				String[] fields = line.split(delimiter);
				//System.out.println(fields[6]);
				//List<Double> scores = parseReview(fields[6]);
				//System.out.println(scores);
				bw.write(fields[6]);
				bw.close();
				scores = processReviews(tmpfileName);
				String newRecord = new String(line+"\t"+scoresToString(scores)+"\t"+sentenceCounter+"\t"+wordCounter+"\t"+countStr+"\t"+swStr+"\t"+sfStr+"\n");
				outWriter.write(newRecord);
				wordCounter=0;
				sentenceCounter=0;
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

	String scoresToString(List<Double> scores){
		String scoreStr = new String();
		for (Double s : scores)
		{
			scoreStr += s + "$";
		}
		
		return scoreStr;
	}
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		String trainDataPath=null,testDataPath=null,parserName=null,outputName=null;
		
		//cmds - train, parse
		String cmd=new String(args[0]);
		if(cmd.equals("train")){
			trainDataPath=new String(args[1]);
			parserName=new String(args[2]);
			
			//create and train parser on given training data
			YelpReviewParser yp = new YelpReviewParser(cmd,trainDataPath);
			
			//save parser
			yp.lp.saveParserToSerialized(parserName);
		}
		else if(cmd.equals("parse")){
			
			parserName=new String(args[1]);
			testDataPath=new String(args[2]);
			outputName=new String(args[3]);
			
			//parserName="edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz";
			//testDataPath="/home/vidhoonv/Desktop/sample-data.tsv";
			//outputName="/home/vidhoonv/Desktop/pcfg-features.tsv";
			
			//load given parser and create test data
			YelpReviewParser yp = new YelpReviewParser(cmd,parserName);
			
			yp.processData(testDataPath,outputName);
		}
		
		
		
		
		return;
	}

}
