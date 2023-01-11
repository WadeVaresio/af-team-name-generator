import heapq
import silabeador as sil
import spacy
from pyphonetics import RefinedSoundex
from sys import argv


# generates syllable permutations for better matching (silabeador sometimes breaks up words wierdly -> bad pun matching)
# radiohead -> [ra, dio, he, ad] (silabeador)
# Better breakup -> [ra, dio, head] 
# Also possible breakup -> [radio, head] (pun might become 'radio HUD')
# Permute generates all possible permutations by combining the more 'atomic' syllables from silabeador
# [ra, dio, he, ad]
# [radio, he, ad]
# [ra, dio, head]
# [radio, head]
# etc...
def permute(name):
  syllables = sil.syllabify(name)
  permutations = [syllables]

  for i in range(0, len(syllables)):
    permutations.append(syllables[0:i] + [''.join(syllables[i:i+2])] + syllables[i+2:])
#     if permutations[0] == permutations[-1]:
#     permutations.pop()

  return permutations


def score_lev(str1, str2):
  rs = RefinedSoundex()
  return rs.distance(str1, str2)


def score_spacy(str1, str2):
  return nlp(str1).similarity(nlp(str2))

def compute(name, method, top_n, recurse, puns=[]):
  # stores top pun matches
  ranking = []

  with open('terms.txt', 'r') as f:
    # all terms
    terms = [term.lower() for term in f]

    # names might be multiple words, aka 'parts', i.e. 'Pearl Jam' -> ['pearl', 'jam']
    # Each part is treated separately
    for k, part in enumerate(name):
      perms = permute(part)

      for perm in perms:

        for i, syllable in enumerate(perm):
          # get the best pun match for this syllable
          for term in terms:
            if method == 'spacy':
              score = score_spacy(term, syllable)
            elif method == 'lev':
              score = score_lev(term, syllable)

            heapq.heappush(ranking, (score, term))

          # get x highest rated scores
          if method == 'spacy':
            top = heapq.nlargest(top_n, ranking, key=lambda x: x[0])
          elif method == 'lev':
            top = heapq.nsmallest(top_n, ranking, key=lambda x: x[0])

          # stores the recombined name/pun replaced name with no dupes
          new_names = set() 
          for t in top:
            # new_names.add(''.join(perm[0:i]) + '[' + t[1].rstrip() + ']' + ''.join(perm[i+1:]))

            new_names.add((t[0], ''.join(perm[0:i]) + t[1].rstrip() + ''.join(perm[i+1:])))

          # preserves names with mulitple words/parts
          # i.e. Pearl Jam -> Perl Jam (Jam is preserved)
          # i.e. Pearl Jam -> Pearl Gem (Pearl is preserved)
          # i.e. Pearl Jam -> Perl Gem (shouldn't be possible)
          for nn in new_names:
            printable_name = name[0:k] + [nn[1]] + name[k+1:]
            puns.append(" ".join(printable_name))

  if recurse:
    return compute(name=printable_name, method=method, top_n=top_n, recurse=False, puns=puns)
  else:
    return puns



# load scorer
nlp = spacy.load('en_core_web_md')
#nlp = en_core_web_md.load()

if __name__ == "__main__":
  scorer, top_n, recurse = argv[1], int(argv[2]), argv[3]

  band_name = input("Enter input: ").split()

  if recurse.lower() == 'yes':
    print(compute(name=band_name, method=scorer, top_n=top_n, recurse=True))
  else:
    print(compute(name=band_name, method=scorer, top_n=top_n, recurse=False))
