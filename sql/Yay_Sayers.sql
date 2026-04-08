-- Yay Sayers
SELECT "ParlGroupName", "DecisionText", COUNT(*) as vote_count
FROM voting
WHERE "DecisionText" = 'Ja'
GROUP BY "ParlGroupName", "DecisionText"
ORDER BY vote_count DESC;
