import glob
from habanero import Crossref
import sys
import os
from pathlib import Path
wd = Path(os.getcwd())
sys.path.insert(1, f'{wd.parent.parent.absolute()}/utils')
from preprocessing import *

cr = Crossref()
#homedir = '/home/jovyan/'
homedir = os.getcwd() + '/'
bib_files = glob.glob(homedir + '*.bib')
paper_aux_file = glob.glob(homedir + '*.aux')
paper_bib_file = 'library_paper.bib'
try:
    tex_file = glob.glob(homedir + "*.tex")[0]
except:
    print('No optional .tex file found.')

yourFirstAuthor = 'Stiso, Jennifer '
yourLastAuthor = 'Bassett, Dani '
optionalEqualContributors = ['Zhou, Dale']
checkingPublishedArticle = False

## end of user input
if paper_aux_file:
    find_unused_cites(paper_aux_file)

bib_data = get_bib_data(bib_files[0])
if checkingPublishedArticle:
    get_names_published(homedir, bib_data, cr)
else:
    # find and print duplicates
    bib_data = get_duplicates(bib_data, bib_files[0])
    # get names, remove CDS, find self cites
    get_names(homedir, bib_data, yourFirstAuthor, yourLastAuthor, optionalEqualContributors, cr)