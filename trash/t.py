txt = input("gimme text: ")

txt_split = txt.split()

wordcount = 0
text = []
line = []

#Max length per line is 55 characters
if len(txt) > 55:
    #Loop through all the words
    for word in txt_split:
        #Check wether the max length has been reached
        if len(word) + wordcount >= 55:
            #If the max length has been reached, check if a new line can be added to this page, add the line to the text list, empty the line, and reset the wordcount
            text.append(line)
            line = []
            wordcount = 0

        #Add the word to the line
        wordcount += len(word)
        line.append(word)

    #Add the last line to the text list
    text.append(line)

else:
    text.append(txt)

print(text)