import nltk
from nltk.corpus import inaugural,genesis
import nltk.tokenize as tokenize

#nltk.download()
a =inaugural.raw() # doctest: +ELLIPSIS


sents = tokenize.sent_tokenize(a)
print(len(sents))
sents=['<s>'+x.replace('\n','')+"</s>\n" for x in sents]
filtered = sents[0:100]
with open('hw3-my-test.txt','w+') as f:
    f.writelines(filtered)

'''inaugural.words('1789-Washington.txt')
inaugural.sents('1789-Washington.txt') # doctest: +ELLIPSIS
inaugural.paras('1789-Washington.txt') # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE'''