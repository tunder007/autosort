The problem:

I have multiple files of multiple types (pdf, word, png, jpeg, etc.) => this is why it is autosort (and autodetect type)

I want to sort them into different folders by type:

Input:

Un folder MARE cu foarte multe fisiere (ignora folderele din el)

Output:

Un folder MARE, iar acele fisiere sa fie sortate in mai multe foldere cu titluri type of file: png_folder, word_folder, ... <type_folder>

How:
    1. un fisier care parcurge fisierele dintr-un folder si le noteaza adresele (absolute path) intr-o matrice si le noteaza pe randuri in functie de tipul fisierului. De ex: pe randul 1 voi avea word-uri (path-urile pentru documentele word din acel folder), pe randul 2, randul 3 - randurile se fac in functie de ordinea aparitiei in folder etc.
    2. un fisier care se apuca si creeaza cate un folder cu <type_folder> ca titlu pentru fiecare rand din matrice
    3. un fisier care se ocupa cu mutarea fisierelor din folder-ul mare in folderele create cu titlurile <type_folder>
    4. un UI in care: sa pot selecta cu usurinta folder-ul pe care vreau sa il sortez, si sa pot documenta git history 