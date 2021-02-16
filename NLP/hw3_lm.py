# imports go here
import sys

"""
Don't forget to put your name and a file comment here
"""


# Feel free to implement helper functions

class LanguageModel:
  # constants to define pseudo-word tokens
  # access via self.UNK, for instance
  UNK = "<UNK>"
  SENT_BEGIN = "<s>"
  SENT_END = "</s>"

  def __init__(self, n_gram, is_laplace_smoothing):
    """Initializes an untrained LanguageModel
    Parameters:
      n_gram (int): the n-gram order of the language model to create
      is_laplace_smoothing (bool): whether or not to use Laplace smoothing
    """
    pass


  def train(self, training_file_path):
    """Trains the language model on the given data. Assumes that the given data
    has tokens that are white-space separated, has one sentence per line, and
    that the sentences begin with <s> and end with </s>
    Parameters:
      training_file_path (str): the location of the training data to read

    Returns:
    None
    """
    pass

  def score(self, sentence):
    """Calculates the probability score for a given string representing a single sentence.
    Parameters:
      sentence (str): a sentence with tokens separated by whitespace to calculate the score of
      
    Returns:
      float: the probability value of the given string for this model
    """
    pass

  def generate_sentence(self):
    """Generates a single sentence from a trained language model using the Shannon technique.
      
    Returns:
      str: the generated sentence
    """
    pass

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
  training_path = sys.argv[1]
  testing_path1 = sys.argv[2]
  testing_path2 = sys.argv[3]
  
  pass

    
if __name__ == '__main__':
    
  # make sure that they've passed the correct number of command line arguments
  if len(sys.argv) != 4:
    print("Usage:", "python hw3_lm.py training_file.txt testingfile1.txt testingfile2.txt")
    sys.exit(1)

  main()

