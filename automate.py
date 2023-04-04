# -*- coding: utf-8 -*-
from transition import *
from state import *
import os
import copy
from itertools import product
from automateBase import AutomateBase



class Automate(AutomateBase):

    def succElem(self, state, lettre):
        """State x str -> list[State]
        rend la liste des états accessibles à partir d'un état
        state par l'étiquette lettre
        """
        successeurs = []
        # t: Transitions
        for t in self.getListTransitionsFrom(state):
            if t.etiquette == lettre and t.stateDest not in successeurs:
                successeurs.append(t.stateDest)
        return successeurs


    def succ (self, listStates, lettre):
        """list[State] x str -> list[State]
        rend la liste des états accessibles à partir de la liste d'états
        listStates par l'étiquette lettre
        """
        #L:list[State]
        L = []
        #s:state
        for s in listStates:
                for t in self.getListTransitionsFrom(s):
                        if t.etiquette == lettre:
                                L.extend(self.succElem(s,lettre))
        return L




    """ Définition d'une fonction déterminant si un mot est accepté par un automate.
    Exemple :
            a=Automate.creationAutomate("monAutomate.txt")
            if Automate.accepte(a,"abc"):
                print "L'automate accepte le mot abc"
            else:
                print "L'automate n'accepte pas le mot abc"
    """
    @staticmethod
    def accepte(auto,mot) :
        """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
        """
        IS=auto.getListInitialStates()
        for l in mot:
                IS=auto.succ(IS,l)
        FS=auto.getListFinalStates()
        for f in IS:
                if f in FS:
                        return True
        return False


    @staticmethod
    def estComplet(auto,alphabet) :
        """ Automate x str -> bool
         rend True si auto est complet pour alphabet, False sinon
        """
        for s in auto.listStates:
                for a in alphabet:
                        if auto.succElem(s,a)==[]:
                                return False
        return True


    @staticmethod
    def estDeterministe(auto) :
        """ Automate  -> bool
        rend True si auto est déterministe, False sinon
        """
        #s:state
        for s in auto.listStates:
                for a in auto.getAlphabetFromTransitions():
                        if len(auto.succElem(s, a))>=2 :
                                return False;
        return True;



    @staticmethod
    def completeAutomate(auto,alphabet) :
        """ Automate x str -> Automate
        rend l'automate complété d'auto, par rapport à alphabet
        """
        if auto.estComplet(auto,alphabet):
                return auto
        else:
                for a in alphabet:
                        i=len(auto.listStates)
                        sini= State(-1,False,False)
                        auto.addState(sini)
                        for s in auto.listStates:
                                lt=[t.etiquette for t in auto.getListTransitionsFrom(s)]
                                if not (a in lt):
                                        # puit : State
                                        st = State(i, False, False)
                                        i=i+1
                                        auto.addState(st)
                                        #tt: Transition
                                        tt=Transition(sini,a,st)
                                        sini=st

        return auto



    @staticmethod
    def determinisation(auto) :
        """ Automate  -> Automate
        rend l'automate déterminisé d'auto
        """
        if (auto.estDeterministe()):
                return auto
        else:
                # listeTransition: List[Transition]
                liste = []
                #listState: List[State]
                ListS=[]
                #i:int
                i=0
                #premier_tour: bool
                premier_tour=True
                #state_not_in_auto: bool
                state_not_in_auto=True
                #s1 : State
                s1 = State(i,True,False)
                s1.label=auto.getListInitialStates()
                #FinlistS: List[State]
                FinlistS=[]
                FinlistS=auto.succElem(s1,a) #liste de toutes les trans  de s1 avec a
                ListS.append(s1)
                for s in FinlistS:
                        for a in auto.getAlphabetFromTransitions():
                                if (len(FinListS)!=0): #si transition existe
                                        i=i+1 
                                        if premier_tour:#pour eviter de refaire 2 fois ligne 149
                                                premier_tour=False
                                        else:
                                                FinlistS=auto.succElem(s1,a) #permet de faire avancer la boucle
                                        #st: State
                                        if (s.fin[2]==True):#ajout d'un état
                                                st= State(i,False,True)#avec caractere final si s final
                                        else:
                                                st=State(i,False,False)
                                        for f in FinlistS:
                                                st.label=st.label+FinlistS.label
                                        for si in ListS:#pour s'assurer que état avec le mm label pas déjà présent dans l'auto
                                                if si.label==st.label:
                                                        state_not_in_auto=False
                                                        st=si #transition ira vers un etat déjà existant
                                        if state_not_in_auto:        
                                                ListS.append(st)
                                liste.append(Transition(s1,a,st))#ajout à la liste finale de transition pr construire automate
                        s1=st
            return Automate(liste)

    @staticmethod
    def complementaire(auto,alphabet):  #tous les états finaux deviennent non finaux et si un état non complet, on ajoute une trans avec toutes les autres lettres vers un etat final où il ya boucle de ttes les lettres
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
        #s1 : State
        s1 = State(1,True,False)
        # LT: List[Transition]
        LT=auto.getListTransitionsFrom(s1)
        # aut : Automate
        aut = Automate(LT) # creation d'automate avec juste l'état init et ses trans
        #add: bool
        add = True #sert juste de support de retour à la fct addTransition, mais pas utile en soit
        #i :int
        i=len(auto.getListStates())
        while s in auto.getListStates():
                if (s.fin):
                        s.fin=False
                if not aut.estComplet(aut,alphabet):
                        #sf: State
                        sf=(i,False,True)
                        i=i+1
                        for a in alphabet:
                                #s_etiq:str
                                s_etiq=""
                                for t in LT:
                                        s=s+t.etiquette
                                if not (a in s): #pr ajouter seulement les transitions aux étiq différents de ceux déjà partant de s
                                        add=aut.addTransition(Transition(s1,a,st))
                                add=aut.addTransition(Transition(st,a,st)) #toutes les trans boucles
        return aut 

    @staticmethod
    def intersection (auto0, auto1):
        """ OBLIGATOIRE JUSQu'ICI Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        T=[]
        done=[] 
        L= list(intertools.product( auto0.getListInitialStates() , auto1.getListInitialStates() ))
        dico=dict()
        i=0

        while L!=[]:
            for lettre in auto.getAlphabetFromTransitions():
                if( auto0.succElem(T[0][0],lettre) != [] and auto1.succElem(T[0][1]) ):
                    key=L[0]
                    liste_c=list(intertools.product( auto0.succElem(T[0][0],lettre),auto1.succElem(T[0][1]) ) )
                    for c in liste_c:
                        if key not in dico:
                            s=State(i,key[0].init and key[1].init, key[0].fin and key[1].fin )
                            dico[key]=s
                            i+=1
                            if c in dico:
                              T.addTransition( Transition(dico[key],lettre, dico[c]) )
                            else :
                                s= State(i,c[0].init and c[1].init ,c[0].fin and c[1].fin )
                                T.addTransition( Transition(dico[key],lettre,s) )
                                i+=1
                                dico[c]=s
                        else :
                            if c in dico:
                                T.addTransition( Transition(dico[key], lettre , dico[c]) )
                            else:
                                s=State(i, c[0].init and c[1].init , c[0].fin and c[1].fin )
                                T.addTransition( Transition(dico[key] ,lettre , s) )
                                dico[c]=s
                                i+=1
                        if (c not in L) and (c not in done) :
                            L.append(c)
            done.append(L[0])
            L.pop(0)

        return Automate(T)

    @staticmethod
    def union (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        return


    @staticmethod
    def concatenation (auto1, auto2):
        """  SOIT SA OBLIGATOIRE Automate x Automate -> Automate
        rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """
        
        return


    @staticmethod
    def etoile (auto):
        """ SOIT SA OBLIGATOIRE Automate  -> Automate
        rend l'automate acceptant pour langage l'étoile du langage de a
        """
        return
