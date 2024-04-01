from collections import Counter
def duplicate_character(input):
# creating the dictionary by using counter method having strings as key and its frequencies as value
   string = Counter(input)
   # Find the number of occurrence of a character and getting the index of it.
   for char, count in string.items():
      if (count > 1):
         print(char)
# Driver code
if __name__ == "__main__":
   input = 'folio'
   duplicate_character(input)
