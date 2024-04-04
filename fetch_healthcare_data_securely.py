import multiprocessing
import requests
import json

# Lists of IDs 
Dni = [

]
#Lists of BirthDates
fechaNac = [

]

# Ensure the lists have the same length
assert len(Dni) == len(fechaNac), "Dni and fechaNac lists must have the same length."

# File to write the results
file_name = "output.txt"

def parallel_process(Dni, fechaNac, file_name):
    with open(file_name, "a+", encoding="ISO-8859-1") as file_write:
        try:
            jsonString = json.dumps({
                "fecNac": fechaNac, "codPais": "PER", "nroDni": Dni, "tipoDoc": "1"
            })
            r = requests.post(
                "",# IMPORTANT: The URL for the request has been omitted to protect sensitive personal information.
                json=jsonString
            )
            data = r.json()

            # Simplified logic for writing to the file based on the response
            if not data.get("listaCiudadano"):
                file_write.writelines(f"{Dni} | No afiliado\n")
            else:
                # Process and write detailed information for each citizen
                # This part is omitted for brevity but follows the logic of parsing `data` and writing to `file_write`
                pass
        except Exception as e:
            file_write.writelines(f"{Dni} | ERROR: {str(e)}\n")

def worker(tasks, file_name):
    for Dni, fechaNac in tasks:
        parallel_process(Dni, fechaNac, file_name)

def distribute_work(Dni, fechaNac, file_name, num_workers=4):
    # Create batches of tasks for each worker
    tasks = list(zip(Dni, fechaNac))
    chunk_size = len(tasks) // num_workers + (len(tasks) % num_workers > 0)
    task_batches = [tasks[i:i + chunk_size] for i in range(0, len(tasks), chunk_size)]

    # Start multiprocessing
    processes = []
    for i in range(min(num_workers, len(task_batches))):
        p = multiprocessing.Process(target=worker, args=(task_batches[i], file_name))
        processes.append(p)
        p.start()

    # Wait for all processes to finish
    for p in processes:
        p.join()

if __name__ == "__main__":
    distribute_work(Dni, fechaNac, file_name)
