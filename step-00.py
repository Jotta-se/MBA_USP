import subprocess
import sys
import time
import os

def check_preconditions(expected_files):
    for filepath in expected_files:
        if not os.path.exists(filepath):
            return False, f"Arquivo não encontrado: {filepath}"
        if os.path.getsize(filepath) == 0:
            return False, f"Arquivo vazio: {filepath}"
    return True, ""

def run_step(step_script, expected_inputs):
    print(f"\n{'='*50}")
    print(f"Iniciando {step_script}...")
    print(f"{'='*50}")
    
    # Validação de pré-condições
    ok, error_msg = check_preconditions(expected_inputs)
    if not ok:
        print(f"\n[FALHA NA PRÉ-CONDIÇÃO] {step_script}: {error_msg}")
        sys.exit(1)
        
    start_time = time.time()
    
    try:
        # Executa o script e redireciona a saída para o terminal atual
        result = subprocess.run(
            [sys.executable, step_script],
            check=True,
            text=True
        )
        elapsed_time = time.time() - start_time
        print(f"\n[SUCESSO] {step_script} concluído em {elapsed_time:.2f} segundos.")
    except subprocess.CalledProcessError as e:
        print(f"\n[ERRO] A execução de {step_script} falhou com o código de saída {e.returncode}.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERRO INESPERADO] ao tentar executar {step_script}: {e}")
        sys.exit(1)

def main():
    steps = [
        {"script": "step-01.py", "inputs": ["Base_Estudo_PIB_IDH.csv"]},
        {"script": "step-02.py", "inputs": ["output/base_step_01.csv"]},
        {"script": "step-03.py", "inputs": ["output/base_step_01.csv"]},
        {"script": "step-04.py", "inputs": ["output/base_step_01.csv"]},
        {"script": "step-05-idh.py", "inputs": ["output/base_step_04.csv"]},
        {"script": "step-06-idh.py", "inputs": ["output/base_step_04.csv"]},
        {"script": "step-07-idh.py", "inputs": ["output/base_step_04.csv"]},
        {"script": "step-08-pib.py", "inputs": ["output/base_step_04.csv"]},
        {"script": "step-09-pib.py", "inputs": ["output/base_step_04.csv"]},
        {"script": "step-10-viz.py", "inputs": ["output/base_step_04.csv"]},
        {"script": "step-11.py", "inputs": ["output/base_step_04.csv"]},
        {"script": "step-12-viz.py", "inputs": ["output/base_step_04.csv"]},
        {"script": "step-13-viz.py", "inputs": ["output/base_step_04.csv", "output/modelo_pibagro_step_09.pkl"]},
        {"script": "step-14-viz.py", "inputs": ["output/base_step_04.csv"]}
    ]
    
    print("Iniciando orquestração dos passos (STEP-01 ao STEP-14)...\n")
    total_start_time = time.time()
    
    for step in steps:
        run_step(step["script"], step["inputs"])
        
    total_elapsed_time = time.time() - total_start_time
    print(f"\n{'='*50}")
    print(f"Todos os scripts foram executados com sucesso!")
    print(f"Tempo total de execução: {total_elapsed_time:.2f} segundos.")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
