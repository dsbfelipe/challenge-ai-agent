from agent.agent import run_search

if __name__ == "__main__":
    print("Busca inteligente (digite 'exit' para sair)")
    while True:
        q = input("Buscar: ")
        if q.lower() == "exit":
            break

        response = run_search(q)
        print(response)