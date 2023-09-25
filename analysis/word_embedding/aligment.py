import numpy as np
import models

def align_models(model_1, model_2):
    """
    Align two word embedding models using the Orthogonal Procrustes algorithm
    https://en.wikipedia.org/wiki/Orthogonal_Procrustes_problem
    """
    embs1, (idx1, iidx1) = models.w2v_to_numpy(model_1)
    embs2, (idx2, iidx2) = models.w2v_to_numpy(model_2)

    aligned_embs1, aligned_embs2, (common_idx, common_iidx) = align_matrices(embs1, embs2, idx1, idx2)

    return aligned_embs1, aligned_embs2, (common_idx, common_iidx)

def procrustes(matrix_a, matrix_b):
    """
    Learn the best rotation matrix to align matrix B to A
    https://en.wikipedia.org/wiki/Orthogonal_Procrustes_problem
    """
    U, _, Vt = np.linalg.svd(matrix_b.T.dot(matrix_a))
    return U.dot(Vt)

def intersect_vocabulary(idx1: dict, idx2: dict):
  """ Intersect the two vocabularies

  Parameters:
  ===========
  idx1 (dict): the mapping for vocabulary in the first group
  idx2 (dict): the mapping for vocabulary in the second group

  Returns:
  ========
  common_idx, common_iidx (tuple): the common mapping for vocabulary in both groups
  """
  common = idx1.keys() & idx2.keys()
  common_vocab = [v for v in common]

  common_idx, common_iidx = {v:i for i,v in enumerate (common_vocab)}, {i:v for i,v in enumerate (common_vocab)}
  return common_vocab, (common_idx, common_iidx)

def align_matrices (mat1, mat2, idx1, idx2):
  """ Align the embedding matrices and their vocabularies.

  Parameters:
  ===========
  mat1 (numpy.ndarray): embedding matrix for first group
  mat2 (numpy.ndarray): embedding matrix for second group

  index1 (dict): the mapping dictionary for first group
  index2 (dict): the mapping dictionary for the second group

  Returns:
  ========
  remapped_mat1 (numpy.ndarray): the aligned matrix for first group
  remapped_mat2 (numpy.ndarray): the aligned matrix for second group
  common_vocab (tuple): the mapping dictionaries for both the matrices
  """  
  common_vocab, (common_idx, common_iidx) = intersect_vocabulary(idx1, idx2)
  row_nums1 = [idx1[v] for v in common_vocab]
  row_nums2 = [idx2[v] for v in common_vocab]

  #print (len(common_vocab), len (common_idx), len (common_iidx))
  remapped_mat1 = mat1[row_nums1, :]
  remapped_mat2 = mat2[row_nums2, :]
  #print (mat1.shape, mat2.shape, remapped_mat1.shape, remapped_mat2.shape)
  omega = procrustes (remapped_mat1, remapped_mat2)
  #print (omega.shape)
  # rotated_mat2 = np.dot (omega, remapped_mat2)
  rotated_mat2 = np.dot (remapped_mat2, omega)

  return remapped_mat1, rotated_mat2, (common_idx, common_iidx)