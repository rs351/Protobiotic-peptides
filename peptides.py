import os
import subprocess

root_dir = "/path/to/your/root/directory"  # Change this to your actual root directory
tmalign_executable = os.path.join(root_dir, "TMalign")
tmscore_executable = os.path.join(root_dir, "TMscore")

output_file = os.path.join(root_dir, "outs_all_combined.txt")

with open(output_file, "w") as out:
    pass  # clear file

for enzyme_dir in [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]:
    enzyme_path = os.path.join(root_dir, enzyme_dir)

    for pdb_folder in [d for d in os.listdir(enzyme_path) if os.path.isdir(os.path.join(enzyme_path, d))]:
        pdb_folder_path = os.path.join(enzyme_path, pdb_folder)
        orig_pdb = next((os.path.join(pdb_folder_path, f) for f in os.listdir(pdb_folder_path) if f.endswith(".pdb")), None)
        if not orig_pdb:
            continue

        for folder in ["johnson", "murch_recent", "parker", "bennu"]:
            folder_dir = os.path.join(pdb_folder_path, folder)
            if not os.path.isdir(folder_dir):
                continue

            range_N = 6 if folder == "murch_recent" else 4 if folder == "johnson" else 3 if folder == "bennu" else 7

            for subfolder in map(str, range(range_N)):
                subfolder_dir = os.path.join(folder_dir, subfolder)
                if not os.path.isdir(subfolder_dir):
                    continue

                for test_folder in [d for d in os.listdir(subfolder_dir) if os.path.isdir(os.path.join(subfolder_dir, d))]:
                    test_folder_dir = os.path.join(subfolder_dir, test_folder)
                    test_pdb = next((os.path.join(test_folder_dir, f) for f in os.listdir(test_folder_dir) if f.endswith(".pdb")), None)
                    if not test_pdb:
                        continue

                    # Run TMalign
                    tmalign_result = subprocess.run([tmalign_executable, orig_pdb, test_pdb], capture_output=True, text=True)
                    rmsd = "NA"
                    for line in tmalign_result.stdout.splitlines():
                        if "RMSD=" in line:
                            try:
                                rmsd = line.split("RMSD=")[1].split(",")[0].strip()
                            except (IndexError, ValueError):
                                continue
                            break

                    # Run TMscore
                    tmscore_result = subprocess.run([tmscore_executable, orig_pdb, test_pdb], capture_output=True, text=True)
                    tmscore = "NA"
                    maxsub = "NA"
                    for line in tmscore_result.stdout.splitlines():
                        if line.strip().startswith("TM-score") and "d0=" in line:
                            try:
                                tmscore = line.split("=")[1].split("(")[0].strip()
                            except (IndexError, ValueError):
                                continue
                        if "MaxSub-score" in line:
                            try:
                                maxsub = line.split("=")[1].strip().split()[0]
                            except (IndexError, ValueError):
                                continue

                    with open(output_file, "a") as out:
                        out.write(f"Enzyme: {enzyme_dir}, PDB: {pdb_folder}, Source: {folder}, Index: {subfolder}\n")
                        out.write(f"TM-score: {tmscore}, RMSD: {rmsd}, MaxSub-score: {maxsub}\n\n")

                    print(f"✔ {enzyme_dir}, {pdb_folder}, {folder}, {subfolder},{test_folder_dir[-1]}→ TM-score: {tmscore}, RMSD: {rmsd}, MaxSub-score: {maxsub}")