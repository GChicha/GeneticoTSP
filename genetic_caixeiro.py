#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import *
from math import hypot
import sys
import csv
import argparse
custos = {}
parsed = ()


class filho:
    def __init__(self, vertices):
        self.vertices = vertices
        self.mutation(parsed.mutation_rate)
        self.custo = custo(self.vertices)
        self.firstImprovement()

    def firstImprovement(self):
        for v in opt2(self.vertices):
            f = custo(v)
            if f < self.custo:
                self.vertices = v
                self.custo = f
                break

    def mutation(self, chance):
        if randint(chance - 100, chance) > 0:
            x = randint(0, len(self.vertices)-1)
            y = randint(0, len(self.vertices)-1)
            temp = self.vertices[x]
            self.vertices[x] = self.vertices[y]
            self.vertices[y] = temp

    def crossover(self, filho2):
        populacao = [self, filho2]
        tam = len(self.vertices)

        while len(populacao) < parsed.populacao:
            vertices = []
            inicio = randint(0, len(self.vertices))
            fim = randint(inicio, len(self.vertices))
            keep2 = filho2.vertices[fim:]
            keep2.extend(filho2.vertices[:fim])
            vertices = self.vertices[inicio:fim]
            while(len(vertices) < tam):
                a = keep2.pop()
                if a not in vertices:
                    vertices.append(a)
            populacao.append(filho(vertices))
        return populacao

    def to_dot_file(self):
        f = parsed.dot
        f.write("digraph {")
        for x in self.vertices:
            f.write(x.label + "[sfixedsize=true,\
                               height=2,\
                               width=2,\
                               style=filled,\
                               color=blue,\
                               pos = \"" + str(x.cord1) + "," +
                                                          str(x.cord2) +
                                                          "!\"];\n")
        for x in range(1, len(self.vertices)):
            custo = self.vertices[x-1].distancia(self.vertices[x])
            f.write(self.vertices[x - 1].label +
                    " -> " + self.vertices[x].label)
            f.write("[penwidth=12,label=\"" +
                    str(custo) +
                    "\",weight=\"" +
                    str(custo) + "\"];\n")
        custo = self.vertices[1].distancia(self.vertices[0])
        f.write(self.vertices[-1].label + " -> " + self.vertices[0].label)
        f.write("[penwidth=12,label=\"" +
                str(custo) +
                "\",weight=\"" +
                str(custo) + "\"];\n")
        f.write("}")

def opt2(vertices):
    i = 0
    k = i + 1
    tam = len(vertices)
    while i < tam -1:
        f = vertices[:i]
        m = vertices[i:k]
        m.reverse()
        e = vertices[k:]
        if k < tam - 1:
            k += 1
        else:
            i += 1
            k = i + 1
        yield f + m + e

def custo(vertices):
    global custos
    if tuple(vertices) not in custos:
        custo = 0
        for x in range(len(vertices)):
            custo += vertices[x-1].distancia(vertices[x])
        custos[tuple(vertices)] = custo
    return custos[tuple(vertices)]


class vertice(object):
    def __init__(self, lbl, cord1, cord2):
        super(vertice, self).__init__()
        self.label = lbl
        self.cord1 = cord1
        self.cord2 = cord2
        self.distancias = {}

    def distancia(self, vertice2):
        if vertice2 not in self.distancias:
            self.distancias[vertice2] = hypot(self.cord1 - vertice2.cord1,
                                              self.cord2 - vertice2.cord2)
        return self.distancias[vertice2]


def ler_mapa():
    arqIn = parsed.input
    num_vertices = int(arqIn.readline())
    vertices = []
    for i in range(num_vertices):
        linha = str(arqIn.readline())
        linha = " ".join(linha.split())
        valores = linha.split(" ")
        vertices.append(vertice(
            cord1=float(valores[1]),
            cord2=float(valores[2]),
            lbl=str(valores[0])))
    return vertices


def genetico():
    vertices = ler_mapa()
    populacao = []
    i = 0
    if not parsed.csv is None:
        grafico_out = csv.writer(parsed.csv, delimiter=',')
    populacao.append(filho(vertices))	 
    cp = vertices[:]
    shuffle(cp)
    populacao.append(filho(cp))
    tam = len(populacao) // 3
    MelhorAnt = 0
    j = 0
    while True:
        i += 1
        populacao.sort(key=lambda x: x.custo)
        if not parsed.csv is None:
            grafico_out.writerow([i, populacao[0].custo])
        pai2 = int((pow(random(), 8) % (tam+1)) + 1)
        populacao = populacao[0].crossover(populacao[pai2])
        if i % parsed.step_size == 0 and parsed.debug:
            print ("Iteracao " + str(i) + " :" + str(populacao[0].custo))
        if MelhorAnt - populacao[0].custo == 0:
            j += 1
            if j == parsed.geracoes_desiste:
                break
        else:
            j = 0
            MelhorAnt = populacao[0].custo
    if parsed.dot is not None:
        populacao[0].to_dot_file()
    print (str(populacao[0].custo))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Genetico TSP")
    parser.add_argument('-d', '--dot', metavar="Nome do aruvivo dot",
                        action="store", type=argparse.FileType('w'),
                        help="Se especificado escreve\
                        um arquivo dot")
    parser.add_argument('-c', '--csv', action="store", type=argparse.FileType('w'),
                        help="Saida em arquivo CSV")
    parser.add_argument('-g', '--geracoes-desiste', metavar="Quantidade",
                        action="store", default=80, type=int,
                        help="Especifica o numero de gerações igauis até\
                        desistir")
    parser.add_argument('-p', '--populacao', metavar="Quantidade",
                        action="store", default=15, type=int,
                        help="Tamanho da populacão")
    parser.add_argument('-m', '--mutation-rate', metavar='Porcentagem',
                        action="store", default=15, type=int,
                        help="Porcentagem da probabilidade de ocorrer\
                        mutação")
    parser.add_argument('-s', '--step-size', metavar="Quantidade",
                        action="store", type=int, default=10,
                        help="Tamanho do passo da saida")
    parser.add_argument('-i', '--input', metavar="Arquivo de Entrada",
                        action="store", type=argparse.FileType('r'),
                        default=sys.stdin,
                        help="Nome do arquivo de entrada, se não\
                        especificado será tomada a entrada STDIN")
    parser.add_argument('--debug', action="store_true",
                        help="Imprimi iterações")
    parsed = parser.parse_args(sys.argv[1:])
    genetico()
