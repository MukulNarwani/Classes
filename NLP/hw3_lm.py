import sys
from collections import Counter
from functools import reduce 
import operator
import numpy as np
import random 
import re
import statistics

class LanguageModel:

  UNK = "<UNK>"
  SENT_BEGIN = "<s>"
  SENT_END = "</s>"
  """
  multigram_count is the count of all the sentence when they've been
  formatted to be compatible with the n_gram
  """
  multigram_count = {}
  """"
  Unigram_count is the count of all the tokens in the sentence
  """
  unigram_count = {}
  
  def __init__(self, n_gram, is_laplace_smoothing):
    """Initializes an untrained LanguageModel
    Parameters:
      n_gram (int): the n-gram order of the language model to create
      is_laplace_smoothing (bool): whether or not to use Laplace smoothing
    """
    self.n_gram=n_gram
    self.is_laplace_smoothing=is_laplace_smoothing


  def train(self, training_file_path):
    """Trains the language model on the given data. Assumes that the given data
    has tokens that are white-space separated, has one sentence per line, and
    that the sentences begin with <s> and end with </s>
    Parameters:
      training_file_path (str): the location of the training data to read
    Returns:
    None
    """        
    with open(training_file_path) as file:
      data = file.read()

      #first pass- Replace unknown words with <UNK>
      self.unigram_count = Counter(data.split())
      #calculate vocab before replacing with Unk

      least_common = self.unigram_count.most_common()
      i=0
      least_common.reverse()
      #Checks the least common keys if they occur only once
      while least_common[i][1]==1:
        unk = least_common[i][0]
        if not(unk == '</s>' or unk == '<s>'):
          data=re.sub(r'\b'+unk+r'\b','<UNK>',data)
        i+=1
   
      #train model after replacing UNKs 
      n_gramed_sentences = []
      self.unigram_count = Counter(data.split())
      sentences = data.split('\n')
      for sentence in sentences:
        words = sentence.split()
        n_gramed_sentences.extend(self.make_n_gram_list(words))
      self.vocab = len(self.unigram_count.keys()) 
      self.multigram_count = Counter(n_gramed_sentences)
      self.probabilities = {n_gram: self.score(n_gram) for n_gram, _ in self.multigram_count.items()}


  def make_n_gram_list(self,sentences):
    """Converts the sentence into an appropriate structre for the required n_gram
    Parameters: 
      sentences: tokenized sentence. ie: A list of words
    """
    
    n_gramed_sentences=[]
    for i in range(len(sentences)-self.n_gram+1):
      n_gramed_sentences.append(" ".join(sentences[i:i+self.n_gram])) 
    return n_gramed_sentences

  def score(self, sentence):
    """Calculates the probability score for a given string representing a single sentence.
    Parameters:
      sentence (str): a sentence with tokens separated by whitespace to calculate the score of
    Returns:
      float: the probability value of the given string for this model
    """
    tokenized = sentence.split()
    for i,token in enumerate(tokenized):
      if not(token in self.unigram_count.keys()):
        tokenized[i]='<UNK>'
    score = self.getScore(tokenized)
    #print(score)
    return reduce(operator.mul, score)


  def getScore(self,words):
    """Generates a  list of scores given a tokenized sentence
    Parameters:
      words (list): A list representing the words of a sentence
    Returns:
      list: a list of scores for each n_gram in the sentence 
    """
    scores = []
    vocab = self.vocab if self.is_laplace_smoothing else 0
    addOne=1 if self.is_laplace_smoothing else 0
    n_gram_list = self.make_n_gram_list(words)
    for n_gram in n_gram_list:
      word = n_gram.split()[0]  
      denominator = sum(self.multigram_count.values()) if self.n_gram == 1 else self.unigram_count[word]
      word_prob = (self.multigram_count[n_gram]+addOne)/(denominator+vocab)
      scores.append(word_prob)
    '''print('Numerator',self.multigram_count[n_gram])
    print('denominator',denominator)
    print(vocab)'''
    return scores



  def generate_sentence(self):
    """Generates a single sentence from a trained language model using the Shannon technique.
    Returns:
      str: the generated sentence
    """
    sentence = "<s>"
    while not('</s>' in sentence):
      if self.n_gram == 2:
        n_grams = self.ngrams_startingwith(sentence.split()[-1])
        choices = {n_gram: self.probabilities[n_gram] for n_gram in n_grams} 
      else:
            choices = self.probabilities
      choice= random.choices(list(choices.keys()),weights = choices.values())[0]    
      sentence= sentence + " " +(choice) 
    #would not work for some reason
    #start=re.compile('<.*?s>')
    #Removes all the STAR and STOP tokens from the sentence, and then adds them at the begginning/end
    start=re.compile('(\s+)*<s>(\s+)*')
    stop=re.compile('(\s+)*</s>(\s+)*')
    sentence=re.sub(stop,' ',(re.sub(start, ' ', sentence)))
    
    sentence_start="</s>"+"".join(['</s>' for _ in range(2,self.n_gram)])
    sentence_end="</s>"+"".join(['</s>' for _ in range(2,self.n_gram)])
    sentence=sentence_start+sentence+sentence_end
    return sentence


  def ngrams_startingwith(self,start):
    """Genereates a list of n_grams that begin with the given word.
    Parameters:
      start(str): the first token in the n_gram
    Returns:
      list: A list of n_grams that begin with the given word
    """
    return [n_gram  for n_gram in list(self.multigram_count.keys()) if n_gram.startswith(start)]


  def generate(self, n):
    """Generates n sentences from a trained language model using the Shannon technique.
    Parameters:
      n (int): the number of sentences to generate
      
    Returns:
      list: a list containing strings, one per generated sentence
    """
    return [self.generate_sentence() for _ in range(n)]

  def perplexity(self, test_sequence):
    """Measures the perplexity for the given test sequence with this trained model. 
              As described in the text, you may assume that this sequence 
              may consist of many sentences "glued together".
    Parameters:
      test_sequence (string): a sequence of space-separated tokens to measure the perplexity of
    Returns:
      float: the perplexity of the given sequence
    """ 
    


def main():
  # TODO: implement
  models={'unigram':1,'bigram':2}
  for key,value in models.items():
    print('Model: {0}, laplace smoothed'.format(key))
    lm = LanguageModel(value,True)
    training_path = sys.argv[1]
    testing_path1 = sys.argv[2]
    testing_path2 = sys.argv[3]
    
    #Genereate 50 sentences
    lm.train(training_path)
    print('Sentences:')
    sentences=lm.generate(50)
    print(*sentences,sep='\n')
    #TestFile1
    print('test corpus: ',testing_path1)
    with open(testing_path1) as f:
      sentences = f.read().split('\n')
      sentences = list(filter(None, sentences))
      NO_OF_SENTENCES1=len(sentences)
    print('# of sentences: ',NO_OF_SENTENCES1)
    scores=[]
    for sent in sentences:
      if sent:
        #print(sent)
        scores.append(lm.score(sent))
    mean = statistics.mean(scores)
    stdev = statistics.stdev(scores)
    
    print('mean',str(mean))
    print('stdev',str(stdev))

    #TestFile2
    print('test corpus: ',testing_path2)
    with open(testing_path2) as f:
      NO_OF_SENTENCES2=len(f.read().split('\n'))
    print('# of sentences: ',NO_OF_SENTENCES2)
    scores=[]
    for sent in sentences:
      if sent:
        scores.append(lm.score(sent))
    mean = statistics.mean(scores)
    stdev = statistics.stdev(scores)
    
    print('mean',str(mean))
    print('stdev',str(stdev))



if __name__ == '__main__':
  
  # make sure that they've passed the correct number of command line arguments
  '''if len(sys.argv) != 4:
    print("Usage:", "python hw3_lm.py training_file.txt testingfile1.txt testingfile2.txt")
    sys.exit(1)
  #main()
  '''
  lm = LanguageModel(3,True)
  lm.train("training_files/unknowns_mixed.txt")
  lm.generate_sentence()
  #print(lm.score("<s> flamingo"))
  #print(lm.getScore(("<s> flamingo").split()))
  #lm.score('<s> i')
  