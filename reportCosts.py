#!/usr/bin/env python3
"""
reportCosts.py: Read TSV receipts from ./Database and output the most expensive
keywords.

The TSVs are slightly processed input and consist of <receipt item
text>\t<price number in USD>. Price can be NaN.

"""

import os
import math
import collections
import operator
import random

import tsv
        
def main():

    # Where do we put them?
    DATABASE_PATH = 'Database'
    
    # This holds total price by keyword, for all observed keywords
    total_by_keyword = collections.defaultdict(float)
    occurrences = collections.Counter()
    
    # This holds an example for each keyword
    examples = dict()

    for root, dirs, files in os.walk(DATABASE_PATH):
        for filename in files:
            if filename.endswith('.tsv'):
                # We found a TSV
                
                with open(os.path.join(root, filename)) as tsv_in:
                    # Read the TSV
                    reader = tsv.TsvReader(tsv_in)
                    
                    for item, price in reader:
                        # For each recorded item
                        # Parse the price
                        price = float(price)
                        
                        if math.isnan(price):
                            # Skip unpriceable items
                            continue
                            
                        # Compute all unique keywords in the item
                        keywords = set(item.upper().split())
                        
                        for keyword in keywords:
                            # The price contributes to every keyword
                            total_by_keyword[keyword] += price
                            # We count the occurrences
                            occurrences[keyword] += 1
                            if keyword not in examples or random.random() < 0.5:
                                # This ought to be our example for this keyword
                                examples[keyword] = item.upper()
                        
    # Make a big table
    keywords_with_totals = list(total_by_keyword.items())
    # Sort by total cost, descending
    keywords_with_totals.sort(key=operator.itemgetter(1), reverse=True)
    
    print("=== Top 10 Expensive Grocery Keywords ===")
    for i, (keyword, cost) in enumerate(keywords_with_totals[:10]):
        print("#{}:\t${}\t{} (x{}, e.g. \"{}\")".format(i + 1, cost, keyword, occurrences[keyword], examples[keyword]))
            
if __name__ == "__main__":
    main()
