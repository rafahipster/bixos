################################################################
#                                                              #
# Coisas legais a se fazer:                                    #
# - Adicionar BeautifulSoup pra pegar os dados direto do site  #
# - Solucionar a gambiarra dos Bar Plots                       #
################################################################


from matplotlib import pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from scipy.stats import norm
import statistics
import math
import numpy as np
import requests


####### MODO VERBOSO PRA VER O QUE TA PRINTANDO #######
VERBOSE = True # Se não quiser nada printando no console só seta pra False

###### DIRETORIO DE ENTRADA #######
diretorio_entrada = "bixos_raw"
####################################



################################# FUNCOES UTEIS ###########################################################################
def classificacao(bixo):
    return bixo[7]

def hist_plot(data, titlename = 10,x_axis = "Nota", y_axis = "Quantity", title = "Distribuicao de notas"):
    ## get statistics from data #
    mu = statistics.mean(data)
    std = statistics.stdev(data)
    n_bins = np.arange(min(data), max(data), 0.1)
    #############################

    fig, axs = plt.subplots(1,2, tight_layout=True)
    fig.suptitle("{}: Média: {:.3f}     Desvio Padrão: {:.3f}".format(titlename, mu, std))
    axs[0].set_title(" ")#Media {:.3f}".format(mu))
    axs[1].set_title(" ")#Desvio padrao {:.3f}".format(std))
    axs[0].set_xlabel(x_axis)
    axs[0].set_ylabel(y_axis)
    axs[1].set_xlabel(x_axis)
    axs[1].set_ylabel('Porcentagem em relação à moda')
    N, bins, patches = axs[0].hist(data, bins=n_bins)
    axs[1].hist(data, bins=n_bins, histtype = 'stepfilled', density=True, alpha = 0.6)
    #N, bins, patches = axs[0].hist(data) #, bins=n_bins)
    fracs = N/N.max()
    norm_c = colors.Normalize(fracs.min(), fracs.max())

    for thisfrac, thispatch in zip(fracs, patches):
        color = plt.cm.viridis(norm_c(thisfrac))
        thispatch.set_facecolor(color)


    xmin, xmax = plt.ylim()
    axs[1].yaxis.set_major_formatter(PercentFormatter(xmax))

    ## Create probability density function based on data ##################
    xmin = bins.min()
    xmax = bins.max()
    dist = np.linspace(xmin, xmax, 100)
    p = norm.pdf(dist, mu, std)
    axs[1].plot(dist, p, 'k', linewidth=2, label = "Densidade de Probabilidade")
    ######################################################################

    ## Print plot ##############################################
    plt.grid(True)
    plt.show()
    ########################################################


# Bar plots
def bar_plot(titlename, names, values, rotate = False):
    #val_mean = statistics.mean(values) Ia fazer um gradiente de cores com as notas aqui mas sugou
    plt.bar(names, values, linewidth=0.5)
    plt.gcf().set_size_inches(10.5,10.5)
    plt.ylabel('Nota')
    plt.xlabel('Matéria')
    if (rotate):
        plt.xticks(names, rotation=90)
    else:
        plt.xticks(names)
    plt.title(titlename)
    plt.grid(True)
    plt.show()


# Reduz o tamanho das palavras das cidades pra caber no plot (gabiarra total)
def reduz_cidade(entry):
    cidades = {
    "RIO DE JANEIRO" : "RJ",
    "SAO JOSE DOS CAMPOS" : "SJC",
    "SAO PAULO" : "SP",
    "BELO HORIZONTE": "BH",
    "JUIZ DE FORA" : "JF",
    "FORTALEZA" : "FORTAL",
    "RIBEIRAO PRETO": "RP",
    "CURITIBA": "CWB",
    "PORTO ALEGRE": "PA"
    }

    for cidade in cidades:
        if cidade in entry:
            return cidades[cidade]
    return entry
##################################################################################################################


# Incializações
bixos = []
cidades = []
contagem = []
notas = [[],[], []]
medias = [0,0,0,0,0,0]

# magia negra pra pegar os dados de cada candidato.
with open(diretorio_entrada) as arq:
    for line in arq:
         if ("-" not in line and "MEDIA" not in line and "FASE" not in line):
             if line[2:43] != '':
                 bixos.append((line[2:43], float(line[46:53].replace(',', '.')), float(line[56:63].replace(',', '.')),
                 float(line[64:71].replace(',', '.')), float(line[72:79].replace(',', '.')),
                 float(line[80:87].replace(',', '.')), float(line[88:95].replace(',', '.')),
                 int(line[96:101]), line[104:124]))


for bixo in bixos:
    medias[0] += bixo[1] # Media primeira fase
    medias[1] += bixo[2] # MAT
    medias[2] += bixo[3] # FIS
    medias[3] += bixo[4] # QUI
    medias[4] += bixo[5] # RED
    medias[5] += bixo[6] # Media final
    notas[0].append(bixo[2])
    notas[1].append(bixo[3])
    notas[2].append(bixo[4])

############## Sort por cidade ########################################
# implementar um plot bonitinho aqui no futuro pfvr
for bixo in bixos:
    if reduz_cidade(bixo[8]) in cidades:
        contagem[cidades.index(reduz_cidade(bixo[8]))] += 1
    else:
        cidades.append(reduz_cidade(bixo[8]))
        contagem.append(1)
#######################################################################

print(cidades)

############# HISTOGRAMAS DA DISTRIBUIÇÃO DE NOTAS ###############
hist_plot(notas[0], titlename="Distribuicao de notas de MAT")
hist_plot(notas[1], titlename="Distribuicao de notas de FIS")
hist_plot(notas[2], titlename="Distribuicao de notas de QUI")
#################################################################

################### BAR PLOT DAS MATERIAS #################################
medias = [x/len(bixos) for x in medias] # Achando as medias de cada materia
materias = ["Primeira Fase", "MAT", "FIS", "QUI", "RED", "Media Final"]
bar_plot("Médias", materias, medias)
###########################################################################

################### BAR PLOT DAS CIDADES ##################################
bar_plot("Cidades", cidades, contagem, rotate = True)


if (VERBOSE):
    for index, cid in enumerate(cidades):
        print("{}: {}".format(cid, contagem[index]))
    print(medias)
