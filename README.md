# Receipts: Easy Receipt Processing

"Receipts" is a system to organize your receipts and tell you want you spend money on. It operates on the principle that OCR errors are randomly distributed, while what you buy has real trends in it.

## Installation

```
pip3 install tsv
git clone https://github.com/interfect/receipts.git
cd receipts
```

## Usage

1. Scan your receipts as PDF files into the Inbox folder.

2. Use [gImageReader](https://github.com/manisandro/gImageReader) to OCR the part of your receipt that has actual items. Each line ought to be an item with a price last. Save the result as a .txt next to the .pdf for each receipt.

3. Run `./processReceipts.py` to analyze the items on the receipts and mopve them from the Inbox folder to the Database folder.

4. Run `./reportCost.py` to see your top 10 expensive keywords, with total prices, counts and example items:

```
=== Top 10 Expensive Grocery Keywords ===
#1:	$16.45	ORG (x5, e.g. "PWR 7 JHICE ORG 33.8 UZ")
#2:	$13.96	PILLAR (x2, e.g. "PILLAR UANDLE 3X3")
#3:	$12.96	PASTA (x4, e.g. "PASTA CAPELLINT")
#4:	$11.17	CHEDDAR (x3, e.g. "SLICEG SHARP CHEDDAR")
#5:	$10.07	SWEET (x3, e.g. "SWEET CURN TAMALES")
#6:	$9.99	CAPELLINT (x1, e.g. "PASTA CAPELLINT")
#7:	$9.98	COLUMB (x2, e.g. "SLCD CHICKEN BRST RSTED COLUMB")
#8:	$9.98	BRST (x2, e.g. "SLCD CHICKEN BRST RSTED COLUMB")
#9:	$9.98	CHICKEN (x2, e.g. "SLGD CHICKEN BRST ROTEN COLUMB =")
#10:	$8.97	MUSHROOMS (x3, e.g. "MUSHROOMS CRIMINT GRG 8 OZ")
```

My OCR data in this example is relatively poor, but frim just 2 receipts we can already see that organic things are expensive and numerous at Trader Joe's.





