#!/usr/bin/env python3
"""
processReceipts.py: Clean and file input receipts from ./Inbox into ./Database.

Receipts must already be OCR'd and saved as <name>.pdf and <name>.txt, with the
TXT just being the items and prices, one per line, prices last.

It is recommended to use gImageReader for this.

The database will hold .pdf, .txt, and .tsv files for each receipt, filed
year/month/day, and with unique names.

The TSVs are slightly processed input and consist of <receipt item
text>\t<price number in USD>

"""

import os
import time
import shutil
import re
import uuid
import math

import tsv

def get_new_id(data_dir):
    """
    Produce a new unique ID for a receipt, amond the receipts in the given
    folder.
    """
    
    # A UUID is always unique
    return str(uuid.uuid4())
    
def move (src_path, dest_path):
    """
    Move a file from one place to another
    """
    
    print("Move {} to {}".format(src_path, dest_path))
    shutil.move(src_path, dest_path)
    
def parse_items(lines):
    """
    Read in receipt items, one per line, with prices last.
    
    Prices may have ',' for '.' or other OCR errors.
    
    Produce pairs of (item text, corrected price).
    
    The item string will not contain tab, and the price will be NaN if not
    obtainable.
    """
    
    for line in lines:
        line = line.strip()
        
        if line.endswith('T') or line.endswith(' 7'):
            # This is just a taxable item. Drop the T
            line = line[:-1].strip()
        
        if line == "":
            # Skip blank lines
            continue
            
        if line.startswith('[File'):
            # Skip OCR info lines from gImageReader
            continue
        
        price_match = re.search('([0-9]+[.,-:][0-9][0-9])$', line)
        
        if not price_match:
            # We have no idea where the price is
            print("Warning: unable to find a price in: {}".format(line))
            item_string = line
            price_float = float('NaN')
        else:
            # We found the price, so pull out it and the item
            price_string = price_match.group(1).replace(',', '.').replace('-', '.').replace(':', '.')
            item_string = line[:-len(price_string)].strip()
            price_float = float(price_string)
            
        # Drop any tabs
        item_string.replace('\t', ' ')
        
        yield (item_string, price_float)
            
            
        
        
def main():

    # Wehre do we find receipts to import
    INBOX_PATH = 'Inbox'
    # Where do we put them?
    DATABASE_PATH = 'Database'
    

    if not os.path.exists(INBOX_PATH):
        os.makedirs(INBOX_PATH)
        
    if not os.path.exists(DATABASE_PATH):
        os.makedirs(DATABASE_PATH)

    # All imported receipts will be assigned to today, no matter when they were made
    date_string = time.strftime('%Y/%m/%d')
    
    # Determine where to put today's receipts
    dest_dir = os.path.join(DATABASE_PATH, date_string)

    # Find all the inbox files
    inbox_files = list(os.listdir(INBOX_PATH))
    
    # Find all the TXTs
    txt_files = [f for f in inbox_files if f.lower().endswith('.txt')]
    # And the PDFs
    pdf_files = [f for f in inbox_files if f.lower().endswith('.pdf')]
    
    # TODO: Check for duplicates in different cases of the same extension
        
    # File them by basename
    txt_by_basename = {f[:-4]: f for f in txt_files}
    pdf_by_basename = {f[:-4]: f for f in pdf_files}
    
    # Count imported receipts
    import_count = 0
    
    for basename in txt_by_basename.keys():
        if basename not in pdf_by_basename:
            print("Warning: {} exists but PDF is missing. Skipping!".format(txt_by_basename[basename]))
        
        # Find the pair of files
        txt_filename = os.path.join(INBOX_PATH, txt_by_basename[basename])
        pdf_filename = os.path.join(INBOX_PATH, pdf_by_basename[basename])
        
        if not os.path.exists(dest_dir):
            # Make sure the destination directory exists
            os.makedirs(dest_dir)
            
        # Get a new unique receipt ID
        # This is super N^2, but you should not have large N receipts for one day.
        receipt_id = get_new_id(dest_dir)
        
        # Where do we put the raw OCR text
        dest_txt_filename = os.path.join(dest_dir, '{}.txt'.format(receipt_id))
        # And the processed items
        dest_tsv_filename = os.path.join(dest_dir, '{}.tsv'.format(receipt_id))
        # And the PDF
        dest_pdf_filename = os.path.join(dest_dir, '{}.pdf'.format(receipt_id))
        
        # Count the items
        item_count = 0
        # And the price
        total_price = 0.0
        
        # Create the TSV
        with open(txt_filename, 'r') as text_in:
            with open(dest_tsv_filename, 'w') as tsv_out:
                # Prepare a TSV writer
                writer = tsv.TsvWriter(tsv_out)
                
                for item, price in parse_items(text_in):
                    # Save each item and its price
                    writer.line(item, str(price))
                    
                    item_count += 1
                    if not math.isnan(price):
                        total_price += price
                    
        # Move the other files
        move(txt_filename, dest_txt_filename)
        move(pdf_filename, dest_pdf_filename)
        
        print('Imported {} items with total price {} as {}'.format(item_count, total_price, receipt_id))
        
        import_count += 1
        
    print("Imported {} receipts".format(import_count))
            
if __name__ == "__main__":
    main()
