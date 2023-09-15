import sys

from pathlib import Path
CURRENT_POSITION = Path(__file__).parent
sys.path.append(f"{CURRENT_POSITION}/../..")


from phidias.Types import *
from phidias.Lib import *
from phidias.Main import *
from phidias.Agent import *

# beliefs interpreted by the robot
class go_to(Belief): pass
class add_to(Belief): pass
class queue_element(Belief): pass
class clear_path(Belief): pass

class target_reached(Reactor): pass

class add(Procedure): pass # aggiunte un punto in coda al percorso;
class go(Procedure): pass  # avvia il robot facendo si che esso raggiunga i punti stabiliti secondo i diagrammi di Voronoi
class clear(Procedure): pass # cancella i dati di un percorso precedentemente stabilito

def_vars('X', 'Y', 'F')

# ---------------------------------------------------------------------
# Agent 'main'
# ---------------------------------------------------------------------
class main(Agent):
    def main(self):
        # per andare al prossimo checkpoint
        go(X,Y) >> [ +go_to(X,Y)[{'to': 'robot@127.0.0.1:6566'}] ] 
        # per aggiungere un punto alla coda di target
        add(X,Y) >> [ +queue_element(X,Y), show_line("Aggiunto (", X, ",", Y, ") alla coda di target."), \
                      +add_to(X,Y)[{'to': 'robot@127.0.0.1:6566'}]]
        # avviare il robot
        go() / queue_element(X,Y) >> [ -queue_element(X,Y), \
                                        go(X,Y), \
                                        show_line("Nuovo target: (", X, ",", Y, ")"),
                                        ]
        # pulire coda di target
        clear() / queue_element(X,Y) >> [ -queue_element(X,Y), \
                                          clear(), show_line("La coppia (", X, ",", Y, ") è stata cancellata."), \
                                          +clear_path()[{'to': 'robot@127.0.0.1:6566'}]]
        # notificare il raggiungimento del target
        +target_reached()[{'from': F}] >> [ show_line("Target reached"), go()]

        


ag = main()
ag.start()
PHIDIAS.run_net(globals(), 'http')
PHIDIAS.shell(globals())