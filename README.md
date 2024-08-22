This repo accompanies our manuscript in preparation on the extent of gender and race/ethnicity imbalance in infectious disease dynamics publication and citation practices. Much of the code is drawn from Dale Zhou and colleagues' [repository](https://github.com/dalejn/cleanBib) and this work was inspired by Jordan Dworkin and colleagues' [work](https://doi.org/10.1038/s41593-020-0658-y) in neuroscience.

## Instructions

The goal of the coding notebook is to analyze the predicted gender and race/ethnicity of first and last authors in reference lists of *manuscripts in progress*. The code will clean your `.bib` file to only contain references that you have cited in your manuscript. This cleaned `.bib` will then be used to generate a data table of names that will be used to query the probabilistic gender ([Gender API](https://gender-api.com) or [genderize.io](https://genderize.io)) and race/ethnicity ([ethnicolr](https://github.com/appeler/ethnicolr)) database. Proportions of the predicted gender for first and last author pairs (man/man, man/woman, woman/man, and woman/woman) and predicted race (white and author of color) will be calculated using the database probabilities.

1. Obtain a `.bib` file of your manuscript's reference list. You can do this with common reference managers. __Please try to export your .bib in an output style that uses full first names (rather than only first initials) and using the full author lists (rather than abbreviated author lists with "et al.").__ If a journal only provides first initials, our code will try to automatically find the full first name using the paper title or DOI (this can typically retrieve the first name 70% of the time).

   * [Export `.bib` from Mendeley](https://blog.mendeley.com/2011/10/25/howto-use-mendeley-to-create-citations-using-latex-and-bibtex/)
   * [Export `.bib` from Zotero](https://libguides.mit.edu/ld.php?content_id=34248570)
    <details>
      <summary>Tips for Microsoft Word and Google Docs integration</summary>

     Set your citation style to [BibTex](https://www.zotero.org/styles?q=id%3Abibtex) in Word and Google docs, and copy the reference list into a `.bib` file. Make sure you edit `Zotero/styles/bibtex.csl`: change `et-al-min` and `et-al-first` to something large (like 100) to avoid the last author being listed as 'et al.' Remove the line `text variable="abstract" prefix=" abstractNote={" suffix="}"/>` to avoid the `.bib` file getting very large.
    </details> 

   * [Export `.bib` from EndNote](https://www.reed.edu/cis/help/LaTeX/EndNote.html). Note: Please export full first names by either [choosing an output style that does so by default (e.g. in MLA style)](https://canterbury.libguides.com/endnote/basics-output)
   * [Export `.bib` from Read Cube Papers](https://support.papersapp.com/support/solutions/articles/30000024634-how-can-i-export-references-from-readcube-papers-)

2. Launch the coding environment. Please refresh the page if the Binder does not load after 5-10 mins.

   This part doesn't work yet!!! Download the code as a zip file in the meantime.

    __Option 1 (recommended)__: Visit https://notebooks.gesis.org/binder/, paste https://github.com/dalejn/cleanBib into the GitHub repository name or URL field, and press "launch."

    __Option 2 (experiencing intermittent server issues)__: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/dalejn/cleanBib/HEAD?urlpath=/tree/)

4. Open the notebook `cleanBib.ipynb`. Follow the instructions above each code block. It can take 10 minutes to 1 hour complete all of the instructions, depending on the state and size of your `.bib` file. We expect that the most time-consuming step will be manually modifying the `.bib` file to find missing author names, fill incomplete entries, and fix formatting errors. These problems arise because automated methods of reference mangagers and Google Scholar sometimes can not retrieve full information, for example if some journals only provide an author's first initial instead of their full first name.

## Input/output

| Input                 | Output                                                                                                                        |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------|
| `.bib` file(s)**(REQUIRED)**    | `cleanedBib.csv`: table of author first names, titles, and .bib keys                                                            |
| `.aux` file (OPTIONAL)| `predictions.csv`: table of author first names, estimated gender classification, and confidence                                   |
| `.tex` file (OPTIONAL) | `race_gender_citations.pdf`: heat map of your citations broken down by probabilistic gender and race estimations
|                       | `yourTexFile_gendercolor.tex`: your `.tex` file modified to compile .pdf with in-line citations colored-coded by gender pairs |

# FAQ

<details>
  <summary>Why do I receive an error when running the code?</summary>

* The most common errors are due to misformatted .bib files. Errors messages are very detailed, and at the bottom of the printed message will be an indication of the line and type of problem in the .bib file. They will require you to manually correct the `.bib` file of formatting errors or incomplete entries. After editing the `.bib` file, try re-running the code block that gave you the error. If you cannot resolve an error, please open an [Issue](https://github.com/jtaube/IDD_bib_analysis/issues/new/choose), paste the error text or a screenshot of the error, and attach the files that you used so that we can reproduce the error. We will try to help resolve it.
</details>

<details>
<summary>Common errors</summary>

<details>
<summary>TokenRequired</summary>

```TokenRequired: syntax error in line X: entry key expected```

This error message indicates that on line X of your uploaded .bib file, there is an incomplete entry that is missing a unique key for the citation. For instance, `@article{,` should be changed to `@article{yourUniqueCitationKey`
</details>

<details>
<summary>Syntax Error</summary>

```in line X: ‘Y‘ expected```

This error message could indicate that there is an unexpected character at line X of your .bib file, such as a space in the name of a field. For example, instead of `Early Access Date = …`, the field should be changed to `EarlyAccessDate = …`
</details>

<details>
<summary>Key Error</summary>

```KeyError: 'author'``` or ```KeyError: 'editor'```

This error message could indicate that you have cited a book and there is no `author` field. In this case, if there is an `editor` field, please change `editor` to `author`. Otherwise, add the `author` metadata.
</details>

</details>

<details>
  <summary>What should I do if the Binder crashes, times out, or takes very long to launch?</summary>

* Please refresh the Binder or re-launch from our step 2 instruction upon a crash. This has often resolved the issue. The environment will time out if you are inactive for over 10 minutes (but leaving the window open counts as activity). Long launch times (>15 minutes) can be due to a recent patch by us (temporary slow-down from re-building the Docker image) or heavy load on the server. Please try again at a later time. Please refer to the [Binder User Guide](https://mybinder.readthedocs.io/en/latest/index.html) and [FAQ](https://mybinder.readthedocs.io/en/latest/index.html) for other questions.
</details>

<details>
  <summary>Will this method work on non-Western names and how accurate is it?</summary>

* Yes, the [Gender API supports 177 countries](https://gender-api.com/en/frequently-asked-questions?gclid=Cj0KCQiAmZDxBRDIARIsABnkbYTy9MHmGoR2uBhxEKANbT9B9EFVOSiRzbGeQi7nUn6ODH83s6-RZKwaAjpZEALw_wcB#which-countries-are-supported) but will classify genders with varying confidence. [Dworkin et al. (2020; Supplementary Tables 1 and 2)](https://doi.org/10.1038/s41593-020-0658-y) assessed the extent of potential gender mislabeling by manual inspecting a sample of 200 authors. They found that the relative accuracy of the automated determination procedure at the level of both individual authors had an accuracy ≈ 0.96 and article gender categories had an accuracy ≈ 0.92. Because errors in gender determination would break the links between citation behavior and author gender, any incorrect estimation in the present data likely biases the results towards the null. The [ethnicolr](https://github.com/appeler/ethnicolr) race probabilities use the last-name–race data from the [2000 census and 2010 census](https://github.com/appeler/ethnicolr/blob/master/ethnicolr/data/census), the [Wikipedia data](https://github.com/appeler/ethnicolr/blob/master/ethnicolr/data/wiki) collected by Skiena and colleagues, and the [Florida voter registration data](http://dx.doi.org/10.7910/DVN/UBIG3F) from early 2017. Across cross-validation folds, the average precision was 0.83, recall was 0.84, and f1-support scores were 0.83 for the Florida model. Please see this [confusion matrix for the accuracy and precision of the algorithm during cross-validation](https://github.com/mb3152/balanced_citer) and [Sood & Laohaprapanon (2018)](https://arxiv.org/abs/1805.02109).

</details>

<details>
  <summary>How are proportions calculated, especially when considering gender-neutral or race-ambiguous names?</summary>

* MIGHT NEED TO CHANGE The proportions for predicted gender and race are now weighted probabilistically. For instance, if Gender-API predicts a name as man with 72% accuracy, then the 0.72 is added to the man proportion. The proportions are calculated from weighted sums across all author pairs. Similarly for predicted race, the ethnicolor package can be used to make binary predictions but also provides probabilities that an author belongs to each racial category. Consider the last name “Smith.” The model’s probabilities for the name “Smith” are 73% white, 25% Black, 1% Hispanic, and <1% Asian. We use all four probabilities to estimate how citers probabilistically assign racial categories to names, either implicitly or explicitly, while reading and citing papers. Note that imperfections in the algorithm’s predictions will break the links between citation behavior and author race, and therefore any incorrect estimation in the present data likely biases the results towards the null model.
</details>

<details>
  <summary>Are self-citations included?</summary>

* We do not include self-citations by default because we seek to measure engagement with and citation of other researchers' work. We define self-citations as those including your first or last author as a co-author.
</details>

<details>
  <summary>What if a reference has only 1 author?</summary>

* We count that author as both the first and last author.
</details>

<details>
  <summary>What if the author list includes a committee or consortium?</summary>

* Please use either the last named author or the lead of the committee/consortium.
</details>

<details>
  <summary>What if a reference has more than 1 first author or last author?</summary>

* We do not automatically account for these cases. If you are aware of papers with co-first or co-last authors, then you could manually add duplicate entries for each co-first or co-last author so that they are double-counted.
</details>

<details>
  <summary>Should I include the diversity statement references in the proportion calculations?</summary>

* Please do not include the diversity statement references. The descriptive statistic of primary interest is of your citation practices.
</details>

<details>
  <summary>What is a .bib file?</summary>

* The `.bib` file is a bibliography with tagged entry fields used by LaTeX to format a typesetted manuscript's reference list and its in-line citations. If you are not using LaTeX to write your manuscript, common reference managers that are linked to Microsoft Word or Google Docs also allow you to export `.bib` files (See Instructions, Step 1). When you are asked to edit the `.bib` file, this means that you should open the file with a text editor (if you want to edit your own copy of the file) or within the Binder environment (if you want to edit a temporary copy of your uploaded file). Each entry starts with an `@` symbol and includes a reference key, then lists metadata for author, year, journal, etc. Some instructions will ask you to edit the list of names in the "author" data, and some will ask you to remove entire entries.
</details>

<details>
  <summary>What is an .aux file?</summary>

* The `.aux` file is generated when you compile the `.tex` file to build your manuscript. It is linked to the `.bib` file(s) used to populate your manuscript's reference list and records the citations used.
</details>

<details>
  <summary>I have an idea to advance this project, suggestions about how to improve the notebook, and/or found a bug. Can I contribute? How do I contribute?</summary>

* If you have suggestions for changes, please open an `Issue` or `Pull Request`. We welcome feedback on any pain points in running this code notebook (there is an Issue in which you can submit feedback). 

* To modify the notebook cleanBib.ipynb, please:
1. Test the code works as intended and does not seem break any existing code (we can also help to check this later) by pasting it into the cleanBib.ipynb Jupyter notebook and running it in an active Binder session.
2. When you're confident it works as intended, copy the code again if you made any modifications from testing. Close/end the current Binder session, and start a fresh one to open the cleanBib.ipynb and do not run anything in this notebook (to remove traces of when you last ran it/how many times you've run the code). Go to File > Download As > Notebook (.ipynb).
3. [Create a fork of our GitHub repository to your own GitHub account.](https://docs.github.com/en/enterprise/2.13/user/articles/fork-a-repo#:~:text=A%20fork%20is%20a%20copy,point%20for%20your%20own%20idea.)
4. [Upload and commit your modified cleanBib.ipynb to your fork.](https://docs.github.com/en/enterprise/2.13/user/articles/adding-a-file-to-a-repository)
5. [Submit a Pull Request to our GitHub repository.](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork)
</details>


