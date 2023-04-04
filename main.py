from automate import *

##creation d'etats
#s1 : State
s1 = State(1,True,False)
#s2 : State
s2 = State(2,False,True)

#listeStates : List[States]
listeStates = [s1,s2]


##creation de transitions
#t1 : Transition
t1 = Transition(s1,"a",s1)
# t2 : Transition
t2 = Transition(s1,"a",s2)
# t3 : Transition
t3 = Transition(s1,"b",s2)
# t4 : Transition
t4 = Transition(s2,"a",s2)
# t5 : Transition
t5 = Transition(s2,"b",s2)

# listeTransition: List[Transition]
liste = [t1,t2,t3,t4,t5]

## création de l’automate
# aut : Automate
aut = Automate(liste)
autbis = Automate([t1,t3,t4])

#test succ
print(aut.succ(listeStates,"a"))

#test accepte
print(aut.accepte(aut,"aab"))
print(aut.accepte(aut,"abaab"))
print(aut.accepte(aut,""))

#test estComplet
print(aut.estComplet(aut,"ab"))
print(aut.estComplet(aut,"abc"))

#test estDeterministe
print(aut.estDeterministe(aut))

#test completeAutomate
print(aut.completeAutomate(aut,"ab"))

#test Determinisation
print(aut.determinisation(aut))

#test Complémentaire
print(aut.complementaire(aut,"ab"))

#test Intersection
print(aut.intersection(aut, autbis))
