from hdbcli import dbapi
import numpy as np

from wordcloud import WordCloud

import matplotlib.pyplot as plt


connection = dbapi.connect('52.17.42.3', 39015, 'SYSTEM', 'Glorp2018!')
cursor = connection.cursor()


def getAverageDocumentLength():
    cursor.execute('SELECT TOP 10000 CMPLID, TA_TOKEN FROM "SYSTEM"."$TA_CDESCRIND" ORDER BY CMPLID;')

    totalLength = 0
    documentID = -1
    countDocuments = 0
    for row in cursor:
        if (row[0] != documentID):
            documentID = row[0]
            countDocuments = countDocuments + 1
            # print(row[0])


        # print(row[1])
        totalLength = totalLength + len(row[1])

    print("Number Documents:")
    print(countDocuments)
    print("Average Length:")
    print(totalLength/countDocuments)

def getAverageSentenceLength():
    cursor.execute('SELECT TOP 10000 CMPLID, TA_TOKEN, TA_SENTENCE FROM "SYSTEM"."$TA_CDESCRIND" ORDER BY CMPLID, TA_SENTENCE;')

    totalLength = 0
    documentID = -1

    SentenceNumber = -1
    countSentence = 0
    for row in cursor:
        if (row[0] != documentID):
            documentID = row[0]
            SentenceNumber = row[2]
            countSentence = countSentence + 1

        if(row[2] != SentenceNumber):
            SentenceNumber = row[2]
            countSentence = countSentence + 1

        # print(row[1])
        totalLength = totalLength + len(row[1])

    print("Number Sentences:")
    print(countSentence)
    print("Average Length:")
    print(totalLength/countSentence)



def generateWordCloud(sqlcommand):
    cursor.execute(sqlcommand)

    tmpDict = {}
    for row in cursor:
        tmpval = row[1]
        tmpDict[row[0]] = tmpval
        print(row[0] + ", " + str(row[1]))

    wordcloud = WordCloud(width=480, height=480, margin=0).generate_from_frequencies(tmpDict)
    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.show()

def generateBarChart(sqlcommand):
    import pandas as pd
    df = pd.read_sql(sqlcommand, connection)

    print(df)

    df.plot(kind='bar', x='TA_TOKEN', y='COUNTTOKENS')
    plt.show()


def lemmatisierung(word):
    import spacy
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(word)

    # origWord = doc[0].text
    lemmWord = doc[0].lemma_
    return lemmWord

def createLemmTableNouns():
    sqlcommand = 'SELECT TOP 50000 CMPLID, TA_TOKEN, TA_TYPE, TA_SENTENCE FROM "SYSTEM"."$TA_CDESCRIND" WHERE TA_TYPE = \'noun\' AND NOT TA_TOKEN LIKE \'%\'\'%\''
    cursor.execute(sqlcommand)

    rowsNouns = []
    counter = 0
    for row in cursor:
        print(counter)
        counter = counter + 1
        lemmWord = lemmatisierung(row[1])
        NewStatement = (row[0], lemmWord, row[3])
        rowsNouns.append(NewStatement)

    for row in rowsNouns:
        sqlcommand = f" insert into \"SYSTEM\".\"LemmedNoun\" (CMPLID, \"Lemmed_Word\", \"TA_SENTENCE\") VALUES ('{row[0]}','{row[1]}','{row[2]}')"
        cursor.execute(sqlcommand)

def createLemmTableVerbs():
    sqlcommand = 'SELECT TOP 50000 CMPLID, TA_TOKEN, TA_TYPE, TA_SENTENCE FROM "SYSTEM"."$TA_CDESCRIND" WHERE TA_TYPE = \'verb\' AND NOT TA_TOKEN LIKE \'%\'\'%\''
    cursor.execute(sqlcommand)

    rowsVerbs = []
    counter = 0
    for row in cursor:
        print(counter)
        counter = counter + 1
        lemmWord = lemmatisierung(row[1])
        NewStatement = (row[0], lemmWord, row[3])
        rowsVerbs.append(NewStatement)

    for row in rowsVerbs:
        sqlcommand = f" insert into \"SYSTEM\".\"LemmedVerb\" (CMPLID, \"Lemmed_Word\", \"TA_SENTENCE\") VALUES ('{row[0]}','{row[1]}','{row[2]}')"
        cursor.execute(sqlcommand)

def createLemmTableAdjectives():
    sqlcommand = 'SELECT TOP 50000 CMPLID, TA_TOKEN, TA_TYPE, TA_SENTENCE FROM "SYSTEM"."$TA_CDESCRIND" WHERE TA_TYPE = \'adjective\' AND NOT TA_TOKEN LIKE \'%\'\'%\''
    cursor.execute(sqlcommand)

    rowsAdjectives = []
    counter = 0
    for row in cursor:
        print(counter)
        counter = counter + 1
        lemmWord = lemmatisierung(row[1])
        NewStatement = (row[0], lemmWord, row[3])
        rowsAdjectives.append(NewStatement)

    for row in rowsAdjectives:
        sqlcommand = f" insert into \"SYSTEM\".\"LemmedAdjective\" (CMPLID, \"Lemmed_Word\", \"TA_SENTENCE\") VALUES ('{row[0]}','{row[1]}','{row[2]}')"
        cursor.execute(sqlcommand)

def createLemmTable():
    createLemmTableNouns()
    createLemmTableVerbs()
    createLemmTableAdjectives()



# getAverageDocumentLength()
# getAverageSentenceLength()


#
# print("Most used Words:")
# sqlcommand = 'SELECT TOP 20 TA_TOKEN, count(*) as CountTokens FROM "$TA_CDESCRIND" as t GROUP BY t.TA_TOKEN ORDER BY CountTokens DESC;'
# generateWordCloud(sqlcommand)
# generateBarChart(sqlcommand)
#
# print("Least used Words:")
# sqlcommand = 'SELECT TOP 20 TA_TOKEN, sum(NUMBEROFTOKENS) AS CountTokens FROM WORTCOUNTERTABLE GROUP BY TA_TOKEN ORDER BY CountTokens ASC;'
# generateWordCloud(sqlcommand)
# generateBarChart(sqlcommand)

# print("Most used Nouns:")
# sqlcommand = 'SELECT TOP 20 TA_TOKEN, count(*) as CountTokens FROM "$TA_CDESCRIND" as t WHERE t.TA_TYPE = \'noun\' GROUP BY t.TA_TOKEN ORDER BY CountTokens DESC;'
# generateWordCloud(sqlcommand)
# generateBarChart(sqlcommand)
#
# print("Most used verbs:")
# sqlcommand = 'SELECT TOP 20 TA_TOKEN, count(*) as CountTokens FROM "$TA_CDESCRIND" as t WHERE t.TA_TYPE = \'verb\' GROUP BY t.TA_TOKEN ORDER BY CountTokens DESC;'
# generateWordCloud(sqlcommand)
# generateBarChart(sqlcommand)
#
# print("Most used adjectives:")
# sqlcommand = 'SELECT TOP 20 TA_TOKEN, count(*) as CountTokens FROM "$TA_CDESCRIND" as t WHERE t.TA_TYPE = \'adjective\' GROUP BY t.TA_TOKEN ORDER BY CountTokens DESC;'
# generateWordCloud(sqlcommand)
# generateBarChart(sqlcommand)

sqlcommand = 'SELECT TOP 10 n."TA_TOKEN" as noun, count(*) as CountOccurences FROM "SYSTEM"."$TA_CDESCRIND" n, "SYSTEM"."$TA_CDESCRIND" a WHERE n."TA_TYPE" = \'noun\' AND (a."TA_TYPE" = \'noun\' OR a."TA_TYPE" = \'adjective\') AND n.CMPLID = a.CMPLID AND n.TA_SENTENCE = a.TA_SENTENCE AND a."TA_TOKEN" = \'DEFECT\' AND NOT n."TA_TOKEN" = \'DEFECT\' GROUP BY n."TA_TOKEN" ORDER BY count(*) DESC;'
generateWordCloud(sqlcommand)
generateBarChart(sqlcommand)

# createLemmTable()