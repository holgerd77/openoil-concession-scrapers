# -*- coding: utf-8 -*-
# Script for downloading/renaming pdf files from ftp.perupetro.com.pe
# Usage: 'python pe_perupetro_pdf_download.py [start (optional, 1 ~ first content row)]'
#
# Expects a file 'pe_contracts.csv' in 'scripts' folder with two columns:
# Column 1: File URL (e.g. ftp://extlegal@ftp.perupetro.com.pe/LOTE 1 AB/L 1AB-1.pdf)
# Column 2: File Name without .pdf ending (e.g. pe_1-AB_dd19860323_EXPLOTACION-LICENCIA_Pluspetrol)
import csv, os, sys
import urllib2
from dbupload import DropboxConnection

dropbox_user = ''
dropbox_password = ''

download_path = 'download/pe_perupetro_pdf/'
csv_path      = 'scripts/pe_contracts.csv'

if len(sys.argv) <= 1:
    start = 1
else:
    start = int(sys.argv[1])
print "Starting at content row %s." % start

if not os.path.exists(download_path):
    os.makedirs(download_path)
    print "Creating new directory '%s' for download..." % download_path
else:
    print "Using existing directory '%s' for download..." % download_path

if not os.path.exists(csv_path):
    sys.exit("CSV file '%s' not found!" % csv_path)
else:
    print "Using CSV file '%s' for URLs and file names..." % csv_path

print "Reading CSV file..."

with open(csv_path, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    cnt = 0
    for row in reader:
        cnt += 1
        if cnt <= start + 1:
            continue
        url = row[0]
        url = url.replace(' ', '%20')
        name = row[1] + '.pdf'
        if url == '':
            print "Omitting row, no URL available."
        else:
            file_path = os.path.join(download_path, name)
            u = urllib2.urlopen(url)
            f = open(file_path, 'wb')
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])
            print "Downloading: %s Bytes: %s" % (url, file_size)

            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status = status + chr(8)*(len(status)+1)
                print status,
            print "File saved as '%s'." % file_path
            f.close()

            print "Uploading file to Dropbox..."
            conn = DropboxConnection(dropbox_user, dropbox_password)
            conn.upload_file(file_path, '/Petroleum Contracts/', name)
            print "File uploaded to Dropbox."





