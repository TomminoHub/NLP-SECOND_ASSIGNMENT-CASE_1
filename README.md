# NLP-SECOND_ASSIGNMENT-CASE_1

In this project I divide a text in a sequence of smaller slices.
At the start of the code I ask to write the dimension of the context window. This is used to create a set of paragraph that are smaller or equal the dimension of the context window.
In the folder 'slices' there is a set of paragraph created previously, when you run the code they will be eliminated by the function 'cancella_file()'.
In the folder 'testo_da_suddividere' you need to put the text you want divide. It's already there a file I used for my test, if you want to change it and working with another text you have to put that text inside the folder and eliminate the previous one. It only works with a single file in it.
The main work of the project is made by the function 'slice_build()'.
This function firstly check if the length of the text is lesser than the context window, in this case we don't do anything.
If it's not, it creates the first paragraph respecting the dimension of the context window.
Then it creates another paragraph that is equal to the first one.
With the function 'check_cosine()' it continue iterating until the second paragraph is different enough from the first one.
In order to make them different enough it eliminates the first row and add another row to the paragraph.
The function 'check_cosine()' create the two dict for both of paragraph and check the cosine similarity between them using the function 'check_cosine()'.
When the value of this function is less or equal than 0.8 the second paragraph is cosidered to be different enough so we write it in the folder 'slices' and we create the third one and so on.
I've chosen to consider two paragraphs 'different enough' when the cosine distance is less than 0.8.
