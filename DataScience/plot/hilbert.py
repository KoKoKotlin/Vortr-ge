import numpy as np
import os

def create_hiltbert_mat(n):
    hilbert_mat = []
    for j in range(n):
        hilbert_mat.append([])
        for i in range(n):
            hilbert_mat[j].append(1 / (i+j+1))

    return np.array(hilbert_mat)

def main():
    for n in range(10, 40, 5):
        with open("eigs.csv", "w") as f:
            hilbert = create_hiltbert_mat(n)
            
            for idx, val in enumerate(np.linalg.eigvals(hilbert)):
                f.write(f"{idx+1},{val}\n")

        with open("errors.csv", "w") as f:
            P, D, Q = np.linalg.svd(hilbert, full_matrices=False)
            for rank in range(1, n):
                k_approx = np.matrix(P[:, :rank]) * np.diag(D[:rank]) * np.matrix(Q[:rank, :])
                f.write(f"{rank},{np.linalg.norm(hilbert - k_approx)}\n")
        
        os.system(f"gnuplot -e \"filename=\'hilbert{n}.png\'\" eigs.gnuplot")
        os.system(f"gnuplot -e \"filename=\'errors{n}.png\'\" errors.gnuplot")

if __name__ == "__main__":
    main()