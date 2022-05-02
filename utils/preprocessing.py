import subprocess
from pylatexenc.latex2text import LatexNodes2Text
import unicodedata

def checkcites_output(aux_file):
    '''take in aux file for tex document, return list of citation keys
    that are in .bib file but not in document'''

    result = subprocess.run(['texlua', 'checkcites.lua', aux_file[0]], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')
    unused_array_raw = result.split('\n')
    # process array of unused references + other output
    unused_array_final = list()
    for x in unused_array_raw:
        if len(x) > 0: # if line is not empty
            if x[0] == '-':  # and if first character is a '-', it's a citation key
                unused_array_final.append(x[2:]) # truncate '- '
    if "------------------------------------------------------------------------" in unused_array_final:
        return result
    else:
        return unused_array_final

def clean_name(name, flag):
    """

    :param name:
            flag: utf or latex
    :return: clean_name
    """
    if flag=='latex':
        clean_name = convertLatexSpecialChars(str(name)[7:-3]).replace(
            "', Protected('", ""
        ).replace(
            "'), '", ""
        )
    elif flag=='utf':
        clean_name = convertSpecialCharsToUTF8(str(name)[7:-3]).replace(
            "', Protected('", ""
        ).replace(
            "'), '", ""
        )
    else:
        raise ValueError

def removeMiddleName(line):
    """

    :param line:
    :return:
    """
    arr = line.split()
    last = arr.pop()
    n = len(arr)
    if n == 4:
        first, middle = ' '.join(arr[:2]), ' '.join(arr[2:])
    elif n == 3:
        first, middle = arr[0], ' '.join(arr[1:])
    elif n == 2:
        first, middle = arr
    elif n==1:
        return line
    return str(first + ' ' + middle)


def returnFirstName(line):
    """

    :param line:
    :return:
    """
    arr = line.split()
    n = len(arr)
    if n == 4:
        first, middle = ' '.join(arr[:2]), ' '.join(arr[2:])
    elif n == 3:
        first, middle = arr[0], ' '.join(arr[1:])
    elif n == 2:
        first, middle = arr
    elif n==1:
        return line
    return str(middle)


def convertLatexSpecialChars(latex_text):
    """

    :param latex_text:
    :return:
    """
    return LatexNodes2Text().latex_to_text(latex_text)


def convertSpecialCharsToUTF8(text):
    """

    :param text:
    :return:
    """
    data = LatexNodes2Text().latex_to_text(text)
    return unicodedata.normalize('NFD', data).encode('ascii', 'ignore').decode('utf-8')

def namesFromXrefSelfCite(doi, title):
    """

    :param doi:
    :param title:
    :return:
    """
    selfCiteCheck = 0
    # get cross ref data
    authors = ['']
    # first try DOI
    if doi != "":
        works = cr.works(query=title, select=["DOI", "author"], limit=1, filter={'doi': doi})
        if works['message']['total-results'] > 0:
            authors = works['message']['items'][0]['author']

    for i in authors:
        if i != "":
            first = i['given'].replace('.', ' ').split()[0]
            last = i['family'].replace('.', ' ').split()[0]
            authors = removeMiddleName(last + ", " + first)
            if authors in removeMiddleName(yourFirstAuthor) or authors in removeMiddleName(
                    convertSpecialCharsToUTF8(yourFirstAuthor)) or authors in removeMiddleName(
                    yourLastAuthor) or authors in removeMiddleName(convertSpecialCharsToUTF8(yourLastAuthor)):
                selfCiteCheck += 1
    return selfCiteCheck


def find_unused_cites(paper_aux_file):
    """

    :param paper_aux_file: path to auxfile
    :return:
    """
    print(checkcites_output(paper_aux_file))
    unused_in_paper = checkcites_output(paper_aux_file)  # get citations in library not used in paper
    print("Unused citations: ", unused_in_paper.count('=>'))

def get_bib_data(homedir):
    """

    :param homedir: home directory
    :return: bib_data
    """
    ID = glob.glob(homedir + '*bib')
    with open(ID[0]) as bibtex_file:
        bib_data = bibtexparser.bparser.BibTexParser(common_strings=True,
                                                     ignore_nonstandard_types=False).parse_file(bibtex_file)
    return bib_data

def get_duplicates(bib_data):
    """
    take bib_data, and get duplicates
    :param homedir: home directory
    :return:
    """

    duplicates = []
    for key in bib_data.entries_dict.keys():
        count = str(bib_data.entries).count("'ID\': \'" + key + "\'")
        if count > 1:
            duplicates.append(key)

    if len(duplicates) > 0:
        raise ValueError("In your .bib file, we found and removed duplicate entries for:",
                         ' '.join(map(str, duplicates)))


def get_names_published(outPath, bib_data):
    """
    whole pipeline for published papers
    :return: FA,
            LA
    """
    FA = []
    LA = []
    counter = 1
    selfCiteCount = 0
    titleCount = 1  #
    counterNoDOI = list()  # row index (titleCount) of entries with no DOI
    outPath = homedir + 'cleanedBib.csv'

    if os.path.exists(outPath):
        os.remove(outPath)

    with open(outPath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Article', 'FA', 'LA', 'Title', 'SelfCite', 'CitationKey'])

    citedArticleDOI = list()
    citedArticleNoDOI = list()
    allArticles = list()
    for entry in bib_data.entries:
        my_string = entry['cited-references'].split('\n')
        for citedArticle in my_string:
            allArticles.append(citedArticle)
            if citedArticle.partition("DOI ")[-1] == '':
                citedArticleNoDOI.append(citedArticle)
                counterNoDOI.append(titleCount)
            else:
                line = citedArticle.partition("DOI ")[-1].replace("DOI ", "").rstrip(".")
                line = ''.join(c for c in line if c not in '{[}] ')
                if "," in line:
                    line = line.partition(",")[-1]
                citedArticleDOI.append(line)
                with open('citedArticlesDOI.csv', 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow([line])
            titleCount += 1

    articleNum = 0
    for doi in citedArticleDOI:
        try:
            FA = namesFromXref(doi, '', 'first')
        except UnboundLocalError:
            sleep(1)
            continue

        try:
            LA = namesFromXref(doi, '', 'last')
        except UnboundLocalError:
            sleep(1)
            continue

        try:
            selfCiteCount = namesFromXrefSelfCite(doi, '')
        except UnboundLocalError:
            sleep(1)
            continue

        with open(outPath, 'a', newline='') as csvfile:
            if selfCiteCount == 0:
                writer = csv.writer(csvfile, delimiter=',')
                getArticleIndex = [i for i, s in enumerate(allArticles) if doi in s]
                writer.writerow([counter, convertSpecialCharsToUTF8(FA), convertSpecialCharsToUTF8(LA),
                                 allArticles[[i for i, s in enumerate(allArticles) if doi in s][0]], '', ''])
                print(str(counter) + ": " + doi)
                counter += 1
            else:
                print(str(articleNum) + ": " + doi + "\t\t\t <-- self-citation")
        articleNum += 1

    if len(citedArticleNoDOI) > 0:
        print()
        for elem in citedArticleNoDOI:
            with open(outPath, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerow([counter, '', '', elem, '', ''])
                print(str(counter) + ": " + elem)
            counter += 1
        print()
        raise ValueError("WARNING: No article DOI was provided for the last " + str(
            len(citedArticleNoDOI)) + " listed papers. Please manually search for these articles. IF AND ONLY IF your citing paper's first and last author are not co-authors in the paper that was cited, enter the first name of the first and last authors of the paper that was cited manually. Then, continue to the next code block.")

    return FA, LA


def get_names(bib_data):
    """
    take bib_data, and get lists of first and last names. should also get self cites and CDS cites
    :return: FA
              LA
    """
    counter = 1
    nameCount = 0
    outPath = homedir + 'cleanedBib.csv'

    if os.path.exists(outPath):
        os.remove(outPath)

    with open(outPath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Article', 'FA', 'LA', 'Title', 'SelfCite', 'CitationKey'])

    for key in bib_data.entries.keys():
        diversity_bib_titles = ['The extent and drivers of gender imbalance in neuroscience reference lists',
                                'The gender citation gap in international relations',
                                'Quantitative evaluation of gender bias in astronomical publications from citation counts',
                                '\# CommunicationSoWhite',
                                '{Just Ideas? The Status and Future of Publication Ethics in Philosophy: A White Paper}',
                                'Gendered citation patterns across political science and social science methodology fields',
                                'Gender Diversity Statement and Code Notebook v1.0',
                                'Racial and ethnic imbalance in neuroscience reference lists and intersections with gender',
                                'Gender Diversity Statement and Code Notebook v1.1',
                                'Gendered citation practices in the field of communication',
                                'Gender disparity in citations in high- impact journal articles',
                                'Gender (im)balance in citation practices in cognitive neuroscience',
                                'Name-ethnicity classification from open sources',
                                'Predicting race and ethnicity from the sequence of characters in a name']
        if bib_data.entries[key].fields['title'] in diversity_bib_titles:
            continue

        try:
            author = bib_data.entries[key].persons['author']
        except:
            author = bib_data.entries[key].persons['editor']
        FA = author[0].rich_first_names
        LA = author[-1].rich_first_names
        FA = convertLatexSpecialChars(str(FA)[7:-3]).translate(str.maketrans('', '', string.punctuation)).replace(
            'Protected', "").replace(" ", '')
        LA = convertLatexSpecialChars(str(LA)[7:-3]).translate(str.maketrans('', '', string.punctuation)).replace(
            'Protected', "").replace(" ", '')

        # check if we grabbed a first initial when a full middle name was available
        if (len(FA) == 1):
            mn = author[0].rich_middle_names
            mn = convertLatexSpecialChars(str(mn)[7:-3]).translate(
                str.maketrans('', '', string.punctuation)).replace('Protected', "").replace(" ", '')
            if len(mn) > 1:
                FA = mn
        if (len(LA) == 1):
            mn = author[-1].rich_middle_names
            mn = convertLatexSpecialChars(str(mn)[7:-3]).translate(
                str.maketrans('', '', string.punctuation)).replace('Protected', "").replace(" ", '')
            if len(mn) > 1:
                LA = mn

        # check that we got a name (not an initial) from the bib file, if not try using the title in the crossref API
        try:
            title = bib_data.entries[key].fields['title'].replace(',', '').\
                replace(',', '').replace('{', '').replace('}','')
        except:
            title = ''
        try:
            doi = bib_data.entries[key].fields['doi']
        except:
            doi = ''
        if FA == '' or len(FA.split('.')[0]) <= 1:
            while True:
                try:
                    FA = namesFromXref(doi, title, 'first')
                except UnboundLocalError:
                    sleep(1)
                    continue
                break
        if LA == '' or len(LA.split('.')[0]) <= 1:
            while True:
                try:
                    LA = namesFromXref(doi, title, 'last')
                except UnboundLocalError:
                    sleep(1)
                    continue
                break

        self_cites(author, yourFirstAuthor,yourLastAuthor, optionalEqualContributors)
        counter += 1
        with open(outPath, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                [counter, convertSpecialCharsToUTF8(FA), convertSpecialCharsToUTF8(LA), title, selfCite, key])


def self_cites(author, yourFirstAuthor, yourLastAuthor, optionalEqualContributors):
    """
    take author list, and find self citations

    :param author:
    :param yourFirstAuthor:
    :param yourLastAuthor:
    :param optionalEqualContributors:
    :return:
    """
    if (yourFirstAuthor == 'LastName, FirstName OptionalMiddleInitial') or (
            yourLastAuthor == 'LastName, FirstName OptionalMiddleInitial'):
        raise ValueError("Please enter your manuscript's first and last author names")

    selfCiteCheck1 = [s for s in author if removeMiddleName(yourLastAuthor) in
                      str(
                          [clean_name(s.rich_last_names, 'latex'),
                           clean_name(s.rich_first_names, 'latex')]
                      ).replace("'", "")]

    selfCiteCheck1a = [s for s in author if removeMiddleName(yourLastAuthor) in
                      str(
                          [clean_name(s.rich_last_names, 'utf'),
                           clean_name(s.rich_first_names, 'utf')]
                      ).replace("'", "")]
    selfCiteCheck1b = [s for s in author if removeMiddleName(yourLastAuthor) in
                       str(
                           [clean_name(s.rich_last_names, 'utf'),
                            LA]).replace("'","")]
    # I was in the process of cleaning all thisup when we stopped
    selfCiteCheck2 = [s for s in author if removeMiddleName(yourFirstAuthor) in str([
        convertLatexSpecialChars(
            str(s.rich_last_names)[
            7:-3]).replace(
            "', Protected('",
            "").replace(
            "'), '", ""),
        convertLatexSpecialChars(
            str(s.rich_first_names)[
            7:-3]).replace(
            "', Protected('",
            "").replace(
            "'), '",
            "")]).replace(
        "'", "")]
    selfCiteCheck2a = [s for s in author if removeMiddleName(yourFirstAuthor) in str([
        convertSpecialCharsToUTF8(
            str(s.rich_last_names)[
            7:-3]).replace(
            "', Protected('",
            "").replace(
            "'), '", ""),
        convertSpecialCharsToUTF8(
            str(s.rich_first_names)[
            7:-3]).replace(
            "', Protected('",
            "").replace(
            "'), '",
            "")]).replace(
        "'", "")]
    selfCiteCheck2b = [s for s in author if removeMiddleName(yourFirstAuthor) in str([
        convertSpecialCharsToUTF8(
            str(s.rich_last_names)[
            7:-3]).replace(
            "', Protected('",
            "").replace(
            "'), '", ""),
        FA]).replace("'",
                     "")]

    nameCount = 0
    if optionalEqualContributors != (
            'LastName, FirstName OptionalMiddleInitial', 'LastName, FirstName OptionalMiddleInitial'):
        for name in optionalEqualContributors:
            selfCiteCheck3 = [s for s in author if removeMiddleName(name) in str([convertLatexSpecialChars(
                str(s.rich_last_names)[7:-3]).replace("', Protected('", "").replace("'), '", ""),
                                                                                  convertLatexSpecialChars(
                                                                                      str(s.rich_first_names)[
                                                                                      7:-3]).replace(
                                                                                      "', Protected('",
                                                                                      "").replace("'), '",
                                                                                                  "")]).replace(
                "'", "")]
            selfCiteCheck3a = [s for s in author if removeMiddleName(name) in str([
                convertSpecialCharsToUTF8(
                    str(s.rich_last_names)[
                    7:-3]).replace(
                    "', Protected('",
                    "").replace(
                    "'), '", ""),
                convertSpecialCharsToUTF8(
                    str(s.rich_first_names)[
                    7:-3]).replace(
                    "', Protected('",
                    "").replace(
                    "'), '",
                    "")]).replace("'",
                                  "")]
            if len(selfCiteCheck3) > 0:
                nameCount += 1
            if len(selfCiteCheck3a) > 0:
                nameCount += 1
    selfCiteChecks = [selfCiteCheck1, selfCiteCheck1a, selfCiteCheck1b, selfCiteCheck2, selfCiteCheck2a,
                      selfCiteCheck2b]
    if sum([len(check) for check in selfCiteChecks]) + nameCount > 0:
        selfCite = 'Y'
        if len(FA) < 2:
            print(
                str(counter) + ": " + key + "\t\t  <-- self-citation <--  ***NAME MISSING OR POSSIBLY INCOMPLETE***")
        else:
            print(str(counter) + ": " + key + "  <-- self-citation")
    else:
        selfCite = 'N'
        if len(FA) < 2:
            print(str(counter) + ": " + key + "\t\t  <--  ***NAME MISSING OR POSSIBLY INCOMPLETE***")
        else:
            print(str(counter) + ": " + key)





