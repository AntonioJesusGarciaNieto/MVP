import html2text

#################################
#    Métodos de utilidad        #
#################################

def convertHTML2MD(html):

    #Convierte HTML a formato .md

    h = html2text.HTML2Text()
    md = ""
    splits = str(html).split("\n")

    for element in splits:
        md = md + str(h.handle(element))

    return md

def remove_values_from_list(the_list, val):
    
    #Elimina los val de una lista

    return [value for value in the_list if value != val]