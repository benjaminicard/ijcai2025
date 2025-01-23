# -*- coding: utf-8 -*-
"""ijcai2025_asp_clingor.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1j9rHxy7mQytPD91zpJftNaxErNX3G18S
"""

!pip install clingo
!pip install clyngor-with-clingo

import clingo
import tempfile
from clyngor import ASP, solve

# Commented out IPython magic to ensure Python compatibility.
# program1 = """
# 
# % FACTS
# 
# % Main protagonists of the story
# person(p1;p2).
# 
# % Possible locations
# location(madrid;cemetery;family).
# 
# % Current and potential situations
# situation(s1).
# situation(s2).
# situation(s3).
# 
# 
# % Belief base for the environment's objective facts and for the main agent's beliefs
# beliefbase(env;p1).
# 
# 
# % Description of situation s1 (current situation)
# 
# %% Beliefs about location
# bel(env, at(r,cemetery)) :-situation(s1).
# bel(p1, at(r,family)):-situation(s1).
# 
# %% Beliefs about hostility
# bel(p1,hostile(p2)) :-situation(s1).
# bel(env,hostile(p2)):-situation(s1).
# bel(env,murderer(p2)):-situation(s1).
# %bel(p1,murderer(p2)):-situation(s1).
# 
# %% Beliefs about credible locations
# bel(p1,cred(at(r,madrid), p2)):-situation(s1).
# bel(p1,cred(at(r,cemetery), p2)):-situation(s1).
# bel(p1,cred(at(r,family), p2)):-situation(s1).
# bel(env,cred(at(r,cemetery), p2)):-situation(s1).
# bel(env,cred(at(r,family), p2)):-situation(s1).
# 
# % Relation between questioning round and actions
# nbAsk(0..1).
# bel(0,env,ask(p2,where,p1,0)).
# bel(0,p1,ask(p2,where,p1,0)).
# 0{act(D,tell(p1,at(r,L), p2, N)):location(L)}1 :- bel(D,env,ask(p2,where,p1,N)), bel(D,p1,ask(p2,where,p1,N)), nbAsk(N).
# 0{act(D+1,tell(p1,at(r,L), p2, N)):location(L)}1 :- bel(D,env,ask(p2,where,p1,N)), not bel(D,p1,ask(p2,where,p1,N)), nbAsk(N).
# act(D, silence(p1, p2, N)):- not act(D,tell(p1,_,p2,N)), bel(D,env,ask(p2,where,p1,N)), bel(D,p1,ask(p2,where,p1,N)), nbAsk(N).
# act(D+1, silence(p1, p2, N)):- not act(D+1,tell(p1,_,p2,N)), bel(D,env,ask(p2,where,p1,N)), not bel(D,p1,ask(p2,where,p1,N)), nbAsk(N).
# 
# 
# 
# % ----------------------------------------------------------------------------------------------------------------
# 
# % RULES FOR PHYSICAL ACTIONS
# % Rule for checking a location
# bel(D,Y,check(P2,X,P1)) :- act(D,tell(P1, at(r,X), P2, N)), bel(Y,cred(at(r,X), P2)),nbAsk(N).
# 
# % Rule for reasking a question based on non-credible information
# bel(D,Y,ask(P2, where, P1, N+1)) :- act(D,tell(P1, at(r,X), P2, N)), not bel(Y,cred(at(r,X), P2)), nbAsk(N),nbAsk(N+1), beliefbase(Y).
# 
# % Rule for evasion
# bel(D,Y,evade(P1,P2)) :- bel(D,Y,check(P2,madrid,P1)).
# 
# % Rule for killing
# bel(D,Y,kill(P2,r,P1)) :- bel(D,Y,check(P2,X,P1)), bel(Y,at(r,X)), bel(Y,hostile(P2)).
# 
# % Rule for helping
# bel(D,Y,help(P2)) :- bel(D,Y,check(P2,X,P1)), bel(Y,at(r,X)), not bel(Y,hostile(P2)).
# 
# % Rule for agents loosing patience (first condition)
# bel(D,Y,patienceLost(P2, P1)) :- act(D,tell(P1, at(r,X), P2, N)), not bel(Y,cred(at(r,X), P2)), bel(Y,hostile(P2)), nbAsk(N), not nbAsk(N+1).
# 
# % Rule for agents loosing patience (second condition)
# bel(D,Y,patienceLost(P2, P1)) :- act(D,silence(P1, P2,N)), bel(Y,hostile(P2)),nbAsk(N).
# 
# % Rule for wrong information provided
# bel(D,Y,wrongInfo(P2, P1)) :- bel(D,Y,check(P2, X, P1)), not bel(Y,at(r,X)).
# 
# % Rule for an agent being harmed based on another agenr loosing patience
# bel(D,Y,harm(P2, P1)) :- bel(D,Y,patienceLost(P2, P1)).
# 
# % Rule for an agent being harmed based on hostility and another agent providing wrong information
# bel(D,Y,harm(P2, P1)) :- bel(D,Y,wrongInfo(P2, P1)), bel(Y,hostile(P2)), not bel(D,Y,evade(P1,P2)).
# 
# 
# % ----------------------------------------------------------------------------------------------------------------
# 
# % RULES FOR SPEECH ACTS
# % Rule for honest communication based on agents' telling what they believe
# honest(D,P,F) :- act(D,tell(P,F,_,_)), bel(P,F).
# 
# % Rule for dishonest communication based on agents' not telling what they believe
# dishonest(D,P,F) :- act(D,tell(P,F,_,_)), not bel(P,F).
# 
# % Rules for telling objective truth based on the environment's belief
# truth(D,P,F) :- act(D,tell(P,F,_,_)), bel(env,F).
# 
# % Rules for telling objective falsity based on the environment's belief
# falsity(D,P,F) :- act(D,tell(P,F,_,_)), not bel(env,F).
# 
# % Rules for telling an objective truth or an erroneous truth
# objective_truth(D,P,F) :- honest(D,P,F), truth(D,P,F).
# erroneous_truth(D,P,F) :- honest(D,P,F), falsity(D,P,F).
# 
# % Rules for telling an objective lie or an erroneous lie
# objective_lie(D,P,F) :- dishonest(D,P,F), falsity(D,P,F).
# erroneous_lie(D,P,F) :- dishonest(D,P,F), truth(D,P,F).
# 
# 
# %%%%%%%%%%%%%%%  DEONTOLOGISM %%%%%%%%%%%%%%%%%%
# 
# % Maxims prohibiting lying and murder for deontologism
# maxim(doNotLie;doNotEnableMurder).
# 
# % Rule concerning the violation of the maxim against lying
# violated(D,doNotLie) :- dishonest(D,P,F).
# 
# % Rule concerning the violation of the maxim against murder
# violated(D,doNotEnableMurder) :- bel(D,P1,kill(P2,r,P1)).
# 
# % Permissibility and impermissibility for deontologism
# imp(deontologism,D):- violated(D,R), maxim(R).
# per(deontologism,D):- not imp(deontologism,D), act(D,_).
# 
# 
# %%%%%%%%%%%%%%%  PRINCIPIALISM VERSION 1 %%%%%%%%%%%%%%%
# 
# % Principle prohibiting lying with exception and murder for principialism1
# principle(doNotLieExcept;doNotEnableMurder).
# 
# % Rule stating violation of lying principle in the absence of first exception
# violated(D,doNotLieExcept) :- act(D,tell(P,F,P2,N)), not bel(P,F), not exception(act(D,tell(P,F,P2,N)),doNotLieExcept).
# 
# % Rule stating that Falangists do not deserve truth
# dontDeserveTruth(P2):- bel(p1,murderer(P2)).
# 
# % First exception rule for lies: lying is permitted if truth is not deserved
# exception(act(D,tell(P,F,P2,N)),doNotLieExcept):- act(D,tell(P,F,P2,N)), dontDeserveTruth(P2).
# 
# % Permissibility and impermissibility for principialism1
# imp(principialism1, D) :- violated(D, R), principle(R).
# per(principialism1, D) :- not imp(principialism1, D), act(D, _).
# 
# 
# %%%%%%%%%%%%%%%  UTILITIES CALCULATIONS %%%%%%%%%%%%%%%%%%
# 
# % Expected utilities for various physical actions according to consequentialism
# uti(kill(P2,r,P1),-4):-person(P2), person(P1).
# uti(harm(P1,P2),-2):-person(P2), person(P1).
# uti(wrongInfo(P1,P2),0):-person(P2), person(P1).
# uti(help(P),2):-person(P).
# 
# % Actions triggering specific utility values
# trigUti(D,Y,F,N) :- uti(F,N), bel(D,Y,F), beliefbase(Y).
# 
# % Calculation of total utility values for agents and actions
# totalUti(D,Y,T):- T=#sum{N:uti(F,N),bel(D,Y,F)}, beliefbase(Y),act(D,_).
# 
# 
# #show act/2.
# #show bel/2.
# #show bel/3.
# #show imp/2.
# #show per/2.
# #show violated/2.
# #show trigUti/4.
# #show totalUti/3.
# #show objective_lie/3.
# #show objective_truth/3.
# #show subjective_lie/3.
# #show erroneous_truth/3.
# #show beliefbase/1.
# #show principle/1.
# 
# """
#

answers = ASP(program1)

def imprimer(N, L):
    print("Answer Set ", N)
    for X in L:
        print(X[0], X[1])
n = 1
for answer in answers:
    imprimer(n, answer)
    n = n+1

# Commented out IPython magic to ensure Python compatibility.
# #############  PRINCIPIALISM VERSION 2 ####################  +  #############  CONSEQUENTIALISM VERSIONS 1 AND 2 ####################
# 
# 
# # Define program2
# program2 = """
# 
# 
# % PRINCIPIALISM VERSION 2
# % Rule for comparing decisions based on counterfactual comparison
# counterfactual(S1, S2, tell(P1, at(r, L1), P2, N)) :-
#     act(S1, D, tell(P1, at(r, L1), P2, N)), L1!=L2,
#     bel(P1, at(r, L2)),
#     act(S2, D, tell(P1, at(r, L2), P2, N)),
#     {act(S1, D2, A2) : D2<D, not act(S2, D2, A2)}0,
#     {act(S2, D3, A3) : D3<D, not act(S1, D3, A3)}0,
#     {act(S1, D, A4) : A4 != tell(p1, at(r, L1), p2, N), not act(S2, D, A4)}0.
# 
# % Second exception rule for lies: lying is permitted if truth leads to worst consequences
# exceptionRel(S, D, doNotLieExcept) :-
#     act(S, D, tell(p1, at(r, L1), P2, N)),
#     counterfactual(S, S2, tell(p1, at(r, L1), P2, N)),
#     totalUti(S, D, p1, T1),
#     totalUti(S2, D, p1, T2),
#     T1 > T2.
# 
# % Rule stating (local) violation of lying principle in the absence of second exception
# violated(S, D, R) :-
#     locally_violated(S,D,R),
#     not exceptionRel(S, D, R).
# 
# % Permissibility and impermissibility for principialism2
# per(principialism2, S, D) :- not imp(principialism2, S, D), act(S,D, _).
# imp(principialism2, S, D) :- violated(S, D, R), principle(R).
# 
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# 
# % CONSEQUENTIALISM VERSION 1
# % Permissibility and impermissibility for consequentialism1
# imp(consequentialism1,S,D) :- totalUti(S,D,p1,N1), totalUti(S2,D,p1,N2), N2>N1.
# per(consequentialism1,S,D) :- not imp(consequentialism1,S,D), act(S,D,_).
# 
# 
# % CONSEQUENTIALISM VERSION 2
# % Calculation of total utility based on sums of total utilities of each action
# totalUti2(S,D,Y,T) :- T=#sum{N:totalUti(S,D2,Y,N),D2>=D}, beliefbase(Y),act(S,D,_).
# 
# % Permissibility and impermissibility for consequentialism2
# imp(consequentialism2,S,D) :- totalUti2(S,D,env,N1), totalUti2(S2,D,env,N2), N2>N1.
# per(consequentialism2,S,D) :- not imp(consequentialism2,S,D), act(S,D,_).
# 
# %#show totalUti/4.
# %#show locally_violated/3.
# #show violated/3.
# %#show act/3.
# #show exceptionRel/3.
# #show counterfactual/3.
# #show per/3.
# #show imp/3.
# """
# 
# # Function to convert answer sets to valid ASP facts
# def answer_set_to_facts(answer_set,n,first):
#     formatted_facts = []
#     transmit= [("bel",2),("beliefbase",1), ("principle",1)]
#     augment = [("act",2),("totalUti",3)]
#     renamedAug = {("violated",2):"locally_violated"}
#     for fact in answer_set:
#         # Handle complex terms
#         name = fact[0]
#         args = fact[1] if isinstance(fact[1], tuple) else (fact[1],)
#         arity = len(args)
#         if first and (name,arity) in transmit :
#           formatted_facts.append(f"{name}({','.join(map(str, args))}).")
#         if (name,arity) in augment:
#           newargs = ('s'+str(n),)+args
#           formatted_facts.append(f"{name}({','.join(map(str, newargs))}).")
#         if (name,arity) in renamedAug:
#           newargs = ('s'+str(n),)+args
#           newname = renamedAug[(name,arity)]
#           formatted_facts.append(f"{newname}({','.join(map(str, newargs))}).")
#     return "\n".join(formatted_facts)
# 
# # Run program1 to get its answer sets
# answers_program1 = ASP(program1)
# combined_program = ""
# 
# # Process each answer set from program1
# for n, answer_set in enumerate(answers_program1, start=1):
#     print(f"Processing Answer Set {n} of program1...")
# 
#     # Convert answer set to ASP facts
#     facts_from_program1 = answer_set_to_facts(answer_set,n,(n==1))
# 
#     # Combine program1 and program2
#     combined_program = combined_program+"%AS"+str(n)+"\n"+f"{facts_from_program1}\n"
# 
# combined_program=combined_program+"\n"+program2
# print(combined_program)
# 
# # Run the combined program
# answers_program2 = ASP(combined_program)
# 
# # Output results for this specific answer set
# for m, result in enumerate(answers_program2, start=1):
#         print(f"Answer Set {m} of program2 for Answer Set {n}:")
#         for fact in result:
#             print(fact)
