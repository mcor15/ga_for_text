# Simplistic Genetic Algorithm for Text
---
This is a simplistic [genetic algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm) for evolving target text from random solutions in Python 3. The fitness function uses the sum of the absolute “ascii” distances between the answer character and evolving solution. This means that this is a minimization problem, solutions with lower fitnesses are favoured over ones with higher fitnesses. 
---
## Usage
The usage of the module is as follows. 

```ga_for_text.py  “string-to-evolve-for” size-of-population -gen_num optional-number-of-generations, default 50```

Module will then evolve populations of solutions until the target is found or the number of generations is reached. Then the result will be printed out.
