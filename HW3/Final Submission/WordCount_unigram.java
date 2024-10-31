import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.util.Map;
import java.util.TreeMap;
import java.util.Arrays;


public class WordCount_unigram {
    
   public static class TokenizerMapper extends Mapper<Object, Text, Text, Text>
   {
      private Text word = new Text(); 
      private Text word2 = new Text();      
      private Text mapDetails = new Text();
      private final String[] bigrams = {"computer science", "information retrieval", "power politics", "los angeles", "bruce willis"};
                                         
      public void map(Object key, Text value, Context context) throws IOException, InterruptedException 
      {
          String[] parts = value.toString().toLowerCase().split("\t", 2);

          String cleanedLine = parts[1].replaceAll("[^a-z]+", " ");
          
          StringTokenizer itr = new StringTokenizer(cleanedLine);

          while (itr.hasMoreTokens()) 
               {
                  mapDetails.set(parts[0] + ":" + 1);
                   word.set(itr.nextToken());
                  context.write(word, mapDetails);
               }
      }
   }

   public static class StringReducer extends Reducer<Text,Text,Text,Text> 
   {
      private final Text result = new Text();
      public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException 
      {
          Map<String, Integer> hashMap = new TreeMap<>();
          for (Text value : values) {
              String[] line = value.toString().split(":");
              String docId = line[0];
              int count = Integer.parseInt(line[1].trim());
              hashMap.put(docId, hashMap.getOrDefault(docId, 0) + count);
          }
          
          StringBuilder sb = new StringBuilder();
          for (Map.Entry<String, Integer> entry : hashMap.entrySet()) {
              sb.append(entry.getKey()).append(":").append(entry.getValue()).append(" ");
          }
          result.set(sb.toString());
          context.write(key, result);
      }
   }

   public static void main(String[] args) throws Exception 
   {
      Configuration conf = new Configuration();
      Job job = Job.getInstance(conf, "word count");

      job.setJarByClass(WordCount_unigram.class);
      job.setMapperClass(TokenizerMapper.class);
      job.setCombinerClass(StringReducer.class);
      job.setReducerClass(StringReducer.class);

      job.setOutputKeyClass(Text.class);
      job.setOutputValueClass(Text.class);

      FileInputFormat.addInputPath(job, new Path(args[0]));
      FileOutputFormat.setOutputPath(job, new Path(args[1]));

      System.exit(job.waitForCompletion(true) ? 0 : 1);
   }
}

