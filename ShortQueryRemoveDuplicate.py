def remove_duplicates(file_path):
    seen_lines = set()
    unique_lines = []

    with open(file_path, 'r') as file:
        for line in file:
            # Assuming the line format is "1 0 AP880620-0218 1 5.21 run_1"
            columns = line.strip().split()

            # Ignore the fifth column (index 4)
            key = tuple(columns[:4])

            # Check for duplicates based on the modified key
            if key not in seen_lines:
                seen_lines.add(key)
                unique_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(unique_lines)

if __name__ == "__main__":
    file_path = r"TRECAP88-90/collectiondedocuments/results.txt"

    remove_duplicates(file_path)

    print(f"Duplicates removed from {file_path}.")


