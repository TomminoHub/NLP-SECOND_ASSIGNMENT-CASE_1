import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import math
import copy
import os


nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')


def slice_build(testo, context_window):
    sentences = sentence_tokenization(testo)
    text_norm = []  #lista che contiene il testo in lingua naturale di un paragrafo
    text_token = [] #lista che contiene i token di un paragrafo
    idx = 0 
    count = 0   #variabile che tiene in considerazione la lunghezza dei paragrafi
    finish = 0  #flag per uscire dal ciclo
    
    #creazione del primo paragrafo
    while idx < len(sentences)-1:
        sentence = sentences[idx]
        words = word_tokenization(sentence)
        #controllo che l'aggiunta della nuova frase al paragrafo non superi la dimensione della context window
        if (len(words) + count) < context_window:
            idx += 1
            count += len(words)
            text_norm, text_token = sentence_union(text_norm, text_token, sentence, words)
        else:
            break
    
    #scrittura del primo paragrafo
    paragraph(text_norm)
    #creazione di nuove liste per poter confrontare i paragrafi due alla volta
    text_token_2 = []
    text_norm_2 = []
    text_token_2 = copy.copy(text_token)
    text_norm_2= copy.copy(text_norm)
    while finish != 1 and idx < len(sentences):
        
        #il primo paragrafo è uguale al secondo
        text_token= copy.copy(text_token_2)
        text_norm = copy.copy(text_norm_2)
        
        #controllo che i due paragrafi siano abbastanza diversi tra loro
        #se non sono abbastanza diversi entro nel ciclo
        #continua a eliminare la prima frase e aggiungerne un'altra fintanto che i due paragrafi sono abbastanza diversi
        while not check_cosine(text_token, text_token_2):
            
            #elimino la prima frase e il corrispondente contatore della lunghezza del paragrafo
            text_norm_2.pop(0)
            count -= len(text_token_2.pop(0))
            #controllo se l'aggiunta di una nuova frase non supera la context_window 
            if (count + len(word_tokenization(sentences[idx])) < context_window):
                #controllo di non uscire dal range di sentences
                if idx < len(sentences) - 1:
                    idx += 1
                    count += len(word_tokenization(sentences[idx]))
                    #aggiungo la frase
                    text_norm_2, text_token_2 = sentence_union(text_norm_2, text_token_2, sentences[idx], word_tokenization(sentences[idx]))
                else:
                    #se sforo il range imposto il flag a 1
                    finish = 1
            else:
                #se aggiungendo la nuova frase esco dalla context_window elimino un'altra volta la prima frase
                count -= len(text_token_2.pop(0))
                text_norm_2.pop(0)
        
        paragraph(text_norm_2) 
               
        if finish:
            break
        


#FUNZIONE CHE SCRIVE NELLA CARTELLA SLICES I PARAGRAFI
def paragraph(lista):
    frase_token_finale = '' 
    indici_pregressi = [int(nome.split('_')[1].split('.')[0]) for nome in os.listdir('slices') if nome.startswith('paragrafo_')]
    prossimo_indice = max(indici_pregressi, default=0) + 1
    for paragrafo in lista:
        frase_token_finale += paragrafo + ' '
    nome_file = os.path.join('slices', f"paragrafo_{prossimo_indice}.txt")
    with open(nome_file, 'w') as file:
        file.write(frase_token_finale)
  
  

#FUNZIONE CHE RESTITUISCE TRUE SE I DUE PARAGRAFI SONO ABBASTANZA DIVERSI TRA LORO, ALTRIMENTI FALSE
def check_cosine(text_token_1, text_token_2):  
    dict_segmento_1 = dictionary(text_token_1)
    dict_freq_segmento_1 = frequencies(dict_segmento_1)
    dict_segmento_2 = dictionary(text_token_2)
    dict_freq_segmento_2 = frequencies(dict_segmento_2)
    
    valore = calculate_cosine_distance(dict_freq_segmento_1, dict_freq_segmento_2)
    if  valore <= 0.8:
        return True
    else:
        return False



#FUNZIONE CHE AGGIUNGE AI PARAGRAFI IN LINGUA NORMALE E QUELLI COMPOSTI DA TOKEN LE NUOVE FRASI
def sentence_union(text_norm_funct, text_token_funct, sentence_funct, words_funct):
    text_norm_funct.append(sentence_funct)
    text_token_funct.append(words_funct)
    return text_norm_funct,text_token_funct



#FUNZIONE CHE RESTITUISCE UNA LISTA DI TOKEN CHE COMPONGONO IL TESTO CHE GLI VIENE PASSATO COME PARAMETRO
def word_tokenization(sentence):
    lista = []
    lemmatizzatore = WordNetLemmatizer()
    stoplist = stopwords.words('english')
    parole = word_tokenize(sentence)
    for parola in parole:
        parola_minuscola = parola.lower()
        parola_minuscola = lemmatizzatore.lemmatize(parola_minuscola)
        if parola_minuscola not in stoplist and parola_minuscola.isalnum() and not parola_minuscola.isnumeric():
            lista.append(parola)
    return lista


#FUNZIONE CHE SUDDIVIDE IL TESTO IN FRASI
def sentence_tokenization(text):
    sentences = sent_tokenize(text)
    return sentences
    

#FUNZIONE CHE MI CREA IL DIZIONARIO CHE CONTA LE OCCORRENZE PER OGNI TESTO PASSATO IN INPUT
def dictionary(text):
    lemmatizzatore = WordNetLemmatizer()
    stoplist = stopwords.words('english')
    my_dict = {}
    for parole in text:
        for parola in parole:
            #print(parola)
            parola_minuscola = parola.lower()
            parola_minuscola = lemmatizzatore.lemmatize(parola_minuscola)
            if parola_minuscola not in stoplist and parola_minuscola.isalnum() and not parola_minuscola.isnumeric():
                # Aggiungi la parola al dizionario se non è nella lista delle stopword, è alfanumerica e non è numerica
                if parola_minuscola not in my_dict:
                    my_dict[parola_minuscola] = 1
                else:
                    my_dict[parola_minuscola] += 1

    # Ordina per numero di occorrenze
    my_dict = dict(sorted(my_dict.items(), key=lambda x: x[1], reverse=True))

    return my_dict



#FUNZIONE CHE CALCOLA LA FREQUENZA DI OGNI PAROLA DI UN PARAGRAFO 
def frequencies(dict):
    total_occurrences = sum(dict.values())
    for key in dict:
        dict[key] = float(dict[key] / total_occurrences)
    return dict


#FUNZIONE CHE CALCOLA LA COSINE DISTANCE TRA DUE DIZIONARI
#RESTITUISCE UN NUMERO COMPRESO TRA 0 E 1
#PIU' E' ALTRO IL NUMERO PIU' I PARAGRAFI SONO SIMILI
def calculate_cosine_distance(vec1, vec2):   
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        #print(float(numerator) / denominator)
        return float(numerator) / denominator


#FUNZIONE CHE CANCELLA TUTTI I FILE ALL'INTERNO DI SLICES CREATI PRECEDENTEMENTE
def cancella_file():
    for file in os.listdir('slices'):
        file_path = os.path.join('slices', file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Errore durante l'eliminazione di {file_path}: {e}")


#FUNZIONE CHE LEGGE IL FILE DA SUDDIVIDERE IN SLICES ALL'INTERNO DELLA CARTELLA 'TESTO DA SUDDIVIDERE'
#DEVE ESSERCI SOLO UN FILE ALL'INTERNO DELLA CARTELLA
def lettura_testo(cartella):
            # Elenco dei file nella cartella
    files = os.listdir(cartella)
    for file in files:
        percorso_file = os.path.join(cartella, file)
    with open(percorso_file, 'r', encoding='utf-8') as file:
        testo = file.read()
    return testo         
                


cancella_file()    
testo = lettura_testo('testo_da_suddividere')
#inserire la grandezza della context_window interessata
context_window = int(input("Inserisci la context window massima: "))
slice_build(testo, context_window)
