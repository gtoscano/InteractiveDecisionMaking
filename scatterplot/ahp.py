# Analytic Hierarchy Process (AHP) for Multi-Criteria Decision Making (MCDM)

import numpy as np

# User-provided Pairwise Comparison Matrix for Criteria
criteria_matrix = np.array([[1, 3, 5],
                            [1/3, 1, 4],
                            [1/5, 1/4, 1]])

# User-provided Pairwise Comparison Matrix for Alternatives (for one criterion, e.g., f1)
alternative_matrix = np.array([[1, 3, 5, 2],
                               [1/3, 1, 4, 1],
                               [1/5, 1/4, 1, 1/3]])

# Calculate the priority vectors for Criteria and Alternatives
criteria_priority_vector = np.mean(criteria_matrix, axis=1)
alternative_priority_vector = np.mean(alternative_matrix, axis=1)

# Normalize the priority vectors
criteria_priority_vector /= np.sum(criteria_priority_vector)
alternative_priority_vector /= np.sum(alternative_priority_vector)

# Transpose the criteria_priority_vector to make it a column vector
criteria_priority_vector = criteria_priority_vector[:, np.newaxis]

# Calculate the final ranking score for each alternative
final_ranking_scores = np.dot(alternative_matrix, criteria_priority_vector)

# Rank the alternatives based on final ranking scores
ranking_order = np.argsort(final_ranking_scores, axis=0).flatten()  # Sort in ascending order

# Print the final ranking
print("Final Ranking Order of Alternatives:", ranking_order)
