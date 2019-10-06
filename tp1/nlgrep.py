#!/usr/bin/env python3

import fileinput
import sys
from getopt import getopt
import re

ANSI_RESET = "\u001B[0m"
ANSI_RED = "\u001B[31m"


#Funão que irá imprimir os padrões encontrados a vermelho
def coloreador(match):
	return ANSI_RED+match.group(0)+ANSI_RESET


opts, resto = getopt(sys.argv[1:],"spf:")

if resto == []:
	print("Indique o padrão a encontrar")
	exit()

dop = dict(opts)
texto = dop.get("-f","-")

#Modo frase
if dop.get("-s") == "":
	excecoes = "(?<!D)(?<!Sr|Dr|Mr|Ms)(?<!Dra|Sra)" + "([.!?])" #Padrao que identifica o fim de uma frase, prevendo casos como, por ex: D. Manuel II
	frase=""
	for line in fileinput.input(texto):
		line = line.rstrip('\n')
		if line == "":
			continue
		line += " "
		x = re.split(excecoes,line)
		frase = frase + x[0]
		for i in range(len(x)//2):
			frase = frase + x[i*2+1]  #Concatena com a pontuação que terminou a frase
			#Se pertence imprime frase
			if re.search(resto[0],frase) != None:
				if sys.stdout.isatty():
						frase = re.sub(resto[0], coloreador, frase)
				print(frase.lstrip())
			frase = x[i*2+2]    #Pega na proxima frase da linha a ser processada

#Modo paragrafo por defeito
else:
	paragrafo=""
	for line in fileinput.input(texto):
		line = line.rstrip('\n') + " " #Substituir \n por espaço
		if re.fullmatch(r"\s*",line) != None:
			if re.search(resto[0],paragrafo) != None:
				if sys.stdout.isatty():
					paragrafo = re.sub(resto[0], coloreador, paragrafo)
				print(paragrafo)
			paragrafo = ""
		else:
			paragrafo = paragrafo + line

	#caso o ficheiro nao acabe com uma nova linha, é necessário processar o ultimo paragrafo
	if re.search(resto[0],paragrafo) != None:
		if sys.stdout.isatty():
			paragrafo = re.sub(resto[0], coloreador, paragrafo)
		print(paragrafo)

fileinput.close()




