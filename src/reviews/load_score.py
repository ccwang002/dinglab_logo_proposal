from collections import defaultdict

scores_by_proposals = defaultdict(list)
ranked_proposal_ids = [18, 23, 20, 17, 6, 19, 3, 5, 25, 9, 28, 11, 16, 21]


def add_score(score_str):
    scores = score_str.strip().split()
    assert len(scores) == 14
    for proposal_id, score in zip(ranked_proposal_ids, scores):
        score = int(score)
        if score > 0:
            scores_by_proposals[proposal_id].append(score)


with open('./second_round_scores.txt') as f:
    for line in f:
        add_score(line)
