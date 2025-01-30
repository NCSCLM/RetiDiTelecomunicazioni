import copy

def initialize_routing_table(nodes, edges):
    """
    Genera la tabella di routing iniziale per ciascun nodo della rete.
    :param nodes: Lista contenente i nodi presenti nella rete.
    :param edges: Lista di tuple (nodo1, nodo2, costo) che rappresentano i collegamenti tra i nodi.
    :return: Dizionario con la tabella di routing di ogni nodo.
    """
    routing_table = {}
    for node in nodes:
        # Assegna inizialmente un costo infinito verso tutti gli altri nodi tranne se stesso
        routing_table[node] = {n: {'cost': float('inf'), 'next_hop': None} for n in nodes}
        routing_table[node][node] = {'cost': 0, 'next_hop': node}  # Percorso a se stesso con costo zero

    for edge in edges:
        # Configura il costo e il next-hop per i collegamenti diretti tra nodi
        nodo1, nodo2, costo = edge
        routing_table[nodo1][nodo2] = {'cost': costo, 'next_hop': nodo2}
        routing_table[nodo2][nodo1] = {'cost': costo, 'next_hop': nodo1}

    return routing_table

def print_routing_table(routing_table):
    """
    Mostra la tabella di routing per ogni nodo, indicando costi e next-hop.
    :param routing_table: Dizionario contenente tutte le tabelle di routing.
    """
    for node, table in routing_table.items():
        print(f"Tabella di routing del nodo {node}:")
        for dest, data in table.items():
            cost = data['cost']
            next_hop = data['next_hop']
            print(f"  {dest}: costo={cost}, next_hop={next_hop}")
        print("\n")

def distance_vector_routing(nodes, edges, max_iterations=10):
    """
    Simula il funzionamento del protocollo Distance Vector Routing aggiornando iterativamente le tabelle di routing.
    :param nodes: Lista di nodi all'interno della rete.
    :param edges: Lista di connessioni dirette con relativi costi.
    :param max_iterations: Numero massimo di iterazioni per la convergenza dell'algoritmo.
    :return: Tabella di routing risultante dopo la simulazione.
    """
    # Generazione della tabella di routing iniziale
    routing_table = initialize_routing_table(nodes, edges)

    for iteration in range(max_iterations):
        print(f"Iterazione {iteration + 1}:")
        updated = False
        # Creazione di una copia della tabella per evitare modifiche simultanee
        new_table = copy.deepcopy(routing_table)

        for node in nodes:
            for neighbor in nodes:
                # Ignora i nodi che non sono direttamente connessi
                if neighbor == node or routing_table[node][neighbor]['cost'] == float('inf'):
                    continue

                for dest in nodes:
                    # Evita di calcolare percorsi inutili verso se stesso
                    if dest == node:
                        continue

                    # Calcola un possibile nuovo percorso passando per il nodo vicino
                    new_cost = routing_table[node][neighbor]['cost'] + routing_table[neighbor][dest]['cost']
                    if new_cost < routing_table[node][dest]['cost']:
                        # Aggiornamento della tabella con il percorso più efficiente individuato
                        new_table[node][dest]['cost'] = new_cost
                        new_table[node][dest]['next_hop'] = routing_table[node][neighbor]['next_hop']
                        updated = True

        # Aggiornamento della tabella di routing per l'iterazione successiva
        routing_table = new_table
        print_routing_table(routing_table)

        # Se non ci sono stati cambiamenti, la convergenza è raggiunta e l'algoritmo si arresta
        if not updated:
            print("Le tabelle di routing hanno raggiunto la stabilità. Simulazione terminata.")
            break

    return routing_table

if __name__ == "__main__":
    # Definizione dei nodi e dei collegamenti nella rete
    nodes = ["Nodo A", "Nodo B", "Nodo C", "Nodo D"]
    edges = [
        ("Nodo A", "Nodo B", 1),
        ("Nodo B", "Nodo C", 2),
        ("Nodo A", "Nodo C", 4),
        ("Nodo C", "Nodo D", 1)
    ]

    print("Avvio della simulazione del protocollo Distance Vector Routing:\n")
    final_routing_table = distance_vector_routing(nodes, edges)

    print("Tabelle di routing finali:")
    print_routing_table(final_routing_table)