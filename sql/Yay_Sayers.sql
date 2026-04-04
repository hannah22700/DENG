-- Ja-Sager
SELECT "ParlGroupName", "DecisionText", "BillTitle", COUNT(*) as vote_count
FROM voting
WHERE "DecisionText" = 'Ja'
GROUP BY "ParlGroupName", "DecisionText"
ORDER BY vote_count DESC;