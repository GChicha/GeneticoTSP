#!/usr/bin/env python

from random import *
from math import hypot
import sys
custos = {}


class filho(object):
    """docstring for fiho."""
    def __init__(self, vertices):
        super(filho, self).__init__()
        self.vertices = vertices
        self.mutation(20)
        self.custo = self.__custo()
        self.firstImprovement()

    def firstImprovement(self):
        for v in opt2(self.vertices):
            f = custo(v)
            if f < self.custo:
                self.vertices = v
                self.custo = f
                break

    def mutation(self, chance):
        for i in range(5):
            if randint(chance - 100, chance) > 0:
                x = randint(0, len(self.vertices)-1)
                y = randint(0, len(self.vertices)-1)
                temp = self.vertices[x]
                self.vertices[x] = self.vertices[y]
                self.vertices[y] = temp

    def __custo(self):
        custo = custos.get(tuple(self.vertices))
        if custo is None:
            custo = 0
            for x in range(len(self.vertices)):
                custo += self.vertices[x-1].distancia(self.vertices[x])
        return custo

    def crossover(self, filho2):
        populacao = [self, filho2]
        tam = len(self.vertices)
        while len(populacao) < 15:
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

    def to_dot_file(self, arquivo):
        f = open(arquivo, "w")
        f.write("digraph {")
        for x in self.vertices:
            f.write(x.label + "[sfixedsize=true,\
                               height=2,\
                               width=2,\
                               style=filled,\
                               color=blue,\
                               pos = \"" + str(x.cord1) + "," +
                                                          str(x.cord2) +
                                                          "!\"];")
        for x in range(1, len(self.vertices)):
            custo = self.vertices[x-1].distancia(self.vertices[x])
            f.write(self.vertices[x - 1].label +
                    " -> " + self.vertices[x].label)
            f.write("[penwidth=12,label=\"" +
                    str(custo) +
                    "\",weight=\"" +
                    str(custo) + "\"];")
        custo = self.vertices[1].distancia(self.vertices[0])
        f.write(self.vertices[-1].label + " -> " + self.vertices[0].label)
        f.write("[penwidth=12,label=\"" +
                str(custo) +
                "\",weight=\"" +
                str(custo) + "\"];")
        f.write("}")


class opt2(object):
    """docstring for opt2."""
    def __init__(self, vertices):
        super(opt2, self).__init__()
        self.vertices = vertices
        self.i = 0
        self.k = self.i + 1
        self.tam = len(self.vertices)

    def __iter__(self):
        return self

    def next(self):
        if self.i > self.tam - 1:
            raise StopIteration()
        f = self.vertices[:self.i]
        m = self.vertices[self.i:self.k]
        m.reverse()
        e = self.vertices[self.k:]
        if self.k < self.tam - 1:
            self.k = self.k + 1
        else:
            self.i = self.i + 1
            self.k = self.i + 1
        return f + m + e


def custo(vertices):
    custo = custos.get(tuple(vertices))
    if custo is None:
        custo = 0
        for x in range(len(vertices)):
            custo += vertices[x-1].distancia(vertices[x])
    return custo


class vertice(object):
    def __init__(self, lbl, cord1, cord2):
        super(vertice, self).__init__()
        self.label = lbl
        self.cord1 = cord1
        self.cord2 = cord2
        self.distancias = {}

    def distancia(self, vertice2):
        if self.distancias.get(vertice2) is None:
            self.distancias[vertice2] = hypot(self.cord1 - vertice2.cord1,
                                              self.cord2 - vertice2.cord2)
        return self.distancias.get(vertice2)


def ler_mapa():
    if len(sys.argv) > 2:
        arqIn = open(sys.argv[2])
    else:
        arqIn = sys.stdin
    num_vertices = int(arqIn.readline())
    vertices = []
    for i in range(num_vertices):
        linha = str(arqIn.readline())
        valores = linha.split(" ")
        vertices.append(vertice(
            cord1=float(valores[1]),
            cord2=float(valores[2]),
            lbl=str(valores[0])))
    return vertices


def genetico():
    if len(sys.argv) > 1:
        persiste = int(sys.argv[1])
    else:
        persiste = 5
    vertices = ler_mapa()
    populacao = []
    i = 0
    while len(populacao) < 15:
        cp = vertices[:]
        shuffle(cp)
        populacao.append(filho(cp))
    MelhorAnt = 0
    j = 0
    while True:
        i += 1
        populacao.sort(key=lambda x: x.custo)
        populacao = populacao[0].crossover(populacao[1:5][randint(0, 3)])
        if i % 100 == 0:
            print "Iteracao " + str(i) + " :" + str(populacao[0].custo)
            if MelhorAnt - populacao[0].custo == 0:
                j += 1
                if j == persiste:
                    break
            else:
                j = 0
                MelhorAnt = populacao[0].custo
    if len(sys.argv) > 2:
        populacao[0].to_dot_file(sys.argv[2])
    print "Melhor solucao: " + str(populacao[0].custo)


if __name__ == '__main__':
    genetico()
